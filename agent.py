from abc import ABC, abstractmethod
from card import Helper
from functions import list_and
import config

class Agent(ABC):
    
    def __init__(self,name) -> None:
        self.name = name
        self.hand = []
    
    def __str__(self) -> str:
        return f"{self.name} with {len(self.hand)} cards left ({self.hand})."
    
    def get_name(self):
        return self.name
    
    def generate_moves(self):
        self.moves = [0,] * (config.num_of_norm + 2 * config.num_of_suites)
        for card in self.hand:
            if card.index == config.num_of_norm:
                for i in range(config.num_of_norm,config.num_of_norm + config.num_of_suites):
                    self.moves[i] = 1
            if card.index == config.num_of_norm + 1:
                for i in range(config.num_of_norm + config.num_of_suites,config.num_of_norm + 2 * config.num_of_suites):
                    self.moves[i] = 1
            else:
                self.moves[card.index] = 1
    
    def count_w(self):
        return len(list(filter(lambda x: x.suite=='w',self.hand)))
    
    @abstractmethod
    def play(self, gamepile, legal_moves):
        """This is the part where the playing logic comes in"""
        pass
    
    def reset(self):
        """Reset the state"""
        self.hand = []


class Random_Bot(Agent):
    def play(self, gamepile, legal_moves):
        return self.moves
    
class Player(Agent):
    def play(self, gamepile, legal_moves):
        lst = [0,] * 60
        print('Current top card is:', gamepile[-1].name)
        print('My cards:', self.hand)
        action = input('Move: ')
        index = Helper.find_action_index(action)
        lst[index] = 1
        return lst
    
class Smart_Bot(Agent):
    def play(self, gamepile, legal_moves):
        # print(self.hand)
        # If there is no wildcard, act as random bot
        if sum(self.moves[config.num_of_norm:]) == 0:
            return self.moves
        else:
            legal_possible_moves = list_and(self.moves, legal_moves)
            # If can play something, don't play the wildcard
            if sum(legal_possible_moves[:config.num_of_norm]) != 0:
                return self.moves[:config.num_of_norm] + [0,0,0,0,0,0,0,0]
            else:
                hand_suite = list(map(lambda x: x.suite, self.hand))
                suite = max(set(hand_suite), key=hand_suite.count)              # One-liner to pick the most common colour
                if suite == 'b':
                    return [0,]*config.num_of_norm + [1,0,0,0] + [1,0,0,0]
                if suite == 'g':
                    return [0,]*config.num_of_norm + [0,1,0,0] + [0,1,0,0]
                if suite == 'r':
                    return [0,]*config.num_of_norm + [0,0,1,0] + [0,0,1,0]
                if suite == 'y':
                    return [0,]*config.num_of_norm + [0,0,0,1] + [0,0,0,1]
                else:
                    return [0,]*config.num_of_norm + [1,1,1,1] + [1,1,1,1]


class Stupid_Bot(Agent):
    def play(self, gamepile, legal_moves):
        print(self.hand)
        # If there is no wildcard, act as random bot
        if sum(self.moves[config.num_of_norm:]) == 0:
            return self.moves
        else:
            # If there is wildcard, play the least numerous suite on hand
            hand_suite = list(map(lambda x: x.suite, self.hand))
            suite = min(set(hand_suite), key=hand_suite.count)              # One-liner to pick the least common colour
            if suite == 'c':
                return [0,]*config.num_of_norm + [1,0,0,0] + [1,0,0,0]
            if suite == 'd':
                return [0,]*config.num_of_norm + [0,1,0,0] + [0,1,0,0]
            if suite == 'h':
                return [0,]*config.num_of_norm + [0,0,1,0] + [0,0,1,0]
            if suite == 's':
                return [0,]*config.num_of_norm + [0,0,0,1] + [0,0,0,1]
            else:
                return [0,]*config.num_of_norm + [1,1,1,1] + [1,1,1,1]

    