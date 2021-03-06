import os
import numpy as np
import nibabel as nib
import networkx as nx
import matplotlib.pyplot as plt

###### Parameters
targetDeg = 10  # target average degree
targetK = 200 # target K for the atlas



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

# flipping positive and negative
R = -R

# making the diagonal elements to zero
for iRow in range(R.shape[0]):
    R[iRow,iRow] = 0



###### Thresholding
# Correlation
G = net_builder_HardTh(R, nodes, targetDeg)


###### writing network to a file
# Correlation
fNet = 'DataConnectivity/Oxford_sub16112_Rt2_K' + str(targetK)
fNet += '_deg' + str(targetDeg) + '_negative.adjlist'
nx.write_adjlist(G, fNet)



###### visualizing the networks
# dictionary of xy-coordinates
pos = {}
for iROI in range(len(nodes)):
    pos[nodes[iROI]] = xyz[iROI,:2]


# Loop over all graphs for visualization
# first, hard-thresholding network
plt.figure(figsize=[3,4])
nx.draw_networkx_nodes(G, pos, node_color='salmon',
                       node_size=30)
nx.draw_networkx_edges(G, pos, width=0.5,
                       edge_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=3, font_color='black')
plt.title('Negative correlation network')
plt.axis('off')
plt.show()




