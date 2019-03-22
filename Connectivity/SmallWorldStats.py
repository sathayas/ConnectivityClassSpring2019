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


##### Clustering coefficients
print('Clustering coefficients')
print('C. Elegans: %4.2f' % nx.average_clustering(G_CEleg))
print('Power grid: %5.3f' % nx.average_clustering(G_Power))
print('Brain (ROI): %4.2f' % nx.average_clustering(G_ROI))
print('Brain (Voxel): %4.2f' % nx.average_clustering(G_Voxel))
