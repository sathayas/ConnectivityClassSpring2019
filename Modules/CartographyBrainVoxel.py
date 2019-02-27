import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import community   # Louvain method

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

##### assigning roles
role = []
for i, iRow in dataModules.iterrows():
    # hubs or non-hubs
    if iRow.Z>=2.5:  # hubs
        if iRow.PC<=0.3:
            role.append(5)   # 5: provincial hub
        elif iRow.PC<=0.75:
            role.append(6)   # 6: connector hub
        else:
            role.append(7)   # 7: kinless hub
    else:
        if iRow.PC<=0.05:
            role.append(1)   # 1: ultra-peripheral node
        elif iRow.PC<=0.63:
            role.append(2)   # 2: peripheral node
        elif iRow.PC<=0.8:
            role.append(3)   # 3: non-hub connector node
        else:
            role.append(4)   # 4: non-hub kinless node
dataModules['Role'] = role



# Plotting PC vs Z
roleString = {1:'ultra-peripheral node',
              2:'peripheral node',
              3:'non-hub connector node',
              4:'non-hub kinless node'}
for iRole in range(1,5):
    plt.plot(dataModules[dataModules.Role==iRole].PC,
             dataModules[dataModules.Role==iRole].Z,
             '.', label=roleString[iRole])
plt.xlabel('Participation coefficient')
plt.ylabel('Within module degree Z-score')
plt.legend()
plt.show()
