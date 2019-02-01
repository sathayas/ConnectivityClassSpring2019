import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# loading the C Elegans neural network
G = nx.read_gml('DataSmallWorld/celegansneural.gml')

# converting to undirected network
H = G.to_undirected()

# writing out to an adjacency list so that edge weight is ignored
nx.write_adjlist(H,'DataSmallWorld/CElegans.adjlist')
