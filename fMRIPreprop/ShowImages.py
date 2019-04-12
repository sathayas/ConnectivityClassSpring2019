import numpy as np
import nibabel as nib
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



###### Loading images
f_T1 = 'DatafMRIPreprop/Oxford_sub16112_T1.nii.gz'
f_WB = 'DatafMRIPreprop/Oxford_sub16112_WB.nii.gz'
f_WM = 'DatafMRIPreprop/Oxford_sub16112_WM.nii.gz'
f_CSF = 'DatafMRIPreprop/Oxford_sub16112_CSF.nii.gz'
X_T1 = nib.load(f_T1).get_data()
X_WB = nib.load(f_WB).get_data()
X_WM = nib.load(f_WM).get_data()
X_CSF = nib.load(f_CSF).get_data()




##### showing images
zSlice = 48
plt.figure(figsize=[12,4])

plt.subplot(141)
show_section(X_T1,'xy',zSlice)
plt.title('T1 image')

plt.subplot(142)
show_section(X_WB,'xy',zSlice)
plt.title('Whole brain\nparenchyma')

plt.subplot(143)
show_section(X_WM,'xy',zSlice)
plt.title('Deep white matter')

plt.subplot(144)
show_section(X_CSF,'xy',zSlice)
plt.title('CSF')
plt.show()

