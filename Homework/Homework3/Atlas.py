import numpy as np
import nibabel as nib
import pandas as pd

# getting the index for K=200
K = list(range(10,301,10)) + list(range(350,1000,50))  
indK = K.index(200)

# Loading the atlas data into arrays
X_aal = nib.load('DataHomework3/aal_MNI_V4_r.nii.gz').get_data()
X_rt2 = nib.load('DataHomework3/tcorr05_2level_all_r.nii.gz').get_data()[:,:,:,indK]

# loading the ROI names into a dictionary
roiData = pd.read_csv('DataHomework3/aal_MNI_V4_coord.csv')
roiInd = roiData.ROI_ID
roiName = roiData.ROI_Name
roiDict = {roiInd[i]:roiName[i] for i in range(len(roiInd))}

# initializing the data storage
roiTable = []

# for loop over ROIs in Rt2 atlas
listROI = np.unique(X_rt2[X_rt2>0])
for iROI in listROI:
    # voxels in AAL atlas corresponding to ROI iROI
    voxAAL = X_aal[X_rt2==iROI]
    # frequency counts
    ROIunique, ROIcounts = np.unique(voxAAL, return_counts=True)
    ROIprop = ROIcounts / len(voxAAL)
    # recording
    # if any non-zero ROI dominates more than 50%
    if np.max(ROIprop)>0.5 and ROIunique[np.argmax(ROIprop)]!=0:
        newRecord = [iROI, roiDict[ROIunique[np.argmax(ROIprop)]], np.max(ROIprop)]
        roiTable.append(newRecord)
    else:
        newRecord = [iROI, np.nan, np.nan]
        roiTable.append(newRecord)


# writing out the table
roiTableDF=pd.DataFrame(roiTable, columns=['Rt2_ROI_ID', 'AnatLabel', 'Confidence'])
roiTableDF.to_csv('DataHomework3/Rt2_ROItable.csv', index=None)
