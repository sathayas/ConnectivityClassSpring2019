import os
import numpy as np
import nibabel as nib
import networkx as nx
import matplotlib.pyplot as plt

# importing external functions for MI and PC calculation
from partial_corr import partial_corr
from mutual_info import mutual_information

###### Parameters
targetDeg = 10  # target average degree
targetK = 200 # target K for the atlas
nBins = 11  # number of bins for mutual information




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





###### Loadin the data from the previous time
f_TS = 'DataConnectivity/Oxford_sub16112_Rt2_K' + str(targetK) + '.npz'
infile = np.load(f_TS)
ts = infile['ts']
nodes = infile['nodes']
xyz = infile['xyz']


###### Calculating the correlation matrix
R = np.corrcoef(ts, rowvar=False)

# making the diagonal elements to zero
for iRow in range(R.shape[0]):
    R[iRow,iRow] = 0

    
###### Calculating the partial correlaiton matrix
Rpc = partial_corr(ts)

# making the diagonal elements to zero
for iRow in range(Rpc.shape[0]):
    Rpc[iRow,iRow] = 0


###### Calculating the mutual information matrix
Rmi = mutual_information(ts, nBins)



###### Thresholding
# Correlation
G = net_builder_HardTh(R, nodes, targetDeg)
# partial correlation
G_pc = net_builder_HardTh(Rpc, nodes, targetDeg)
# mutual information
G_mi = net_builder_HardTh(Rmi, nodes, targetDeg)
# and all together
G_all = [G, G_pc, G_mi]


###### writing network to a file
# Correlation
fNet = 'DataConnectivity/Oxford_sub16112_Rt2_K' + str(targetK)
fNet += '_deg' + str(targetDeg) + '.adjlist'
nx.write_adjlist(G, fNet)
# partial correlation
fNet = 'DataConnectivity/Oxford_sub16112_Rt2_K' + str(targetK)
fNet += '_deg' + str(targetDeg) + '_pc.adjlist'
nx.write_adjlist(G_pc, fNet)
# mutual information
fNet = 'DataConnectivity/Oxford_sub16112_Rt2_K' + str(targetK)
fNet += '_deg' + str(targetDeg) + '_mi.adjlist'
nx.write_adjlist(G_mi, fNet)



###### visualizing the networks
# dictionary of xy-coordinates
pos = {}
for iROI in range(len(nodes)):
    pos[nodes[iROI]] = xyz[iROI,:2]


# Loop over all graphs for visualization
connMethods = ['Correlation','Partial correlation','Mutual information']
plt.figure(figsize=[9,4])
for i in range(len(G_all)):


    # first, hard-thresholding network
    plt.subplot(1,3,i+1)
    nx.draw_networkx_nodes(G_all[i], pos, node_color='salmon',
                           node_size=30)
    nx.draw_networkx_edges(G_all[i], pos, width=0.5,
                           edge_color='lightblue')
    nx.draw_networkx_labels(G_all[i], pos, font_size=3, font_color='black')
    plt.title(connMethods[i])
    plt.axis('off')
    
plt.subplots_adjust(left=0.01, right=0.99, wspace=0.06, bottom=0.025, top=0.90)
plt.show()




