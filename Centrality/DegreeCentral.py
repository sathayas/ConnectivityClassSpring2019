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




##### degree centrality
Cdeg_Flo = nx.degree_centrality(G_Flo)
Cdeg_Berlin = nx.degree_centrality(G_Berlin)  




##### sorting nodes by degree centrality
# first, Florentine network
Cdeg_Flo_node = Cdeg_Flo.keys()
Cdeg_Flo_k = Cdeg_Flo.values()
sortedNodes_Flo = sorted(zip(Cdeg_Flo_node, Cdeg_Flo_k), 
                            key=lambda x: x[1], reverse=True)
sCdeg_Flo_node, sCdeg_Flo_k = zip(*sortedNodes_Flo)

# next, brain network (Berlin)
Cdeg_Berlin_node = Cdeg_Berlin.keys()
Cdeg_Berlin_k = Cdeg_Berlin.values()
sortedNodes_Berlin = sorted(zip(Cdeg_Berlin_node, Cdeg_Berlin_k), 
                            key=lambda x: x[1], reverse=True)
sCdeg_Berlin_node, sCdeg_Berlin_k = zip(*sortedNodes_Berlin)



###### top nodes and their degree centrality
print('Florentine family network -- Top degree centrality nodes')
print('Node           \tDegree centrality')
for iNode in range(5):
    print('%-14s\t' % str(sCdeg_Flo_node[iNode]), end='')
    print('%6.4f' % sCdeg_Flo_k[iNode])
print()

print('Brain network (Berlin) -- Top degree centrality nodes')
print('Node           \t\tDegree centrality')
for iNode in range(10):
    print('%-20s\t' % str(sCdeg_Berlin_node[iNode]), end='')
    print('%6.4f' % sCdeg_Berlin_k[iNode])
print()




###### drawing the graph (Florentine network) --- Kamada-Kawai layout
plt.figure(figsize=[9,9])
pos = nx.kamada_kawai_layout(G_Flo, weight=None) # positions for all nodes
nx.draw_networkx_nodes(G_Flo, pos, 
                       cmap=plt.cm.coolwarm, node_color=list(Cdeg_Flo_k))
nx.draw_networkx_edges(G_Flo, pos, edge_color='lightblue')
nx.draw_networkx_labels(G_Flo, pos, font_size=10, font_color='black')
plt.axis('off')
plt.title('Florentine family network\nand degree centrality')
vmin = sCdeg_Flo_k[-1]
vmax = sCdeg_Flo_k[0]
sm = plt.cm.ScalarMappable(cmap=plt.cm.coolwarm, 
                           norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = plt.colorbar(sm, shrink=0.5)
cbar.ax.set_ylabel('Degree centrality')
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
                       cmap=plt.cm.coolwarm, node_color=list(Cdeg_Berlin_k))
nx.draw_networkx_edges(G_Berlin, pos, edge_color='lightblue')
nx.draw_networkx_labels(G_Berlin, pos, font_size=7, font_color='black')
plt.axis('off')
plt.title('Brain network (Berlin)\nand degree centrality')
vmin = sCdeg_Berlin_k[-1]
vmax = sCdeg_Berlin_k[0]
sm = plt.cm.ScalarMappable(cmap=plt.cm.coolwarm, 
                           norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = plt.colorbar(sm, shrink=0.5)
cbar.ax.set_ylabel('Degree centrality')
plt.show()

