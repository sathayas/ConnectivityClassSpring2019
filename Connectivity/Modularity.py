import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import community   # Louvain method


##### Custom distinct color function --- to be used later
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


##### loading network data
# correlatio network
G = nx.read_adjlist('DataConnectivity/Oxford_sub16112_Rt2_K200_deg10.adjlist',
                    nodetype=int)
# partial correlatio network
G_pc = nx.read_adjlist('DataConnectivity/Oxford_sub16112_Rt2_K200_deg10_pc.adjlist',
                       nodetype=int)
# mutual information network
G_mi = nx.read_adjlist('DataConnectivity/Oxford_sub16112_Rt2_K200_deg10_mi.adjlist',
                       nodetype=int)
G_all = [G, G_pc, G_mi]
# time series data
f_TS = 'DataConnectivity/Oxford_sub16112_Rt2_K200.npz'
infile = np.load(f_TS)
xyz = infile['xyz']





##### Community detection 
# Community detection with the Louvain method
partition = community.best_partition(G)
partition_pc = community.best_partition(G_pc)
partition_mi = community.best_partition(G_mi)
partition_all = [partition, partition_pc, partition_mi]


###### Modularity
print('Modularity')
print('Correlaiton: %6.4f' % community.modularity(partition,G))
print('Partial correlaiton: %6.4f' % community.modularity(partition_pc,G_pc))
print('Mutal information: %6.4f' % community.modularity(partition_mi,G_mi))




###### visualizing the networks
# dictionary of xy-coordinates
pos = {}
for iROI in range(len(nodes)):
    pos[nodes[iROI]] = xyz[iROI,:2]

# next, graph with communities in different colors 
connMethods = ['Correlation','Partial correlation','Mutual information']
plt.figure(figsize=[9,4])
for i in range(len(G_all)):
    plt.subplot(1,3,i+1)
    nComm = max([comm for comm in partition_all[i].values()])+1
    node_color_list = get_cmap(nComm+1,'rainbow')
    for iComm in range(nComm):
        nodeList = [iNode for iNode,Comm in partition_all[i].items()
                    if Comm==iComm]
        nx.draw_networkx_nodes(G_all[i], pos, 
                               nodelist=nodeList,
                               node_color = np.array([node_color_list(iComm)]),
                               node_size=30)
    nx.draw_networkx_edges(G_all[i], pos, width=0.5,
                           edge_color='lightblue')
    nx.draw_networkx_labels(G_all[i], pos, font_size=3, font_color='Black')
    plt.title(connMethods[i])
    plt.axis('off')

plt.subplots_adjust(left=0.01, right=0.99, wspace=0.06, bottom=0.025, top=0.90)
plt.show()
