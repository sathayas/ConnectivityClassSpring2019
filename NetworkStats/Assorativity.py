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


##### Assortativity coefficients
print('Assortativity coefficients')
print('C. Elegans: %5.3f' % nx.degree_assortativity_coefficient(G_CEleg))
print('Power grid: %5.3f' % nx.degree_assortativity_coefficient(G_Power))
print('Brain (ROI): %5.3f' % nx.degree_assortativity_coefficient(G_ROI))
print('Brain (Voxel): %5.3f' % nx.degree_assortativity_coefficient(G_Voxel))


##### Assorativity mixing matrix
plt.figure(figsize=[9,9])

plt.subplot(221)
M_CEleg = nx.degree_mixing_matrix(G_CEleg)
plt.imshow(M_CEleg)
plt.colorbar()
plt.title('Mixing matrix, C Elegan')
plt.xlabel('Terminus degree')
plt.ylabel('Origin degree')

plt.subplot(222)
M_Power = nx.degree_mixing_matrix(G_Power)
plt.imshow(M_Power)
plt.colorbar()
plt.title('Mixing matrix, power grid')
plt.xlabel('Terminus degree')
plt.ylabel('Origin degree')

plt.subplot(223)
M_ROI = nx.degree_mixing_matrix(G_ROI)
plt.imshow(M_ROI)
plt.colorbar()
plt.title('Mixing matrix, brain (ROI)')
plt.xlabel('Terminus degree')
plt.ylabel('Origin degree')

plt.subplot(224)
M_Voxel = nx.degree_mixing_matrix(G_Voxel)
plt.imshow(M_Voxel)
plt.colorbar()
plt.title('Mixing matrix, brain (voxel)')
plt.xlabel('Terminus degree')
plt.ylabel('Origin degree')

plt.show()
