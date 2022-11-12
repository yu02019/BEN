

## Plug-and-play functions for pre-/post-processing

- [x] Orientation detection 
- [x] Top-K largest connected region selection 
- [x] todo: update CRF before November 12th.

| Name                                     | File               | Description                                                                                                                                        | Update date |
|------------------------------------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| Orientation detection                    | load_data.py       | Check the orientation of input MR scans and automatically correct them during runtime. The output files will keep the original user's orientation. | 2022/11     |
| Top-K largest connected region selection | postprocess.py     | Remove small objects after brain extraction.                                                                                                       | 2022/11     |
| Conditional Random Field (CRF)           | postprocess_crf.py | Optimize segmentation. (provide 2D and 3D version of CRF)                                                                                          | 2022/11     |

## Running log for quick inspection

- [ ] todo: update before November 12th.

| Name                      | File             | Description                                                                                                                                                                   | Update date |
|---------------------------|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| Visual report (tentative) | updating         | Summary all outputs in figures or HTML format. It has been integrated into the BEN pipeline (BEN_infer.py), and can also run independently.                                   | 2022/11     |
| Check orientation         | reorient_sitk.py | Check the orientation of user's data. It has been integrated into the BEN pipeline (load_data.py), and can also run independently to reorient the orientation of user's data. | 2022/11     |
| Volumetric report         | updating         | Report the brain volumes of segmentations in csv format tables.                                                                                                               | 2022/11     |



[//]: # (Todo: add voxel size check and norm step in load_data.py !)
