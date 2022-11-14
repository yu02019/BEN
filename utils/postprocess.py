# -*- coding: utf-8 -*-
"""
Remove false positive small regions in segmentation results.

"""
import os
import cv2
import numpy as np
from glob import glob
from skimage import measure
from utils.load_data import get_itk_array, get_itk_image, write_itk_imageArray


def remove_small_objects_v1(input_path='/*', output_path=None, return_nii=True):
    """
    (Revised from https://github.com/Robin970822/DABC-Net-for-COVID-19 )
    Remove small objects after lung prediction. (3D volume-level)
    :param input_path: The folder contains nii format files.
    :param output_path: If you only need to save postprocessed results, keep output_path = None
    :param return_nii: save to nii format.
    :return: None
    """
    niilabel_path = glob(input_path + '/*nii*')
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

        label_matrix = measure.label(nii, 8, return_num=True)  # version:0.16.2

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
            output_name = output_path + '/' + os.path.basename(
                name)  # Note: Windows: name.split('\\')[-1]; Linux: name.split('/')[-1]
            nii = nii.astype(float)
            write_itk_imageArray(nii, output_name, ref_nii)
            tag = tag + 1

        tag = tag + 1


def remove_small_objects_v2(input_path='/*', output_path=None, return_nii=True):
    """
    Top-K largest connected region selection (slice-level)

    Limitation: Some False-Positive regions (skull) are connected to the brain.
    Therefore, they are regarded as ONE connected region and cannot be removed correctly.
    Maybe it is better to add a priori knowledge constraint on this step.
    :param input_path:
    :param output_path:
    :param return_nii:
    :return:
    """
    niilabel_path = glob(input_path + '/*nii*')
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
        nii = get_itk_array(name, False, orientation='RIA')
        print('matrix shape:\t', nii.shape)

        slice_num = nii.shape[0]
        nii_post = np.zeros_like(nii)
        for slice_id in range(slice_num):
            nii_post[slice_id] = find_max_region(nii[slice_id])

        if return_nii:
            ref_nii = get_itk_image(name)
            output_name = output_path + '/' + os.path.basename(
                name)  # Note: Windows: name.split('\\')[-1]; Linux: name.split('/')[-1]
            nii_post = nii_post.astype(float)
            write_itk_imageArray(nii_post, output_name, ref_nii, orientation='RIA')
            tag = tag + 1
        tag = tag + 1


def find_max_region(mask_sel):
    mask_sel = mask_sel.astype(np.uint8)
    # __, contours, hierarchy = cv2.findContours(mask_sel, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # old cv2 version
    contours, hierarchy = cv2.findContours(mask_sel, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if contours == []:
        return np.zeros_like(mask_sel)

    # Find the largest area/region and fill it
    area = []

    for j in range(len(contours)):
        area.append(cv2.contourArea(contours[j]))

    max_idx = np.argmax(area)

    max_area = cv2.contourArea(contours[max_idx])

    for k in range(len(contours)):

        if k != max_idx:
            cv2.fillPoly(mask_sel, [contours[k]], 0)
    return mask_sel


if __name__ == '__main__':
    # remove_small_objects_v1(input_path=r'cross_domain/rat/pred-Rat-42d-2022-%1-DA', output_path=r'cross_domain/rat/pred-Rat-42d-2022-%1-DA-post')
    # remove_small_objects_v1(input_path=r'cross_domain/rat/pred-Rat-42d-2022-%1-ft', output_path=r'cross_domain/rat/pred-Rat-42d-2022-%1-ft-post')
    # remove_small_objects_v1(
    #     input_path=r'E:\New\Data_repo\doi_10.5061_dryad.1vhhmgqv8__v2\dataset\pred-DA_pipe_30epoch_11141008',
    #     output_path=r'E:\New\Data_repo\doi_10.5061_dryad.1vhhmgqv8__v2\dataset\pred-topK')
    pass
