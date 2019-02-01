import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

##### loading the network data
# C Elegans neural network
G_CEleg = nx.read_adjlist('DataSmallWorld/CElegans.adjlist')
# Power grid
G_Power = nx.read_gml('DataSmallWorld/power.gml', label='id')
# Brain (ROI)
G_ROI = nx.read_adjlist('DataSmallWorld/Oxford_sub16112_aal90_d5.adjlist')
# Brain (Voxel)
G_Voxel = nx.read_adjlist('DataSmallWorld/Oxford_sub16112_voxel_d20.adjlist')


# getting the network sizes (number of nodes)
print('Number of nodes')
print('C.Elegans: ', len(G_CEleg.nodes()))
print('Power grid: ', len(G_Power.nodes()))
print('Brain (ROI): ', len(G_ROI.nodes()))
print()

# getting the network sizes (number of edges)
print('Number of edges')
print('C.Elegans: ', len(G_CEleg.edges()))
print('Power grid: ', len(G_Power.edges()))
print('Brain (Voxel): ', len(G_Voxel.edges()))
print()

# average degree (2*NumEdges / NumNodes)
print('Average degree')
print('C.Elegans: %5.2f' % (2*len(G_CEleg.edges())/len(G_CEleg.nodes())))
print('Power grid: %5.2f' % (2*len(G_Power.edges())/len(G_Power.nodes())))
print('Brain (Voxel): %5.2f' % (2*len(G_Voxel.edges())/len(G_Voxel.nodes())))
