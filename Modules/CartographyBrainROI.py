import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.community import girvan_newman, modularity
import community   # Louvain method
import pandas as pd


##### Custom distinct color function --- to be used later
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


##### girman-newman method, optimized with modularity
def girvan_newman_opt(G, verbose=False):
    runningMaxMod = 0
    commIndSetFull = girvan_newman(G)
    for iNumComm in range(2,len(G)):
        if verbose:
            print('Commnity detection iteration : %d' % iNumComm, end='')
        iPartition = next(commIndSetFull)  # partition with iNumComm communities
        Q = modularity(G, iPartition)  # modularity
        if verbose:
            print('  Modularity : %6.4f' % Q)
        if Q>runningMaxMod:  # saving the optimum partition and associated info
            runningMaxMod = Q
            OptPartition = iPartition
    return OptPartition


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
# Brain network (ROI, Oxford)
G = nx.read_adjlist('DataModules/Oxford_sub16112_aal90_d5_connected_annotated.adjlist')  


##### Community detection 
# Community detection with the girvan-newman algorithm
commInd = girvan_newman_opt(G)
# converting the partitions into dictionaries
partition_GN = {}
for i,iComm in enumerate(commInd):
    for iNode in iComm:
        partition_GN[iNode] = i


# Community detection with the Louvain method
partition_L = community.best_partition(G)


##### degree sequence
dictK = dict(G.degree())

##### Within node degree Z-scores
dictZ_GN = withinModDegree(G, partition_GN)
dictPC_GN = PC(G, partition_GN)


##### Creating a dataframe for all info
dataModules = pd.DataFrame(partition_GN.items(),
                           columns=['Node','ModuleID'])
# adding degree (from the original network)
dataModules = pd.merge(dataModules,
                       pd.DataFrame(dictK.items(),columns=['Node','Degree']),
                       on='Node')
# adding Z score
dataModules = pd.merge(dataModules,
                       pd.DataFrame(dictZ_GN.items(),columns=['Node','Z']),
                       on='Node')
# adding PC
dataModules = pd.merge(dataModules,
                       pd.DataFrame(dictPC_GN.items(),columns=['Node','PC']),
                       on='Node')

    
