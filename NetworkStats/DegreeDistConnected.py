import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

##### loading the network data
# Brain (ROI), connected
G_ROI_conn = nx.read_adjlist('DataNetStats/Oxford_sub16112_aal90_d5_connected.adjlist')
# Brain (Voxel), connected
G_Voxel_conn = nx.read_adjlist('DataNetStats/Oxford_sub16112_voxel_d20_connected.adjlist')


##### Degree sequence
k_ROI_conn = [d for n, d in G_ROI_conn.degree()]
k_Voxel_conn = [d for n, d in G_Voxel_conn.degree()]


###### Cumulative distributions
sk_ROI_conn = sorted(k_ROI_conn, reverse=True) 
sk_Voxel_conn = sorted(k_Voxel_conn, reverse=True) 


###### Cumulative distribution plots together
plt.plot(sk_ROI_conn, np.arange(1,len(sk_ROI_conn)+1)/len(sk_ROI_conn), 
         label='Brain (ROI), connected')
plt.plot(sk_Voxel_conn, np.arange(1,len(sk_Voxel_conn)+1)/len(sk_Voxel_conn), 
         label='Brain (voxel), connected')
plt.title('Degree distributions')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show()
