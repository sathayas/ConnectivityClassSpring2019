import numpy as np
import nibabel as nib



###### Image data files
# atlas data files
f_atlasAAL = 'DataAtlas/aal_MNI_V4.nii.gz'
f_atlasRt2 = 'DataAtlas/tcorr05_2level_all.nii.gz'

#fMRI data file (processed)
f_fMRI = 'DataAtlas/Oxford_sub16112_func2standard_r_bp_reg_ms.nii.gz'



##### Header information (fMRI)
# loading the fMRI data
fMRI = nib.load(f_fMRI)   # image object
hdr_fMRI = fMRI.header   # header information
X_fMRI = fMRI.get_data()  # image data array

# priting out the header information
print(hdr_fMRI)

# image dimension
print(hdr_fMRI.get_data_shape())

# voxel size
print(hdr_fMRI.get_zooms())



##### Header information (AAL atlas)
# loading the AAL atlas data
AAL = nib.load(f_atlasAAL)   # image object
hdr_AAL = AAL.header   # header information
X_AAL = AAL.get_data()  # image data array

# image dimension
print(hdr_AAL.get_data_shape())

# voxel size
print(hdr_AAL.get_zooms())

