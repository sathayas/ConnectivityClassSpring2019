import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import community   # Louvain method


##### Custom distinct color function --- to be used later
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)



###### Parameters
targetDeg = 10  # target average degree



###### Loading network data and estimage modular partition by Louvain
# Ks for clustering algorithm
K = list(range(10,301,10)) + list(range(350,1000,50))  
subK = [50, 100, 200, 500, 950]   # Ks for example atlases
indK = [list(K).index(k) for k in subK]  # indices corresponding to subK

GC_list = []
nodes_list = []
xyz_list = []
partition_list = []
for i,targetK in enumerate(subK):
    ###### file name, then loading network
    fNet = 'DataAtlas/Oxford_sub16112_Rt2_K' + str(targetK)
    fNet += '_deg' + str(targetDeg) + '.adjlist'
    G = nx.read_adjlist(fNet, nodetype=int)
    GC_nodes = max(nx.connected_components(G), key=len)  
    GC = G.subgraph(GC_nodes)  
    GC_list.append(GC)    

    ###### loading nodal info
    fTS = 'DataAtlas/Oxford_sub16112_rt2_K' + str(targetK) + '.npz'
    infile = np.load(fTS)
    nodes_full = infile['nodes']
    xyz_full = infile['xyz']
    nodes = []
    xyz = []
    for iNode in GC.nodes():
        indNode = np.where(nodes_full==iNode)[0]
        nodes.append(iNode)
        xyz.append(list(xyz_full[np.squeeze(indNode),:]))
    nodes_list.append(nodes)
    xyz_list.append(np.array(xyz))

    ###### modular partition by Louvain
    partition = community.best_partition(GC)
    partition_list.append(partition)


###### drawing the graph 
# Loop over K for visualization
plt.figure(figsize=[9,7.5])
for i,targetK in enumerate(subK):
    
    # dictionary of xy-coordinates
    pos = {}
    for iROI in range(len(nodes_list[i])):
        pos[nodes_list[i][iROI]] = xyz_list[i][iROI,:2]


    # finally, graph with communities in different colors (Louvain)
    plt.subplot(2,3,i+1)
    nComm = max([comm for comm in partition_list[i].values()])+1
    node_color_list = get_cmap(nComm+1,'rainbow')
    for iComm in range(nComm):
        nodeList = [iNode for iNode,Comm in partition_list[i].items()
                    if Comm==iComm]
        nx.draw_networkx_nodes(GC_list[i], pos, 
                               nodelist=nodeList,
                               node_color = np.array([node_color_list(iComm)]),
                               node_size=30)
        nx.draw_networkx_edges(GC_list[i], pos, width=0.5,
                               edge_color='lightblue')
    plt.title('Rt2 atlas\n' + 'K=' + str(targetK))
    plt.axis('off')
    
plt.subplots_adjust(left=0.01, right=0.99, wspace=0.05,
                    bottom=0.025, top=0.925)
plt.show()
