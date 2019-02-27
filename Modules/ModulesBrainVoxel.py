import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import community   # Louvain method
import pandas as pd

##### Parameters
voxDim = [46, 56, 42]


###### Within module degree function
def withinModDegree(G, partition):
    '''
    Calculates within module degrees, then returns the 
    Z-scores as a dictionary
    '''
    # number of modules
    nComm = max([comm for comm in partition.values()])+1
    # initialize output dictionary
    dictZ = {}
    # loop over communitites
    for iComm in range(nComm):
        # list of nodes for the module
        nodeList = [iNode for iNode,Comm in partition.items()
                    if Comm==iComm] 
        GMod = G.subgraph(nodeList)  # subgraph for the module
        KMod = dict(GMod.degree())  # degree sequence for the module
        KModList = [K for K in KMod.values()]
        meanK = np.mean(KModList)  # mean degree
        sdK = np.std(KModList)     # sd degree
        # loop over nodes within the module
        for iNode in nodeList:
            dictZ[iNode] = (KMod[iNode]-meanK)/sdK
    return dictZ


###### Participation coefficient function
def PC(G, partition):
    '''
    Calculates participation coefficients, then returns the
    PCs as a dictionary
    '''
    # number of modules
    nComm = max([comm for comm in partition.values()])+1
    # degree sequence for the original network
    dictK = dict(G.degree())
    # initialize the dictionary for intermediate results
    dictSum = {}
    # for loop over communitites
    for iComm in range(nComm):
        # list of nodes for the module
        nodeList = [iNode for iNode,Comm in partition.items()
                    if Comm==iComm] 
        GMod = G.subgraph(nodeList)  # subgraph for the module
        KMod = dict(GMod.degree())  # degree sequence for the module
        # loop over nodes within the module
        for iNode in nodeList:
            dictSum.setdefault(iNode,0)
            dictSum[iNode] += (KMod[iNode]/dictK[iNode])**2
    # converting to pc
    dictPC = {}
    for iNode, iSum in dictSum.items():
        dictPC[iNode] = 1 - iSum
    # returning the PC dictionary
    return dictPC


##### loading network data
# Brain network (Voxel, Oxford)
G = nx.read_adjlist('DataModules/Oxford_sub16112_voxel_d20_connected.adjlist',
                    nodetype=int)  


##### Community detection 
# Community detection with the Louvain method
#partition_L = community.best_partition(G)

#np.save('DataModules/partition_L.npy', partition_L)
partition_L = np.load('DataModules/partition_L.npy').item()



##### Creating a 3D image of module assignments
X = np.zeros(voxDim)  # initializing the module image
nComm = max([comm for comm in partition_L.values()])+1
for iComm in range(nComm):
    # list of nodes in a particular module
    nodeList = [iNode for iNode,Comm in partition_L.items()
                if Comm==iComm]
    # converting the node number (linear index) to 3D coord
    nodeXYZ = np.unravel_index(nodeList, voxDim)
    X[nodeXYZ] = iComm+1

# blanking the background
X[X==0] = None



##### visualing the modules in the brain space
plt.figure(figsize=[10,8])

for i,z in enumerate(np.arange(12,35,2)):
    plt.subplot(3,4,i+1)
    plt.imshow(np.rot90(X[:,:,z]), cmap='tab20')
    plt.title('Z='+str(z))
    plt.axis('off')

plt.subplots_adjust(hspace=0.2, wspace=0.0, bottom=0.025, top=0.95,
                    left=0, right=1.0)
plt.show()

