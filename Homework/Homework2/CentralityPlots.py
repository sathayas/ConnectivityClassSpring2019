import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##### loading the network data
G = nx.read_adjlist('DataProblem1/Leiden_sub30943_aal90_d10_annotated.adjlist')


##### Calculating centralities
Ceig = nx.eigenvector_centrality(G)  # eigenvector centraltiy
Cbet = nx.betweenness_centrality(G)  # betweenness centrality
Cclo = nx.closeness_centrality(G)    # closeness centraltiy


##### Combining the centraility measures into a single data frame
eigData = pd.DataFrame(Ceig.items(), columns=['Node','Ceig'])
betData = pd.DataFrame(Cbet.items(), columns=['Node','Cbet'])
cloData = pd.DataFrame(Cclo.items(), columns=['Node','Cclo'])
CentralData = eigData.merge(betData, on='Node')
CentralData = CentralData.merge(cloData, on='Node')


##### plotting
plt.figure(figsize=[9,3])

# eigenvector vs betweenness
plt.subplot(131)
plt.plot(CentralData.Ceig, CentralData.Cbet, 'b.')
plt.xlabel('Eigenvector centrality')
plt.ylabel('Betweenness centraltiy')

# eigenvector vs closeness
plt.subplot(132)
plt.plot(CentralData.Ceig, CentralData.Cclo, 'b.')
plt.xlabel('Eigenvector centrality')
plt.ylabel('Closeness centraltiy')

# betweenness vs closeness
plt.subplot(133)
plt.plot(CentralData.Cbet, CentralData.Cclo, 'b.')
plt.xlabel('Betweenness centraltiy')
plt.ylabel('Closeness centraltiy')



plt.subplots_adjust(bottom=0.2, left=0.075, top=0.95, wspace=0.45, right=0.95)
plt.show()



