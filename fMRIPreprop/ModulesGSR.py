import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import community   # Louvain method
from sklearn.metrics import adjusted_rand_score

# ROI IDs
# Left precentral gyrus: 50
# Left post-cingulate, precuneus: 58

##### Custom distinct color function --- to be used later
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


####### Loading the network data
fTS = 'DatafMRIPreprop/Oxford_sub16112_Rt2_K200.npz'
nodes = np.load(fTS)['nodes']
xyz = np.load(fTS)['xyz']
fG = 'DatafMRIPreprop/Oxford_sub16112_Rt2_K200_deg20.adjlist'
fG_WBWMCSF = 'DatafMRIPreprop/Oxford_sub16112_WBWMCSF_Rt2_K200_deg20.adjlist'
fG_WMCSF = 'DatafMRIPreprop/Oxford_sub16112_WMCSF_Rt2_K200_deg20.adjlist'
G = nx.read_adjlist(fG, nodetype=int)
G_WBWMCSF = nx.read_adjlist(fG_WBWMCSF, nodetype=int)
G_WMCSF = nx.read_adjlist(fG_WMCSF, nodetype=int)
G_list = [G, G_WBWMCSF, G_WMCSF]
netLabel = ['No regression',
            'Whole brain, white matter\nCSF regressed out',
            'White matter\nCSF regressed out']


####### Finding the giant component and modular partition
partition_list = []
GC_list = []
for iG in G_list:
    # finding the giant component
    GC_nodes = max(nx.connected_components(iG), key=len)  
    GC = iG.subgraph(GC_nodes)
    GC_list.append(iG)
    ###### modular partition by Louvain
    partition = community.best_partition(GC)
    partition_list.append(partition)



###### drawing the graph
# dictionary of xy-coordinates
pos = {}
for iROI in range(len(nodes)):
    pos[nodes[iROI]] = xyz[iROI,:2]

# Loop over states for visualization
plt.figure(figsize=[9,4])
for i,iGC in enumerate(GC_list):
    
    # finally, graph with communities in different colors (Louvain)
    plt.subplot(1,3,i+1)
    nComm = max([comm for comm in partition_list[i].values()])+1
    node_color_list = get_cmap(nComm+1,'rainbow')
    for iComm in range(nComm):
        nodeList = [iNode for iNode,Comm in partition_list[iG].items()
                    if Comm==iComm]
        nx.draw_networkx_nodes(iGC, pos, 
                               nodelist=nodeList,
                               node_color = np.array([node_color_list(iComm)]),
                               node_size=30)
        nx.draw_networkx_edges(iGC, pos, width=0.5,
                               edge_color='lightblue')
    plt.title(netLabel[i])
    plt.axis('off')

plt.subplots_adjust(left=0.01, right=0.99, wspace=0.05,
                    bottom=0.025, top=0.925)
plt.show()


