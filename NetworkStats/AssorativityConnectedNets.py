import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

##### loading the network data
# Brain (ROI)
G_ROI = nx.read_adjlist('DataNetStats/Oxford_sub16112_aal90_d5.adjlist')
# Brain (Voxel)
G_Voxel = nx.read_adjlist('DataNetStats/Oxford_sub16112_voxel_d20.adjlist')
# Brain (ROI), connected
G_ROI_conn = nx.read_adjlist('DataNetStats/Oxford_sub16112_aal90_d5_connected.adjlist')
# Brain (Voxel), connected
G_Voxel_conn = nx.read_adjlist('DataNetStats/Oxford_sub16112_voxel_d20_connected.adjlist')


##### Number of nodes and edges
print('Number of nodes and edges')
print('Brain (ROI): nodes: %d' % len(G_ROI.nodes()),
      ' edges: %d' % len(G_ROI.edges()))
print('Brain (Voxel): nodes: %d' % len(G_Voxel.nodes()),
      ' edges: %d' % len(G_Voxel.edges()))
print('Brain (ROI, connected): nodes: %d' % len(G_ROI_conn.nodes()),
      ' edges: %d' % len(G_ROI_conn.edges()))
print('Brain (Voxel, connected): nodes: %d' % len(G_Voxel_conn.nodes()),
      ' edges: %d' % len(G_Voxel_conn.edges()))


##### Assortativity coefficients
print('Assortativity coefficients')
print('Brain (ROI): %5.3f' % nx.degree_assortativity_coefficient(G_ROI))
print('Brain (Voxel): %5.3f' % nx.degree_assortativity_coefficient(G_Voxel))
print('Brain (ROI, connected): %5.3f' % nx.degree_assortativity_coefficient(G_ROI_conn))
print('Brain (Voxel, connected): %5.3f' % nx.degree_assortativity_coefficient(G_Voxel_conn))


##### Assorativity mixing matrix
plt.figure(figsize=[9,9])

plt.subplot(221)
M_ROI = nx.degree_mixing_matrix(G_ROI)
plt.imshow(M_ROI)
plt.colorbar()
plt.title('Mixing matrix, brain (ROI)')
plt.xlabel('Terminus degree')
plt.ylabel('Origin degree')

plt.subplot(222)
M_Voxel = nx.degree_mixing_matrix(G_Voxel)
plt.imshow(M_Voxel)
plt.colorbar()
plt.title('Mixing matrix, brain (voxel)')
plt.xlabel('Terminus degree')
plt.ylabel('Origin degree')

plt.subplot(223)
M_ROI = nx.degree_mixing_matrix(G_ROI_conn)
plt.imshow(M_ROI)
plt.colorbar()
plt.title('Mixing matrix, brain (ROI, connected)')
plt.xlabel('Terminus degree')
plt.ylabel('Origin degree')

plt.subplot(224)
M_Voxel = nx.degree_mixing_matrix(G_Voxel_conn)
plt.imshow(M_Voxel)
plt.colorbar()
plt.title('Mixing matrix, brain (voxel, connected)')
plt.xlabel('Terminus degree')
plt.ylabel('Origin degree')

plt.subplots_adjust(wspace=0.3, hspace=0.3)
plt.show()
