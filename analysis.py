import numpy as np
import matplotlib.pyplot as plt
import pickle


if __name__=="__main__":
    lim = 51
    size = 1000000
    with open('pickles/trj_fwd_no-plus.pickle', 'rb') as f:
        fwd_trajectories = pickle.load(f)[:size]

    with open('pickles/trj_bwd_no-plus.pickle', 'rb') as f:
        bwd_trajectories = pickle.load(f)[:size]
    
    fig1, ax1 = plt.subplots(1,1)
    fig2, ax2 = plt.subplots(2,1)
    
    ax1.set_xlim(-1,lim)
    ax1.set_ylim(-10,5)
    ax2[0].set_xlim(-1,lim)
    ax2[0].set_ylim(-10,0)
    ax2[1].set_xlim(-1,lim)
    ax2[1].set_ylim(-10,0)
    
    # lst = [(4,3,'red'),
    #        (5,4,'darkorange'),
    #        (6,5,'goldenrod'),
    #        (7,6,'limegreen'),
    #        (8,7,'green'),
    #        (9,8,'lightseagreen'),
    #        (10,9,'blue'),
    #        (11,10,'navy'),
    #        (12,11,'darkmagenta'),
    #        (13,12,'deeppink')]
    
    lst = [(6,5,'black')]
    
    for start,end,color in lst:
        oe = (start - end) % 2
        dist = np.zeros(lim)
        for trajectory in fwd_trajectories:
            work_start = -1
            work_end = -1
            for point in trajectory:
                if point[0] == start and work_start == -1:
                    work_start = point[1]
                elif point[0] == end and work_start > -1:
                    work_end = point[1]
                    if work_end - work_start < lim: dist[work_end - work_start] += 1
                    work_start = -1
                    work_end = -1
        fwd_dist = dist[oe:lim:2]
        # fwd_dist = dist

        start, end = end, start
        dist = np.zeros(lim)
        for trajectory in bwd_trajectories:
            work_start = -1
            work_end = -1
            for point in trajectory:
                if point[0] == start and work_start == -1:
                    work_start = point[1]
                elif point[0] == end and work_start > -1:
                    work_end = point[1]
                    if work_end - work_start < lim: dist[work_end - work_start] += 1
                    work_start = -1
                    work_end = -1
        bwd_dist = dist[oe:lim:2]
        # bwd_dist = dist
        
        start, end = end, start
        fwd_dist = fwd_dist/sum(fwd_dist)
        bwd_dist = bwd_dist/sum(bwd_dist)

        ax1.plot(np.arange(oe,lim,2),np.log(fwd_dist/bwd_dist),'o:',c=color,markerfacecolor='none', markeredgecolor=color, label='{} -> {}'.format(start,end))
        ax2[0].plot(np.arange(oe,lim,2),np.log(fwd_dist),'x:',c=color,label='{} -> {}'.format(start,end))
        ax2[1].plot(np.arange(oe,lim,2),np.log(bwd_dist),'x:',c=color,label='{} -> {}'.format(end,start))
        # ax1.plot(np.arange(lim),np.log(fwd_dist/bwd_dist),'o:',c=color,markerfacecolor='none', markeredgecolor=color, label='{} -> {}'.format(start,end))
        # ax2[0].plot(np.arange(lim),np.log(fwd_dist),'x:',c=color,label='{} -> {}'.format(start,end))
        # ax2[1].plot(np.arange(lim),np.log(bwd_dist),'x:',c=color,label='{} -> {}'.format(end,start))
        print(start,end)
    
    ax1.legend(loc='best')
    ax2[0].legend(loc='best')
    ax2[1].legend(loc='best')
    plt.show()
    np.savetxt('fwd_dist_diff1.csv',fwd_dist,delimiter=',')
    np.savetxt('bwd_dist_diff1.csv',bwd_dist,delimiter=',')