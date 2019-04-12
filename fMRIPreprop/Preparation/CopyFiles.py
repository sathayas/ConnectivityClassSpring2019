import os
from shutil import copyfile

def copy_files(Site, SiteOut, subjID, outDir='.'):
    dirOriginBase = '/home/satoru/Projects/Connectome/Data/1000FCP/'
    dirOrigin = os.path.join(dirOriginBase,
                             os.path.join(Site,'Processed/'+subjID))

    # fMRI (up to bp)
    ffMRI = os.path.join(dirOrigin, 'Processed.feat/reg/func2standard_r_bp_reg.nii.gz')
    ffMRIout = os.path.join(outDir, SiteOut+'_'+subjID+'.nii.gz')
    copyfile(ffMRI, ffMRIout)

    # mask image
    fMask = os.path.join(dirOrigin, 'Processed.feat/reg/aal_fmri_brain.nii.gz')
    fMaskout = os.path.join(outDir, SiteOut+'_'+subjID+'_mask.nii.gz')
    copyfile(fMask, fMaskout)

    # Phys par file (aka global means)
    fPhysPar = os.path.join(dirOrigin, 'Processed.feat/reg/PhysPar.npz')
    fPhysParout = os.path.join(outDir, SiteOut+'_'+subjID+'_PhysPar.npz')
    copyfile(fPhysPar, fPhysParout)

    # Motion parameter file 
    fMoPar = os.path.join(dirOrigin, 'Processed.feat/mc/prefiltered_func_data_mcf.par')
    fMoParout = os.path.join(outDir, SiteOut+'_'+subjID+'_MoPar.par')
    copyfile(fMoPar, fMoParout)
    
    
Site = 'Oxford'
SiteOut = 'Oxford'
subjID = 'sub16112'
copy_files(Site, SiteOut, subjID)

Site = 'NewYork_b'
SiteOut = 'NewYork'
subjID = 'sub83453'
copy_files(Site, SiteOut, subjID)

Site = 'Queensland'
SiteOut = 'Queensland'
subjID = 'sub66095'
copy_files(Site, SiteOut, subjID)
