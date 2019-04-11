#
# regress.py
#
# regresses out the motion and mean time course data.
#

import os
import numpy as np
import nibabel as nib

def regress_global(ffmri, fmask, fMoPar, fPhysPar, colInd):

    # directory and file names
    fout = ffmri.replace('.nii.gz','') + '_reg.nii.gz'
    # reading motion parameters
    MoPar = np.genfromtxt(fMoPar,
                          delimiter="  ",
                          missing_values=["NA"])
    NScan = MoPar.shape[0]
    # reading mean time courses
    infile = np.load(fPhysPar)
    PhysPar = infile['PhysPar'][:,colInd]
    # concatenating parameters and centering
    M = np.hstack((MoPar, PhysPar))
    if len(X)>0:
        M = np.hstack((M, X))
    cM = M - np.ones([NScan, 1])*(np.sum(M, axis=0)/NScan)
    # loading the image data
    img_data = nib.load(ffmri)
    X_data = img_data.get_data()
    img_mask = nib.load(fmask)
    X_mask = img_mask.get_data()    
    # then creating a data matrix of elements within-mask elements
    # the dimension of the matrix is T x V, where T is tne number of schans
    # and V is the number of within-mask voxels
    indMaskV = np.nonzero(X_mask)
    for iTime in range(NScan):
        tmpX_data = X_data[:,:,:,iTime]
        tmptrX_data = tmpX_data[indMaskV]
        if iTime==0:
            Y = np.array(tmptrX_data)
        else:
            Y = np.vstack((Y, tmptrX_data))
    # regressing out the motion and mean signals
    Beta = np.dot(np.linalg.pinv(cM), Y)
    eY = Y - np.dot(cM, Beta)
    # putting back the calculation results to a 4D matrix
    outY = np.zeros_like(X_data)
    for iTime in range(NScan):
        tmpY = np.zeros_like(X_mask)
        tmpY[indMaskV] = eY[iTime, :]
        outY[:,:,:,iTime] = tmpY
    # writing out the result image
    regimg = nib.Nifti1Image(outY, img_data.get_affine())
    nib.save(regimg, fout)

