import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##### loading the network data
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
Ceig_Berlin = nx.eigenvector_centrality(G_Berlin)  
Ceig_Leiden = nx.eigenvector_centrality(G_Leiden)  
Ceig_NY = nx.eigenvector_centrality(G_NY)  
Ceig_Oxford = nx.eigenvector_centrality(G_Oxford)  
Ceig_Queen = nx.eigenvector_centrality(G_Queen)  


##### averaging eigenvector centralities
Ceig_Avg = Ceig_Berlin.copy()
listCeig = [Ceig_Berlin, Ceig_Leiden, Ceig_NY, Ceig_Oxford, Ceig_Queen]
for iNode in Ceig_Avg.keys():
    sumCeig = 0
    for iNet in listCeig:
        sumCeig += iNet[iNode]
    Ceig_Avg[iNode] = sumCeig/5


##### sorting nodes by eigenvector centrality
Ceig_Avg_node = Ceig_Avg.keys()
Ceig_Avg_k = Ceig_Avg.values()
sortedNodes_Avg = sorted(zip(Ceig_Avg_node, Ceig_Avg_k), 
                            key=lambda x: x[1], reverse=True)
sCeig_Avg_node, sCeig_Avg_k = zip(*sortedNodes_Avg)


###### top nodes and their eigenvector centrality
print('Brain network (average) -- Top eigenvector centrality nodes')
print('Node           \t\tEigenvector centrality')
for iNode in range(10):
    print('%-20s\t' % str(sCeig_Avg_node[iNode]), end='')
    print('%6.4f' % sCeig_Avg_k[iNode])
print()



###### drawing the nodes (Brain, average) --- their brain space coordinate
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
                       cmap=plt.cm.coolwarm, node_color=list(Ceig_Avg_k))
nx.draw_networkx_labels(G_Berlin, pos, font_size=7, font_color='black')
plt.axis('off')
plt.title('Brain network average eigenvector centrality')
vmin = sCeig_Avg_k[-1]
vmax = sCeig_Avg_k[0]
sm = plt.cm.ScalarMappable(cmap=plt.cm.coolwarm, 
                           norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = plt.colorbar(sm, shrink=0.5)
cbar.ax.set_ylabel('Eigenvector centrality')
plt.show()

