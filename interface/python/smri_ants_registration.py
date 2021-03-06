#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
==================================
sMRI: Using ANTS for registration
==================================

In this simple tutorial we will use the Registration interface from ANTS to
coregister two T1 volumes.

1. Tell python where to find the appropriate functions.

"""

from __future__ import print_function, unicode_literals
from builtins import open

from future import standard_library
standard_library.install_aliases()

import os
import urllib.request
import urllib.error
import urllib.parse
from nipype.interfaces.ants import Registration
from nipype.testing import example_data
from BEN_infer import BEN_infer
"""
2. Download T1 volumes into home directory

"""

homeDir = os.getenv("HOME")
requestedPath = os.path.join(homeDir, 'nipypeTestPath')
mydatadir = os.path.realpath(requestedPath)
if not os.path.exists(mydatadir):
    os.makedirs(mydatadir)
print(mydatadir)

MyFileURLs = [
    ('http://slicer.kitware.com/midas3/download?bitstream=13121',
     '01_T1_half.nii.gz'),
    ('http://slicer.kitware.com/midas3/download?bitstream=13122',
     '02_T1_half.nii.gz'),
]
for tt in MyFileURLs:
    myURL = tt[0]
    localFilename = os.path.join(mydatadir, tt[1])
    if not os.path.exists(localFilename):
        remotefile = urllib.request.urlopen(myURL)

        localFile = open(localFilename, 'wb')
        localFile.write(remotefile.read())
        localFile.close()
        print("Downloaded file: {0}".format(localFilename))
    else:
        print("File previously downloaded {0}".format(localFilename))

input_images = [
    os.path.join(mydatadir, '01_T1_half.nii.gz'),
    os.path.join(mydatadir, '02_T1_half.nii.gz'),
]
"""
3. Define the parameters of the registration. Settings are
found in the file ``smri_ants_registration_settings.json``
distributed with the ``example_data`` of `nipype`.

"""

reg = Registration(
    from_file=example_data('smri_ants_registration_settings.json'))
reg.inputs.fixed_image = input_images[0]
reg.inputs.moving_image = input_images[1]
"""
Alternatively to the use of the ``from_file`` feature to load ANTs settings,
the user can manually set all those inputs instead::

    reg.inputs.output_transform_prefix = 'thisTransform'
    reg.inputs.output_warped_image = 'INTERNAL_WARPED.nii.gz'
    reg.inputs.output_transform_prefix = "output_"
    reg.inputs.transforms = ['Translation', 'Rigid', 'Affine', 'SyN']
    reg.inputs.transform_parameters = [(0.1,), (0.1,), (0.1,), (0.2, 3.0, 0.0)]
    reg.inputs.number_of_iterations = ([[10000, 111110, 11110]] * 3 +
                                       [[100, 50, 30]])
    reg.inputs.dimension = 3
    reg.inputs.write_composite_transform = True
    reg.inputs.collapse_output_transforms = False
    reg.inputs.metric = ['Mattes'] * 3 + [['Mattes', 'CC']]
    reg.inputs.metric_weight = [1] * 3 + [[0.5, 0.5]]
    reg.inputs.radius_or_number_of_bins = [32] * 3 + [[32, 4]]
    reg.inputs.sampling_strategy = ['Regular'] * 3 + [[None, None]]
    reg.inputs.sampling_percentage = [0.3] * 3 + [[None, None]]
    reg.inputs.convergence_threshold = [1.e-8] * 3 + [-0.01]
    reg.inputs.convergence_window_size = [20] * 3 + [5]
    reg.inputs.smoothing_sigmas = [[4, 2, 1]] * 3 + [[1, 0.5, 0]]
    reg.inputs.sigma_units = ['vox'] * 4
    reg.inputs.shrink_factors = [[6, 4, 2]] + [[3, 2, 1]] * 2 + [[4, 2, 1]]
    reg.inputs.use_estimate_learning_rate_once = [True] * 4
    reg.inputs.use_histogram_matching = [False] * 3 + [True]
    reg.inputs.initial_moving_transform_com = True

"""

print(reg.cmdline)
"""
3. Run the registration
"""
# Skull-stripping before analysis
BEN_infer('/INPUT/PATH', '/OUTPUT/PATH', 'WEIGHT')

reg.run()
