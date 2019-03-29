#
# Preprocessing only (just before the correlation matrix calculation)
#
# ds114, sub03, test data -- covert verb generation data
#

import os
import sys
sys.path.append('/home/satoru/Projects/DynamicConn/Development/')
import MyCodes

BaseDir = '/home/satoru/Projects/ModularMapping/Analysis/Pilot_R21_Oct2017/ds114_sub03_test'
fStruct = os.path.join(BaseDir, 'sub-03_ses-test_T1w.nii.gz')
fStruct_bet = os.path.join(BaseDir, 'sub-03_ses-test_T1w_brain.nii.gz')
ffMRI_orig = os.path.join(BaseDir, 'sub-03_ses-test_task-covertverbgeneration_bold.nii.gz')


ListTiming = ['onset-covertverbgeneration-minus10s.txt']


# parameters
imgDim = [46, 56, 42]
voxSize = [4, 4, 4]


# first, making a copy of the fMRI data
ffMRI = os.path.join(BaseDir, 'PSY381D_fMRI_covertverb.nii.gz')
com_cp = 'cp ' + ffMRI_orig + ' ' + ffMRI
res = os.system(com_cp)

# directory business
FeatDir = os.path.join(BaseDir, 'PSY381D_fMRI_covertverb.feat')
fGMMask = os.path.join(FeatDir, 'reg/highres2standard_seg_1_d_r.nii.gz')

# running feat with normalization
tmpDir = MyCodes.run_feat(fStruct_bet, ffMRI, bNorm=True, nVolDel=4)

# constructing the desing files for a block model
GLM = MyCodes.run_feat_model(fStruct_bet, ffMRI, ListTiming, nVolDel=4)

# warping (or re-orienting, centering, and reslicing) the functional
MyCodes.run_warp(FeatDir, imgDim, voxSize)

# band-pass filtering
MyCodes.run_bp(FeatDir)

# segmentation
MyCodes.run_fast(FeatDir)

# creating masks
MyCodes.mask_gm(FeatDir)
MyCodes.generate_mask(FeatDir, fGMMask)

# extracting the mean time series
MyCodes.extract_global(FeatDir)

# running regression
MyCodes.regress_global(FeatDir, GLM)

# motion scrubbing - disabled
#MyCodes.scrub_motion(FeatDir)

    


            


