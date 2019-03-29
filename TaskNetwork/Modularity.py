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

#
#  First, covert verb generation task
#

###### loading the coordinates for nodes
fTS = 'DataTaskNetwork/fMRI_covertverb_r_bp_reg_Rt2_K200.npz'
infile = np.load(fTS)
nodes = infile['nodes']
xyz = infile['xyz']


###### loading network data
# task (task regressed out)
fNet_task_reg = 'DataTaskNetwork/fMRI_covertverb_r_bp_reg_Rt2_K200_deg20.adjlist'
G_task_reg = nx.read_adjlist(fNet_task_reg, nodetype=int)
# task (task NOT regressed out)
fNet_task_noreg = 'DataTaskNetwork/fMRI_covertverb_nomodel_r_bp_reg_Rt2_K200_deg20.adjlist'
G_task_noreg = nx.read_adjlist(fNet_task_noreg, nodetype=int)
# rest (absence of task)
fNet_rest = 'DataTaskNetwork/fMRI_covertverb_nomodel_r_bp_reg_Rt2_K200_deg20_rest.adjlist'
G_rest = nx.read_adjlist(fNet_rest, nodetype=int)
# consolidating all into a list
G_list = [G_task_reg, G_task_noreg, G_rest]
listLabel = ['During task\n(task regressed out)',
             'During task\n(task NOT regressed out)',
             'Rest\n(absence of task)']


####### Community detection
# Community detection with the Louvain method
partition_list = []
for iG in G_list:
    partition = community.best_partition(iG)
    partition_list.append(partition)





    
###### visualizing the modular organization
# dictionary of xy-coordinates
pos = {}
for iROI in range(len(nodes)):
    pos[nodes[iROI]] = xyz[iROI,:2]
    
# loop over networks for visualization
plt.figure(figsize=[10,4])
for i,iG in enumerate(G_list):

    plt.subplot(1,3,i+1)
    nComm = max([comm for comm in partition_list[i].values()])+1
    node_color_list = get_cmap(nComm+1,'rainbow')
    for iComm in range(nComm):
        nodeList = [iNode for iNode,Comm in partition_list[i].items()
                    if Comm==iComm]
        nx.draw_networkx_nodes(iG, pos, 
                               nodelist=nodeList,
                               node_color = np.array([node_color_list(iComm)]),
                               node_size=30)
    nx.draw_networkx_edges(iG, pos, width=0.5,
                           edge_color='lightblue')
    plt.title(listLabel[i])
    plt.axis('off')
    
plt.subplots_adjust(left=0.01, right=0.97, wspace=0.1, bottom=0.025)
plt.show()





#
#  Second, finger foot lips task
#


###### loading network data
# task (task regressed out), finger
fNet_reg_finger = 'DataTaskNetwork/fMRI_fingerfootlips_r_bp_reg_Rt2_K200_deg20_finger.adjlist'
G_reg_finger = nx.read_adjlist(fNet_reg_finger, nodetype=int)
# task (task regressed out), foot
fNet_reg_foot = 'DataTaskNetwork/fMRI_fingerfootlips_r_bp_reg_Rt2_K200_deg20_foot.adjlist'
G_reg_foot = nx.read_adjlist(fNet_reg_foot, nodetype=int)
# task (task regressed out), lips
fNet_reg_lips = 'DataTaskNetwork/fMRI_fingerfootlips_r_bp_reg_Rt2_K200_deg20_lips.adjlist'
G_reg_lips = nx.read_adjlist(fNet_reg_lips, nodetype=int)
# task (task NOT regressed out), finger
fNet_noreg_finger = 'DataTaskNetwork/fMRI_fingerfootlips_nomodel_r_bp_reg_Rt2_K200_deg20_finger.adjlist'
G_noreg_finger = nx.read_adjlist(fNet_noreg_finger, nodetype=int)
# task (task NOT regressed out), foot
fNet_noreg_foot = 'DataTaskNetwork/fMRI_fingerfootlips_nomodel_r_bp_reg_Rt2_K200_deg20_foot.adjlist'
G_noreg_foot = nx.read_adjlist(fNet_noreg_foot, nodetype=int)
# task (task NOT regressed out), lips
fNet_noreg_lips = 'DataTaskNetwork/fMRI_fingerfootlips_nomodel_r_bp_reg_Rt2_K200_deg20_lips.adjlist'
G_noreg_lips = nx.read_adjlist(fNet_noreg_lips, nodetype=int)
# consolidating all into a list
G_list = [G_reg_finger, G_reg_foot, G_reg_lips,
          G_noreg_finger, G_noreg_foot, G_noreg_lips]
listLabel = ['Finger\n(task regressed out)',
             'Foot\n(task regressed out)',
             'Lips\n(task regressed out)',
             'Finger\n(task NOT regressed out)',
             'Foot\n(task NOT regressed out)',
             'Lips\n(task NOT regressed out)']



####### Community detection
# Community detection with the Louvain method
partition_list = []
for iG in G_list:
    partition = community.best_partition(iG)
    partition_list.append(partition)





    
###### visualizing the degree centrality
# dictionary of xy-coordinates
pos = {}
for iROI in range(len(nodes)):
    pos[nodes[iROI]] = xyz[iROI,:2]
    
# Loop over K for visualization
plt.figure(figsize=[10,8])
for i,iG in enumerate(G_list):

    plt.subplot(2,3,i+1)
    nComm = max([comm for comm in partition_list[i].values()])+1
    node_color_list = get_cmap(nComm+1,'rainbow')
    for iComm in range(nComm):
        nodeList = [iNode for iNode,Comm in partition_list[i].items()
                    if Comm==iComm]
        nx.draw_networkx_nodes(iG, pos, 
                               nodelist=nodeList,
                               node_color = np.array([node_color_list(iComm)]),
                               node_size=30)
    nx.draw_networkx_edges(iG, pos, width=0.5,
                           edge_color='lightblue')
    plt.title(listLabel[i])
    plt.axis('off')
    
plt.subplots_adjust(left=0.01, right=0.97, wspace=0.1, bottom=0.025,
                    hspace=0.4)
plt.show()
