import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# loading the Les Miserables network
G = nx.read_gml('IntroNetworkData/lesmis.gml')

# drawing the graph  --- Kamada-Kawai layout
plt.figure(figsize=[9,9])
pos = nx.kamada_kawai_layout(G, weight=None) # positions for all nodes
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos, edge_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=10, font_color='DarkGreen')
plt.axis('off')
plt.title('Les Miserables interaction network')
plt.show()


# loading the college football network
G = nx.read_gml('IntroNetworkData/football.gml')

# drawing the graph  --- Kamada-Kawai layout
plt.figure(figsize=[12,12])
pos = nx.kamada_kawai_layout(G, weight=None) # positions for all nodes
# extracting conference information
conf = []
for i,d in G.nodes(data=True):
    conf.append(d['value'])
# drawing nodes, different conferences in different colors
for iConf in range(12):
    nx.draw_networkx_nodes(G, pos,
                           cmap=plt.cm.tab20b, node_color=conf)
nx.draw_networkx_edges(G, pos, edge_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=10, font_color='DarkGreen')
plt.axis('off')
plt.title('College football network')
plt.show()



# loading the C Elegans neural network
G = nx.read_gml('IntroNetworkData/celegansneural.gml')

# drawing the graph  --- Kamada-Kawai layout
plt.figure(figsize=[12,12])
pos = nx.random_layout(G) # positions for all nodes
nx.draw_networkx_nodes(G, pos, node_size=30, node_color='salmon')
nx.draw_networkx_edges(G, pos, edge_color='lightblue')
plt.axis('off')
plt.title('C Elegans neural network')
plt.show()



# loading the fMRI network
G = nx.read_adjlist('IntroNetworkData/Oxford_sub16112_aal90_K20.adjlist', 
                    nodetype=int)
# loading the label for different brain areas
AALTable = pd.read_csv('IntroNetworkData/aal_MNI_V4_coord.csv')
# dictionary of node names and xy-coordinates
roiNames = {}
pos = {}
for i in range(1,91):
    roiNames[i] = AALTable.iloc[i-1,1]
    pos[AALTable.iloc[i-1,1]] = np.array(AALTable.loc[i-1,
                                                      ['centerX',
                                                       'centerY']])
# renaming nodes
H = nx.relabel_nodes(G, roiNames)

# drawing the graph  --- random
plt.figure(figsize=[10,10])
nx.draw_networkx_nodes(H, pos, node_size=30, node_color='lime')
nx.draw_networkx_edges(H, pos, edge_color='palegreen')
nx.draw_networkx_labels(H, pos, font_size=10, font_color='DarkRed')
plt.axis('off')
plt.title('fMRI network')
plt.show()

# Saving the network for future use
nx.write_adjlist(H,'IntroNetworkData/fMRI_Labeled.adjlist')


