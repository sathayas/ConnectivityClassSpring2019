import networkx as nx
import matplotlib.pyplot as plt

# a list of emplyees on the same shift
listWorkers = [['Manager1', 1, 3, 4, 5],
               ['Manager1', 1, 2, 3],
               ['Manager1', 3, 5, 6, 7],
               ['Manager1', 1, 7, 8],
               ['Manager1', 2, 4, 6, 7],
               ['Manager2', 4, 8, 9, 10, 11],
               ['Manager2', 8, 10, 11, 12]]

# first, creating a graph
G=nx.Graph()

# loop over days
for iDay in range(len(listWorkers)):
    # adding nodes. Check if node exists first before adding
    for iNode in listWorkers[iDay]:
        if iNode not in G:
            G.add_node(iNode)
    # adding edges. Check if edge exists before adding
    for i,iNode in enumerate(listWorkers[iDay]):
        for j,jNode in enumerate(listWorkers[iDay],i+1):
            # if iNode and jNode are not connected
            if (iNode!=jNode) and (jNode not in G[iNode]):  
                G.add_edge(iNode,jNode,weight=1.0)
            # if iNode and jNode are connected            
            elif iNode!=jNode:  
                G[iNode][jNode]['weight'] += 1.0


                
# drawing the graph  --- Kamada-Kawai layout
pos = nx.kamada_kawai_layout(G) # positions for all nodes
# nodes
nx.draw_networkx_nodes(G, pos)

# edges
nx.draw_networkx_edges(G, pos)

# labels
nx.draw_networkx_labels(G, pos)

plt.axis('off')
plt.show()
