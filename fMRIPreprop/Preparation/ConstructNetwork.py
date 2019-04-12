import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

###### Parameters
targetDeg = 20  # target average degree


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


###### Loadin the time series data
fTS = 'Oxford_sub16112_Rt2_K200.npz'
fTS_WBWMCSF = 'Oxford_sub16112_WBWMCSF_Rt2_K200.npz'
fTS_WMCSF = 'Oxford_sub16112_WMCSF_Rt2_K200.npz'
TS = np.load(fTS)['ts']
TS_WBWMCSF = np.load(fTS_WBWMCSF)['ts']
TS_WMCSF = np.load(fTS_WMCSF)['ts']

# other info about the data as well
nodes = np.load(fTS)['nodes']
xyz = np.load(fTS)['xyz']
nNodes = len(nodes)


###### Calculating the correlation matrix
R = np.corrcoef(TS, rowvar=False)
R_WBWMCSF = np.corrcoef(TS_WBWMCSF, rowvar=False)
R_WMCSF = np.corrcoef(TS_WMCSF, rowvar=False)

# zeroing the main diagonal
R[np.arange(nNode), np.arange(nNode)] = 0
R_WBWMCSF[np.arange(nNode), np.arange(nNode)] = 0
R_WMCSF[np.arange(nNode), np.arange(nNode)] = 0




###### Thresholding for form networks
G = net_builder_HardTh(R, nodes, targetDeg)
G_WBWMCSF = net_builder_HardTh(R_WBWMCSF, nodes, targetDeg)
G_WMCSF = net_builder_HardTh(R_WMCSF, nodes, targetDeg)



###### Saving the networks
fG = fTS.replace('.npz','_deg20.adjlist')
fG_WBWMCSF = fTS_WBWMCSF.replace('.npz','_deg20.adjlist')
fG_WMCSF = fTS_WMCSF.replace('.npz','_deg20.adjlist')
nx.write_adjlist(G, fG)
nx.write_adjlist(G_WBWMCSF, fG_WBWMCSF)
nx.write_adjlist(G_WMCSF, fG_WMCSF)

