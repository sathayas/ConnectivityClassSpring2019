import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


###### Parameters
targetDeg = 10  # target average degree



###### Loading network data and calculate small-worldness stats
# Ks for clustering algorithm
K = list(range(10,301,10)) + list(range(350,1000,50))  
subK = [50, 100, 200, 500, 950]   # Ks for example atlases
indK = [list(K).index(k) for k in subK]  # indices corresponding to subK

G_list = []
N_list = []
C_list = []
L_list = []
for i,targetK in enumerate(subK):
    ###### file name, then loading
    fNet = 'DataAtlas/Oxford_sub16112_Rt2_K' + str(targetK)
    fNet += '_deg' + str(targetDeg) + '.adjlist'
    G = nx.read_adjlist(fNet, nodetype=int)
    G_list.append(G)

    ###### number of nodes
    N_list.append(len(G.nodes()))

    ##### clistering coefficient
    C_list.append(nx.average_clustering(G))

    ##### path length, giant component only
    GC_nodes = max(nx.connected_components(G), key=len)  
    GC = G.subgraph(GC_nodes)  
    L_list.append(nx.average_shortest_path_length(GC))


###### Plotting C and L
plt.figure(figsize=[9,4])

plt.subplot(131)
plt.plot(subK,N_list,'b.-')
plt.xscale('log')
plt.xlabel('Atlas K')
plt.ylabel('Number of nodes')
plt.title('Number of nodes vs K')

plt.subplot(132)
plt.plot(subK,C_list,'b.-')
plt.xscale('log')
plt.xlabel('Atlas K')
plt.ylabel('Clustering coefficient')
plt.title('Clusetering coefficient vs K')

plt.subplot(133)
plt.plot(subK,L_list,'b.-')
plt.xscale('log')
plt.xlabel('Atlas K')
plt.ylabel('Path length')
plt.title('Path length vs K')

plt.subplots_adjust(wspace=0.4)
plt.show()
