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


##### Degree sequence
k_CEleg = [d for n, d in G_CEleg.degree()]
k_Power = [d for n, d in G_Power.degree()]
k_ROI = [d for n, d in G_ROI.degree()]
k_Voxel = [d for n, d in G_Voxel.degree()]


##### Degree histogram
plt.figure(figsize=[9,9])

plt.subplot(221)
plt.hist(k_CEleg,50)
plt.title('Degree histogram, C Elegan')

plt.subplot(222)
plt.hist(k_Power,20)
plt.title('Degree histogram, power grid')

plt.subplot(223)
plt.hist(k_ROI,10)
plt.title('Degree histogram, brain (ROI)')

plt.subplot(224)
plt.hist(k_Voxel,100)
plt.title('Degree histogram, brain (Voxel)')

plt.show()


##### Re-plotting the degree distribution (C Elegan)
# getting counts for each bin
[n_CEleg, bin_CEleg] = np.histogram(k_CEleg,100)

# plotting the counts
plt.plot(bin_CEleg[:-1], n_CEleg)
plt.title('Degree histogram, C Elegan')
plt.show()

# log-log scale
plt.plot(bin_CEleg[:-1], n_CEleg)
plt.title('Log-log scale, C Elegan')
plt.xscale('log')
plt.yscale('log')
plt.show()

# plotting the degree sequence vs rank
sk_CEleg = sorted(k_CEleg, reverse=True) # sorting in descending
plt.plot(sk_CEleg, np.arange(1,len(sk_CEleg)+1))
plt.title('Degree vs rank, C Elegan')
plt.xscale('log')
plt.yscale('log')
plt.show()



###### Cumulative distribution plots
sk_CEleg = sorted(k_CEleg, reverse=True) 
sk_Power = sorted(k_Power, reverse=True) 
sk_ROI = sorted(k_ROI, reverse=True) 
sk_Voxel = sorted(k_Voxel, reverse=True) 

plt.figure(figsize=[9,9])

plt.subplot(221)
plt.plot(sk_CEleg, np.arange(1,len(sk_CEleg)+1))
plt.title('Degree distribution, C Elegan')
plt.xscale('log')
plt.yscale('log')

plt.subplot(222)
plt.plot(sk_Power, np.arange(1,len(sk_Power)+1))
plt.title('Degree distribution, power grid')
plt.xscale('log')
plt.yscale('log')

plt.subplot(223)
plt.plot(sk_ROI, np.arange(1,len(sk_ROI)+1))
plt.title('Degree distribution, brain (ROI)')
plt.xscale('log')
plt.yscale('log')

plt.subplot(224)
plt.plot(sk_Voxel, np.arange(1,len(sk_Voxel)+1))
plt.title('Degree distribution, brain (Voxel)')
plt.xscale('log')
plt.yscale('log')

plt.show()



###### Cumulative distribution plots together
plt.plot(sk_CEleg, np.arange(1,len(sk_CEleg)+1)/len(sk_CEleg), 
         label='C Elegan')
plt.plot(sk_Power, np.arange(1,len(sk_Power)+1)/len(sk_Power), 
         label='Power grid')
plt.plot(sk_ROI, np.arange(1,len(sk_ROI)+1)/len(sk_ROI), 
         label='Brain (ROI)')
plt.plot(sk_Voxel, np.arange(1,len(sk_Voxel)+1)/len(sk_Voxel), 
         label='Brain (voxel)')
plt.title('Degree distributions')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show()
