import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import community   # Louvain method

# ROI IDs
# Left precentral gyrus: 50
# Left post-cingulate, precuneus: 58

##### Custom distinct color function --- to be used later
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


####### Loading the network data
fTS = 'DatafMRIPreprop/NewYork_sub83453_Rt2_K200.npz'
nodes = np.load(fTS)['nodes']
xyz = np.load(fTS)['xyz']
fG = 'DatafMRIPreprop/NewYork_sub83453_Rt2_K200_deg20.adjlist'
fG_ms = 'DatafMRIPreprop/NewYork_sub83453_ms_Rt2_K200_deg20.adjlist'
G = nx.read_adjlist(fG, nodetype=int)
G_ms = nx.read_adjlist(fG_ms, nodetype=int)
G_list = [G, G_ms]
netLabel = ['Without motion scrubbing',
            'With motion scrubbing']


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
plt.figure(figsize=[6,4])
for i,iGC in enumerate(GC_list):
    
    # finally, graph with communities in different colors (Louvain)
    plt.subplot(1,2,i+1)
    nComm = max([comm for comm in partition_list[i].values()])+1
    node_color_list = get_cmap(nComm+1,'rainbow')
    for iComm in range(nComm):
        nodeList = [iNode for iNode,Comm in partition_list[i].items()
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
                    bottom=0.025, top=0.85)
plt.show()




###### drawing the graph (SM module)
# Identifying SM module for each network
ROI_SM = 50  # ROI=50 --> Left precentral gyrus
indSM_list = []
for iMod in partition_list:
    indSM_list.append(iMod[ROI_SM])
    
# Loop over states for visualization
plt.figure(figsize=[6,4])
for i,iGC in enumerate(GC_list):
    
    # finally, graph with communities in different colors (Louvain)
    plt.subplot(1,2,i+1)
    nComm = max([comm for comm in partition_list[i].values()])+1
    for iComm in range(nComm):
        nodeList = [iNode for iNode,Comm in partition_list[i].items()
                    if Comm==iComm]
        if iComm==indSM_list[i]:
            nx.draw_networkx_nodes(iGC, pos, 
                                   nodelist=nodeList,
                                   node_color = 'orangered',
                                   node_size=30)
        else:
            nx.draw_networkx_nodes(iGC, pos, 
                                   nodelist=nodeList,
                                   node_color = 'skyblue',
                                   node_size=15)
            
        nx.draw_networkx_edges(iGC, pos, width=0.5,
                               edge_color='lightblue')
    plt.title(netLabel[i])
    plt.axis('off')

plt.subplots_adjust(left=0.01, right=0.99, wspace=0.05,
                    bottom=0.025, top=0.85)
plt.show()





###### drawing the graph (DMN module)
# Identifying DMN module for each network
ROI_DMN = 58  # ROI=58 --> Left posterior cingulate / precuneus
indDMN_list = []
for iMod in partition_list:
    indDMN_list.append(iMod[ROI_DMN])
    
# Loop over states for visualization
plt.figure(figsize=[6,4])
for i,iGC in enumerate(GC_list):
    
    # finally, graph with communities in different colors (Louvain)
    plt.subplot(1,2,i+1)
    nComm = max([comm for comm in partition_list[i].values()])+1
    for iComm in range(nComm):
        nodeList = [iNode for iNode,Comm in partition_list[i].items()
                    if Comm==iComm]
        if iComm==indDMN_list[i]:
            nx.draw_networkx_nodes(iGC, pos, 
                                   nodelist=nodeList,
                                   node_color = 'orangered',
                                   node_size=30)
        else:
            nx.draw_networkx_nodes(iGC, pos, 
                                   nodelist=nodeList,
                                   node_color = 'skyblue',
                                   node_size=15)
            
        nx.draw_networkx_edges(iGC, pos, width=0.5,
                               edge_color='lightblue')
    plt.title(netLabel[i])
    plt.axis('off')

plt.subplots_adjust(left=0.01, right=0.99, wspace=0.05,
                    bottom=0.025, top=0.85)
plt.show()
