import os
import numpy as np
import nibabel as nib
import networkx as nx
import matplotlib.pyplot as plt


###### Network construction functions, based on correlation matrix

def net_builder_RankTh(R, NodeInd, d, cType=1):
    '''
    a function to construct the network by the rank-based thresholding
     
    input parameters:
          R:         A dense correlation matrix array.
          NodeInd:   A list of nodes in the network.
          d:         The rank threshold for the rank-based thresholding.
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
    # the working copy of R, depending on the connectivity type
    if cType==1:
        WorkR = np.copy(R)
    elif cType==0:
        WorkR = abs(np.copy(R))
    elif cType==-1:
        WorkR = np.copy(-R)
    # then add edges
    for iRank in range(d):
        I = np.arange(NNodes)
        J = np.argmax(WorkR, axis=1)
        # R has to be non-zero
        trI = [i for i in range(NNodes) if WorkR[i, J[i]]>0]
        trJ = [J[i] for i in range(NNodes) if WorkR[i, J[i]]>0]
        # adding connections (for R>0)
        Elist = np.vstack((NodeInd[trI], NodeInd[trJ])).T 
        G.add_edges_from(Elist)
        WorkR[trI, trJ] = 0  # clearing the correlation matrix
    # finally returning the resultant graph
    return G



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





############### Network according to AAL #################

###### Loadin the data from the previous time
f_TS = 'DataAtlas/Oxford_sub16112_aal_ts.npz'
infile = np.load(f_TS)
ts = infile['ts']
nodes = infile['nodes']
xyz = infile['xyz']


###### Calculating the correlation matrix
R = np.corrcoef(ts, rowvar=False)

# showing the correlation coefficient
plt.imshow(R)
plt.title('Correlation matrix')
plt.show()

# making the diagonal elements to zero
for iRow in range(R.shape[0]):
    R[iRow,iRow] = 0

# showing the correlation coefficient
plt.imshow(R)
plt.title('Correlation matrix (no diagonal)')
plt.show()



###### Thresholding
# hard thresholding -- with user-defined target degree
targetDeg = 10
G_degree = net_builder_HardTh(R, nodes, targetDeg)
# rank thresholding -- with user-defined d
target_d = 7
G_rank = net_builder_RankTh(R, nodes, target_d)



###### visualizing the network
# dictionary of xy-coordinates
pos = {}
for i in range(len(nodes)):
    pos[nodes[i]] = xyz[i,:2]

# first, hard-thresholding network
plt.figure(figsize=[12,6])
plt.subplot(121)
nx.draw_networkx_nodes(G_degree, pos, node_color='salmon',
                       node_size=100)
nx.draw_networkx_edges(G_degree, pos,
                       edge_color='lightblue')
nx.draw_networkx_labels(G_degree, pos, font_size=7, font_color='black')
plt.title('Hard thresholding, avg deg=' + str(targetDeg))
plt.axis('off')

# second, rank-thresholding network
plt.subplot(122)
nx.draw_networkx_nodes(G_rank, pos, node_color='salmon',
                       node_size=100)
nx.draw_networkx_edges(G_rank, pos,
                       edge_color='lightblue')
nx.draw_networkx_labels(G_rank, pos, font_size=7, font_color='black')
plt.title('Node-wise thresholding, target d=' + str(target_d))
plt.axis('off')

plt.show()







############### Network according to Rt2 #################

# Ks for clustering algorithm
K = list(range(10,301,10)) + list(range(350,1000,50))  
subK = [50, 100, 200, 500, 950]   # Ks for example atlases
indK = [list(K).index(k) for k in subK]  # indices corresponding to subK

###### Loop over K for constructing networks
G_degree = []
nodes_degree = []
xyz_degree = []
for i,targetK in enumerate(subK):

    ###### Loadin the data from the previous time
    f_TS = 'DataAtlas/Oxford_sub16112_Rt2_K' + str(targetK) + '.npz'
    infile = np.load(f_TS)
    ts = infile['ts']
    nodes = infile['nodes']
    xyz = infile['xyz']


    ###### Calculating the correlation matrix
    R = np.corrcoef(ts, rowvar=False)
    
    # making the diagonal elements to zero
    for iRow in range(R.shape[0]):
        R[iRow,iRow] = 0
        

    ###### Thresholding
    # hard thresholding -- with user-defined target degree
    targetDeg = 10
    G = net_builder_HardTh(R, nodes, targetDeg)
    # saving the results for later
    G_degree.append(G)
    nodes_degree.append(nodes)
    xyz_degree.append(xyz)



###### visualizing the networks
# Loop over K for visualization
plt.figure(figsize=[15,4])
for i,targetK in enumerate(subK):

    # dictionary of xy-coordinates
    pos = {}
    for iROI in range(len(nodes_degree[i])):
        pos[nodes_degree[i][iROI]] = xyz_degree[i][iROI,:2]

    # first, hard-thresholding network
    plt.subplot(1,5,i+1)
    nx.draw_networkx_nodes(G_degree[i], pos, node_color='salmon',
                           node_size=50)
    nx.draw_networkx_edges(G_degree[i], pos,
                           edge_color='lightblue')
    nx.draw_networkx_labels(G_degree[i], pos, font_size=4, font_color='black')
    plt.title('Hard thresholding\navg deg=' + str(targetDeg))
    plt.axis('off')
    
plt.subplots_adjust(left=0.025, right=0.975, wspace=0.1)
plt.show()




