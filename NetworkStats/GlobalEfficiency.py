import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

##### loading the network data
# C Elegans neural network
G_CEleg = nx.read_adjlist('DataNetStats/CElegans.adjlist')
# Power grid
G_Power = nx.read_gml('DataNetStats/power.gml', label='id')
# Brain (ROI)
G_ROI = nx.read_adjlist('DataNetStats/Oxford_sub16112_aal90_d5.adjlist')
# Brain (Voxel)
G_Voxel = nx.read_adjlist('DataNetStats/Oxford_sub16112_voxel_d20.adjlist')

##### Global efficiencies
print('Global eddiciencies')
print('C. Elegans: %5.3f' % nx.global_efficiency(G_CEleg))
print('Power grid: %5.3f' % nx.global_efficiency(G_Power))
print('Brain (ROI): %5.3f' % nx.global_efficiency(G_ROI))
print('Brain (Voxel): %5.3f' % nx.global_efficiency(G_Voxel))
#0.1869544358446755
