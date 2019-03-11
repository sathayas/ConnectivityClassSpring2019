import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import community 
import os
import pandas as pd


####### Target ROIs
target_SM = 'Precentral_L'
target_DMN = 'Cingulum_Post_L'


####### Make a list of networks
dirData = 'DataProblem2'
listFiles = os.listdir(dirData)
listSubj = [iFile for iFile in listFiles if 'sub' in iFile]


####### Loop over subjects
roi_SM = {}   # initializing empty dictionary to record occurrence of ROI, SM module
roi_DMN = {}   # initializing empty dictionary to record occurrence of ROI, DMN module
for iSubj in listSubj:
    # loading the network data
    fNet = os.path.join(dirData,iSubj)
    G = nx.read_adjlist(fNet)
    # community detection Louvain
    partition_L = community.best_partition(G)

    ###### recording SM module nodes
    # identifying module number for the SM module
    ind_SM = partition_L[target_SM]
    # list of nodes in the SM module
    listROI_SM = [i for i,iMod in partition_L.items() if iMod==ind_SM]
    # recording the occurrence of different ROIs in the dictionary
    for iROI_SM in listROI_SM:
        roi_SM.setdefault(iROI_SM, 0)
        roi_SM[iROI_SM] += 1

    ###### recording DMN module nodes
    # identifying module number for the DMN module
    ind_DMN = partition_L[target_DMN]
    # list of nodes in the DMN module
    listROI_DMN = [i for i,iMod in partition_L.items() if iMod==ind_DMN]
    # recording the occurrence of different ROIs in the dictionary
    for iROI_DMN in listROI_DMN:
        roi_DMN.setdefault(iROI_DMN, 0)
        roi_DMN[iROI_DMN] += 1


####### Printing out the 10 most represented nodes
# convert dictionary to DataFrame for ease of sorting
roiSMData = pd.DataFrame(roi_SM.items(), columns=['Node','Occurrence'])
roiDMNData = pd.DataFrame(roi_DMN.items(), columns=['Node','Occurrence'])

# printing out the top 10 lists
# SM module
print('Top 10 ROIs represented in SM module:')
print(roiSMData.sort_values(by='Occurrence', ascending=False).head(10))
print()
# DMN module
print('Top 10 ROIs represented in DMN module:')
print(roiDMNData.sort_values(by='Occurrence', ascending=False).head(10))


