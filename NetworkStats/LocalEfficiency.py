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

##### Local efficiencies
print('Local efficiencies')
print('C. Elegans: %5.3f' % nx.local_efficiency(G_CEleg))
print('Power grid: %5.3f' % nx.local_efficiency(G_Power))
print('Brain (ROI): %5.3f' % nx.local_efficiency(G_ROI))
print('Brain (Voxel): %5.3f' % nx.local_efficiency(G_Voxel))



##### Custom local efficiency functions to speed up a littie bit
def subgraph(G, xNode):
    ''''
    A function to extract a subgraph of a node xNode
    
    input parameters:
          G:      A graph in networkX format.
          xNode:  The node where the nodal global efficiency is calculated.
    returns:
          subG:   A subgraph of G, containing neighbors of xNode but not xNode
                  itself.
    '''
    subNodes = list(nx.all_neighbors(G, xNode))
    Edges = G.edges()
    subEdges = []       #create list of subgraph edges
    for iEdge in Edges:
        if (iEdge[0] in subNodes and iEdge[1] in subNodes):
            subEdges.append(iEdge)
    subG = nx.Graph()             # create subgraph
    subG.add_nodes_from(subNodes)    #populate subgraph with nodes
    subG.add_edges_from(subEdges)    # populate subgraph with edges
    return subG

def eloc_node(G, xNode):
    '''
    A function to calculate the nodal local efficiency
    from a node xNode.
    
    input parameters:
          G:      A graph in networkX format.
          xNode:  The node where the nodal global efficiency is calculated.
    returns:
          Eloc:   The nodal local efficiency at node xNode.
    '''

    subG = subgraph(G, xNode)
    #Eloc, tmpEloci, tmpNodes = eglob_net(subG)
    NNodes = len(subG.nodes())
    if NNodes>1:
        #Dij = nx.all_pairs_shortest_path_length(subG)
        Dij = nx.floyd_warshall(subG)
        D = [Dij[i].values() for i in subG.nodes()]
        cD = []
        for irow in D:
            cD += irow            
        NZD = np.array(cD)[np.nonzero(cD)]
        if len(NZD)>0:
            Eloc = (1.0/(NNodes*(NNodes-1.0))) * np.sum(1.0/NZD)
        else:
            Eloc = 0
    else:
        Eloc = 0
    return Eloc


def eloc_net(G):
    '''
    A function to calculate the network local efficiency
    
    input parameters:
          G:       A graph in networkX format.
    returns:
          Eloc:    The network-wide average local efficiency.
          sEloci:  The nodal local efficiency
          sNodes:  The nodes used in calculation of local efficiency. The same
                   order as the sEloci. Node numbers are sorted in the ascending
                   order.
    '''

    Nodes = G.nodes()
    Eloci = []
    nodecount = 1
    for iNode in Nodes:
        if (nodecount % 250)==0:
            print('Eloc:  Working on node: ' +str(nodecount))
        nodecount += 1
        tmpEloc = eloc_node(G, iNode)
        Eloci.append(tmpEloc)
    Eloc = np.mean(Eloci)
    # sorting the nodal local efficiency
    sNodes, sEloci = sort_nodestat(Nodes, Eloci)
    return Eloc, sEloci, sNodes

def sort_nodestat(NodeList, Stats):
    '''
    A function to sort node stats by ROI number
    
    This is a function used internally.
    '''
    iNode = [int(i) for i in NodeList]
    zipstat = zip(iNode, Stats)
    zipsstat = sorted(zipstat, key = lambda t: t[0])
    sNodeList, sStats = zip(*zipsstat)
    return sNodeList, sStats


##### Local efficiencies, redux
print('Local efficiencies')
print('C. Elegans: %5.3f' % eloc_net(G_CEleg)[0])
print('Power grid: %5.3f' % eloc_net(G_Power)[0])
print('Brain (ROI): %5.3f' % eloc_net(G_ROI)[0])
print('Brain (Voxel): %5.3f' % eloc_net(G_Voxel)[0])
