from agent import Random_Bot, Player, Smart_Bot, Stupid_Bot
from game import Game
from printing import HiddenPrints
import numpy as np
import config
import pickle

if __name__=="__main__":
    Tally = []
    bot1 = Smart_Bot('Alice')
    bot2 = Smart_Bot('Bob')
    bot3 = Smart_Bot('Charlie')
    bot4 = Smart_Bot('David')
    
    trajectories = []
    rng = np.random.default_rng()
    
    with HiddenPrints(off=config.debug):
        for _ in range(1000000):
            list_of_players = [bot1, bot2, bot3, bot4]
            rng.shuffle(list_of_players)
            g = Game(list_of_players,plus=config.plus)
            g.setup()
            victor = None
            while not victor:
                victor = g.step()
            print(g.memory)
            if config.debug:
                input()
            Tally.append(victor.get_name())
            trajectories.append(g.memory)
    
    print(Tally.count('Alice'))
    print(Tally.count('Bob'))
    print(Tally.count('Charlie'))
    print(Tally.count('David'))
    
    with open('pickles/new/appendix/trj_fwd_plus.pickle','wb') as f:
        pickle.dump(trajectories, f)
    
    Tally = []
    bot1 = Stupid_Bot('Alice')
    bot2 = Smart_Bot('Bob')
    bot3 = Smart_Bot('Charlie')
    bot4 = Smart_Bot('David')
    
    trajectories = []
    
    with HiddenPrints(off=False):
        for _ in range(1000000):
            list_of_players = [bot1, bot2, bot3, bot4]
            rng.shuffle(list_of_players)
            g = Game(list_of_players,plus=config.plus)
            g.setup()
            victor = None
            while not victor:
                victor = g.step()
            Tally.append(victor.get_name())
            trajectories.append(g.memory)
    
    print(Tally.count('Alice'))
    print(Tally.count('Bob'))
    print(Tally.count('Charlie'))
    print(Tally.count('David'))
    
    with open('pickles/new/appendix/trj_bwd_plus.pickle','wb') as f:
        pickle.dump(trajectories, f)
