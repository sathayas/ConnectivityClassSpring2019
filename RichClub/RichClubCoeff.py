import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

##### network rewiring functions -- used to generate random network models
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



##### loading the network data
# C Elegan neural network
G_CEleg = nx.read_adjlist('DataRichClub/CElegans.adjlist')
# Centrality literature network
H_Lit = nx.Graph(nx.read_pajek('DataRichClub/centrality_literature.paj'))
GCnodes_Lit = max(nx.connected_components(H_Lit), key=len)  # giant component nodes
G_Lit = G_Lit.subgraph(GCnodes_Lit)   # giant component network
# Power grid
G_Power = nx.read_gml('DataRichClub/power.gml', label='id')
# Brain (Berlin)
G_Berlin = nx.read_adjlist('DataRichClub/Berlin_sub91116_aal90_d10_annotated.adjlist')
# Brain (Leiden)
G_Leiden = nx.read_adjlist('DataRichClub/Leiden_sub30943_aal90_d10_annotated.adjlist')
# Brain (New York)
G_NY = nx.read_adjlist('DataRichClub/NewYork_sub78118_aal90_d10_annotated.adjlist')
# Brain (Oxford)
G_Oxford = nx.read_adjlist('DataRichClub/Oxford_sub16112_aal90_d10_annotated.adjlist')
# Brain (Queensland)
G_Queen = nx.read_adjlist('DataRichClub/Queensland_sub42533_aal90_d10_annotated.adjlist')



##### Rich club coefficient (original network)
RC_dict_Berlin = nx.rich_club_coefficient(G_Berlin, normalized=False)

K_Berlin = [k for k, rc in RC_dict_Berlin.items()]
RC_Berlin = [rc for k, rc in RC_dict_Berlin.items()]
plt.plot(K_Berlin, RC_Berlin)
plt.show()



##### Rich club coefficient (random network)
Grand_Berlin = rewire_multi(G_Berlin, 10*len(G_Berlin.nodes()))

RCrand_dict_Berlin = nx.rich_club_coefficient(Grand_Berlin, normalized=False)

Krand_Berlin = [k for k, rc in RCrand_dict_Berlin.items()]
RCrand_Berlin = [rc for k, rc in RCrand_dict_Berlin.items()]
plt.plot(Krand_Berlin, RCrand_Berlin)
plt.show()


##### Rich club coefficient (original vs random
RC = np.array(RC_Berlin) / np.array(RCrand_Berlin)
