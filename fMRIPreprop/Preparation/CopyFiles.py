import os
from shutil import copyfile

def copy_files(Site, SiteOut, subjID, outDir='.'):
    dirOriginBase = '/home/satoru/Projects/Connectome/Data/1000FCP/'
    dirOrigin = os.path.join(dirOriginBase,
                             os.path.join(Site,'Processed/'+subjID))

    # fMRI (up to bp)
    ffMRI = os.path.join(dirOrigin, 'Processed.feat/reg/func2standard_r_bp.nii.gz')
    ffMRIout = os.path.join(outDir, SiteOut+'_'+subjID+'.nii.gz')
    copyfile(ffMRI, ffMRIout)


Site = 'Oxford'
SiteOut = 'Oxford'
subjID = 'sub16112'
copy_files(Site, SiteOut, subjID)
