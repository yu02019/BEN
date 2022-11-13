

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

- [x] todo: update before November 12th.

| Name                          | File                   | Description                                                                                                                                                                   | Update date |
|-------------------------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| Visual report (HTML + Images) | check_result.py        | Summary all outputs in figures or HTML format. It has been integrated into the BEN pipeline (BEN_infer.py), and can also run independently.                                   | 2022/11     |
| Visual report (Video)         | check_nii2video.py     | Summary all outputs in .mp4 format.                                                                                                                                           |             |
| Check orientation             | check_reorient_sitk.py | Check the orientation of user's data. It has been integrated into the BEN pipeline (load_data.py), and can also run independently to reorient the orientation of user's data. | 2022/11     |
| Volumetric report (Table)     | check_result.py        | Report the brain volumes of segmentations in csv format tables.                                                                                                               | 2022/11     |


---
## Todo
(in the near feature plans)
1. -[ ] Add voxel size check and norm step in load_data.py
2. -[ ] Update postprocess.py at slice-level.
