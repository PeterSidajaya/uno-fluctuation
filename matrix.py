"""This file is for generating the transition matrix to build a markovian random walk"""

import numpy as np
import pickle
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True

lim = 20
tr = np.zeros([lim,lim])

def normalise(smat):
    size = np.shape(smat)[0]
    for i in range(size):
        if sum(smat[i,:]) == 0:
            continue
        smat[i,:] = smat[i,:]/sum(smat[i,:])
    return smat

with open('pickles/new/trj_bwd_no-plus.pickle', 'rb') as f:
    trajectories = pickle.load(f)
    
for path in trajectories:
    for i in range(len(path)-1):
        start = path[i][0]
        end = path[i+1][0]
        if start < lim and end < lim:
            tr[start,end] += 1

tr = normalise(tr)

np.savetxt('transitions/new/transitions_bwd_no-plus.csv',tr,delimiter=',')

fig, ax = plt.subplots(1,1,figsize=(4, 4))

size = 10

pos = ax.imshow(tr[:size,:size], cmap='hot', interpolation='none')
ax.set_xlabel(r'$y$',fontsize=16)
ax.set_ylabel(r'$x$',fontsize=16)
ax.set_xticks(np.arange(size))
ax.set_xticklabels(labels=list(map(lambda x: r'$'+str(x)+'$',np.arange(size)+1)))
ax.set_yticks(np.arange(size))
ax.set_yticklabels(labels=list(map(lambda x: r'$'+str(x)+'$',np.arange(size)+1)))
fig.colorbar(pos, ax=ax)

# plt.show()
