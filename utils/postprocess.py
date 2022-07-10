# -*- coding: utf-8 -*-
"""
Remove false positive small regions in segmentation results.

"""
# from .utils_mri import *
import numpy as np
import os
from glob import glob
from skimage import measure
from utils.load_data import get_itk_array, get_itk_image, write_itk_imageArray


def remove_small_objects(input_path='/*', output_path=None, return_nii=True):
    """
    Remove small objects after lung prediction.
    :param input_path: The folder contains nii format files.
    :param output_path: If you only need to save postprocessed results, keep output_path = None
    :param return_nii: save to nii format.
    :return: None
    """
    niilabel_path = glob(input_path + '/*')
    niilabel_path.sort()

    if output_path is None:
        output_path = input_path
    else:
        if not os.path.exists(output_path):
            print('Makedir:\t', output_path)
            os.makedirs(output_path)
        print('Object will save in (Existing) folder/print(save_filename):\t', output_path)

    tag = 1
    for name in niilabel_path:
        nii = get_itk_array(name, False)
        print('matrix shape:\t', nii.shape)

        label_matrix = measure.label(nii, 8, return_num=True)

        connected_regions = []  # connected_regions
        for k in range(label_matrix[1]):
            connected_regions.append(np.array(label_matrix[0] == [k]).sum())

        connected_regions_sorted = sorted(range(len(connected_regions)),
                                          key=lambda k: connected_regions[k])
        connected_regions_sorted.reverse()

        for _tag, rank in enumerate(connected_regions_sorted):

            if _tag == 2 and connected_regions[rank] < connected_regions[connected_regions_sorted.index(1)] * 0.3:
                nii = nii * (1 - np.array(label_matrix[0] == [rank]))
            if _tag > 2:
                nii = nii * (1 - np.array(label_matrix[0] == [rank]))

        if return_nii:
            ref_nii = get_itk_image(name)
            output_name = output_path + '/' + name.split('\\')[-1]
            nii = nii.astype(float)
            write_itk_imageArray(nii, output_name, ref_nii)
            tag = tag + 1

        tag = tag + 1


remove_small_objects(input_path=r'G:\2020_01_17\G\gmycode\unet-BET_pm2.5\unet-github\data\rat\pred-Rat-42d-2022-%1-DA', output_path=r'G:\2020_01_17\G\gmycode\unet-BET_pm2.5\unet-github\data\rat\pred-Rat-42d-2022-%1-DA-post')
remove_small_objects(input_path=r'G:\2020_01_17\G\gmycode\unet-BET_pm2.5\unet-github\data\rat\pred-Rat-42d-2022-%1-ft', output_path=r'G:\2020_01_17\G\gmycode\unet-BET_pm2.5\unet-github\data\rat\pred-Rat-42d-2022-%1-ft-post')
