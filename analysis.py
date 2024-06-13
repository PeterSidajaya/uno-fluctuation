import numpy as np
import matplotlib.pyplot as plt
import pickle
from math import isnan, isinf
from scipy.stats import linregress, theilslopes
import statsmodels.api as sm

plt.rcParams['text.usetex'] = True

if __name__=="__main__":
    lim = 51
    size = 1000000
    with open('pickles/new/appendix/trj_fwd_plus.pickle', 'rb') as f:
        fwd_trajectories = pickle.load(f)[:size]

    with open('pickles/new/appendix/trj_bwd_plus.pickle', 'rb') as f:
        bwd_trajectories = pickle.load(f)[:size]
    
    fig1, ax1 = plt.subplots(1,1,figsize=(4, 4))
    fig2, ax2 = plt.subplots(2,1,figsize=(4, 4))
    
    ax1.set_xlim(-1,lim)
    ax1.set_ylim(-5,5)
    ax2[0].set_xlim(-1,lim)
    ax2[0].set_ylim(-10,0)
    ax2[1].set_xlim(-1,lim)
    ax2[1].set_ylim(-10,0)
    
    ax1.set_xlabel(r'$W$',fontsize=16)
    ax1.set_ylabel(r'$\ln{\left(\frac{P_F}{P_R}\right)}$',fontsize=16)
    ax2[0].set_xlabel(r'$W$',fontsize=16)
    ax2[0].set_ylabel(r'$P_F$',fontsize=16)
    ax2[1].set_xlabel(r'$W$',fontsize=16)
    ax2[1].set_ylabel(r'$P_R$',fontsize=16)
    
    inset_ax = ax1.inset_axes(
        [0.05, 0.025, 0.4, 0.3],  # [x, y, width, height] w.r.t. axes
            xlim=[1, 15], ylim=[-1, 1], # sets viewport & tells relation to main axes
            xticklabels=[], yticklabels=[]
        )
    
    # lst = [(3,1,'red'),
    #        (4,2,'darkorange'),
    #        (5,3,'goldenrod'),
    #        (6,4,'limegreen'),
    #        (7,5,'green'),
    #        (8,6,'lightseagreen'),
    #        (9,7,'blue'),
    #        (10,8,'navy'),
    #        (11,9,'darkmagenta'),
    #        (12,10,'deeppink')]

    lst = [(5,2,'#9a3140'),(4,2,'#54917d'),(4,1,'#c09253')]
    # lst = [(5,2,'#9a3140')]
    
    # lst = [(8,11,'purple'),(8,14,'red'),(8,5,'blue'),(8,2,'darkorange'),(10,4,'green'),(4,10,'black')]
    # lst = [(8,3,'black')]
    
    for start,end,color in lst:
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
                    if work_end - work_start < lim: dist[work_end - work_start] += 1
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
        
        # This is for creating a separate list with the outliers cut
        # fwd_dist_reg = fwd_dist.copy()
        # bwd_dist_reg = bwd_dist.copy()
        # for i in range(lim):
        #     if fwd_dist[i] < 10:
        #         fwd_dist_reg[i] = 0
        #     if bwd_dist[i] < 10:
        #         bwd_dist_reg[i] = 0
        # fwd_dist_reg = fwd_dist_reg/sum(fwd_dist_reg)
        # bwd_dist_reg = bwd_dist_reg/sum(bwd_dist_reg)
        
        # Error bars
        # fwd_std_error = np.sqrt((fwd_dist/sum(fwd_dist)*(1-fwd_dist/sum(fwd_dist)))/sum(fwd_dist))
        # bwd_std_error = np.sqrt((bwd_dist/sum(bwd_dist)*(1-bwd_dist/sum(bwd_dist)))/sum(bwd_dist))
        
        # Normalisation
        fwd_dist = fwd_dist/sum(fwd_dist)
        bwd_dist = bwd_dist/sum(bwd_dist)

        # std_error_ratio = np.abs(fwd_dist/bwd_dist) * np.sqrt((fwd_std_error/fwd_dist)**2+(bwd_std_error/bwd_dist)**2)
        # std_error_final = np.abs(std_error_ratio / np.log(fwd_dist/bwd_dist))
                
        x = np.arange(lim)

        # for ax in (ax1,):
        for ax in ax1, inset_ax:
            ax.plot(x,np.log(fwd_dist/bwd_dist),'.',c=color, markersize=5)
            # ax.errorbar(x,np.log(fwd_dist/bwd_dist),yerr=std_error_final,lw=1,ls='',marker='.',c=color, markersize=5)
        ax2[0].plot(x,np.log(fwd_dist),'x',c=color,label=r'${} \rightarrow {}$'.format(start,end))
        ax2[1].plot(x,np.log(bwd_dist),'x',c=color,label=r'${} \rightarrow {}$'.format(end,start))
        
        # Regression
        x,y = x, np.log(fwd_dist/bwd_dist)
        # weights = 1/std_error_final
        # weights = np.array([weights[i] for i in np.arange(len(weights)) if not (isinf(y[i]) or isnan(y[i]))])
        x = np.array([x[i] for i in np.arange(len(x)) if not (isinf(y[i]) or isnan(y[i]))])
        y = np.array([y[i] for i in np.arange(len(y)) if not (isinf(y[i]) or isnan(y[i]))])
        
        # Normal OLS
        # res = linregress(x,y)
        # ax1.plot(x,res.slope*x+res.intercept,'-',alpha=0.6,c=color)
        
        # Theil-Shen
        slope, intercept, low_slope, high_slope = theilslopes(y, x)
        ax1.plot(x,slope*x+intercept,'-',alpha=0.6,c=color)
        
        # WLS
        # result = sm.WLS(y, sm.add_constant(x), weights=weights).fit()
        # intercept, slope = result.params
        # ax1.plot(x,slope*x+intercept,'-',alpha=0.6,c=color)
        
        # Legend
        ax1.plot((100,101),(100,101),'-',marker='.',markersize=5, alpha=0.6,c=color,label=r'${} \rightarrow {}$'.format(start,end))
        
    ax1.indicate_inset_zoom(inset_ax, edgecolor="black")
    ax1.legend(loc='best',fontsize=12,frameon=False)
    ax2[0].legend(loc='best',fontsize=12)
    ax2[1].legend(loc='best',fontsize=12)
    fig1.subplots_adjust(left=0.2)
    fig2.subplots_adjust(left=0.2)
    plt.show()
    # np.savetxt('fwd_dist_diff1.csv',fwd_dist,delimiter=',')
    # np.savetxt('bwd_dist_diff1.csv',bwd_dist,delimiter=',')