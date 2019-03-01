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



##### loading network data
# Brain network (ROI, Oxford)
G_Oxford = nx.read_adjlist('DataModules/Oxford_sub16112_aal90_d5_connected_annotated.adjlist')  



##### Community detection 
# Community detection with the girvan-newman algorithm
commInd_Oxford = girvan_newman_opt(G_Oxford)
# converting the partitions into dictionaries
partition_Oxford_GN = {}
for i,iComm in enumerate(commInd_Oxford):
    for iNode in iComm:
        partition_Oxford_GN[iNode] = i


# Community detection with the Louvain method
partition_Oxford_L = community.best_partition(G_Oxford)



###### Modularity
print('Modularity')
print('Girvan-Newman: %6.4f' % community.modularity(partition_Oxford_GN,
                                                    G_Oxford))
print('Louvain: %6.4f' % community.modularity(partition_Oxford_L,
                                              G_Oxford))




###### drawing the graph 
# loading the coordinates info for brain areas
AALTable = pd.read_csv('DataModules/aal_MNI_V4_coord.csv')
# dictionary of xy-coordinates
pos = {}
for i in range(1,91):
    pos[AALTable.iloc[i-1,1]] = np.array(AALTable.loc[i-1,
                                                      ['centerX',
                                                       'centerY']])

# first, graph without community assignments
plt.figure(figsize=[7,7])
nx.draw_networkx_nodes(G_Oxford, pos, node_color='salmon',
                       node_size=100)
nx.draw_networkx_edges(G_Oxford, pos,
                       edge_color='lightblue')
nx.draw_networkx_labels(G_Oxford, pos, font_size=7, font_color='black')
plt.title('Original brain network (ROI, Oxford)')
plt.axis('off')
plt.show()

# next, graph with communities in different colors (Girvan-Newman)
plt.figure(figsize=[7,7])
nComm = max([comm for comm in partition_Oxford_GN.values()])+1
node_color_list = get_cmap(nComm+1,'rainbow')
for iComm in range(nComm):
    nodeList = [iNode for iNode,Comm in partition_Oxford_GN.items()
                if Comm==iComm]
    nx.draw_networkx_nodes(G_Oxford, pos, 
                           nodelist=nodeList,
                           node_color = np.array([node_color_list(iComm)]),
                           node_size=100)
nx.draw_networkx_edges(G_Oxford, pos,
                       edge_color='lightblue')
nx.draw_networkx_labels(G_Oxford, pos, font_size=7, font_color='Black')
plt.title('Girvan-Newman method')
plt.axis('off')
plt.show()

# finally, graph with communities in different colors (Louvain)
plt.figure(figsize=[7,7])
nComm = max([comm for comm in partition_Oxford_L.values()])+1
node_color_list = get_cmap(nComm+1,'rainbow')
for iComm in range(nComm):
    nodeList = [iNode for iNode,Comm in partition_Oxford_L.items()
                if Comm==iComm]
    nx.draw_networkx_nodes(G_Oxford, pos, 
                           nodelist=nodeList,
                           node_color = np.array([node_color_list(iComm)]),
                           node_size=100)
nx.draw_networkx_edges(G_Oxford, pos,
                       edge_color='lightblue')
nx.draw_networkx_labels(G_Oxford, pos, font_size=7, font_color='Black')
plt.title('Louvain method')
plt.axis('off')
plt.show()

