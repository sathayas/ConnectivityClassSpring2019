#
# Preprocessing only (just before the correlation matrix calculation)
#
# ds114, sub03, test data -- motor data
#

import os
import sys
sys.path.append('/home/satoru/Projects/DynamicConn/Development/')
import MyCodes

BaseDir = '/home/satoru/Projects/ModularMapping/Analysis/Pilot_R21_Oct2017/ds114_sub03_test'
fStruct = os.path.join(BaseDir, 'sub-03_ses-test_T1w.nii.gz')
fStruct_bet = os.path.join(BaseDir, 'sub-03_ses-test_T1w_brain.nii.gz')
ffMRI_orig = os.path.join(BaseDir, 'sub-03_ses-test_task-fingerfootlips_bold.nii.gz')

ListTiming = [os.path.join(BaseDir,'onset-finger-minus10s.txt'),
              os.path.join(BaseDir,'onset-foot-minus10s.txt'),
              os.path.join(BaseDir,'onset-lips-minus10s.txt')]

# parameters
imgDim = [46, 56, 42]
voxSize = [4, 4, 4]
tasks = ['finger', 'foot', 'lips', 'combo']
models = ['NoRegress', 'Regress']


# running bet
MyCodes.run_bet(fStruct)


# running separate preprocessing for fMRI with or without GLM regression.
for iModel in models:

    # first, making a copy of the fMRI data
    ffMRI = os.path.join(BaseDir, 'fMRI_' + iModel + '.nii.gz')
    com_cp = 'cp ' + ffMRI_orig + ' ' + ffMRI
    res = os.system(com_cp)

    # directory business
    FeatDir = os.path.join(BaseDir, 'fMRI_' + iModel + '.feat')
    fGMMask = os.path.join(FeatDir, 'reg/highres2standard_seg_1_d_r.nii.gz')

    # running feat without normalization
    tmpDir = MyCodes.run_feat(fStruct_bet, ffMRI, bNorm=False, nVolDel=4)

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
    if iModel=='NoRegress':
        MyCodes.regress_global(FeatDir)
    else:
        MyCodes.regress_global(FeatDir, GLM)

    # motion scrubbing
    MyCodes.scrub_motion(FeatDir)

    
    # the loop for different tasks
    for iTask in tasks:

        # directory business
        CorrDir = os.path.join(FeatDir, 'CorrDir_'+iTask)
        if not os.path.exists(CorrDir):
            os.makedirs(CorrDir)

        # GLM time series
        if iTask=='finger':
            ts = MyCodes.GLM_column(FeatDir,0)
        elif iTask=='foot':
            ts = MyCodes.GLM_column(FeatDir,2)
        elif iTask=='lips':
            ts = MyCodes.GLM_column(FeatDir,4)
        else:
            ts1 = MyCodes.GLM_column(FeatDir,0)
            ts2 = MyCodes.GLM_column(FeatDir,2)
            ts3 = MyCodes.GLM_column(FeatDir,4)
            ts = ts1 + ts2 + ts3

        # calculating the correlation matrix
        MyCodes.run_crosscorr(CorrDir,PosOnly=1,ts=ts)

            


