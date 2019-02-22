import networkx as nx
import numpy as np
import matplotlib.pyplot as plt



##### loading the network data
H = nx.read_gml('DataRichClub/dolphins.gml')
# extracting giant component nodes
GCnodes = max(nx.connected_components(H), key=len)  
# giant component as a network
G = H.subgraph(GCnodes)   


###### drawing the graph --- Kamada-Kawai layout
plt.figure(figsize=[9,9])
pos = nx.kamada_kawai_layout(G, weight=None) # positions for all nodes
nx.draw_networkx_nodes(G, pos, node_color='salmon', node_size=200)
nx.draw_networkx_edges(G, pos, edge_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=7, font_color='black')
plt.axis('off')
plt.title('Dolphin social network')
plt.show()



##### K-core number
KcoreDict = nx.core_number(G)


###### drawing the graph --- Kamada-Kawai layout
node_color_list = ['salmon','gold','limegreen','royalblue','fuchsia']
plt.figure(figsize=[9,9])
nx.draw_networkx_nodes(G, pos, node_color='salmon', node_size=150)
# k-core nodes
for iCore in range(2,5):
    nodeCore = [node for node, coreNum in KcoreDict.items()
                if coreNum>=iCore]
    subG = G.subgraph(nodeCore)
    nx.draw_networkx_nodes(subG, pos, node_color=node_color_list[iCore],
                           node_size=iCore*200)
nx.draw_networkx_edges(G, pos, edge_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=8, font_color='black')
plt.axis('off')
plt.title('Dolphin social network')
plt.show()

