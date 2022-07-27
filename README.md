<div>
<img src="fig/logo.png" align="left" style="margin: 10 10 10 10;" height="150px">
	<h1>BEN</h1>
<blockquote> A generalized Brain Extraction Net for multimodal MRI data from rodents, nonhuman primates, and humans
</blockquote>
</div>
<br />

<hr />


### [Paper](https://www.biorxiv.org/content/10.1101/2022.05.25.492956v2.abstract) | [Feature](#feature) | [Replicate demo](#replicate-demo) | [MRI data release](/dataset_release) | [Pretrained weight](/dataset_release) | [Interface](/interface) | [Contributing to BEN](/dataset_release) | [Documentation](https://ben-docs.readthedocs.io/en/latest/)  | [Contents](#Quick-Start-Contents)


![](fig/BEN-workflow.png)

## Overview
🚀 Quick start to use BEN or replicate our experiments in 5 minutes!

### Feature


| Feature                       | Description                                                                                                                                                                                                           | Colab link                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|-------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Transferability & flexibility | BEN outperforms traditional SOTA methods and advantageously adapts to datasets from diverse domains across multiple species [1], modalities [2], and MR scanners with different field strengths [3].                  | [1] [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1qsBg-_6NxVFUJCk0tbTyQ7vY8_FLnrc9?usp=sharing)<br/> [2] [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/14NWqdbkpsdt0cS4-SLCvcDmHLU05UlmV?usp=sharing) <br/> [3] [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1xrREREKEs0HvDvhxA0sGCLsIdAFNLd2w?usp=sharing) |
| Quality assessment            | Unlike traditional toolboxes, which mainly rely on manual inspection to assess the brain extraction quality, BEN incorporates a quality assessment module to automatically evaluate its brain extraction performance. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1MMglzvMXC8YHI58vSQbi7VbHl5xsBpKN?usp=sharing)                                                                                                                                                                                                                                                                                                                                                                |
| Speed 🚀                      | Inference: Less than 1 sec/scan;<br/>Adaptation to a new imaging center/application: About 10 min for deployment.                                                                                                     | -                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |


### Replicate demo
 

| Name                                                    | Description                                                                                                                                                   | Related Fig.<br/> in paper | Snapshot                                                                                                  | Colab link                                                                                                                                                                                                                                                                                                                                                                                        |
|---------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|-----------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1. BEN workflow & architecture                          | BEN renovates the brain extraction workflow to adapt to multiple species, modalities and platforms                                                            | Fig. 1 & 2                 | <img src="./fig/BEN.png" width = "110" height = "120" alt="Snapshot on Win" align=center />               | This repository                                                                                                                                                                                                                                                                                                                                                                                   |
| 2. ✨ Cross species                                      | Deploying BEN to new species requires minimal or even no labels.                                                                                              | Fig. 3                     | <img src="./fig/cross-species-post.png" width = "150" height = "74" alt="Snapshot on Win" align=center /> | Cross species [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1qsBg-_6NxVFUJCk0tbTyQ7vY8_FLnrc9?usp=sharing)                                                                                                                                                                                                                 |
| 3. Cross modalities / MR scanners                       | Deploying BEN to new modalities/MR platforms requires minimal or even no labels.                                                                              | Fig. S1 & S2               | <img src="./fig/cross-field.png" width = "150" height = "74" alt="Snapshot on Win" align=center />        | Cross modalities [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/14NWqdbkpsdt0cS4-SLCvcDmHLU05UlmV?usp=sharing) <br/> Cross MR scanners [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1xrREREKEs0HvDvhxA0sGCLsIdAFNLd2w?usp=sharing)                  |
| 4. Compare with other toolbox                           | BEN outperforms traditional SOTA methods and advantageously adapts to datasets from various domains across multiple species, modalities, and field strengths. | Fig. 4                     | <img src="./fig/Fig4.png" width = "150" height = "74" alt="Snapshot on Win" align=center />               | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1HgHgqli-mVuIj9QolJ85KEB8LJcgN5qh?usp=sharing)                                                                                                                                                                                                                               |
| 5. Uncertainty & inter-rater variations                 | Compared to traditional toolboxes, BEN provides a measure of uncertainty that potentially reflects rater disagreement                                         | Fig. 5                     | <img src="./fig/Fig5.png" width = "150" height = "74" alt="Snapshot on Win" align=center />               | Disagree map [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1xPVzA_FrZN1pI3l7fFRBlCNsRAEwQ0gG?usp=sharing)<br/> Uncertainty [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1MMglzvMXC8YHI58vSQbi7VbHl5xsBpKN?usp=sharing)                             |
| 6. ✨ Volumetric quantification for longitudinal studies | BEN improves the accuracy of atlas registration and benefits brain volumetric quantification compared with using other toolbox.                               | Fig. 6 & 7                 | <img src="./fig/Fig7.png" width = "150" height = "44" alt="Snapshot on Win" align=center />               | Registration comparision [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1mnlBcRBxpLb2QbcVqQsU5p50fRaM5Ifq?usp=sharing)  <br/> Volumetric quantification [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/13oZcuAsJ4yQcZ5jGl5kYNV3DlW-eFgVB?usp=sharing) |




### MRI data release | pretrained weight

The details can be found in this [folder](/dataset_release).



---
## Quick Start Contents

Visit our [documentation](https://ben-docs.readthedocs.io/en/latest/) for installation, tutorials and more.

* [Installation](#installation)
* [Quick Start / Tutorial](#quick-start)
    + [Cross modalities](#cross-modality) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/14NWqdbkpsdt0cS4-SLCvcDmHLU05UlmV?usp=sharing)
    + [Cross MR scanner with different field strengths](#cross_MR_scanner_with_different_field_strengths) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1xrREREKEs0HvDvhxA0sGCLsIdAFNLd2w?usp=sharing)
    + [Cross species](#cross-species)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1qsBg-_6NxVFUJCk0tbTyQ7vY8_FLnrc9?usp=sharing)
    + [Try your data](#try-your-data)  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1tfPfHg0Artjb2Ob8F_l9oOWb8u3y0lzi?usp=sharing)
* [Resources](#resources)
  * [Interface for neruoimaging toolboxes](#interface-for-neruoimaging-toolboxes)
  * [Data release](/dataset_release)
  * [Pretained weight](/dataset_release)
  * [Contributing to BEN](/dataset_release)


## Installation

An Nvidia GPU is needed for faster inference (less than 1 sec/scan on 1080ti gpu).

Requirements:

* tensorflow-gpu == 1.15.4
* Keras == 2.2.4
* numpy == 1.16
* SimpleITK == 2.0
* opencv-python == 4.1
* scikit-image == 0.16.2

[//]: # (* matplotlib == 3.3.1)

Install dependencies:


```shell
git clone https://github.com/yu02019/BEN.git
cd BEN
pip install -r requirement.txt
```

The target domain data folder looks like this: (Download data from this repository/Colab or put your data here.)

<img src="./fig/folder_tree.png" width = "320" height = "230" alt="folder_tree" align=center/>

## Quick Start

* All the undermentioned results can be repeated via our tutorial Notebook.
* New weight will be saved independently for further customized application.

### Cross modalities

#### Results:

1. Modality: T2WI -> EPI
2. For this exemplar domain adaptation (DA) task, No label is used (zero-shot).
3. From top raw to the third raw: Raw image, Baseline result, BEN's result.

   ![Alt text](fig/cross-modality.png "fig.1")

### Cross MR scanner with different field strengths

1. MR scanner with different field strengths: 11.7 T -> 7 T
2. For this exemplar domain adaptation (DA) task, No label is used (zero-shot).
3. From top raw to the third raw: Raw image, Baseline result, BEN's result.

   ![](fig/cross-field.png)

### Cross species

1. Species: Mouse -> Rat
2. For this exemplar domain adaptation (DA) task, only ONE label is used.
3. The segmentation results are shown in red, the ground truth are shown in orange.
4. From top raw to the fifth raw: Raw image, Zero-shot (0 label used), finetune (1 label used), BEN's result (1 label
   used), Ground truth.

   ![](fig/cross-species.png)

5. (Optional) Just do some simple postprocessing here, e.g., only save the top-K largest connected regions.
6. Compared with other methods, it further shows BEN's advantages

   ![](fig/cross-species-post.png)

## Try your data

Feel free to try your data or deploy BEN to your preprocessing pipeline. Details can be found in [notebook](https://colab.research.google.com/drive/1tfPfHg0Artjb2Ob8F_l9oOWb8u3y0lzi?usp=sharing).

[//]: # (todo : add new demo usage here!)
```shell
python BEN_infer.py -i input_folder -o output_folder -m model_weight_path
```

# Resources

##  Interface for neruoimaging toolboxes

The usages and details can be found in this [folder](/interface).

| Name       | Link                             |
|------------|----------------------------------|
| AFNI       | afni.nimh.nih.gov/afni           |
| ANTs       | stnava.github.io/ANTs/           |
| FSL        | fsl.fmrib.ox.ac.uk/fsl/fslwiki   |
| FreeSurfer | freesurfer.net                   |
| SPM        | fil.ion.ucl.ac.uk/spm            |
| Nipype     | pypi.org/project/nipype/         |




## Data release / Pretrained weight / Contributing to BEN

The details can be found in this [folder](/dataset_release).



---



# Citation
If you find our work / datasets / pretrained models useful for your research, please consider citing:

```bibtex
@article{yu2022ben,
  title={BEN: a generalizable Brain Extraction Net for multimodal MRI data from rodents, nonhuman primates, and humans},
  author={Yu, Ziqi and Han, Xiaoyang and Xu, Wenjing and Zhang, Jie and Marr, Carsten and Shen, Dinggang and Peng, Tingying and Zhang, Xiao-Yong and Feng, Jianfeng},
  journal={bioRxiv},
  year={2022},
  publisher={Cold Spring Harbor Laboratory}
}
```

```bibtex
@dataset{yu_ziqi_2022_6844489,
  author       = {Yu Ziqi and
                  Wenjing Xu and
                  Xiao-Yong Zhang},
  title        = {{A longitudinal MRI dataset of young adult C57BL6J 
                   mouse brain}},
  month        = jul,
  year         = 2022,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.6844489},
  url          = {https://doi.org/10.5281/zenodo.6844489}
}
```


[//]: # (Acknowledgements: TODO)

Disclaimer: This toolkit is only for research purpose.

