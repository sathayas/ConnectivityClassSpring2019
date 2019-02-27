import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import community   # Louvain method
import pandas as pd

##### Parameters
voxDim = [46, 56, 42]

##### Custom distinct color function --- to be used later
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


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

