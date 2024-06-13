from agent import Agent
from card import Card, Helper
import numpy as np
import config
from collections import deque
import random
from functions import list_and

class Game:
    
    def __init__(self,players,plus=True) -> None:
        self.players = deque(players)
        self.deck = deque([])
        self.gamepile = deque([])
        self.wildcard_colour = None
        self.top_card = None
        self.victor = False
        self.plus = plus
        
        # For the purpose of data collection (DC)
        self.memory = []
        self.drawn = 0
        self.put = 0
        self.red = 0
        
    def setup(self, plus=True):
        """Setup the game, start with generating the cards."""
        self.generate_deck()
        
        """Distribute the cards."""
        self.shuffle()
        for agent in self.players:
            agent.reset()
            for _ in range(config.starting_hand):
                self.draw(agent)
                
        # DC
        self.drawn = 0
        self.put = 0
        
        for player in self.players:
            if player.name == "Alice":
                self.red = player.count_w()
        
        self.memory = [[config.starting_hand,0,0,self.red]]
        
        """Open a card."""
        open = self.deck.pop()
        while open.suite == 'w':
            self.deck.appendleft(open)
            open = self.deck.pop()
        self.gamepile.append(open)
        self.top_card = open
        print('Card on top is:', self.top_card)
        
        """Player 1 turn."""
        self.playing = self.players.pop()
        print('Starting player is:', self.playing)
                
    def generate_deck(self):
        """Generate the play deck."""
        # Start by generating the coloured cards.
        self.deck = deque([])
        for c in config.suites:
            if c == 'w':
                continue
            for n in config.cards:
                if n == 'w' or n == 'W':
                    continue
                for _ in range(config.repetition):
                    if not self.plus and n == 'p':
                        continue
                    self.deck.append(Card(c,n))
        for _ in range(config.num_of_wildcard):
            self.deck.append(Card('w','w'))
            if self.plus:
                self.deck.append(Card('w','W'))
        print(len(self.deck))
        if config.debug:
            input()
    
    def shuffle(self):
        """Shuffle the deck."""
        deck = list(self.deck)
        random.shuffle(deck)
        self.deck = deque(deck)

    def draw(self,player):
        """Draw a card to the player."""
        if len(self.deck) == 0:
            if len(self.deck) + len(self.gamepile) == 1:        # If no more cards to be drawn, then skip
                print('No more cards!')
                return
            self.deck = self.gamepile
            self.gamepile = deque([self.deck.pop(),])
            self.shuffle()
        card = self.deck.pop()
        player.hand.append(card)
        
        # DC
        if player.name == 'Alice':
            self.drawn += 1
            self.red = player.count_w()
            self.memory.append([len(player.hand),self.put,self.drawn,self.red])
        
    def step(self):
        """Advance the game by one play"""
        # First, generate the available moves
        self.playing.generate_moves()
        
        # Then, generate the legal moves
        if self.top_card.suite != 'w':
            legal_moves = self.top_card.legal
        else:
            legal_moves = self.generate_wildcard_legal()
        
        # If nothing to play, draw
        if sum(list_and(legal_moves, self.playing.moves)) == 0:
            self.draw(self.playing)
            print(f'{self.playing.get_name()} drawed')
            
        # THIS PART IS FOR THE RULE WHERE AFTER A DRAW YOU CAN PLAY A CARD
        # Check again whether NOW there is a legal move
        self.playing.generate_moves()

        # Play according to preference
        if sum(list_and(legal_moves, self.playing.moves)) != 0:
            preference = self.playing.play(self.gamepile, legal_moves)
            # Make sure that the preference list agrees with possible moves and the preference
            playable = list_and(legal_moves, self.playing.moves, preference)
            try:
                played = random.choices(Helper.actions,weights=playable)
            except ValueError:
                print('Invalid move, playable list is zero')
                exit()
            played_card  = Helper.find_card_of_action(played[0])
            self.playing.hand.remove(played_card)
            self.gamepile.append(played_card)
            self.top_card = played_card
            print(f'{self.playing.get_name()} played', played_card)
            
            # DC
            if self.playing.name == 'Alice':
                self.put += 1
                self.red = self.playing.count_w()
                self.memory.append([len(self.playing.hand),self.put,self.drawn,self.red])
        
            # Check for victory
            if len(self.playing.hand) == 0:
                print('VICTORY FOR ', self.playing)
                self.victor = self.playing
                return self.victor
            
            # If a wildcard is played
            if played[0][0] == 'w':
                self.wildcard_colour = played[0][2]
                print('Wildcard color: ', self.wildcard_colour)
            
            # If a plus 4 is played
            if played[0][1] == 'W':
                self.players.appendleft(self.playing)   
                self.playing = self.players.pop()
                print(f'{self.playing.get_name()} got plus four')
                for _ in range(4):
                    self.draw(self.playing)
                    print(f'{self.playing.get_name()} drawed')
                
                # DC, Adjust the work
                if self.playing.name == 'Alice':
                    self.drawn -= 3
                    self.red = self.playing.count_w()
                    self.memory = self.memory[:-4] + [[len(self.playing.hand),self.put,self.drawn,self.red],]
            
            # If a plus 2 is played
            if played[0][1] == 'p':
                self.players.appendleft(self.playing)   
                self.playing = self.players.pop()
                print(f'{self.playing.get_name()} got plus two')
                for _ in range(2):
                    self.draw(self.playing)
                    print(f'{self.playing.get_name()} drawed')
                
                # DC, Adjust the work
                if self.playing.name == 'Alice':
                    self.drawn -= 1
                    self.red = self.playing.count_w()
                    self.memory = self.memory[:-2] + [[len(self.playing.hand),self.put,self.drawn,self.red],]
            
            # If a skip is played
            if played[0][1] == 's':
                self.players.appendleft(self.playing)   
                self.playing = self.players.pop()
                print(f'{self.playing.get_name()} skipped')
            
            # If a reverse is played
            if played[0][1] == 'r':
                self.players.reverse()
                print('Reversed')
        
        self.players.appendleft(self.playing)   
        self.playing = self.players.pop()
        print('Turn of:', self.playing.get_name())

    
    def generate_wildcard_legal(self):
        legal_moves = self.top_card.legal
        for i in range(config.num_of_norm):
            if Helper.find_card(i)[0] == self.wildcard_colour:
                legal_moves[i] = 1
        return legal_moves
