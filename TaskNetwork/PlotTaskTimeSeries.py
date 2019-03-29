import os
import numpy as np
import matplotlib.pyplot as plt


##### First, covert verb generation task
fTask = 'DataTaskNetwork/GLM_model_covertverb.npz'
GLM = np.load(fTask)['X']

plt.figure(figsize=[6,2.5])
timeVec = np.arange(1,GLM.shape[0]+1)
    
plt.subplot(111)
plt.plot(timeVec,GLM[:,0],'b-')
plt.xlabel('Time points')
plt.ylabel('Task regressor')
plt.subplots_adjust(bottom=0.2, right=0.975)
plt.show()



##### Second, finger foot lips task
fTask = 'DataTaskNetwork/GLM_model_fingerfootlips.npz'
GLM = np.load(fTask)['X']
taskList = ['finger','foot','lips']
indTask = [0,2,4]

plt.figure(figsize=[6,6])
timeVec = np.arange(1,GLM.shape[0]+1)
for i, iTask in enumerate(taskList):
    plt.subplot(3,1,i+1)
    plt.plot(timeVec,GLM[:,indTask[i]],'b-')
    plt.xlabel('Time points')
    plt.ylabel('Task regressor\n('+iTask+')')
plt.subplots_adjust(bottom=0.075, right=0.975, left=0.15, top=0.975,
                    hspace=0.4)
plt.show()




