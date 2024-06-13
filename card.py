import config

class Card:
    
    def __init__(self, suite, number) -> None:
        """_summary_

        Args:
            colour (str): 'b', 'g', 'r', 'y', or 'w'
            number (str): '1' to '9', 'p','r','s','w','W'
        """
        self.suite = suite
        self.number = number
        self.name = self.suite + self.number
        self.legal = self.generate_legal()
        self.index = Helper.find_card_index(self.name)
        
    def generate_legal(self):
        """Generate the legal move after this card"""
        if self.name == 'ww' or self.name == 'wW':
            return [0,] * config.num_of_norm + [1,] * 8         # The legal moves will be added in Game.generate_wildcard_legal()
        else:
            lst = [0,] * config.num_of_norm + [1,] * 8
            for index in range(config.num_of_norm):
                card = Helper.find_card(index)
                if card[0] == self.suite:
                    lst[index] = 1
                if card[1] == self.number:
                    lst[index] = 1
            return lst
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other): 
            if not isinstance(other, Card):
                # don't attempt to compare against unrelated types
                return NotImplemented

            return self.name == other.name

class Helper:
    actions = []
    cards = []
    for i in config.suites:
        if i == 'w':
            continue
        for j in config.numbers:
            if j == 'w' or j == 'W':
                continue
            cards.append(i+j)
            actions.append(i+j)
    cards.append('ww')
    actions += ['wwb','wwg','wwr','wwy']
    cards.append('wW')
    actions += ['wWb','wWg','wWr','wWy']

    def find_card_index(name):
        return Helper.cards.index(name)

    def find_action_index(name):
        return Helper.actions.index(name)

    def find_card(index):
        return Helper.cards[index]

    def find_card_of_action(action_name):
        if action_name[0:2] == 'ww':
            return Card('w','w')
        elif action_name[0:2] == 'wW':
            return Card('w','W')
        else:
            index = Helper.find_action_index(action_name)
            card = Helper.find_card(index)
            return Card(card[0],card[1:])
