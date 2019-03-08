import numpy as np
import nibabel as nib
import os
import matplotlib.pyplot as plt


###### functions to display 3D image
def show_plane(x, nameCmap='gray'):
    '''
    Function to show a slice (provided as a 2D array)
    '''
    plt.imshow(x, cmap=nameCmap)
    plt.gca().set_axis_off()


def show_section(xImg, section, xSlice, nameCmap='gray'):
    '''
    Function to return a 2D array of a slice from a 3D array.
    Slice orientation can be specified by the user.
    '''
    if section=='xy':
        tmpImg = xImg[:,:,xSlice]
    elif section=='xz':
        tmpImg = xImg[:,xSlice,:]
    else:
        tmpImg = xImg[xSlice,:,:]
    show_plane(np.rot90(tmpImg),nameCmap)



####### function to reslice 4D image to a user-specified voxel size & dimension
def reslice_fmri(ffMRI, img_dim, vox_sz):
    '''a function to reslice the warped fMRI image to desired size.
    
    This function is necessary since warped fMRI has the same voxel size
    as the structural MRI. The resliced image is written with the same file
    name as the input file name with _r suffix attached at the end.
    
    Input parameters:
          ffMRI:        The file name of the 4D fMRI data to be resliced.
          img_dim:      A 3-element vector describing the number of voxles
                        in x, y, and z directions.
          vox_sz:       A 3-element vector describing the size of each voxel
                        in mm (x, y, and z sizes).
    
    Returns:
          NONE:
    '''

    # file name business first
    WorkDir, fImg = os.path.split(os.path.abspath(ffMRI))
    tmpfname, tmpext = os.path.splitext(fImg)
    if tmpext == '.gz':
        # the extension is .nii.gz
        tmpfname, tmpext = os.path.splitext(tmpfname)
    # the fake header name
    ffakehdr = os.path.join(WorkDir, tmpfname + '_r_tmp')
    # the output 4D fMRI data
    fout = os.path.join(WorkDir, tmpfname + '_r')
    # the identity matrix (a la fsl)
    DirFSL = os.environ['FSLDIR']
    feye = os.path.join(DirFSL, 'etc/flirtsch/ident.mat')

    # then putting together the command to create the fake header
    com_hdr = 'fslcreatehd '
    for iDim in img_dim:
        com_hdr += ' ' + str(iDim)
    com_hdr += ' 1'
    for iSize in vox_sz:
        com_hdr += ' ' + str(iSize)
    com_hdr += ' 1 0 0 0 16 ' + ffakehdr
    # creating the faek header
    res = os.system(com_hdr)

    # then putting together the command for flirt for reslicing
    com_flirt = 'flirt -in ' + ffMRI
    com_flirt += ' -applyxfm -init ' + feye
    com_flirt += ' -out ' + fout
    com_flirt += ' -paddingsize 0.0'
    com_flirt += ' -interp nearestneighbour'
    com_flirt += ' -ref ' + ffakehdr
    # then calling flirt
    res = os.system(com_flirt)

    # finally removing the fake header
    com_rm = 'rm ' + ffakehdr + '.nii.gz'
    res = os.system(com_rm)



###### Image data files
# atlas data files
f_atlasAAL = 'DataAtlas/aal_MNI_V4.nii.gz'
f_atlasRt2 = 'DataAtlas/tcorr05_2level_all.nii.gz'

#fMRI data file (processed)
f_fMRI = 'DataAtlas/Oxford_sub16112_func2standard_r_bp_reg_ms.nii.gz'



##### extracting info from fMRI
# loading the fMRI data
fMRI = nib.load(f_fMRI)   # image object
hdr_fMRI = fMRI.header   # header information
dimfMRI = hdr_fMRI.get_data_shape()[:-1]  # xyz dimension in terms of  
sizefMRI = hdr_fMRI.get_zooms()[:-1]  # voxel size in mm in xyz directions



##### reslicing the AAL atlas
reslice_fmri(f_atlasAAL, dimfMRI, sizefMRI)


##### reslicing the Rt2 atlas
reslice_fmri(f_atlasRt2, dimfMRI, sizefMRI)



##### Quality control
f_atlasAAL_r = 'DataAtlas/aal_MNI_V4_r.nii.gz'
f_atlasRt2_r = 'DataAtlas/tcorr05_2level_all_r.nii.gz'
AAL = nib.load(f_atlasAAL_r)   # image object
Rt2 = nib.load(f_atlasRt2_r)   # image object

X_fMRI = fMRI.get_data()
X_AAL = AAL.get_data()
X_Rt2 = Rt2.get_data()


zSlice = 25
plt.figure(figsize=[9,4])

plt.subplot(131)
show_section(X_fMRI[:,:,:,1],'xy',zSlice)
plt.title('fMRI data')

plt.subplot(132)
show_section(X_AAL,'xy',zSlice, nameCmap='rainbow')
plt.title('AAL atlas')

plt.subplot(133)
show_section(X_Rt2[:,:,:,20],'xy',zSlice, nameCmap='rainbow')
plt.title('Rt2 atlas')

plt.show()
