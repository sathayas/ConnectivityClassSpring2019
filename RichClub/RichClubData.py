import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##### loading the network data
# Centrality literature network
H_Lit = nx.Graph(nx.read_pajek('DataRichClub/centrality_literature.paj'))
GCnodes_Lit = max(nx.connected_components(H_Lit), key=len)  # giant component nodes
G_Lit = G_Lit.subgraph(GCnodes_Lit)   # giant component network
# Power grid
G_Power = nx.read_gml('DataRichClub/power.gml', label='id')
# Brain (Berlin)
G_Berlin = nx.read_adjlist('DataCentrality/Berlin_sub91116_aal90_d10_annotated.adjlist')
# Brain (Leiden)
G_Leiden = nx.read_adjlist('DataCentrality/Leiden_sub30943_aal90_d10_annotated.adjlist')
# Brain (New York)
G_NY = nx.read_adjlist('DataCentrality/NewYork_sub78118_aal90_d10_annotated.adjlist')
# Brain (Oxford)
G_Oxford = nx.read_adjlist('DataCentrality/Oxford_sub16112_aal90_d10_annotated.adjlist')
# Brain (Queensland)
G_Queen = nx.read_adjlist('DataCentrality/Queensland_sub42533_aal90_d10_annotated.adjlist')

