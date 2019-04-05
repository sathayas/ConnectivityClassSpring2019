import numpy as np
import nibabel as nib
import os

# directory business
baseDir = '/home/satoru/Projects/Connectome/Data/1000FCP/Leiden_2200/Processed/'
fPath = 'Processed.feat/reg/func2standard_r_bp_reg_ms.nii.gz'
listDir = os.listdir(baseDir)
listSubj = [x for x in listDir if 'sub' in x]

# extracting number of time points
nTimePoints = []
for iSubj in listSubj:
    subjDir = os.path.join(baseDir,iSubj)
    subjFile = os.path.join(subjDir,fPath)
    X_fMRI = nib.load(fMRI).get_data()
    nTimePoints.append(X_fMRI.shape[-1])

# printing out the results
print('%-12s' % 'Subject' + '%-14s' % 'N time points')
for i,iSubj in enumerate(listSubj):
    print('%-12s' % iSubj + '%4d' % nTimePoints[i])
