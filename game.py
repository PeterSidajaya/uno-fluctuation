from agent import Agent
from card import Card, Helper
import numpy as np
import config
from collections import deque
import random

class Game:
    
    def __init__(self,players) -> None:
        self.players = deque(players)
        self.deck = deque([])
        self.gamepile = deque([])
        self.wildcard_colour = None
        self.top_card = None
        self.victor = False
        
    def setup(self):
        """Setup the game, start with generating the cards."""
        self.generate_deck()
        
        """Distribute the cards."""
        self.shuffle()
        for agent in self.players:
            for _ in range(config.starting_hand):
                self.draw(agent)
        
        """Open a card."""
        open = self.deck.pop()
        while open.name == 'w8':
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
        for c in config.suites:
            for n in config.numbers:
                if n != '8':
                    self.deck.append(Card(c,n))
                else:
                    self.deck.append(Card('w','8'))
    
    def shuffle(self):
        """Shuffle the deck."""
        deck = list(self.deck)
        random.shuffle(deck)
        self.deck = deque(deck)

    def draw(self,player):
        if len(self.deck) == 0:
            self.deck = self.gamepile
            self.gamepile = deque([self.deck.pop(),])
            self.shuffle()
        card = self.deck.pop()
        player.hand.append(card)
        
    def step(self):
        """Advance the game by one play"""
        # First, generate the available moves
        self.playing.generate_moves()
        
        # Then, generate the legal moves
        if self.top_card.name != 'w8':
            legal_moves = self.top_card.legal
        else:
            legal_moves = self.generate_wildcard_legal()
        
        # If nothing to play, draw
        if sum(map(lambda x,y: x*y, legal_moves, self.playing.moves)) == 0:
            self.draw(self.playing)
            print('Draw')
        
        # Play according to preference
        else:
            preference = self.playing.play(self.gamepile)
            playable = list(map(lambda x,y,z: x*y*z, legal_moves, self.playing.moves, preference))
            played = random.choices(Helper.actions,weights=playable)
            played_card  = Helper.find_card_of_action(played[0])
            self.playing.hand.remove(played_card)
            self.gamepile.append(played_card)
            self.top_card = played_card
            print('Played', played_card)
            
            if played[0][0] == 'w':
                self.wildcard_colour = played[0][2]
                print('Wildcard color: ', self.wildcard_colour)
                
            if len(self.playing.hand) == 0:
                print('VICTORY FOR ', self.playing)
                self.victor = self.playing
                return self.victor
        
        self.players.appendleft(self.playing)   
        self.playing = self.players.pop()
        print('Turn of:', self.playing)

    
    def generate_wildcard_legal(self):
        legal_moves = self.top_card.legal
        for i in range(48):
            if Helper.find_card(i)[0] == self.wildcard_colour:
                legal_moves[i] = 1
        return legal_moves
