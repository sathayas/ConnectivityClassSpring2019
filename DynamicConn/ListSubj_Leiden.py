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
    X_fMRI = nib.load(subjFile).get_data()
    nTimePoints.append(X_fMRI.shape[-1])

# printing out the results
print('%-12s' % 'Subject' + '%-14s' % 'N time points')
for i,iSubj in enumerate(listSubj):
    print('%-12s' % iSubj + '%4d' % nTimePoints[i])


#Subject     N time points 
#sub64642     212
#sub40907     212
#sub18456     212
#sub39335     212
#sub72247     212
#sub13537     204
#sub66131     212
#sub01787     212
#sub97690     200
#sub30943     212
#sub86034     212
#sub36743     212
#sub92061     212
#sub68050     212
#sub57187     212
#sub93194     212
#sub04484     212
#sub87320     212
#sub52922     212
