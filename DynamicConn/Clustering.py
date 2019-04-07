import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

####### Loading the data
infile = np.load('DataDynamicConn/Leiden_sub39335_Rt2_K200_Rmat.npz')
Rmat = infile['Rmat']
nNodes = Rmat.shape[-1]
nTime = Rmat.shape[0]
indR = np.triu_indices(nNodes,1) # indices for the upper triangle of R
# initializing the data array, rows = correlation, cols = time
Rdata = np.zeros((nTime,len(indR[0])))
for iTime in range(nTime):
    R = Rmat[iTime,:,:]
    Rdata[iTime,:] = R[indR]


###### Clustering --- Figuring out the  number of clusters
# determinging the number of clusters (up to 30 clusters)
SSE = []
for iClus in range(1,31):
    print('Number of clusters: %d' % iClus)
    # K-means clustering
    km = KMeans(n_clusters=iClus)  # K-means with a given number of clusters
    km.fit(Rdata)  # fitting the principal components
    SSE.append(km.inertia_) # recording the sum of square distances

# plotting the sum of square distance
plt.plot(np.arange(1,31),SSE,marker = "o")
plt.xlabel('Number of clusters')
plt.ylabel('Sum of sq distances')
plt.show()



###### Clustering --- with K=6
km = KMeans(n_clusters=6)  # defining the clustering object
km.fit(Rdata)  # actually fitting the data
y_clus = km.labels_   # clustering info resulting from K-means
y_cent = km.cluster_centers_  # centroid coordinates


####### plotting cluster over time
f = np.load('DataDynamicConn/Leiden_sub39335_Rt2_K200_Efficiency.npz')
EglobMat = f['EglobMat']
xyz = f['xyz']
nodes = f['nodes']
plt.figure(figsize=[4,7])
plt.subplot(211)
plt.plot(y_clus)
plt.title('States over time')
plt.xlabel('Time')
plt.ylabel('State')
plt.xlim(1,nTime)

plt.subplot(212)
plt.imshow(EglobMat, cmap=plt.cm.rainbow, aspect='auto')
plt.title('Global efficiency')
plt.xlabel('Time')
plt.ylabel('Nodes')
plt.xlim(1,nTime)

plt.subplots_adjust(left=0.15, right=0.975, top=0.95, bottom=0.075,
                    hspace=0.4)
plt.show()


####### Saving the centroid information
np.savez('DataDynamicConn/Leiden_sub39335_Rt2_K200_Cluster.npz',
         y_clus = y_clus,
         y_cent = y_cent,
         nodes = nodes,
         xyz = xyz)


