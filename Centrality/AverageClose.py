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




##### closeness centrality
Cclo_Berlin = nx.closeness_centrality(G_Berlin)  
Cclo_Leiden = nx.closeness_centrality(G_Leiden)  
Cclo_NY = nx.closeness_centrality(G_NY)  
Cclo_Oxford = nx.closeness_centrality(G_Oxford)  
Cclo_Queen = nx.closeness_centrality(G_Queen)  


##### averaging closeness centralities
Cclo_Avg = Cclo_Berlin.copy()
listCclo = [Cclo_Berlin, Cclo_Leiden, Cclo_NY, Cclo_Oxford, Cclo_Queen]
for iNode in Cclo_Avg.keys():
    sumCclo = 0
    for iNet in listCclo:
        sumCclo += iNet[iNode]
    Cclo_Avg[iNode] = sumCclo/5


##### sorting nodes by closeness centrality
Cclo_Avg_node = Cclo_Avg.keys()
Cclo_Avg_k = Cclo_Avg.values()
sortedNodes_Avg = sorted(zip(Cclo_Avg_node, Cclo_Avg_k), 
                            key=lambda x: x[1], reverse=True)
sCclo_Avg_node, sCclo_Avg_k = zip(*sortedNodes_Avg)


###### top nodes and their closeness centrality
print('Brain network (average) -- Top closeness centrality nodes')
print('Node           \t\tCloseness centrality')
for iNode in range(10):
    print('%-20s\t' % str(sCclo_Avg_node[iNode]), end='')
    print('%6.4f' % sCclo_Avg_k[iNode])
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
                       cmap=plt.cm.coolwarm, node_color=list(Cclo_Avg_k))
nx.draw_networkx_labels(G_Berlin, pos, font_size=7, font_color='black')
plt.axis('off')
plt.title('Brain network average closeness centrality')
vmin = sCclo_Avg_k[-1]
vmax = sCclo_Avg_k[0]
sm = plt.cm.ScalarMappable(cmap=plt.cm.coolwarm, 
                           norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = plt.colorbar(sm, shrink=0.5)
cbar.ax.set_ylabel('Closeness centrality')
plt.show()

