.. role:: raw-html-m2r(raw)
   :format: html


API
===

Key function
------------

.. list-table::
   :header-rows: 1

   * - Function
     - Description
   * - utils.inference.inference_pipeline(input_folder, output_folder[,...])
     - Run BEN inference to all files in the folder.
   * - utils.update_model.update_weight(train_data, label_data[,...])
     - Update model weight using training data.


Utils
-----

.. list-table::
   :header-rows: 1

   * - Function
     - Description
   * - utils.load_data.get_itk_array(filenameOrImage, normalize)
     - Get an image array given an image filename of extension *TIFF, JPEG, PNG, BMP, DICOM, GIPL, Bio-Rad, LSM, Nifti, Analyze, SDT/SPR (Stimulate), Nrrd or VTK images*.
   * - utils.load_data.write_itk_imageArray(imageArray, filename[,...])
     - Write a numpy array to a specified filename.
   * - utils.load_data.read_from_nii(nii_path[,...])
     - Read nii/nii.gz files in specified folder.


Postprocess
-----------

.. list-table::
   :header-rows: 1

   * - Function
     - Description
   * - utils.postprocess.remove_small_objects
     - Only save the top-K largest connected regions.


Model
-----

.. list-table::
   :header-rows: 1

   * - Function
     - Description
   * - model.backbone_network(IMG_WIDTH, IMG_HEIGHT[,...])
     - Define the backbone model.
   * - model.non_local.non_local_block(input_tensor[,...])
     - Adds a Non-Local block for self attention to the input tensor.


:raw-html-m2r:`<a href="#" title="|          |             |">//</a>`\ : # ()
