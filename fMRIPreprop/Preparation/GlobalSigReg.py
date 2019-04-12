import numpy as np
import nibabel as nib
from regress import regress_global

##### file business
ffmri = 'Oxford_sub16112.nii.gz'
fmask = 'Oxford_sub16112_mask.nii.gz'
fMoPar = 'Oxford_sub16112_MoPar.par'
fPhysPar = 'Oxford_sub16112_PhysPar.npz'


##### regressing out Whole Brain (WB), white matter (WM), CSF
fout = 'Oxford_sub16112_WBWMCSF.nii.gz'
colInd = [0,1,2]
regress_global(ffmri, fmask, fMoPar, fPhysPar, colInd, fout)


##### regressing out Whole Brain (WB), white matter (WM), CSF
fout = 'Oxford_sub16112_WMCSF.nii.gz'
colInd = [1,2]
regress_global(ffmri, fmask, fMoPar, fPhysPar, colInd, fout)
