import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

##### loading the network data
# C Elegans neural network
G_CEleg = nx.read_adjlist('CElegans.adjlist')
# Power grid
G_Power = nx.read_gml('power.gml', label='id')
# Brain (ROI)
G_ROI = nx.read_adjlist('Oxford_sub16112_aal90_d5_connected.adjlist')


##### function for random failures
def randfail(G, propFail=0.20):
    # Random failure process
    # Input:
    #     G:        Graph object
    #     propFail: Proportion of nodes to fail. Default is 20%
    # Returns:
    #     GCSize:   A list of giant component size, after each deletion
    H = G.copy()
    GCsize = []
    nNodesRemove = int(len(H.nodes())*propFail)
    for iNode in np.arange(nNodesRemove):
        xNode = np.random.choice(H.nodes())
        H.remove_node(xNode)
        GC_H = len(max(nx.connected_components(H), key=len))
        GCsize.append(GC_H)
    return GCsize


##### function for targetted attacks
def target(G, propFail=0.20):
    # Targetted attack process
    # Input:
    #     G:        Graph object
    #     propFail: Proportion of nodes to be attacked. Default is 20%
    # Returns:
    #     GCSize:   A list of giant component size, after each deletion
    H = G.copy()
    # data frame for degree info
    degreeData = pd.DataFrame(dict(H.degree()).items())
    degreeData.columns=['node','degree']
    degreeData.sort_values(by='degree',ascending=False,inplace=True)
    # now for loop for targeted attacks
    GCsize = []    
    nNodesRemove = int(len(H.nodes())*propFail)
    for iNode in np.arange(nNodesRemove):
        xNode = degreeData.node.iloc[iNode]
        H.remove_node(xNode)
        GC_H = len(max(nx.connected_components(H), key=len))
        GCsize.append(GC_H)
    return GCsize


#### random failures (by calling randfail function)
GC_fail_CEleg = randfail(G_CEleg)
GC_fail_Power = randfail(G_Power)
GC_fail_ROI = randfail(G_ROI)

#### targeted attacks (by calling target function)
GC_attack_CEleg = target(G_CEleg)
GC_attack_Power = target(G_Power)
GC_attack_ROI = target(G_ROI)


#### Plotting the results
plt.figure(figsize=[4,7.5])

plt.subplot(311)
plt.plot(np.arange(1,len(GC_fail_CEleg)+1)/len(G_CEleg.nodes()),
         GC_fail_CEleg, 'b-', label='Random failure')
plt.plot(np.arange(1,len(GC_attack_CEleg)+1)/len(G_CEleg.nodes()),
         GC_attack_CEleg, 'r-', label='Targeted attack')
plt.xlabel('Proportion of removed nodes')
plt.ylabel('Giant component size')
plt.title('C. Elegans neural network')
plt.legend()

plt.subplot(312)
plt.plot(np.arange(1,len(GC_fail_Power)+1)/len(G_Power.nodes()),
         GC_fail_Power, 'b-', label='Random failure')
plt.plot(np.arange(1,len(GC_attack_Power)+1)/len(G_Power.nodes()),
         GC_attack_Power, 'r-', label='Targeted attack')
plt.xlabel('Proportion of removed nodes')
plt.ylabel('Giant component size')
plt.title('Power grid')

plt.subplot(313)
plt.plot(np.arange(1,len(GC_fail_ROI)+1)/len(G_ROI.nodes()),
         np.array(GC_fail_ROI)+0.25, 'b-', label='Random failure')
plt.plot(np.arange(1,len(GC_attack_ROI)+1)/len(G_ROI.nodes()),
         GC_attack_ROI, 'r-', label='Targeted attack')
plt.xlabel('Proportion of removed nodes')
plt.ylabel('Giant component size')
plt.title('Brain network (ROI)')

plt.subplots_adjust(hspace=0.45, top=0.95, bottom=0.075,
                    left=0.175, right=0.95)
plt.show()





