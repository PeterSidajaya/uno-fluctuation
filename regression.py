import numpy as np
import matplotlib.pyplot as plt
import pickle
from math import isnan, isinf
from scipy.stats import linregress, theilslopes

plt.rcParams['text.usetex'] = True

if __name__=="__main__":
    lim = 51
    size = 1000000
    with open('pickles/new/c8_fwd.pickle', 'rb') as f:
        fwd_trajectories = pickle.load(f)[:size]

    with open('pickles/new/c8_bwd.pickle', 'rb') as f:
        bwd_trajectories = pickle.load(f)[:size]
    
    fig1, ax1 = plt.subplots(1,1,figsize=(4, 4))
    fig2, ax2 = plt.subplots(1,1,figsize=(4, 4))
    # fig3, ax3 = plt.subplots(1,1,figsize=(4, 4))
    
    size = 7
    
    slopes = np.zeros([size,size])
    intercepts = np.zeros([size,size])
    # Rs = np.zeros([size,size])

    for start in range(1,size+1):
        for end in range(1,size+1):
            oe = (start - end) % 2
            dist = np.zeros(lim)
            for trajectory in fwd_trajectories:
                work_start = -1
                work_end = -1
                for point in trajectory:
                    if point[0] == start and work_start == -1:
                        work_start = point[1] + point[2]
                    elif point[0] == end and work_start > -1:
                        work_end = point[1] + point[2]
                        if work_end - work_start < lim:dist[work_end - work_start] += 1
                        work_start = -1
                        work_end = -1
            # fwd_dist = dist[oe:lim:2]
            fwd_dist = dist

            start, end = end, start
            dist = np.zeros(lim)
            for trajectory in bwd_trajectories:
                work_start = -1
                work_end = -1
                for point in trajectory:
                    if point[0] == start and work_start == -1:
                        work_start = point[1] + point[2]
                    elif point[0] == end and work_start > -1:
                        work_end = point[1] + point[2]
                        if work_end - work_start < lim: dist[work_end - work_start] += 1
                        work_start = -1
                        work_end = -1
            # bwd_dist = dist[oe:lim:2]
            bwd_dist = dist
            
            start, end = end, start
            
            # Cut outlier
            for i in range(lim):
                if fwd_dist[i] < 10:
                    fwd_dist[i] = 0
                if bwd_dist[i] < 10:
                    bwd_dist[i] = 0
            
            fwd_dist = fwd_dist/sum(fwd_dist)
            bwd_dist = bwd_dist/sum(bwd_dist)
            
            x,y = np.arange(lim), np.log(fwd_dist/bwd_dist)
            x = np.array([x[i] for i in np.arange(len(x)) if not (isinf(y[i]) or isnan(y[i]))])
            y = np.array([y[i] for i in np.arange(len(y)) if not (isinf(y[i]) or isnan(y[i]))])
            
            # OLS
            # res = linregress(x,y)
            # slopes[start-1,end-1] = res.slope
            # intercepts[start-1,end-1] = res.intercept
            # Rs[start-1,end-1] = np.cov([x,y])[0,1]/(np.std(x)*np.std(y))
            
            # Theil-Shen
            slope, intercept, low_slope, high_slope = theilslopes(y, x)
            slopes[start-1,end-1] = slope
            intercepts[start-1,end-1] = intercept
            
            
            print(start,end)
            # print(res.rvalue)
            # print(np.cov([x,y])[0,1]/(np.std(x)*np.std(y)))
            
    np.savetxt('figures/regression/slopes_c8.csv',slopes,delimiter=',')
    np.savetxt('figures/regression/intercepts_c8.csv',intercepts,delimiter=',')
    # np.savetxt('figures/regression/Rs_plus.csv',Rs,delimiter=',')
    
    slopes = np.loadtxt('figures/regression/slopes_c8.csv',delimiter=',')
    intercepts = np.loadtxt('figures/regression/intercepts_c8.csv',delimiter=',')
    # Rs = np.loadtxt('figures/regression/Rs_plus.csv',delimiter=',')
    
    for array in (slopes,intercepts):
        for i in range(size):
            for j in range(size):
                if i == j:
                    array[i,i] = 0
                if isnan(array[i,j]):
                    array[i,j] = 0
    
    pos1 = ax1.imshow(slopes,cmap='RdBu',vmin=-0.4,vmax=0.4)
    ax1.set_xlabel(r'$y$',fontsize=16)
    ax1.set_ylabel(r'$x$',fontsize=16)
    ax1.set_xticks(np.arange(size))
    ax1.set_xticklabels(labels=list(map(lambda x: r'$'+str(x)+'$',np.arange(size)+1)))
    ax1.set_yticks(np.arange(size))
    ax1.set_yticklabels(labels=list(map(lambda x: r'$'+str(x)+'$',np.arange(size)+1)))
    fig1.colorbar(pos1, ax=ax1)
    
    pos2 = ax2.imshow(intercepts,cmap='RdBu',vmin=-2.5,vmax=2.5)
    ax2.set_xlabel(r'$y$',fontsize=16)
    ax2.set_ylabel(r'$x$',fontsize=16)
    ax2.set_xticks(np.arange(size))
    ax2.set_xticklabels(labels=list(map(lambda x: r'$'+str(x)+'$',np.arange(size)+1)))
    ax2.set_yticks(np.arange(size))
    ax2.set_yticklabels(labels=list(map(lambda x: r'$'+str(x)+'$',np.arange(size)+1)))
    fig2.colorbar(pos2, ax=ax2)

    # pos3 = ax3.imshow(Rs**2,cmap='RdBu',vmin=0.0,vmax=1.0)
    # ax3.set_xlabel(r'$y$',fontsize=16)
    # ax3.set_ylabel(r'$x$',fontsize=16)
    # ax3.set_xticks(np.arange(size))
    # ax3.set_xticklabels(labels=list(map(lambda x: r'$'+str(x)+'$',np.arange(size)+1)))
    # ax3.set_yticks(np.arange(size))
    # ax3.set_yticklabels(labels=list(map(lambda x: r'$'+str(x)+'$',np.arange(size)+1)))
    # fig3.colorbar(pos3, ax=ax3)
    
    plt.show()