import config

class Card:
    
    def __init__(self, suite, number) -> None:
        """_summary_

        Args:
            colour (str): 'c', 'd', 'h', 's', or 'w' for 8
            number (str): '2' to '10', 'J', 'Q', 'K', 'A'
        """
        self.suite = suite
        self.number = number
        self.name = self.suite + self.number
        self.legal = self.generate_legal()
        self.index = Helper.find_card_index(self.name)
        
    def generate_legal(self):
        if self.name == 'w8':
            return [0,] * 48 + [1,] * 4
        else:
            lst = [0,] * 48 + [1,] * 4
            for index in range(48):
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
        for j in config.numbers:
            if j != '8':
                cards.append(i+j)
                actions.append(i+j)
    cards.append('w8')
    actions += ['w8c','w8d','w8h','w8s']

    def find_card_index(name):
        return Helper.cards.index(name)

    def find_action_index(name):
        return Helper.actions.index(name)

    def find_card(index):
        return Helper.cards[index]

    def find_card_of_action(action_name):
        if action_name[0:2] == 'w8':
            return Card('w','8')
        else:
            index = Helper.find_action_index(action_name)
            card = Helper.find_card(index)
            return Card(card[0],card[1:])
