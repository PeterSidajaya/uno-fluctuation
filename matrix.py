"""This file is for generating the transition matrix to build a markovian random walk"""

import numpy as np
import pickle
import matplotlib.pyplot as plt

lim = 20
tr = np.zeros([lim,lim])

def normalise(smat):
    size = np.shape(smat)[0]
    for i in range(size):
        if sum(smat[i,:]) == 0:
            continue
        smat[i,:] = smat[i,:]/sum(smat[i,:])
    return smat

with open('pickles/trj_bwd_no-plus.pickle', 'rb') as f:
    trajectories = pickle.load(f)
    
for path in trajectories:
    for i in range(len(path)-1):
        start = path[i][0]
        end = path[i+1][0]
        if start < lim and end < lim:
            tr[start,end] += 1

tr = normalise(tr)

np.savetxt('transitions_no-plus_bwd.csv',tr,delimiter=',')
plt.imshow(tr, cmap='hot', interpolation='none')
plt.show()
