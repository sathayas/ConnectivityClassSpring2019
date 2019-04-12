import numpy as np
import matplotlib.pyplot as plt

###### Loading the time series data
fTS = 'DatafMRIPreprop/Oxford_sub16112_Rt2_K200.npz'
fTS_WBWMCSF = 'DatafMRIPreprop/Oxford_sub16112_WBWMCSF_Rt2_K200.npz'
fTS_WMCSF = 'DatafMRIPreprop/Oxford_sub16112_WMCSF_Rt2_K200.npz'
TS = np.load(fTS)['ts']
TS_WBWMCSF = np.load(fTS_WBWMCSF)['ts']
TS_WMCSF = np.load(fTS_WMCSF)['ts']
nNode = TS.shape[-1]


####### Calculating the correlation matrices
R = np.corrcoef(TS, rowvar=False)
R_WBWMCSF = np.corrcoef(TS_WBWMCSF, rowvar=False)
R_WMCSF = np.corrcoef(TS_WMCSF, rowvar=False)

# zeroing the main diagonal
R[np.arange(nNode), np.arange(nNode)] = 0
R_WBWMCSF[np.arange(nNode), np.arange(nNode)] = 0
R_WMCSF[np.arange(nNode), np.arange(nNode)] = 0


###### Histograms of the correlation matrices
nBin = 50
plt.figure(figsize=[9,3])

plt.subplot(131)
plt.hist(R[np.triu_indices(nNode,1)], nBin)
plt.xlim(-1,1)
plt.xlabel('Correlation')
plt.ylabel('Frequency')
plt.title('Oiriginal fMRI')

plt.subplot(132)
plt.hist(R_WBWMCSF[np.triu_indices(nNode,1)], nBin)
plt.xlim(-1,1)
plt.xlabel('Correlation')
plt.title('Whole brain, white matter\nCSF regressed out')

plt.subplot(133)
plt.hist(R_WMCSF[np.triu_indices(nNode,1)], nBin)
plt.xlim(-1,1)
plt.xlabel('Correlation')
plt.title('White matter\nCSF regressed out')


plt.subplots_adjust(left=0.1, right=0.975, bottom=0.15, top=0.85,
                    wspace=0.3, hspace=0.4)
plt.show()

