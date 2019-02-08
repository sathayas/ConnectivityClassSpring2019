import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

##### loading the network data
# C Elegans neural network
G_CEleg = nx.read_adjlist('DataNetStats/CElegans.adjlist')
# Power grid
G_Power = nx.read_gml('DataNetStats/power.gml', label='id')
# Brain (ROI)
G_ROI = nx.read_adjlist('DataNetStats/Oxford_sub16112_aal90_d5.adjlist')
# Brain (Voxel)
G_Voxel = nx.read_adjlist('DataNetStats/Oxford_sub16112_voxel_d20.adjlist')

##### Global efficiencies
print('Global eddiciencies')
print('C. Elegans: %5.3f' % nx.global_efficiency(G_CEleg))
print('Power grid: %5.3f' % nx.global_efficiency(G_Power))
print('Brain (ROI): %5.3f' % nx.global_efficiency(G_ROI))
print('Brain (Voxel): %5.3f' % nx.global_efficiency(G_Voxel))
#0.1869544358446755



##### Custom global efficiency functions to speed up a littie bit
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



def eglob_net(G):
    '''
    A function to calculate the network global efficiency
    
    input parameters:
          G:      A graph in networkX format.
    
    returns:
          Eglob:  The network wide average global efficiency
          Eglobi: Nodal global efficiency
          Nodes:  Nodes where nodal global efficency was calculated on. In the
                  same order as Eglobi.
    '''

    Nodes = G.nodes()
    if len(Nodes)>1:
        Eglobi = []
        nodecount = 1
        for iNode in Nodes:
            if (nodecount % 250)==0:
                print('Eglob:  Working on node: ' +str(nodecount))
            nodecount += 1
            tmpEglob = eglob_node(G, iNode)
            Eglobi.append(tmpEglob)
        Eglob = np.mean(Eglobi)
    else:
        Eglob = 0
        Eglobi = []
    return Eglob, Eglobi, Nodes


##### Global efficiencies, redux
print('Global eddiciencies')
print('C. Elegans: %5.3f' % eglob_net(G_CEleg)[0])
print('Power grid: %5.3f' % eglob_net(G_Power)[0])
print('Brain (ROI): %5.3f' % eglob_net(G_ROI)[0])
print('Brain (Voxel): %5.3f' % eglob_net(G_Voxel)[0])

