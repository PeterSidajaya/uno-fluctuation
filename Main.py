from card import Card
from agent import Agent, Random_Bot
from game import Game

if __name__=="__main__":
    bot1 = Random_Bot('Alice')
    bot2 = Random_Bot('Bob')
    
    g = Game([bot2, bot1])
    g.setup()
    victor = None
    while not victor:
        victor = g.step()
    
    
    