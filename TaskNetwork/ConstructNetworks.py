import os
import numpy as np
import nibabel as nib
import networkx as nx
import matplotlib.pyplot as plt


######## Thresholding function
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


###### Parameters
targetDeg = 20  # target average degree


#
# First, we work on the covert verb generation task
#

###### list of ROI time series data and task time series data
fTS = ['fMRI_covertverb_nomodel_r_bp_reg_Rt2_K200.npz',
       'fMRI_covertverb_r_bp_reg_Rt2_K200.npz']
fTask = 'GLM_model_covertverb.npz'
BaseDir = 'DataTaskNetwork'


###### Loop over the time series data, task network
fFullPathTask = os.path.join(BaseDir,fTask)
GLM = np.load(fFullPathTask)['X']
for iTS in fTS:
    # loading the time series data
    fFullPath = os.path.join(BaseDir, iTS)
    infile = np.load(fFullPath)
    ts = infile['ts']
    nodes = infile['nodes']

    # masking the time series with task time series > 0
    mts = ts[GLM[:,0]>0,:]
    
    # calculating correlation
    R = np.corrcoef(mts, rowvar=False)

    # making the diagonal elements to zero
    for iRow in range(R.shape[0]):
        R[iRow,iRow] = 0

    # thresholding
    G = net_builder_HardTh(R, nodes, targetDeg)

    # writing to a file
    fNet = iTS.split('.')[0] + '_deg' + str(targetDeg) + '.adjlist'
    fFullPathNet = os.path.join(BaseDir, fNet)
    nx.write_adjlist(G, fFullPathNet)


###### resting-state network  (from no task period)
fFullPathTask = os.path.join(BaseDir,fTask)
GLM = np.load(fFullPathTask)['X']

# masking the time series with task time series ==0 (i.e., rest)
mts = ts[GLM[:,0]==0,:]
    
# calculating correlation
R = np.corrcoef(mts, rowvar=False)

# making the diagonal elements to zero
for iRow in range(R.shape[0]):
    R[iRow,iRow] = 0

# thresholding
G = net_builder_HardTh(R, nodes, targetDeg)

# writing to a file
fNet = iTS.split('.')[0] + '_deg' + str(targetDeg) + '_rest.adjlist'
fFullPathNet = os.path.join(BaseDir, fNet)
nx.write_adjlist(G, fFullPathNet)






#
# next, we work on the finger foot lips task
#

###### list of ROI time series data and task time series data
fTS = ['fMRI_fingerfootlips_r_bp_reg_Rt2_K200.npz',
       'fMRI_fingerfootlips_nomodel_r_bp_reg_Rt2_K200.npz']
fTask = 'GLM_model_fingerfootlips.npz'
listTask = ['finger','foot','lips']
indTask = [0,2,4]
BaseDir = 'DataTaskNetwork'


###### Loop over the time series data, task network
fFullPathTask = os.path.join(BaseDir,fTask)
GLM = np.load(fFullPathTask)['X']
for iTS in fTS:
    # loading the time series data
    fFullPath = os.path.join(BaseDir, iTS)
    infile = np.load(fFullPath)
    ts = infile['ts']
    nodes = infile['nodes']

    for i,iTask in enumerate(listTask):
        # masking the time series with task time series > 0
        mts = ts[GLM[:,indTask[i]]>0,:]
    
        # calculating correlation
        R = np.corrcoef(mts, rowvar=False)

        # making the diagonal elements to zero
        for iRow in range(R.shape[0]):
            R[iRow,iRow] = 0

        # thresholding
        G = net_builder_HardTh(R, nodes, targetDeg)

        # writing to a file
        fNet = iTS.split('.')[0] + '_deg' + str(targetDeg)
        fNet += '_' + iTask + '.adjlist'
        fFullPathNet = os.path.join(BaseDir, fNet)
        nx.write_adjlist(G, fFullPathNet)



