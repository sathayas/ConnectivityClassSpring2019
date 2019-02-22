import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd


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
H = nx.read_adjlist('DataRichClub/Berlin_sub91116_aal90_d5_annotated.adjlist')
# extracting giant component nodes
GCnodes = max(nx.connected_components(H), key=len)  
# giant component as a network
G = H.subgraph(GCnodes)   


###### drawing the graph --- in the brain space
# loading the coordinates info for brain areas
AALTable = pd.read_csv('DataRichClub/aal_MNI_V4_coord.csv')
# dictionary of xy-coordinates
pos = {}
for i in range(1,91):
    pos[AALTable.iloc[i-1,1]] = np.array(AALTable.loc[i-1,
                                                      ['centerX',
                                                       'centerY']])

# Actual drawing
plt.figure(figsize=[9,9])
nx.draw_networkx_nodes(G, pos, node_color='salmon', node_size=200)
nx.draw_networkx_edges(G, pos, edge_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=7, font_color='black')
plt.axis('off')
plt.title('Brain network (Berlin)')
plt.show()



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



##### Extracting the rich club network
RCthresh = 1.20  # if RCnorm is greater than this, rich club for sure
K_RC_min = K[np.min(np.where(RCnorm>RCthresh))]
K_RC_max = K[np.max(np.where(RCnorm>RCthresh))]
# extracting the nodes whose degree within the range of the rich club
nodes_RC = [node for node, degree in dict(G.degree()).items() 
            if K_RC_min<=degree<=K_RC_max]
G_RC = G.subgraph(nodes_RC)
# removing unconnected nodes
node_K0 = [node for node, degree in dict(G_RC.degree()).items()
           if degree==0]
H_RC = G_RC.copy()
H_RC.remove_nodes_from(node_K0)


###### drawing the graph (rich club only) --- Brain space
plt.figure(figsize=[9,9])

nx.draw_networkx_nodes(G, pos, node_color='salmon', node_size=200)
nx.draw_networkx_nodes(H_RC, pos, node_color='deeppink')
nx.draw_networkx_edges(G, pos, edge_color='lightblue')
nx.draw_networkx_edges(H_RC, pos, width=2.0, edge_color='darkblue')
nx.draw_networkx_labels(H_RC, pos, font_size=10, font_color='black')
plt.axis('off')
plt.title('Brain network (Berlin)\nRich club nodes and edges')
plt.show()
