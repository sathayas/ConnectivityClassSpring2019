import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##### loading the network data
# Florentine family network
G_Flo = nx.Graph(nx.read_pajek('DataCentrality/Padgett.paj'))
G_Flo.remove_node('Pucci') # removing isolated node




##### betweenness centrality
Cbet_Flo = nx.betweenness_centrality(G_Flo)




##### sorting nodes by betweenness centrality
# first, Florentine network
Cbet_Flo_node = Cbet_Flo.keys()
Cbet_Flo_k = Cbet_Flo.values()
sortedNodes_Flo = sorted(zip(Cbet_Flo_node, Cbet_Flo_k), 
                            key=lambda x: x[1], reverse=True)
sCbet_Flo_node, sCbet_Flo_k = zip(*sortedNodes_Flo)


###### top nodes and their betweenness centrality
print('Florentine family network -- Top betweenness centrality nodes')
print('Node           \tBetweenness centrality')
for iNode in range(5):
    print('%-14s\t' % str(sCbet_Flo_node[iNode]), end='')
    print('%6.4f' % sCbet_Flo_k[iNode])
print()


###### drawing the graph (Florentine network) --- Kamada-Kawai layout --- just getting pos
pos = nx.kamada_kawai_layout(G_Flo, weight=None) # positions for all nodes



###### Adding bypasses
G_Flo.add_edges_from([('Strozzi', 'Tornabuoni'),
                      ('Tornabuoni', 'Albizzi'),
                      ('Tornabuoni', 'Salviati'),
                      ('Tornabuoni', 'Acciaiuoli')])


##### betweenness centrality, again
Cbet_Flo = nx.betweenness_centrality(G_Flo)


##### sorting nodes by betweenness centrality
# first, Florentine network
Cbet_Flo_node = Cbet_Flo.keys()
Cbet_Flo_k = Cbet_Flo.values()
sortedNodes_Flo = sorted(zip(Cbet_Flo_node, Cbet_Flo_k), 
                            key=lambda x: x[1], reverse=True)
sCbet_Flo_node, sCbet_Flo_k = zip(*sortedNodes_Flo)


###### top nodes and their betweenness centrality
print('Florentine family network -- Top betweenness centrality nodes')
print('Node           \tBetweenness centrality')
for iNode in range(5):
    print('%-14s\t' % str(sCbet_Flo_node[iNode]), end='')
    print('%6.4f' % sCbet_Flo_k[iNode])
print()





###### drawing the graph (Florentine network) --- Kamada-Kawai layout
plt.figure(figsize=[9,9])
nx.draw_networkx_nodes(G_Flo, pos, 
                       cmap=plt.cm.coolwarm, node_color=list(Cbet_Flo_k))
nx.draw_networkx_edges(G_Flo, pos, edge_color='lightblue')
nx.draw_networkx_labels(G_Flo, pos, font_size=10, font_color='black')
plt.axis('off')
plt.title('Florentine family network\nand betweenness centrality')
vmin = sCbet_Flo_k[-1]
vmax = sCbet_Flo_k[0]
sm = plt.cm.ScalarMappable(cmap=plt.cm.coolwarm, 
                           norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = plt.colorbar(sm, shrink=0.5)
cbar.ax.set_ylabel('Betweenness centrality')
plt.show()



