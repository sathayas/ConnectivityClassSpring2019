import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


# loading the label for different brain areas
AALTable = pd.read_csv('DataCentrality/aal_MNI_V4_coord.csv')
# dictionary of node names and xy-coordinates
roiNames = {}
pos = {}
for i in range(1,91):
    roiNames[i] = AALTable.iloc[i-1,1]

# loading the list of files from the data directory
listFiles = os.listdir('DataCentrality')
listAdjlist = [i for i in listFiles if '.adjlist' in i]

# loop over networks
for iNet in listAdjlist:
    fNet = os.path.join('DataCentrality',iNet)
    G = nx.read_adjlist(fNet, nodetype=int)

    # renaming nodes
    H = nx.relabel_nodes(G, roiNames)

    # Saving the network for future use
    fNewNet = fNet.replace('.adjlist', '_annotated.adjlist')
    nx.write_adjlist(H,fNewNet)


