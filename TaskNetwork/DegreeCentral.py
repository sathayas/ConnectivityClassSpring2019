import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


#
#  First, covert verb generation task
#

###### loading the coordinates for nodes
fTS = 'DataTaskNetwork/fMRI_covertverb_r_bp_reg_Rt2_K950.npz'
infile = np.load(fTS)
nodes = infile['nodes']
xyz = infile['xyz']


###### loading network data
# task (task regressed out)
fNet_task_reg = 'DataTaskNetwork/fMRI_covertverb_r_bp_reg_Rt2_K950_deg20.adjlist'
G_task_reg = nx.read_adjlist(fNet_task_reg, nodetype=int)
# task (task NOT regressed out)
fNet_task_noreg = 'DataTaskNetwork/fMRI_covertverb_nomodel_r_bp_reg_Rt2_K950_deg20.adjlist'
G_task_noreg = nx.read_adjlist(fNet_task_noreg, nodetype=int)
# rest (absence of task)
fNet_rest = 'DataTaskNetwork/fMRI_covertverb_nomodel_r_bp_reg_Rt2_K950_deg20_rest.adjlist'
G_rest = nx.read_adjlist(fNet_rest, nodetype=int)
# consolidating all into a list
G_list = [G_task_reg, G_task_noreg, G_rest]
listLabel = ['During task (task regressed out)',
             'During task (task NOT regressed out)',
             'Rest (absence of task)']


####### degree centrality
Cdeg_list = []
for iG in G_list:
    Cdeg = nx.degree_centrality(iG)
    Cdeg_list.append(Cdeg)





    
###### visualizing the degree centrality
# dictionary of xy-coordinates
pos = {}
for iROI in range(len(nodes)):
    pos[nodes[iROI]] = xyz[iROI,:2]
    
# Loop over K for visualization
plt.figure(figsize=[9,5])
for i,iG in enumerate(G_list):

    plt.subplot(1,3,i+1)
    nx.draw_networkx_nodes(G_list[i], pos, 
                           cmap=plt.cm.coolwarm,
                           node_color=list(Cdeg_list[i]),
                           node_size=30)
    nx.draw_networkx_edges(G_list[i], pos, edge_color='lightblue')
    plt.axis('off')
    plt.title(listLabel[i])
    vmin = min(Cdeg_list[i])
    vmax = max(Cdeg_list[i])
    sm = plt.cm.ScalarMappable(cmap=plt.cm.coolwarm, 
                               norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []
    cbar = plt.colorbar(sm, shrink=0.5)
    cbar.ax.set_ylabel('Degree centrality')
    
plt.subplots_adjust(left=0.01, right=0.95, wspace=0.1, bottom=0.025)
plt.show()
