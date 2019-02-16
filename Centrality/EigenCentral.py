import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##### loading the network data
# Florentine family network
G_Flo = nx.Graph(nx.read_pajek('DataCentrality/Padgett.paj'))
G_Flo.remove_node('Pucci') # removing isolated node
# Brain (Berlin)
G_Berlin = nx.read_adjlist('DataCentrality/Berlin_sub91116_aal90_d10_annotated.adjlist')
# Brain (Leiden)
G_Leiden = nx.read_adjlist('DataCentrality/Leiden_sub30943_aal90_d10_annotated.adjlist')
# Brain (New York)
G_NY = nx.read_adjlist('DataCentrality/NewYork_sub78118_aal90_d10_annotated.adjlist')
# Brain (Oxford)
G_Oxford = nx.read_adjlist('DataCentrality/Oxford_sub16112_aal90_d10_annotated.adjlist')
# Brain (Queensland)
G_Queen = nx.read_adjlist('DataCentrality/Queensland_sub42533_aal90_d10_annotated.adjlist')




##### eigenvector centrality
Ceig_Flo = nx.eigenvector_centrality(G_Flo)
Ceig_Berlin = nx.eigenvector_centrality(G_Berlin)  




##### sorting nodes by eigenvector centrality
# first, Florentine network
Ceig_Flo_node = Ceig_Flo.keys()
Ceig_Flo_k = Ceig_Flo.values()
sortedNodes_Flo = sorted(zip(Ceig_Flo_node, Ceig_Flo_k), 
                            key=lambda x: x[1], reverse=True)
sCeig_Flo_node, sCeig_Flo_k = zip(*sortedNodes_Flo)

# next, brain network (Berlin)
Ceig_Berlin_node = Ceig_Berlin.keys()
Ceig_Berlin_k = Ceig_Berlin.values()
sortedNodes_Berlin = sorted(zip(Ceig_Berlin_node, Ceig_Berlin_k), 
                            key=lambda x: x[1], reverse=True)
sCeig_Berlin_node, sCeig_Berlin_k = zip(*sortedNodes_Berlin)



###### top nodes and their eigenvector centrality
print('Florentine family network -- Top eigenvector centrality nodes')
print('Node           \tEigenvector centrality')
for iNode in range(5):
    print('%-14s\t' % str(sCeig_Flo_node[iNode]), end='')
    print('%6.4f' % sCeig_Flo_k[iNode])
print()

print('Brain network (Berlin) -- Top eigenvector centrality nodes')
print('Node           \t\tEigenvector centrality')
for iNode in range(10):
    print('%-20s\t' % str(sCeig_Berlin_node[iNode]), end='')
    print('%6.4f' % sCeig_Berlin_k[iNode])
print()




###### drawing the graph (Florentine network) --- Kamada-Kawai layout
plt.figure(figsize=[9,9])
pos = nx.kamada_kawai_layout(G_Flo, weight=None) # positions for all nodes
nx.draw_networkx_nodes(G_Flo, pos, 
                       cmap=plt.cm.coolwarm, node_color=list(Ceig_Flo_k))
nx.draw_networkx_edges(G_Flo, pos, edge_color='lightblue')
nx.draw_networkx_labels(G_Flo, pos, font_size=10, font_color='black')
plt.axis('off')
plt.title('Florentine family network\nand eigenvector centrality')
vmin = sCeig_Flo_k[-1]
vmax = sCeig_Flo_k[0]
sm = plt.cm.ScalarMappable(cmap=plt.cm.coolwarm, 
                           norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = plt.colorbar(sm, shrink=0.5)
cbar.ax.set_ylabel('Eigenvector centrality')
plt.show()



###### drawing the graph (Brain, Berlin) --- their brain space coordinate
# loading the coordinates info for brain areas
AALTable = pd.read_csv('DataCentrality/aal_MNI_V4_coord.csv')
# dictionary of xy-coordinates
pos = {}
for i in range(1,91):
    pos[AALTable.iloc[i-1,1]] = np.array(AALTable.loc[i-1,
                                                      ['centerX',
                                                       'centerY']])


# Actual drawing
plt.figure(figsize=[9,9])
nx.draw_networkx_nodes(G_Berlin, pos, 
                       cmap=plt.cm.coolwarm, node_color=list(Ceig_Berlin_k))
nx.draw_networkx_edges(G_Berlin, pos, edge_color='lightblue')
nx.draw_networkx_labels(G_Berlin, pos, font_size=7, font_color='black')
plt.axis('off')
plt.title('Brain network (Berlin)\nand eigenvector centrality')
vmin = sCeig_Berlin_k[-1]
vmax = sCeig_Berlin_k[0]
sm = plt.cm.ScalarMappable(cmap=plt.cm.coolwarm, 
                           norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = plt.colorbar(sm, shrink=0.5)
cbar.ax.set_ylabel('Eigenvector centrality')
plt.show()

