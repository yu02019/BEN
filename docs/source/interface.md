# BEN interface
Codes for neuroimaging analysis via Matlab, Python(Nipype) and shell scripting.

As skull stripping is usually the first preprocessing step in the most pipelines, BEN can be used as a tool independently or called in shell scripts to work with other neuroimaging tool synergistically.

## Usage
Please refer to the Colab notebook examples.

| Neuroimaging tool   | Style          | Colab link                                                                                                                                                                  |
|---------------------|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ANTs (Registration) | Shell scripts  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1mnlBcRBxpLb2QbcVqQsU5p50fRaM5Ifq?usp=sharing) Sec 3.0 |
| ANTs (N4)           | Python(Nipype) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/13V0btuvD6x6c-ClHmKoTClE-El78k6QM?usp=sharing)         |



## File structure
See details in GitHub [repository](https://github.com/yu02019/BEN).

```
tree
│  
├─matlab
│      BEN-skull-strippting.m
│      README.md
│      spm-ben.m
│      
├─python
│      cli.py
│      dmri_camino_dti.py
│      dmri_connectivity.py
│      dmri_connectivity_advanced.py
│      dmri_dtk_dti.py
│      dmri_dtk_odf.py
│      dmri_fsl_dti.py
│      dmri_group_connectivity_camino.py
│      dmri_group_connectivity_mrtrix.py
│      dmri_mrtrix_dti.py
│      dmri_preprocessing.py
│      dmri_tbss_nki.py
│      fmri_ants_openfmri.py
│      fmri_freesurfer_smooth.py
│      fmri_fsl.py
│      fmri_fsl_feeds.py
│      fmri_fsl_reuse.py
│      fmri_nipy_glm.py
│      fmri_openfmri.py
│      fmri_slicer_coregistration.py
│      fmri_spm.py
│      fmri_spm_auditory.py
│      fmri_spm_dartel.py
│      fmri_spm_face.py
│      fmri_spm_nested.py
│      howto_caching_example.py
│      README.md
│      rsfmri_vol_surface_preprocessing.py
│      rsfmri_vol_surface_preprocessing_nipy.py
│      smri_antsregistration_build_template.py
│      smri_ants_build_template.py
│      smri_ants_registration.py
│      smri_cbs_skullstripping.py
│      smri_freesurfer.py
│      smri_fsreconall.py
│      tessellation_tutorial.py
│      test_spm.py
│      utils_ants_os.py
│      utils_trans_os.py
│      workshop_dartmouth_2010.py
│      
└─shell_sript
        afni_proc.sh
        ants_registration.sh
        BEN-skull-strippting.sh
        freesurfer_recon-all.sh
        fsl_dti_tracking.sh
        fsl_registrision.sh
        README.md
        spm.sh
```


