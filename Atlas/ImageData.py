import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt


###### functions to display 3D image
def show_plane(x):
    '''
    Function to show a slice (provided as a 2D array)
    '''
    plt.imshow(x, cmap="gray")
    plt.gca().set_axis_off()


def show_section(xImg, section, xSlice):
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
    show_plane(np.rot90(tmpImg))




###### Image data files
# atlas data files
f_atlasAAL = 'DataAtlas/aal_MNI_V4.nii.gz'
f_atlasRt2 = 'DataAtlas/tcorr05_2level_all.nii.gz'

#fMRI data file (processed)
f_fMRI = 'DataAtlas/Oxford_sub16112_func2standard_r_bp_reg_ms.nii.gz'



##### showing the image (fMRI)
# loading the fMRI data
fMRI = nib.load(f_fMRI)   # image object
hdr_fMRI = fMRI.header   # header information
X_fMRI = fMRI.get_data()  # image data array

# showing fMRI time series, first 5 time points
plt.figure(figsize=[12,3])

for iTime in range(5):
    plt.subplot(1,5,iTime+1)
    show_section(X_fMRI[:,:,:,iTime], 'xy', 20) # xy-section, at time=iTime
    plt.title('Time point ' + str(iTime+1))

plt.show()


##### Showing the time course (fMRI)
# time course from a voxel
xVox = 13
yVox = 10
zVox = 20
timeVox = [X_fMRI[xVox,yVox,zVox,i] for i in range(X_fMRI.shape[-1])]
# plotting the time course
plt.plot(np.arange(1,len(timeVox)+1),timeVox)
plt.title('Time course from voxel ' + str([xVox,yVox,zVox]))
plt.xlabel('Time points')
plt.ylabel('fMRI signal (processed)')
plt.show()



##### showing the atlas (AAL)
# loading the AAL atlas data
AAL = nib.load(f_atlasAAL)   # image object
hdr_AAL = AAL.header   # header information
X_AAL = AAL.get_data()  # image data array

show_section(X_AAL[:,:,:,0], 'xy', 38) # xy-section, at time=iTime
plt.title('AAL atlas')
plt.show()



##### showing the atlas (Rt2)
# loading the Rt2 atlas data
Rt2 = nib.load(f_atlasRt2)   # image object
hdr_Rt2 = Rt2.header   # header information
X_Rt2 = Rt2.get_data()  # image data array

# Ks for clustering algorithm
K = list(range(10,301,10)) + list(range(350,1000,50))  
subK = [50, 100, 200, 500, 950]   # Ks for example atlases
indK = [list(K).index(k) for k in subK]  # indices corresponding to subK


# showing the atlas with different Ks
plt.figure(figsize=[12,3])

for i,K in enumerate(subK):
    plt.subplot(1,5,i+1)
    show_section(X_Rt2[:,:,:,indK[i]], 'xy', 20) # xy-section
    plt.title('Atlas with K=' + str(K))

plt.show()
