import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import community   # Louvain method
from sklearn.metrics import adjusted_rand_score


##### Custom distinct color function --- to be used later
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


###### Network construction functions, based on correlation matrix
def net_builder_HardTh(R, NodeInd, K, cType=1):
    '''
    a function to construct the network by the hard-thresholding.
    input parameters:
          R:         A dense correlation matrix array.
          NodeInd:   A list of nodes in the network.
          K:         The target K, the average connections at each node
          cType:     Type of functional connectivity. 
                        1:  Positive correlation only
                        0:  Both positive and negative correlations
                        -1: Negative correlation only
                     The default is 1 (i.e., positive correlation only).
    
    returns:
          G:         The resulting graph (networkX format)
    '''
    
    # first, initialize the graph
    G = nx.Graph()
    G.add_nodes_from(NodeInd)
    NNodes = R.shape[0]
    # upper triangle of the correlation matrix only
    I,J = np.triu_indices(NNodes,1)
    # creating a vector of correlation coefficients, depending on cType
    if cType==1:
        VecR = np.squeeze(np.array(R[I,J]))
    elif cType==0:
        VecR = np.squeeze(np.array(abs(R[I,J])))
    elif cType==-1:
        VecR = np.squeeze(np.array(-R[I,J]))
    # the number of elements is too big, so we truncate it
    # first, find the appropriate threshold for R
    NthR = 0
    tmpRth = 0.95
    StepTh = 0.05
    while NthR<K*NNodes/2.0:
        tmpRth -= StepTh
        #print('Threshold = %.2f' % tmpRth)
        NthR = len(np.nonzero(VecR>tmpRth)[0])
    # second, truncate the variables
    IndVecR = np.nonzero(VecR>tmpRth)
    thVecR = VecR[IndVecR]
    thI = I[IndVecR]
    thJ = J[IndVecR]
    # sort the correlation values
    zipR = zip(thVecR, thI, thJ)
    zipsR = sorted(zipR, key = lambda t: t[0], reverse=True)
    sVecR, sI, sJ = zip(*zipsR)
    # then adding edges
    m = int(np.ceil(K*NNodes/2.0))  # the number of edges
    trI = np.array(sI[:m])
    trJ = np.array(sJ[:m])
    Elist = np.vstack((NodeInd[trI], NodeInd[trJ])).T
    G.add_edges_from(Elist)
    RTh = sVecR[m-1]  # the threshold
    # finally returning the resultant graph and the threshold
    return G


####### Loading the cluster data
infile = np.load('DataDynamicConn/Leiden_sub39335_Rt2_K200_Cluster.npz')
y_clus = infile['y_clus']
y_cent = infile['y_cent']
xyz = infile['xyz']
nodes = infile['nodes']
nNode = len(nodes)
nClus = max(y_clus) + 1



####### modules for centroid connectivity
targetDeg = 20
partition_list = []
GC_list = []
for i in np.unique(y_clus):
    # reconstructing the connectivity matrix for the centroid
    R = np.zeros((nNode,nNode))
    indR = np.triu_indices(nNode,1)
    R[indR] = y_cent[i]
    R = R.T
    R[indR] = y_cent[i]
    # Constructing a network based on the centroid conenctivty
    G = net_builder_HardTh(R, nodes, targetDeg)
    # finding the giant component
    GC_nodes = max(nx.connected_components(G), key=len)  
    GC = G.subgraph(GC_nodes)
    GC_list.append(G)
    ###### modular partition by Louvain
    partition = community.best_partition(GC)
    partition_list.append(partition)


###### drawing the graph
# dictionary of xy-coordinates
pos = {}
for iROI in range(len(nodes)):
    pos[nodes[iROI]] = xyz[iROI,:2]

# Loop over states for visualization
plt.figure(figsize=[9,7])
for iState in np.unique(y_clus):
    
    # finally, graph with communities in different colors (Louvain)
    plt.subplot(2,3,iState+1)
    nComm = max([comm for comm in partition_list[iState].values()])+1
    node_color_list = get_cmap(nComm+1,'rainbow')
    for iComm in range(nComm):
        nodeList = [iNode for iNode,Comm in partition_list[iState].items()
                    if Comm==iComm]
        nx.draw_networkx_nodes(GC_list[iState], pos, 
                               nodelist=nodeList,
                               node_color = np.array([node_color_list(iComm)]),
                               node_size=30)
        nx.draw_networkx_edges(GC_list[iState], pos, width=0.5,
                               edge_color='lightblue')
    plt.title('State %d' % iState)
    plt.axis('off')

plt.subplots_adjust(left=0.01, right=0.99, wspace=0.05,
                    bottom=0.025, top=0.925)
plt.show()


