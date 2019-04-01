import numpy as np
import networkx as nx
import os
import matplotlib.pyplot as plt


####### Network thresholding function
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


# List of files
listDir = os.listdir('DataHomework3')
listSubjFile = [i for i in listDir if 'Oxford_sub' in i]

# List of target average degrees
degList = np.arange(10,31,2)

# storage space for network metrics
netStat = np.zeros((len(listSubjFile), len(degList)))

# loop over subjects
for i,iSubj in enumerate(listSubjFile):
    print('Woriking on ' + iSubj)
    # loading the data
    infile = np.load(os.path.join('DataHomework3',iSubj))
    ts = infile['ts']
    nodes = infile['nodes']
    # correlation matrix
    R = np.corrcoef(ts, rowvar=False)
    # loop over degrees
    for j,jDeg in enumerate(degList):
        G = net_builder_HardTh(R, nodes, jDeg)
        netStat[i,j] = nx.average_clustering(G)


# plotting
plt.plot(degList, np.mean(netStat, axis=0))
plt.xlabel('Target average degree')
plt.ylabel('Clustering coefficient')
plt.show()

