import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

##### loading the network data
# correlatio network
G = nx.read_adjlist('DataConnectivity/Oxford_sub16112_Rt2_K200_deg10.adjlist',
                    nodetype=int)
# partial correlatio network
G_pc = nx.read_adjlist('DataConnectivity/Oxford_sub16112_Rt2_K200_deg10_pc.adjlist',
                       nodetype=int)
# mutual information network
G_mi = nx.read_adjlist('DataConnectivity/Oxford_sub16112_Rt2_K200_deg10_mi.adjlist',
                       nodetype=int)


##### Degree sequence
k = [d for n, d in G.degree()]
k_pc = [d for n, d in G_pc.degree()]
k_mi = [d for n, d in G_mi.degree()]


###### Cumulative distribution plots
sk = sorted(k, reverse=True) 
sk_pc = sorted(k_pc, reverse=True) 
sk_mi = sorted(k_mi, reverse=True) 


plt.plot(sk, np.arange(1,len(sk)+1)/len(sk), 
         label='Correlation')
plt.plot(sk_pc, np.arange(1,len(sk_pc)+1)/len(sk_pc), 
         label='Partial correlation')
plt.plot(sk_mi, np.arange(1,len(sk_mi)+1)/len(sk_mi), 
         label='Mutual information')
plt.title('Degree distributions')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Degree')
plt.ylabel('1-F(degree)')
plt.legend()
plt.show()
