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
nodes_list = []
xyz_list = []
Cdeg_list = []
for i,targetK in enumerate(subK):
    ###### file name, then loading
    fNet = 'DataAtlas/Oxford_sub16112_Rt2_K' + str(targetK)
    fNet += '_deg' + str(targetDeg) + '.adjlist'
    G = nx.read_adjlist(fNet, nodetype=int)
    G_list.append(G)
    fTS = 'DataAtlas/Oxford_sub16112_rt2_K' + str(targetK) + '.npz'
    infile = np.load(fTS)
    nodes_list.append(infile['nodes'])
    xyz_list.append(infile['xyz'])

    ####### centralities
    # degree centrality
    Cdeg = nx.degree_centrality(G)
    Cdeg_list.append(Cdeg)




    
###### visualizing the degree centrality
# Loop over K for visualization
plt.figure(figsize=[9,7.5])
for i,targetK in enumerate(subK):

    # dictionary of xy-coordinates
    pos = {}
    for iROI in range(len(nodes_list[i])):
        pos[nodes_list[i][iROI]] = xyz_list[i][iROI,:2]

    # first, hard-thresholding network
    plt.subplot(2,3,i+1)
    nx.draw_networkx_nodes(G_list[i], pos, 
                           cmap=plt.cm.coolwarm,
                           node_color=list(Cdeg_list[i]),
                           node_size=30)
    nx.draw_networkx_edges(G_list[i], pos, edge_color='lightblue')
    plt.axis('off')
    plt.title('Brain network (Berlin)\nand degree centrality')
    vmin = min(Cdeg_list[i])
    vmax = max(Cdeg_list[i])
    sm = plt.cm.ScalarMappable(cmap=plt.cm.coolwarm, 
                               norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []
    cbar = plt.colorbar(sm, shrink=0.5)
    cbar.ax.set_ylabel('Degree centrality')
    plt.title('Rt2 atlas\navg deg=' + str(targetDeg) +
              ',  K=' + str(targetK))
    
plt.subplots_adjust(left=0.01, right=0.95, wspace=0.1, bottom=0.025)
plt.show()
