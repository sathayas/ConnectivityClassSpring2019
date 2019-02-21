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



##### loading the network data
H = nx.read_gml('DataRichClub/dolphins.gml')
# extracting giant component nodes
GCnodes = max(nx.connected_components(H), key=len)  
# giant component as a network
G = H.subgraph(GCnodes)   




##### Rich club coefficient (original network)
RCdict = nx.rich_club_coefficient(G, normalized=False)

# extracting the degree and rich club coeff from the dictionary
K = [k for k, rc in RCdict.items()]
RCorig = [rc for k, rc in RCdict.items()]



##### Rich club coefficient (random network)
RCrand = np.zeros_like(RCorig)
nIter = 200 # number of random networks to be generated
print('Generating random networks ')
for iIter in range(nIter):
    print('.',end='')
    if (iIter+1)%20 == 0:
        print()

    # first generating a random network
    Grand = rewire_multi(G, 10*len(G.nodes()))

    # rich club coefficient of the random network
    RCrandDict = nx.rich_club_coefficient(Grand, normalized=False)

    # extracting rich club coeff from the dictionary
    tmpRC = np.array([rc for k, rc in RCrandDict.items()])
    RCrand += tmpRC

print('done!')
# dividing RC by the number of iterations to get the average
RCrand /= nIter


##### Rich club coefficient (original vs random)
RCnorm = np.array(RCorig) / RCrand


##### Finally plotting the rich club coefficients
plt.plot(K,RCorig,'bo-', label='Original network')
plt.plot(K,RCrand,'mo-', label='Random network')
plt.plot(K,RCnorm,'ro-', label='Normalized RC')
plt.xlabel('Degree')
plt.ylabel('Rich club coefficient')
plt.show()

