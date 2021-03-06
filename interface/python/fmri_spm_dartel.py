#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
=================
fMRI: DARTEL, SPM
=================

The fmri_spm_dartel.py integrates several interfaces to perform a first
and second level analysis on a two-subject data set.  The tutorial can
be found in the examples folder.  Run the tutorial from inside the
nipype tutorial directory::

    python fmri_spm_dartel.py

Import necessary modules from nipype."""

from __future__ import print_function
from builtins import str
from builtins import range

import nipype.interfaces.io as nio  # Data i/o
import nipype.interfaces.spm as spm  # spm
import niflow.nipype1.workflows.fmri.spm as spm_wf  # spm
import nipype.interfaces.fsl as fsl  # fsl
from nipype.interfaces import utility as niu  # Utilities
import nipype.pipeline.engine as pe  # pypeline engine
import nipype.algorithms.rapidart as ra  # artifact detection
import nipype.algorithms.modelgen as model  # model specification
import os  # system functions
from BEN_infer import BEN_infer

"""
Preliminaries
-------------
Set any package specific configuration. The output file format
for FSL routines is being set to uncompressed NIFTI and a specific
version of matlab is being used. The uncompressed format is required
because SPM does not handle compressed NIFTI.
"""

# Tell fsl to generate all output in uncompressed nifti format
fsl.FSLCommand.set_default_output_type('NIFTI')

# Set the way matlab should be called
# mlab.MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")
# mlab.MatlabCommand.set_default_paths('/software/spm8')

"""
Setting up workflows
--------------------
In this tutorial we will be setting up a hierarchical workflow for spm
analysis. This will demonstrate how pre-defined workflows can be setup
and shared across users, projects and labs.


Setup preprocessing workflow
----------------------------
This is a generic preprocessing workflow that can be used by different analyses

"""

preproc = pe.Workflow(name='preproc')

"""Use :class:`nipype.interfaces.spm.Realign` for motion correction
and register all images to the mean image.
"""

realign = pe.Node(spm.Realign(), name="realign")
realign.inputs.register_to_mean = True

"""Use :class:`nipype.algorithms.rapidart` to determine which of the
images in the functional series are outliers based on deviations in
intensity or movement.
"""

art = pe.Node(ra.ArtifactDetect(), name="art")
art.inputs.use_differences = [True, False]
art.inputs.use_norm = True
art.inputs.norm_threshold = 1
art.inputs.zintensity_threshold = 3
art.inputs.mask_type = 'file'
art.inputs.parameter_source = 'SPM'

"""Skull strip structural images using
:class:`nipype.interfaces.fsl.BET`.
"""

skullstrip = pe.Node(fsl.BET(), name="skullstrip")
skullstrip.inputs.mask = True

"""Use :class:`nipype.interfaces.spm.Coregister` to perform a rigid
body registration of the functional data to the structural data.
"""

coregister = pe.Node(spm.Coregister(), name="coregister")
coregister.inputs.jobtype = 'estimate'

"""Normalize and smooth functional data using DARTEL template
"""

normalize_and_smooth_func = pe.Node(
    spm.DARTELNorm2MNI(modulate=True), name='normalize_and_smooth_func')
fwhmlist = [4]
normalize_and_smooth_func.iterables = ('fwhm', fwhmlist)

"""Normalize structural data using DARTEL template
"""

normalize_struct = pe.Node(
    spm.DARTELNorm2MNI(modulate=True), name='normalize_struct')
normalize_struct.inputs.fwhm = 2

preproc.connect([
    (realign, coregister, [('mean_image', 'source'), ('realigned_files',
                                                      'apply_to_files')]),
    (coregister, normalize_and_smooth_func, [('coregistered_files',
                                              'apply_to_files')]),
    (normalize_struct, skullstrip, [('normalized_files', 'in_file')]),
    (realign, art, [('realignment_parameters', 'realignment_parameters')]),
    (normalize_and_smooth_func, art, [('normalized_files',
                                       'realigned_files')]),
    (skullstrip, art, [('mask_file', 'mask_file')]),
])

"""
Set up analysis workflow
------------------------
"""

l1analysis = pe.Workflow(name='analysis')

"""Generate SPM-specific design information using
:class:`nipype.interfaces.spm.SpecifyModel`.
"""

modelspec = pe.Node(model.SpecifySPMModel(), name="modelspec")
modelspec.inputs.concatenate_runs = True

"""Generate a first level SPM.mat file for analysis
:class:`nipype.interfaces.spm.Level1Design`.
"""

level1design = pe.Node(spm.Level1Design(), name="level1design")
level1design.inputs.bases = {'hrf': {'derivs': [0, 0]}}

"""Use :class:`nipype.interfaces.spm.EstimateModel` to determine the
parameters of the model.
"""

level1estimate = pe.Node(spm.EstimateModel(), name="level1estimate")
level1estimate.inputs.estimation_method = {'Classical': 1}

"""Use :class:`nipype.interfaces.spm.EstimateContrast` to estimate the
first level contrasts specified in a few steps above.
"""

contrastestimate = pe.Node(spm.EstimateContrast(), name="contrastestimate")

"""Use :class: `nipype.interfaces.utility.Select` to select each contrast for
reporting.
"""

selectcontrast = pe.Node(niu.Select(), name="selectcontrast")

"""Use :class:`nipype.interfaces.fsl.Overlay` to combine the statistical output of
the contrast estimate and a background image into one volume.
"""

overlaystats = pe.Node(fsl.Overlay(), name="overlaystats")
overlaystats.inputs.stat_thresh = (3, 10)
overlaystats.inputs.show_negative_stats = True
overlaystats.inputs.auto_thresh_bg = True

"""Use :class:`nipype.interfaces.fsl.Slicer` to create images of the overlaid
statistical volumes for a report of the first-level results.
"""

slicestats = pe.Node(fsl.Slicer(), name="slicestats")
slicestats.inputs.all_axial = True
slicestats.inputs.image_width = 750

l1analysis.connect([(modelspec, level1design,
                     [('session_info',
                       'session_info')]), (level1design, level1estimate,
                                           [('spm_mat_file', 'spm_mat_file')]),
                    (level1estimate, contrastestimate,
                     [('spm_mat_file', 'spm_mat_file'), ('beta_images',
                                                         'beta_images'),
                      ('residual_image',
                       'residual_image')]), (contrastestimate, selectcontrast,
                                             [('spmT_images', 'inlist')]),
                    (selectcontrast, overlaystats,
                     [('out', 'stat_image')]), (overlaystats, slicestats,
                                                [('out_file', 'in_file')])])

"""
Preproc + Analysis pipeline
---------------------------
"""

l1pipeline = pe.Workflow(name='firstlevel')
l1pipeline.connect([
    (preproc, l1analysis,
     [('realign.realignment_parameters', 'modelspec.realignment_parameters'),
      ('normalize_and_smooth_func.normalized_files',
       'modelspec.functional_runs'), ('art.outlier_files',
                                      'modelspec.outlier_files'),
      ('skullstrip.mask_file',
       'level1design.mask_image'), ('normalize_struct.normalized_files',
                                    'overlaystats.background_image')]),
])

"""
Data specific components
------------------------
The nipype tutorial contains data for two subjects.  Subject data
is in two subdirectories, ``s1`` and ``s2``.  Each subject directory
contains four functional volumes: f3.nii, f5.nii, f7.nii, f10.nii. And
one anatomical volume named struct.nii.

Below we set some variables to inform the ``datasource`` about the
layout of our data.  We specify the location of the data, the subject
sub-directories and a dictionary that maps each run to a mnemonic (or
field) for the run type (``struct`` or ``func``).  These fields become
the output fields of the ``datasource`` node in the pipeline.

In the example below, run 'f3' is of type 'func' and gets mapped to a
nifti filename through a template '%s.nii'. So 'f3' would become
'f3.nii'.

"""

# Specify the location of the data.
# data_dir = os.path.abspath('data')
# Specify the subject directories
subject_list = ['s1', 's3']
# Map field names to individual subject runs.
info = dict(
    func=[['subject_id', ['f3', 'f5', 'f7', 'f10']]],
    struct=[['subject_id', 'struct']])

infosource = pe.Node(
    niu.IdentityInterface(fields=['subject_id']), name="infosource")

"""Here we set up iteration over all the subjects. The following line
is a particular example of the flexibility of the system.  The
``datasource`` attribute ``iterables`` tells the pipeline engine that
it should repeat the analysis on each of the items in the
``subject_list``. In the current example, the entire first level
preprocessing and estimation will be repeated for each subject
contained in subject_list.
"""

infosource.iterables = ('subject_id', subject_list)

"""
Now we create a :class:`nipype.interfaces.io.DataGrabber` object and
fill in the information from above about the layout of our data.  The
:class:`nipype.pipeline.NodeWrapper` module wraps the interface object
and provides additional housekeeping and pipeline specific
functionality.
"""

inputnode = pe.Node(
    niu.IdentityInterface(fields=['in_data']), name='inputnode')
datasource = pe.Node(
    nio.DataGrabber(infields=['subject_id'], outfields=['func', 'struct']),
    name='datasource')
datasource.inputs.template = 'nipype-tutorial/data/%s/%s.nii'
datasource.inputs.template_args = info
datasource.inputs.sort_filelist = True

"""We need to create a separate workflow to make the DARTEL template
"""

datasource_dartel = pe.MapNode(
    nio.DataGrabber(infields=['subject_id'], outfields=['struct']),
    name='datasource_dartel',
    iterfield=['subject_id'])
datasource_dartel.inputs.template = 'nipype-tutorial/data/%s/%s.nii'
datasource_dartel.inputs.template_args = dict(
    struct=[['subject_id', 'struct']])
datasource_dartel.inputs.sort_filelist = True
datasource_dartel.inputs.subject_id = subject_list

"""Here we make sure that struct files have names corresponding to the subject ids.
This way we will be able to pick the right field flows later.
"""

rename_dartel = pe.MapNode(
    niu.Rename(format_string="subject_id_%(subject_id)s_struct"),
    iterfield=['in_file', 'subject_id'],
    name='rename_dartel')
rename_dartel.inputs.subject_id = subject_list
rename_dartel.inputs.keep_ext = True

dartel_workflow = spm_wf.create_DARTEL_template(name='dartel_workflow')
dartel_workflow.inputs.inputspec.template_prefix = "template"

"""This function will allow to pick the right field flow for each subject
"""

def pickFieldFlow(dartel_flow_fields, subject_id):
    from nipype.utils.filemanip import split_filename
    for f in dartel_flow_fields:
        _, name, _ = split_filename(f)
        if name.find("subject_id_%s" % subject_id):
            return f

    raise Exception

pick_flow = pe.Node(
    niu.Function(
        input_names=['dartel_flow_fields', 'subject_id'],
        output_names=['dartel_flow_field'],
        function=pickFieldFlow),
    name="pick_flow")

"""
Experimental paradigm specific components
-----------------------------------------
Here we create a function that returns subject-specific information
about the experimental paradigm. This is used by the
:class:`nipype.interfaces.spm.SpecifyModel` to create the information
necessary to generate an SPM design matrix. In this tutorial, the same
paradigm was used for every participant.
"""

def subjectinfo(subject_id):
    from nipype.interfaces.base import Bunch
    from copy import deepcopy
    print("Subject ID: %s\n" % str(subject_id))
    output = []
    names = ['Task-Odd', 'Task-Even']
    for r in range(4):
        onsets = [list(range(15, 240, 60)), list(range(45, 240, 60))]
        output.insert(r,
                      Bunch(
                          conditions=names,
                          onsets=deepcopy(onsets),
                          durations=[[15] for s in names],
                          amplitudes=None,
                          tmod=None,
                          pmod=None,
                          regressor_names=None,
                          regressors=None))
    return output

"""Setup the contrast structure that needs to be evaluated. This is a
list of lists. The inner list specifies the contrasts and has the
following format - [Name,Stat,[list of condition names],[weights on
those conditions]. The condition names must match the `names` listed
in the `subjectinfo` function described above.
"""

cont1 = ('Task>Baseline', 'T', ['Task-Odd', 'Task-Even'], [0.5, 0.5])
cont2 = ('Task-Odd>Task-Even', 'T', ['Task-Odd', 'Task-Even'], [1, -1])
contrasts = [cont1, cont2]

# set up node specific inputs
modelspecref = l1pipeline.inputs.analysis.modelspec
modelspecref.input_units = 'secs'
modelspecref.output_units = 'secs'
modelspecref.time_repetition = 3.
modelspecref.high_pass_filter_cutoff = 120

l1designref = l1pipeline.inputs.analysis.level1design
l1designref.timing_units = modelspecref.output_units
l1designref.interscan_interval = modelspecref.time_repetition

l1pipeline.inputs.analysis.contrastestimate.contrasts = contrasts

# Iterate over each contrast and create report images.
selectcontrast.iterables = ('index', [[i] for i in range(len(contrasts))])

"""
Setup the pipeline
------------------
The nodes created above do not describe the flow of data. They merely
describe the parameters used for each function. In this section we
setup the connections between the nodes such that appropriate outputs
from nodes are piped into appropriate inputs of other nodes.

Use the :class:`nipype.pipeline.engine.Pipeline` to create a
graph-based execution pipeline for first level analysis. The config
options tells the pipeline engine to use `workdir` as the disk
location to use when running the processes and keeping their
outputs. The `use_parameterized_dirs` tells the engine to create
sub-directories under `workdir` corresponding to the iterables in the
pipeline. Thus for this pipeline there will be subject specific
sub-directories.

The ``nipype.pipeline.engine.Pipeline.connect`` function creates the
links between the processes, i.e., how data should flow in and out of
the processing nodes.
"""

level1 = pe.Workflow(name="level1")
level1.base_dir = os.path.abspath('spm_dartel_tutorial/workingdir')

level1.connect([
    (inputnode, datasource, [('in_data', 'base_directory')]),
    (inputnode, datasource_dartel, [('in_data', 'base_directory')]),
    (datasource_dartel, rename_dartel, [('struct', 'in_file')]),
    (rename_dartel, dartel_workflow, [('out_file',
                                       'inputspec.structural_files')]),
    (infosource, datasource, [('subject_id', 'subject_id')]),
    (datasource, l1pipeline,
     [('func', 'preproc.realign.in_files'), ('struct',
                                             'preproc.coregister.target'),
      ('struct', 'preproc.normalize_struct.apply_to_files')]),
    (dartel_workflow, l1pipeline,
     [('outputspec.template_file', 'preproc.normalize_struct.template_file'),
      ('outputspec.template_file',
       'preproc.normalize_and_smooth_func.template_file')]),
    (infosource, pick_flow, [('subject_id', 'subject_id')]),
    (dartel_workflow, pick_flow, [('outputspec.flow_fields',
                                   'dartel_flow_fields')]),
    (pick_flow, l1pipeline,
     [('dartel_flow_field', 'preproc.normalize_struct.flowfield_files'),
      ('dartel_flow_field',
       'preproc.normalize_and_smooth_func.flowfield_files')]),
    (infosource, l1pipeline, [(('subject_id', subjectinfo),
                               'analysis.modelspec.subject_info')]),
])

"""
Setup storage results
---------------------
Use :class:`nipype.interfaces.io.DataSink` to store selected outputs
from the pipeline in a specific location. This allows the user to
selectively choose important output bits from the analysis and keep
them.

The first step is to create a datasink node and then to connect
outputs from the modules above to storage locations. These take the
following form directory_name[.[@]subdir] where parts between [] are
optional. For example 'realign.@mean' below creates a directory called
realign in 'l1output/subject_id/' and stores the mean image output
from the Realign process in the realign directory. If the @ is left
out, then a sub-directory with the name 'mean' would be created and
the mean image would be copied to that directory.
"""

datasink = pe.Node(nio.DataSink(), name="datasink")
datasink.inputs.base_directory = os.path.abspath(
    'spm_dartel_tutorial/l1output')
report = pe.Node(nio.DataSink(), name='report')
report.inputs.base_directory = os.path.abspath('spm_dartel_tutorial/report')
report.inputs.parameterization = False


def getstripdir(subject_id):
    import os
    return os.path.join(
        os.path.abspath('spm_dartel_tutorial/workingdir'),
        '_subject_id_%s' % subject_id)


# store relevant outputs from various stages of the 1st level analysis
level1.connect([
    (infosource, datasink, [('subject_id', 'container'),
                            (('subject_id', getstripdir), 'strip_dir')]),
    (l1pipeline, datasink,
     [('analysis.contrastestimate.con_images', 'contrasts.@con'),
      ('analysis.contrastestimate.spmT_images', 'contrasts.@T')]),
    (infosource, report, [('subject_id', 'container'),
                          (('subject_id', getstripdir), 'strip_dir')]),
    (l1pipeline, report, [('analysis.slicestats.out_file', '@report')]),
])

"""
Execute the pipeline
--------------------
The code discussed above sets up all the necessary data structures
with appropriate parameters and the connectivity between the
processes, but does not generate any output. To actually run the
analysis on the data the ``nipype.pipeline.engine.Pipeline.Run``
function needs to be called.
"""

if __name__ == '__main__':
    level1.run(plugin_args={'n_procs': 4})
    level1.write_graph()

"""
Setup level 2 pipeline
----------------------
Use :class:`nipype.interfaces.io.DataGrabber` to extract the contrast
images across a group of first level subjects. Unlike the previous
pipeline that iterated over subjects, this pipeline will iterate over
contrasts.
"""

# collect all the con images for each contrast.
contrast_ids = list(range(1, len(contrasts) + 1))
l2source = pe.Node(nio.DataGrabber(infields=['fwhm', 'con']), name="l2source")
# we use .*i* to capture both .img (SPM8) and .nii (SPM12)
l2source.inputs.template = os.path.abspath(
    'spm_dartel_tutorial/l1output/*/con*/*/_fwhm_%d/con_%04d.*i*')
# iterate over all contrast images
l2source.iterables = [('fwhm', fwhmlist), ('con', contrast_ids)]
l2source.inputs.sort_filelist = True

"""Use :class:`nipype.interfaces.spm.OneSampleTTestDesign` to perform a
simple statistical analysis of the contrasts from the group of
subjects (n=2 in this example).
"""

# setup a 1-sample t-test node
onesamplettestdes = pe.Node(spm.OneSampleTTestDesign(), name="onesampttestdes")
l2estimate = pe.Node(spm.EstimateModel(), name="level2estimate")
l2estimate.inputs.estimation_method = {'Classical': 1}
l2conestimate = pe.Node(spm.EstimateContrast(), name="level2conestimate")
cont1 = ('Group', 'T', ['mean'], [1])
l2conestimate.inputs.contrasts = [cont1]
l2conestimate.inputs.group_contrast = True

"""As before, we setup a pipeline to connect these two nodes (l2source
-> onesamplettest).
"""

l2pipeline = pe.Workflow(name="level2")
l2pipeline.base_dir = os.path.abspath('spm_dartel_tutorial/l2output')
l2pipeline.connect([
    (l2source, onesamplettestdes, [('outfiles', 'in_files')]),
    (onesamplettestdes, l2estimate, [('spm_mat_file', 'spm_mat_file')]),
    (l2estimate, l2conestimate,
     [('spm_mat_file', 'spm_mat_file'), ('beta_images', 'beta_images'),
      ('residual_image', 'residual_image')]),
])

"""
Execute the second level pipeline
---------------------------------
"""

if __name__ == '__main__':
    BEN_infer('/INPUT/PATH', '/OUTPUT/PATH', 'WEIGHT')
    l2pipeline.run()
