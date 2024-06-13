"""This file is for simulating the Crooks and pdf plots with markovian random walk"""

import numpy as np
import matplotlib.pyplot as plt
import pickle

plt.rcParams['text.usetex'] = True
plt.rc('font', family='serif')

lim = 51
size = 1000000

with open('pickles/new/trj_fwd_plus.pickle', 'rb') as f:
    fwd_trajectories = pickle.load(f)[:size]

with open('pickles/new/trj_bwd_plus.pickle', 'rb') as f:
    bwd_trajectories = pickle.load(f)[:size]

fig1, ax1 = plt.subplots(1,1,figsize=(4, 4))

ax1.set_xlim(-1,lim)
ax1.set_ylim(-5,5)

ax1.set_xlabel(r'$W$',fontsize=16)
ax1.set_ylabel(r'$\ln{\left(\frac{P_F}{P_R}\right)}$',fontsize=16)

tr_fwd = np.loadtxt('transitions/new/transitions_fwd_plus.csv',delimiter=',')
tr_bwd = np.loadtxt('transitions/new/transitions_bwd_plus.csv',delimiter=',')

lst = [(5,2,'#9a3140')]

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
    fwd_dist = fwd_dist/sum(fwd_dist)
    bwd_dist = bwd_dist/sum(bwd_dist)
    x = np.arange(lim)

    ax1.plot(x,np.log(fwd_dist/bwd_dist),marker='.',c=color,markersize=5,lw=0,label=r'UNO')

fig1.subplots_adjust(left=0.2)

fwd_trajectories = []
bwd_trajectories = []

for _ in range(size):
    start = 8
    path = [[8,0]]
    w = 0
    while True:
        p = tr_fwd[start,:]
        end = np.random.choice(20,1,p=p)[0]
        w += 1
        path.append([end,w])
        start = end
        if start == 0:
            break
    fwd_trajectories.append(path)

for _ in range(size):
    start = 8
    path = [[8,0]]
    w = 0
    while True:
        p = tr_bwd[start,:]
        end = np.random.choice(20,1,p=p)[0]
        w += 1
        path.append([end,w])
        start = end
        if start == 0:
            break
    bwd_trajectories.append(path)
    
for start,end,color in lst:
    lim = 51
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
    fwd_dist = dist

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
    bwd_dist = dist

    fwd_dist = fwd_dist/sum(fwd_dist)
    bwd_dist = bwd_dist/sum(bwd_dist)

    ax1.plot(np.arange(lim),np.log(fwd_dist/bwd_dist),marker='x',markersize=5,lw=0,color='#224358',label=r'Markovianised UNO')
    ax1.legend(loc='best',fontsize=12,frameon=False)

plt.show()