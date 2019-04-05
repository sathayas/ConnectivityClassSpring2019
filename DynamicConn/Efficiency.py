import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

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


####### functions to calculate nodal local efficiencies
def eloc_node(G, xNode):
    '''
    A function to calculate the nodal local efficiency
    from a node xNode.
    
    input parameters:
          G:      A graph in networkX format.
          xNode:  The node where the nodal global efficiency is calculated.
    returns:
          Eloc:   The nodal local efficiency at node xNode.
    '''

    subG = subgraph(G, xNode)
    #Eloc, tmpEloci, tmpNodes = eglob_net(subG)
    NNodes = len(subG.nodes())
    if NNodes>1:
        #Dij = nx.all_pairs_shortest_path_length(subG)
        Dij = nx.floyd_warshall(subG)
        D = [Dij[i].values() for i in subG.nodes()]
        cD = []
        for irow in D:
            cD += irow            
        NZD = np.array(cD)[np.nonzero(cD)]
        if len(NZD)>0:
            Eloc = (1.0/(NNodes*(NNodes-1.0))) * np.sum(1.0/NZD)
        else:
            Eloc = 0
    else:
        Eloc = 0
    return Eloc

def subgraph(G, xNode):
    ''''
    A function to extract a subgraph of a node xNode
    
    input parameters:
          G:      A graph in networkX format.
          xNode:  The node where the nodal global efficiency is calculated.
    returns:
          subG:   A subgraph of G, containing neighbors of xNode but not xNode
                  itself.
    '''
    subNodes = list(nx.all_neighbors(G, xNode))
    Edges = G.edges()
    subEdges = []       #create list of subgraph edges
    for iEdge in Edges:
        if (iEdge[0] in subNodes and iEdge[1] in subNodes):
            subEdges.append(iEdge)
    subG = nx.Graph()             # create subgraph
    subG.add_nodes_from(subNodes)    #populate subgraph with nodes
    subG.add_edges_from(subEdges)    # populate subgraph with edges
    return subG

def eglob_node(G, xNode):
    '''
    A function to calculate the nodal global efficiency
    from a node.
    input parameters:
          G:      A graph in networkX format.
          xNode:  The node where the nodal global efficiency is calculated.
    
    returns:
          Eglob:  The nodal blobal efficiency at xNode.
    '''

    NNodes = len(G.nodes())
    Dx = list(nx.single_source_shortest_path_length(G, xNode).values())
    indZ = np.nonzero(np.array(Dx)==0)[0]
    nzDx = np.delete(Dx, indZ)
    if len(nzDx)>0:
        Eglob = (1.0/(NNodes-1.0)) * np.sum(1.0/nzDx)
    else:
        Eglob = 0
    # returning the nodal global efficiency
    return Eglob




##### Parameters
targetDeg = 20

##### Loading the data
infile = np.load('DataDynamicConn/Leiden_sub39335_Rt2_K200_Rmat.npz')
Rmat = infile['Rmat']
nodes = infile['nodes']
xyz = infile['xyz']

###### Loop over time points
ElocMat = np.zeros((len(nodes),Rmat.shape[0]))
EglobMat = np.zeros((len(nodes),Rmat.shape[0]))
for iTime in range(Rmat.shape[0]):
    print('Working on time point %d' % iTime)

    ###### extracting a network 
    G = net_builder_HardTh(Rmat[iTime,:,:], nodes, targetDeg)

    ###### calculating local and global efficiency
    ElocList = []
    EglobList = []
    for iNode in nodes:
        Eloc = eloc_node(G,iNode)
        ElocList.append(Eloc)
        Eglob = eglob_node(G,iNode)
        EglobList.append(Eglob)

    # saving it for later
    ElocMat[:,iTime] = ElocList
    EglobMat[:,iTime] = EglobList


##### saving to a file so that we don't have to recalculate
np.savez('DataDynamicConn/Leiden_sub39335_Rt2_K200_Efficiency.npz',
         ElocMat = ElocMat,
         EglobMat = EglobMat,
         nodes = nodes,
         xyz = xyz)

##### loading from the file to save time
f = np.load('DataDynamicConn/Leiden_sub39335_Rt2_K200_Efficiency.npz')
ElocMat = f['ElocMat']
EglobMat = f['EglobMat']
nodes = f['nodes']
xyz = f['xyz']



##### plotting efficiency over time
plt.figure(figsize=[9,5])
plt.subplot(121)
plt.imshow(ElocMat, cmap=plt.cm.rainbow)
plt.title('Local efficiency')
plt.xlabel('Time')
plt.ylabel('Nodes')
plt.colorbar()

plt.subplot(122)
plt.imshow(EglobMat, cmap=plt.cm.rainbow)
plt.title('Global efficiency')
plt.xlabel('Time')
plt.ylabel('Nodes')
plt.colorbar()

plt.show()
