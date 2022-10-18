
.. Tag a jupyter notebook cell with "nbsphinx-thumbnail" to choose its output as the
.. icon for the notebook gallery
.. https://nbsphinx.readthedocs.io/en/0.8.9/gallery/cell-metadata.html#Using-Cell-Metadata-to-Select-a-Thumbnail

.. Each notebook should have a least one markdown heading, which will be used as the
.. name of the notebook for the notebook gallery

.. To see the cell tags go to: View -> Cell Toolbar -> Tags in the notebook menu.

Tutorials
=========
This section contains various tutorials showcasing brain tissue extraction with
:mod:`BEN`.


Usage
-----------
Quick start to use BEN or replicate our experiments in 5 minutes!


.. nbgallery::

    notebooks/2_BEN_tutorial_Ⅰ_cross_species
    notebooks/3_BEN_tutorial_Ⅱ_cross_modality
    notebooks/3_BEN_tutorial_Ⅲ_cross_field
    notebooks/4_Compare_with_other_toolbox
    notebooks/5_Disagreement
    notebooks/5_QA
    notebooks/6_(Registration comparision)Volumetric_quantification
    notebooks/6_Volumetric_quantification



Interface
--------------------
Codes for neuroimaging analysis via Matlab, Python(Nipype) and shell scripting.

As skull stripping is usually the first preprocessing step in the most pipelines, BEN can be used as a tool independently or called in shell scripts to work with other neuroimaging tool synergistically.

.. nbgallery::

    notebooks/6_(Registration comparision)Volumetric_quantification
    notebooks/Nipype_interface_N4

Try your data
--------------------
Feel free to try your data or deploy BEN to your preprocessing pipeline. Details can be found in `notebook <https://colab.research.google.com/drive/1tfPfHg0Artjb2Ob8F_l9oOWb8u3y0lzi?usp=sharing>`_.
