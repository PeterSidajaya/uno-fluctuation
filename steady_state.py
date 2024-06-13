import numpy as np
import matplotlib.pyplot as plt
import pickle

plt.rcParams['text.usetex'] = True
plt.rc('font', family='serif')

if __name__=="__main__":
    lim = 51
    size = 1000000
    with open('pickles/new/trj_fwd_plus.pickle', 'rb') as f:
        fwd_trajectories = pickle.load(f)[:size]

    with open('pickles/new/trj_bwd_plus.pickle', 'rb') as f:
        bwd_trajectories = pickle.load(f)[:size]
    
    fig, ax = plt.subplots(2,1)
    ax[0].set_xlim(-1,11)
    ax[1].set_xlim(-1,11)
    
    ax[0].set_ylabel(r'frequency',fontsize=16)
    ax[1].set_xlabel(r'hand size',fontsize=16)
    ax[1].set_ylabel(r'frequency',fontsize=16)
    
    fwd_bin = np.zeros(lim)
    for trajectory in fwd_trajectories:
        for points in trajectory:
            fwd_bin[points[0]] += 1
    print(fwd_bin[0])
    fwd_bin = fwd_bin/sum(fwd_bin)

    bwd_bin = np.zeros(lim)
    for trajectory in bwd_trajectories:
        for points in trajectory:
            bwd_bin[points[0]] += 1
    print(bwd_bin[0])
    bwd_bin = bwd_bin/sum(bwd_bin)
    
    ax[0].bar(np.arange(lim),fwd_bin,color="#54917d")
    ax[1].bar(np.arange(lim),bwd_bin,color="#54917d")
    plt.show()
