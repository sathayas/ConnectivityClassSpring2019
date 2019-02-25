import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

##### Custom distinct color function --- to be used later
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


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



##### K-core number
KcoreDict = nx.core_number(G)
listCoreNum = [kc for kc in KcoreDict.values()]
minKCore = min(listCoreNum)
maxKCore = max(listCoreNum)

###### drawing the graph --- Kamada-Kawai layout
node_color_list = get_cmap(maxKCore+1,'rainbow')
plt.figure(figsize=[9,9])
# k-core nodes
for iCore in range(minKCore,maxKCore+1):
    nodeCore = [node for node, coreNum in KcoreDict.items()
                if coreNum>=iCore]
    subG = G.subgraph(nodeCore)
    nx.draw_networkx_nodes(subG, pos, node_color=node_color_list(iCore),
                           node_size=150+iCore*60, label=str(iCore)+'-core')
nx.draw_networkx_edges(G, pos, edge_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=8, font_color='black')
plt.axis('off')
plt.title('Dolphin social network\nShowing K-cores')
plt.legend()
plt.show()

