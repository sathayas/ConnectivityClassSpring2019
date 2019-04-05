import numpy as np
import matplotlib.pyplot as plt
from sklearn.covariance import GraphicalLassoCV
from sklearn.preprocessing import StandardScaler


##### Function to extract time series data 
def extract_winTS(X, timeStart, winSize):
    # extracting the window
    winX = X[(timeStart-winSize+1):(timeStart+1)]
    # calculating the weights
    th = winSize / 3
    w0 = (1-np.exp(-1/th))/(1-np.exp(-winSize/th))
    wt = []
    for iT in range(1,winSize+1):
        w = w0 * np.exp((iT - winSize)/th)
        wt.append(w)
    wt = np.array(wt).reshape(winSize,1)
    # weighting with wt
    wwinX = wt * winX
    return wwinX


##### Parameters
TR = 2.2   # TR
nTime = 212  # number of time points
winSizeS = 100  # window width in S
winSizeTR = round(winSizeS / TR) # window width in TR


##### loading the data
infile = np.load('DataDynamicConn/Leiden_sub39335_Rt2_K200.npz')
ts = infile['ts']
nodes = infile['nodes']
xyz = infile['xyz']
ts_std = StandardScaler().fit_transform(ts)   # scaling the data



##### plotting the weight and weighted data
# calculating weights
th = winSizeTR / 3
w0 = (1-np.exp(-1/th))/(1-np.exp(-winSizeTR/th))
wt = []
for iT in range(1,winSizeTR+1):
    w = w0 * np.exp((iT - winSizeTR)/th)
    wt.append(w)
wt = np.array(wt).reshape(winSizeTR,1)

# extracting weighted time series
wts = extract_winTS(ts_std, winSizeTR, winSizeTR)

# plotting them 
plt.figure(figsize=[6,3])
plt.subplot(121)
plt.plot(wt)
plt.xlabel('Time points')
plt.xticks([0,winSizeTR],['tau = 1', 'tau = L'])
plt.ylabel('Weight')
plt.title('Weights')

plt.subplot(122)
for iNode in range(len(nodes)):
    plt.plot(wts[:,iNode])
plt.xlabel('Time points')
plt.xticks([0,winSizeTR],['t - L', 't'])
plt.ylabel('Weighted time series')
plt.title('Weighted time series')

plt.subplots_adjust(left=0.125, right=0.975, 
                    bottom=0.15, top=0.90, wspace=0.4)
plt.show()




###### Calculating correlation across windows
Rmat = []
for iTime in range(winSizeTR,nTime):
    # extracting weighted time series
    wts = extract_winTS(ts_std, iTime, winSizeTR)
    # correlation matrix
    R = np.corrcoef(wts, rowvar=False)
    # zeroing the main diagonal
    for i in range(R.shape[0]):
        R[i,i] = 0
    # keeping R
    Rmat.append(R)

Rmat = np.array(Rmat)



###### Saving the Rmat for future use
np.savez('DataDynamicConn/Leiden_sub39335_Rt2_K200_Rmat.npz',
         Rmat = Rmat,
         winSize = winSizeTR,
         nodes = nodes,
         xyz = xyz)




