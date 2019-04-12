import numpy as np
import matplotlib.pyplot as plt


##### File business
fTS = 'DatafMRIPreprop/Oxford_sub16112_Rt2_K200.npz'
fTS_reg = 'DatafMRIPreprop/Oxford_sub16112_WBWMCSF_Rt2_K200.npz'
fGlobalMean = 'DatafMRIPreprop/Oxford_sub16112_PhysPar.npz'


##### Loading the data
X_TS = np.load(fTS)['ts']
X_GM = np.load(fGlobalMean)['PhysPar']
X_TS_reg = np.load(fTS_reg)['ts']


##### plotting
plt.figure(figsize=[6,7])

plt.subplot(311)
plt.plot(X_TS)
plt.xlabel('Time')
plt.ylabel('fMRI signal')
plt.title('Original fMRI data (all ROIs)')

plt.subplot(312)
plt.plot(X_GM[:,0], label='Whole brain')
plt.plot(X_GM[:,1], label='Deep white matter')
plt.plot(X_GM[:,2], label='CSF')
plt.xlabel('Time')
plt.ylabel('Global mean signal')
plt.title('Global mean signals over time')
plt.legend()

plt.subplot(313)
plt.plot(X_TS_reg)
plt.xlabel('Time')
plt.ylabel('fMRI signal')
plt.title('Global signals regressed out (all ROIs)')

plt.subplots_adjust(left=0.15, right=0.95, bottom=0.08, top=0.95,
                    hspace=0.5)
plt.show()
