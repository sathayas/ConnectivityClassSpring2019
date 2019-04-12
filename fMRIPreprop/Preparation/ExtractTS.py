import os
import numpy as np
import nibabel as nib


##### function to extract mean fMRI time series from ROIs 
def extract_roits(datafMRI, dataAtlas):
    '''
    A function to extract the average ROI time series from 4D fMRI
    data.
    input parameters:
          datafMRI: The 4D array of the fMRI image. The fMRI data should
                    have already been normalized and preprocessed.
          dataAtlas:The 3D array of the atlas image defining different ROIs.
                    The atlas image is assumed to be in the same space as the 
                    fMRI data. In other words, it needs to be re-sliced to 
                    the fMRI data voxel size beforehand.
    returns:
          roi_ts:   An array of the extracted time series. Rows correspond to
                    time points, the columns corresponds to ROIs. The ROIs are
                    in the same order as roi_ind.
          roi_ind:  A vector of ROI numbers, in the same order as the columns
                    of the roi_ts.
    '''

    # nan-ing the fMRI data -- voxel-value = zero is replaced with nan
    datafMRI[datafMRI==0] = np.nan

    # creating the roi indices
    roiMin = np.min(np.unique(dataAtlas[dataAtlas>0]))
    roiMax = np.max(np.unique(dataAtlas[dataAtlas>0]))
    roi_ind = np.arange(roiMin, roiMax+1)
    
    # preparing the output time series array
    nTime = datafMRI.shape[-1]
    roi_ts = np.zeros([nTime, len(roi_ind)])

    # for loop to calculate the time series
    for iTime in range(nTime):
        tmpfMRI = datafMRI[:,:,:,iTime]
        for i,iROI in enumerate(roi_ind):
            tmpROIdata = tmpfMRI[dataAtlas==iROI]
            if len(tmpROIdata)> 0 and not all(np.isnan(tmpROIdata)):
                roi_ts[iTime, i] = np.nanmean(tmpROIdata)

    # removing colums with any nan
    removeInd = []   # indices of columns to be removed
    for iCol in range(roi_ts.shape[1]):
        if all(roi_ts[:,iCol]==0):
            removeInd.append(iCol)
    roi_ts = np.delete(roi_ts, removeInd, 1)
    roi_ind= np.delete(roi_ind, removeInd)

    # returning the results
    return roi_ts, roi_ind


###### function to extract mean ROI coordinates for future plotting
def roi_coord(dataAtlas, nodeList):
    xyzROI = []
    for iNode in nodeList:
        ROIvoxels = np.mean(np.where(dataAtlas==iNode), axis=1)
        xyzROI.append(list(ROIvoxels))
    return np.array(xyzROI)



###### Atlas image
# atlas data files (resliced version)
f_atlasRt2 = 'tcorr05_2level_all_r.nii.gz'
X_Rt2 = nib.load(f_atlasRt2).get_data()

# K for clustering algorithm
K = list(range(10,301,10)) + list(range(350,1000,50))  
targetK = 200   # K for example atlases
indK = K.index(targetK) # indices corresponding to targetK



###### Input: fMRI time series data
f_fMRI = 'Oxford_sub16112_WBWMCSF.nii.gz'
X_fMRI = nib.load(f_fMRI).get_data()

###### Extracting the time series data
ts_Rt2, node_Rt2 = extract_roits(X_fMRI, X_Rt2[:,:,:,indK])
xyz_Rt2 = roi_coord(X_Rt2[:,:,:,indK], node_Rt2)

###### saving for later use
fOutBase = f_fMRI.replace('.nii.gz','')
fOut = fOutBase + '_Rt2_K' + str(targetK) +'.npz'
np.savez(fOut,
         ts = ts_Rt2,
         nodes = node_Rt2,
         xyz = xyz_Rt2)

