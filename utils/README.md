

## Plug-and-play functions for pre-/post-processing

- [x] Orientation detection (**Note:** if you want to run MR scans on the original orientation, don't set "-check" parameter in commands)
- [x] Top-K largest connected region selection 
- [x] todo: update CRF before November 12th.

| Name                                                                     | File                                     | Description                                                                                                                                         | Update date |
|--------------------------------------------------------------------------|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| Orientation detection                                                    | load_data.py <br/>check_reorient_sitk.py | Check the orientation of input MR scans and automatically correct them during runtime. The output files will keep the original user's orientation.  | 2022/11     |
| remove_small_objects_v1                                                  | postprocess.py                           | Remove small objects after brain extraction.                                                                                                        | 2022/11     |
| remove_small_objects_v2 <br/> (Top-K largest connected region selection) | postprocess.py                           | Remove small objects after brain extraction.                                                                                                        | 2022/11     |
| Conditional Random Field (CRF)                                           | postprocess_crf.py                       | Optimize segmentation. (provide 2D and 3D version of CRF)                                                                                           | 2022/11     |

## Running log for quick inspection

- [x] todo: update before November 12th.

| Name                          | File                   | Description                                                                                                                                                                   | Update date |
|-------------------------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| Visual report (HTML + Images) | check_result.py        | Summary all outputs in figures or HTML format. It has been integrated into the BEN pipeline (BEN_infer.py), and can also run independently.                                   | 2022/11     |
| Visual report (Video)         | check_nii2video.py     | Summary all outputs in .mp4 format.                                                                                                                                           | 2022/11     |
| Check orientation             | check_reorient_sitk.py | Check the orientation of user's data. It has been integrated into the BEN pipeline (load_data.py), and can also run independently to reorient the orientation of user's data. | 2022/11     |
| Volumetric report (Table)     | check_result.py        | Report the brain volumes of segmentations in csv format tables.                                                                                                               | 2022/11     |


---
## Todo
(in the near feature plans)
1. -[ ] Add voxel size check and norm step in load_data.py
2. -[x] Update postprocess.py at slice-level. (refer to 'remove_small_objects_v2')
3. -[ ] Provide one super unified pretrained weight. In clinical practice, users usually didn't care about networks were pretrained on one or multiple source domains. 
Moreover, we do have multiple domain datasets.
Obviously, pretraining on multi-source domains will further improve the generalizability of the network.
4. -[ ] We are planning to create an open data and open-source web repository, ‘OpenBEN’, to share the data, computer codes and trained models, which will enable scientists everywhere to query and further improve automatic deployment of these datasets.
Currently, we can use Google Drive as an alternative for sharing such codes and data. We will also acknowledge any contribution to BEN!

