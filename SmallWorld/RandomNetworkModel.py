import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def pick_4nodes(G):
    a = random.choice(list(G.nodes()))  # a random node
    b = random.choice(list(G[a]))       # a random node connected to a
    while True:
        # potential pool of nodes to draw c
        cPool = (set(G.nodes())-set(G[a])).intersection(set(G.nodes())-set(G[b]))
        c = random.choice(list(cPool))
        # potential pool of nodes to draw d
        dPool = (set(G[c])-set(G[a])).intersection(set(G[c])-set(G[b]))
        if len(dPool)>0:
            d = random.choice(list(dPool))
            break
    return [a,b,c,d]


def rewire_multi(G,nIter):
    H = G.copy()
    for i in range(nIter):
        list4nodes = pick_4nodes(H)
        H.remove_edge(list4nodes[0],list4nodes[1])
        H.remove_edge(list4nodes[2],list4nodes[3])
        H.add_edge(list4nodes[0],list4nodes[2])
        H.add_edge(list4nodes[1],list4nodes[3])
    return H


def path_length_gc(G):
    GC_nodes = max(nx.connected_components(G), key=len)  # giant component nodes
    GC = G.subgraph(GC_nodes)
    L = nx.average_shortest_path_length(GC)
    return L


##### loading the network data
# C Elegans neural network
G_CEleg = nx.read_adjlist('DataSmallWorld/CElegans.adjlist')
# Power grid
G_Power = nx.read_gml('DataSmallWorld/power.gml', label='id')
# Brain (ROI)
G_ROI = nx.read_adjlist('DataSmallWorld/Oxford_sub16112_aal90_d5.adjlist')
# Brain (Voxel)
G_Voxel = nx.read_adjlist('DataSmallWorld/Oxford_sub16112_voxel_d20.adjlist')


##### C. Elegan network degee sequence before re-wiring
degree_CEleg = [d for n, d in G_CEleg.degree()]
degree_CEleg.sort()
plt.plot(degree_CEleg,'b-')
plt.ylabel('Node degree')
plt.title('Degree sequence (original network)\nsmallest to largest')
plt.show()

##### Rewiring C. Elegans network
H_CEleg = rewire_multi(G_CEleg,10*len(G_CEleg.nodes()))

##### C. Elegan network degee sequence after re-wiring
degree_CEleg_rewire = [d for n, d in H_CEleg.degree()]
degree_CEleg_rewire.sort()
plt.plot(degree_CEleg_rewire,'g-')
plt.ylabel('Node degree')
plt.title('Degree sequence (rewired network)\nsmallest to largest')
plt.show()


##### Clustering coeff, before and after rewiring
print('Clustering, before: %6.4f' % nx.average_clustering(G_CEleg))
print('Clustering, after: %6.4f' % nx.average_clustering(H_CEleg))

##### Path length, before and after rewiring
print('Path length, before: %4.2f' % path_length_gc(G_CEleg))
print('Path length, after: %4.2f' % path_length_gc(H_CEleg))



