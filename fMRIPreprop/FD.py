import numpy as np
import matplotlib.pyplot as plt


##### Loading the time series data
fMoPar = 'DatafMRIPreprop/Queensland_sub66095_MoPar.par'
MoPar = np.genfromtxt(fMoPar,
                      delimiter="  ",
                      missing_values=["NA"])
NScan = MoPar.shape[0]

##### plotting the motion parameters
plt.figure(figsize=[5,5])

plt.subplot(211)
for iPar in range(3):
    plt.plot(MoPar[:,iPar])
plt.xlabel('Frame')
plt.ylabel('Motion (radian)')
plt.title('Rotation')

plt.subplot(212)
for iPar in range(3,6):
    plt.plot(MoPar[:,iPar])
plt.xlabel('Frame')
plt.ylabel('Motion (mm)')
plt.title('Translation')

plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.1,
                    hspace=0.5)
plt.show()


##### plotting changes in motion parameters
dMoPar = np.diff(MoPar, axis=0)
plt.figure(figsize=[5,5])

plt.subplot(211)
for iPar in range(3):
    plt.plot(dMoPar[:,iPar])
plt.xlabel('Frame')
plt.ylabel('Motion (radian)')
plt.title('Rotation')

plt.subplot(212)
for iPar in range(3,6):
    plt.plot(dMoPar[:,iPar])
plt.xlabel('Frame')
plt.ylabel('Motion (mm)')
plt.title('Translation')

plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.1,
                    hspace=0.5)
plt.show()


##### Framewise displacement
FD = np.sum(abs(dMoPar), axis=1)


##### tagging frames to be deleted (1 prior, 2 following)
bDelete = np.zeros_like(FD)
for iFrame in range(len(FD)):
    if FD[iFrame]>0.5:
        for jFrame in range(iFrame-1, min(len(FD), iFrame+3)):
            bDelete[jFrame] = 1
        

##### Plotting
plt.figure(figsize=[5,5])

plt.subplot(211)
tFrames = np.arange(len(FD))
plt.plot(tFrames, FD, 'b.-')
plt.plot(tFrames[bDelete==1], FD[bDelete==1], 'ro')
plt.hlines(0.5, 0, len(FD), linestyles='dotted')
plt.xlim(0,len(FD))
plt.xlabel('Frame')
plt.ylabel('FD')
plt.title('Framewise displacement (FD)')


# loading the original time series
fTS = 'DatafMRIPreprop/Queensland_sub66095_Rt2_K200.npz'
ts = np.load(fTS)['ts']
plt.subplot(212)
plt.imshow(ts.T, cmap=plt.cm.gist_ncar, aspect='auto')
plt.xlim(0,len(FD))
plt.xlabel('Frame')
plt.ylabel('Nodes')
plt.title('ROI time series data')

plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.1,
                    hspace=0.5)
plt.show()
