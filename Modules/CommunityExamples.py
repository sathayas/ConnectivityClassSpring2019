import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.community import girvan_newman, modularity
import community   # Louvain method

##### Custom distinct color function --- to be used later
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


##### girman-newman method, optimized with modularity
def girvan_newman_opt(G, verbose=False):
    runningMaxMod = 0
    commIndSetFull = girvan_newman(G)
    for iNumComm in range(2,len(G)):
        if verbose:
            print('Commnity detection iteration : %d' % iNumComm, end='')
        iPartition = next(commIndSetFull)  # partition with iNumComm communities
        Q = modularity(G, iPartition)  # modularity
        if verbose:
            print('  Modularity : %6.4f' % Q)
        if Q>runningMaxMod:  # saving the optimum partition and associated info
            runningMaxMod = Q
            OptPartition = iPartition
    return OptPartition



##### loading network data
# Karate network
G_karate = nx.read_gml('DataModules/karate.gml', label='id')  
# Football network
G_football = nx.read_gml('DataModules/football.gml')  


##### Community detection 
# Community detection with the girvan-newman algorithm
commInd_karate = girvan_newman_opt(G_karate)
commInd_football = girvan_newman_opt(G_football)
# converting the partitions into dictionaries
partition_karate_GN = {}
for i,iComm in enumerate(commInd_karate):
    for iNode in iComm:
        partition_karate_GN[iNode] = i
partition_football_GN = {}
for i,iComm in enumerate(commInd_football):
    for iNode in iComm:
        partition_football_GN[iNode] = i


# Community detection with the Louvain method
partition_karate_L = community.best_partition(G_karate)
partition_football_L = community.best_partition(G_football)


###### Modularity
print('Modularity -- karate network')
print('Girvan-Newman: %6.4f' % community.modularity(partition_karate_GN,
                                                    G_karate))
print('Louvain: %6.4f' % community.modularity(partition_karate_L,
                                              G_karate))
print()

print('Modularity -- football network')
print('Girvan-Newman: %6.4f' % community.modularity(partition_football_GN,
                                                    G_football))
print('Louvain: %6.4f' % community.modularity(partition_football_L,
                                              G_football))
print()




###### drawing the graph (karate network)
plt.figure(figsize=[9,4])

# first, graph without community assignments
plt.subplot(131)
pos = nx.kamada_kawai_layout(G_karate, weight=None) # positions for all nodes
nx.draw_networkx_nodes(G_karate, pos)
nx.draw_networkx_edges(G_karate, pos,
                       edge_color='lightblue')
nx.draw_networkx_labels(G_karate, pos, font_size=10, font_color='DarkGreen')
plt.title('Original karate network')
plt.axis('off')
plt.xlim([-0.6, 0.65])
plt.ylim([-0.85, 1.2])

# next, graph with communities in different colors (Girvan-Newman)
plt.subplot(132)
nComm = max([comm for comm in partition_karate_GN.values()])+1
node_color_list = get_cmap(nComm+1,'rainbow')
for iComm in range(nComm):
    nodeList = [iNode for iNode,Comm in partition_karate_GN.items()
                if Comm==iComm]
    nx.draw_networkx_nodes(G_karate, pos, 
                           nodelist=nodeList,
                           node_color = node_color_list(iComm),
                           node_size=300)
nx.draw_networkx_edges(G_karate, pos,
                       edge_color='lightblue')
nx.draw_networkx_labels(G_karate, pos, font_size=10, font_color='White')
plt.title('Girvan-Newman method')
plt.axis('off')
plt.xlim([-0.6, 0.65])
plt.ylim([-0.85, 1.2])

# finally, graph with communities in different colors (Louvain)
plt.subplot(133)
nComm = max([comm for comm in partition_karate_L.values()])+1
node_color_list = get_cmap(nComm+1,'rainbow')
for iComm in range(nComm):
    nodeList = [iNode for iNode,Comm in partition_karate_L.items()
                if Comm==iComm]
    nx.draw_networkx_nodes(G_karate, pos, 
                           nodelist=nodeList,
                           node_color = node_color_list(iComm),
                           node_size=300)
nx.draw_networkx_edges(G_karate, pos,
                       edge_color='lightblue')
nx.draw_networkx_labels(G_karate, pos, font_size=10, font_color='White')
plt.title('Louvain method')
plt.axis('off')
plt.xlim([-0.6, 0.65])
plt.ylim([-0.85, 1.2])

plt.subplots_adjust(hspace=0.15, wspace=0.075, bottom=0.025, top=0.875,
                    left=0.05, right=0.95)
plt.show()



#### drawing the graph (football network)
plt.figure(figsize=[10,4.5])
plt.subplot(131)

# first, graph without community assignments
pos = nx.kamada_kawai_layout(G_football, weight=None) # positions for all nodes
nx.draw_networkx_nodes(G_football, pos, node_size=100)
nx.draw_networkx_edges(G_football, pos,
                       edge_color='lightblue')
nx.draw_networkx_labels(G_football, pos, font_size=7, font_color='Black')
plt.title('Original football network')
plt.axis('off')
plt.xlim([-1.15, 1.15])
plt.ylim([-1.15, 1.15])

# next, graph with communities in different colors (Girvan-Newman)
plt.subplot(132)
nComm = max([comm for comm in partition_football_GN.values()])+1
node_color_list = get_cmap(nComm+1,'rainbow')
for iComm in range(nComm):
    nodeList = [iNode for iNode,Comm in partition_football_GN.items()
                if Comm==iComm]
    nx.draw_networkx_nodes(G_football, pos, 
                           nodelist=nodeList,
                           node_color = node_color_list(iComm),
                           node_size=100)
nx.draw_networkx_edges(G_football, pos,
                       edge_color='lightblue')
nx.draw_networkx_labels(G_football, pos, font_size=7, font_color='black')
plt.title('Girvan-Newman method')
plt.axis('off')
plt.xlim([-1.15, 1.15])
plt.ylim([-1.15, 1.15])

# next, graph with communities in different colors (Louvain)
plt.subplot(133)
nComm = max([comm for comm in partition_football_L.values()])+1
node_color_list = get_cmap(nComm+1,'rainbow')
for iComm in range(nComm):
    nodeList = [iNode for iNode,Comm in partition_football_L.items()
                if Comm==iComm]
    nx.draw_networkx_nodes(G_football, pos, 
                           nodelist=nodeList,
                           node_color = node_color_list(iComm),
                           node_size=100)
nx.draw_networkx_edges(G_football, pos,
                       edge_color='lightblue')
nx.draw_networkx_labels(G_football, pos, font_size=7, font_color='black')
plt.title('Louvain method')
plt.axis('off')
plt.xlim([-1.15, 1.15])
plt.ylim([-1.15, 1.15])


plt.subplots_adjust(hspace=0.15, wspace=0.075, bottom=0.025, top=0.875,
                    left=0.05, right=0.95)
plt.show()


