import numpy as np
import nibabel as nib
import pandas as pd

# parameters
nROI = 116

# loading the data
AALTable = pd.read_table('IntroNetworkData/aal_MNI_V4.txt', 
                         skiprows = [0], header=None)
AALTable.columns = ['ROI_ID','ROI_Name']
imgAAL = nib.load('IntroNetworkData/aal_MNI_V4.nii.gz')
X_AAL = imgAAL.get_data()
dim_AAL = X_AAL.shape[:3]
Amat = imgAAL.affine

# calculating the center of each ROI
centerXYZ = np.array([])
for iROI in range(1,nROI+1):
    QROI = np.where(X_AAL==iROI)[:3]
    centerROI = [x.mean() for x in QROI]
    centerROIxyz = np.dot(Amat, np.array([centerROI + [1]]).T)[:3].T
    if len(centerXYZ)==0:
        centerXYZ = centerROIxyz
    else:
        centerXYZ = np.vstack([centerXYZ, centerROIxyz])

# adding the XYZ coordinates to the AALTable
centerTable = pd.DataFrame(centerXYZ, columns=['centerX',
                                               'centerY',
                                               'centerZ'])
AALTable = pd.concat([AALTable, centerTable], axis=1)


# saving the table
AALTable.to_csv('IntroNetworkData/aal_MNI_V4_coord.csv',
                index=False)



