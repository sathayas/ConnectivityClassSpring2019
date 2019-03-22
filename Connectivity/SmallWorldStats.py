import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

##### loading the network data
# correlatio network
G = nx.read_adjlist('DataConnectivity/Oxford_sub16112_Rt2_K200_deg10.adjlist',
                    nodetype=int)
# partial correlatio network
G_pc = nx.read_adjlist('DataConnectivity/Oxford_sub16112_Rt2_K200_deg10_pc.adjlist',
                       nodetype=int)
# mutual information network
G_mi = nx.read_adjlist('DataConnectivity/Oxford_sub16112_Rt2_K200_deg10_mi.adjlist',
                       nodetype=int)


##### Clustering coefficients
print('Clustering coefficients')
print('Correlation network: %4.2f' % nx.average_clustering(G))
print('Partial correlation network: %4.2f' % nx.average_clustering(G_pc))
print('Mutual information network: %4.2f' % nx.average_clustering(G_mi))


##### giant components
GC_nodes = max(nx.connected_components(G), key=len)  # nodes in GC
GC = G.subgraph(GC_nodes)  # nodes & edges in giant component
GC_nodes_pc = max(nx.connected_components(G_pc), key=len)  # nodes in GC
GC_pc = G_pc.subgraph(GC_nodes_pc)  # nodes & edges in giant component
GC_nodes_mi = max(nx.connected_components(G_mi), key=len)  # nodes in GC
GC_mi = G_mi.subgraph(GC_nodes_mi)  # nodes & edges in giant component


##### Path Length
print('Average shortest path lengths (GC size)')
print('Correlation network: %4.2f' %
      nx.average_shortest_path_length(GC) + '(%d)' % len(GC_nodes))
print('Partial correlation network: %4.2f' %
      nx.average_shortest_path_length(GC_pc) + '(%d)' % len(GC_nodes_pc))
print('Mutual information network: %4.2f' %
      nx.average_shortest_path_length(GC_mi) + '(%d)' % len(GC_nodes_mi))


