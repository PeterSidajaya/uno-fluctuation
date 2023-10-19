from abc import ABC, abstractmethod

class Agent(ABC):
    
    def __init__(self,name) -> None:
        self.name = name
        self.hand = []
    
    def __str__(self) -> str:
        return f"{self.name} with {len(self.hand)} cards left ({self.hand})."
    
    def generate_moves(self):
        self.moves = [0,] * 52
        for card in self.hand:
            if card.index == 48:
                for i in range(48,52):
                    self.moves[i] = 1
            else:
                self.moves[card.index] = 1
    
    @abstractmethod
    def play(self, gamepile):
        """Modify this part of the logic when we want to modify it"""
        pass


class Random_Bot(Agent):
    def play(self, gamepile):
        return self.moves
    