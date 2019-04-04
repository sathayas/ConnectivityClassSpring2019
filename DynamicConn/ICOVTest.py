import numpy as np
import matplotlib.pyplot as plt
from sklearn.covariance import GraphicalLassoCV
from sklearn.preprocessing import StandardScaler

# loading the data
infile = np.load('DataDynamicConn/Oxford_sub16112_rt2_K200.npz')
ts = infile['ts']
nodes = infile['nodes']


# correlation matrix
R = np.corrcoef(ts, rowvar=False)

# scaling the input data
ts_std = StandardScaler().fit_transform(ts)

# ICOV
glasso = GraphicalLassoCV(cv=5)
glasso.fit(ts_std)
ICOV = glasso.covariance_


# visual inspection
# zeroing the main diagonal
for i in range(R.shape[0]):
    R[i,i] = 0
    ICOV[i,i] = 0

plt.figure(figsize=[6,3])
plt.subplot(121)
plt.imshow(R, interpolation='nearest', vmin=-1, vmax=1,
           cmap=plt.cm.rainbow)
plt.xticks(())
plt.yticks(())
plt.title('Correlation')

plt.subplot(122)
ICOVmax = np.max(ICOV)
plt.imshow(ICOV, interpolation='nearest', vmin=-ICOVmax, vmax=ICOVmax,
           cmap=plt.cm.rainbow)
plt.xticks(())
plt.yticks(())
plt.title('ICOV')

plt.subplots_adjust(left=0.02, right=0.98)
plt.show()



# plotting R vs ICOV
R_triu = R[np.triu_indices(R.shape[0])]
ICOV_triu = ICOV[np.triu_indices(ICOV.shape[0])]

plt.plot(R_triu,ICOV_triu,'b.')
plt.show()
