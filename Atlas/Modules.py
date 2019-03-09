import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import community   # Louvain method


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
        xyz.append(xyz_full[indNode,:])
    nodes_list.append(nodes)
    xyz_list.append(xyz)

    ###### modular partition by Louvain
    partition = community.best_partition(GC)
    partition_list.append(partition)

