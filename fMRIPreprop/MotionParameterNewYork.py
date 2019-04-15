import numpy as np
import matplotlib.pyplot as plt


##### Loading the time series data
fMoPar = 'DatafMRIPreprop/NewYork_sub83453_MoPar.par'
MoPar = np.genfromtxt(fMoPar,
                      delimiter="  ",
                      missing_values=["NA"])
NScan = MoPar.shape[0]


##### plotting the motion parameters
plt.figure(figsize=[7,7])

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





##### Framewise displacement
dMoPar = np.diff(MoPar, axis=0)
FD = np.sum(abs(dMoPar), axis=1)


##### tagging frames to be deleted (1 prior, 2 following)
bDelete = np.zeros_like(FD)
for iFrame in range(len(FD)):
    if FD[iFrame]>0.5:
        for jFrame in range(iFrame-1, min(len(FD), iFrame+3)):
            bDelete[jFrame] = 1

# number of time points to be delted
print('Number of time points to be deleted: %d' % np.sum(bDelete))


##### Plotting
tFrames = np.arange(len(FD))
plt.plot(tFrames, FD, 'b.-')
plt.plot(tFrames[bDelete==1], FD[bDelete==1], 'ro')
plt.hlines(0.5, 0, len(FD), linestyles='dotted')
plt.xlim(0,len(FD))
plt.xlabel('Frame')
plt.ylabel('FD')
plt.title('Framewise displacement (FD)')
plt.show()
