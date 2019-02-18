import networkx as nx
import numpy as np

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



def top10(G):
    ##### eigenvector centrality
    Ceig = nx.eigenvector_centrality(G)

    ##### sorting nodes by eigenvector centrality
    Ceig_node = Ceig.keys()
    Ceig_k = Ceig.values()
    sortedNodes = sorted(zip(Ceig_node, Ceig_k), 
                            key=lambda x: x[1], reverse=True)
    sCeig_node, sCeig_k = zip(*sortedNodes)

    ###### top nodes and their eigenvector centrality
    print('Node           \t\tEigenvector centrality')
    for iNode in range(10):
        print('%-20s\t' % str(sCeig_node[iNode]), end='')
        print('%6.4f' % sCeig_k[iNode])
    print()


##### top 10 eigenvector centralities
print('Berlin')
top10(G_Berlin)
print('Leiden')
top10(G_Leiden)
print('New York')
top10(G_NY)
print('Oxford')
top10(G_Oxford)
print('Queensland')
top10(G_Queen)
