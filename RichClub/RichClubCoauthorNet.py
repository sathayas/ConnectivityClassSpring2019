import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
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



##### loading the network data, network science co-authorship network
H_Net = nx.read_gml('DataRichClub/netscience.gml')
# extracting giant component nodes
GCnodes_Net = max(nx.connected_components(H_Net), key=len)  
# giant component as a network
G_Net = H_Net.subgraph(GCnodes_Net)   




##### Rich club coefficient (original network)
RCdict_Net = nx.rich_club_coefficient(G_Net, normalized=False)

# extracting the degree and rich club coeff from the dictionary
K_Net = [k for k, rc in RCdict_Net.items()]
RC_Net = [rc for k, rc in RCdict_Net.items()]



##### Rich club coefficient (random network)
# first generating a random network
Grand_Net = rewire_multi(G_Net, 10*len(G_Net.nodes()))

# rich club coefficient of the random network
RCrandDict_Net = nx.rich_club_coefficient(Grand_Net, normalized=False)

# extracting the degree and rich club coeff from the dictionary
Krand_Net = [k for k, rc in RCrandDict_Net.items()]
RCrand_Net = [rc for k, rc in RCrandDict_Net.items()]



##### Rich club coefficient (original vs random)
RC = np.array(RC_Net) / np.array(RCrand_Net)


##### Finally plotting the rich club coefficients
plt.plot(K_Net,RC_Net,'bo-', label='Original network')
plt.plot(Krand_Net,RCrand_Net,'mo-', label='Random network')
plt.plot(K_Net,RC,'ro-', label='Normalized RC')
plt.xlabel('Degree')
plt.ylabel('Rich club coefficient')
plt.show()

