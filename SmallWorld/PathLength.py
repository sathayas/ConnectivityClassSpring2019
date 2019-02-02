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


##### Path Length
print('Average shortest path lengths')
print('C. Elegans: %4.2f' % nx.average_shortest_path_length(G_CEleg))
print('Power grid: %4.2f' % nx.average_shortest_path_length(G_Power))
print('Brain (ROI): %4.2f' % nx.average_shortest_path_length(G_ROI))
print('Brain (Voxel): %4.2f' % nx.average_shortest_path_length(G_Voxel))


#### Checking the connected components
ccSize_ROI = [len(c) for c in sorted(nx.connected_components(G_ROI),
                                     key=len,
                                     reverse=True)]
print('Brain (ROI), connected component sizes: ', ccSize_ROI)

ccSize_Voxel = [len(c) for c in sorted(nx.connected_components(G_Voxel),
                                       key=len,
                                       reverse=True)]
print('Brain (Voxel), connected component sizes: ', ccSize_Voxel)


##### Path length, giant component only
GC_nodes_ROI = max(nx.connected_components(G_ROI), key=len)  # nodes in giant component
GC_ROI = G_ROI.subgraph(GC_nodes_ROI)  # nodes & edges in giant component
print('Path length, brain (ROI): %4.2f'  % nx.average_shortest_path_length(GC_ROI))

GC_nodes_Voxel = max(nx.connected_components(G_Voxel), key=len) 
GC_Voxel = G_Voxel.subgraph(GC_nodes_Voxel)  # nodes & edges in giant component
print('Path length, brain (Voxel): %4.2f'  % nx.average_shortest_path_length(GC_Voxel))
