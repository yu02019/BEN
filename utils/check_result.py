"""
2022/11/13
Generate visual inspecion (png logs) with input Raw images, prediction, (postprocess prediction)

Other implementation:
visual inspection (generate video logs)
"""
import argparse
import os
import time
from glob import glob
from tqdm import tqdm
import SimpleITK as sitk
import matplotlib.pyplot as plt
from utils.load_data import get_itk_image, write_itk_image
import warnings
import numpy as np
import cv2
import pandas as pd

from collections import OrderedDict

''' Utils functions '''


def data_norm(volume):
    # normalize the intensity into [0, 255]
    volume = (volume - np.min(volume)) * 255 / (np.max(volume) - np.min(volume))
    return volume


def toRGB(volume):
    # transform the volume from 1 channel to 3 channels
    volume = volume.astype(np.uint8)
    volume = np.stack((volume,) * 3, axis=-1)
    ##############################################################
    # Note: Rotation here is only for the MSD. Revise it when it is needed.
    # volume shape: [X, Y, Channels, Z]
    volume = np.transpose(volume, (1, 0, 3, 2))[::-1, ::-1, ...]
    ##############################################################
    return volume


COLOR_LIST = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]


def assign_color(seg_volume):
    # assign the RGB for each organ based on predefined color (COLOR_LIST)
    for i in range(1, np.max(seg_volume) + 1):
        for j in range(3):
            seg_volume[:, :, j, :][seg_volume[:, :, j, :] == i] = COLOR_LIST[i - 1][j]

    return seg_volume


def combine_data_seg_v2(data_volume, seg_volume):
    # assign pre-defined color
    data_volume = data_norm(data_volume)
    data_volume = toRGB(data_volume)
    seg_volume = toRGB(seg_volume)
    seg_volume = assign_color(seg_volume)
    data_seg_volume = np.zeros(shape=data_volume.shape, dtype=np.uint8)
    for i in range(data_volume.shape[-1]):
        rate_for_image = 0.7
        data_seg_volume[..., i] = cv2.addWeighted(data_volume[..., i], rate_for_image,
                                                  seg_volume[..., i], 1 - rate_for_image, 0)

    return data_seg_volume


def plot_segmentation_montage(_raw, _pred, _raw_pred=None, color_map='gray', plot_num=9, save_name='test.png'):
    """
    2022/11/13 Reference: https://github.com/Robin970822/DABC-Net-for-COVID-19/blob/master/utils/visualization.py
    Displays the segmentation results (montage).
    Parameters
    ----------
    _raw: ndarray: shape like:(8, 512, 512) or list: [(8, 512, 512),(6, 512, 512)]
    _pred: segmentation results. Shape like:(8, 512, 512)
    _raw_pred: RGB image
    color_map:
    plot_num:
    """

    slice_id = np.linspace(0, _raw.shape[0] - 1, num=plot_num, endpoint=True)
    slice_id = slice_id.astype('int')
    slice_id = slice_id[1:-1]  # remove the first and last image.(usually background)

    _raw = _raw[slice_id]
    _pred = _pred[slice_id]

    _raw = _raw - np.min(_raw)
    _raw = _raw * 1.0 / np.max(_raw)

    row1 = np.column_stack(_raw)
    row2 = np.column_stack(_pred)
    canvas = np.vstack((row1, row2))

    # _raw_pred = _raw_pred[slice_id]
    # if _raw_pred.ndim == 4 and 3 in _raw_pred.shape:  # if is RGB image. todo: update
    #     row3 = np.transpose(_raw_pred, [0, 1, 3, 2])
    #     row3 = np.column_stack(row3)
    #     plt.imshow(row3, cmap=color_map);plt.show()

    # plt.imshow(canvas, cmap=color_map);
    # plt.show()
    plt.imsave(save_name, canvas, cmap='gray')

    return None


def make_result_to_logs(input_folder, predict_folder, species='rodent', orientation=None):
    """

    :param input_folder:
    :param predict_folder:
    :param species:
    :param orientation: When this parameter is set, the parameter 'species' is suppressed.
    :return:
    """
    if predict_folder is not None:
        if not os.path.exists(predict_folder):
            os.makedirs(predict_folder)
    if input_folder == predict_folder:
        warnings.warn('input_folder and predict_folder are consistent, input files will be overwritten!')
        input('Overwrite input files? Press any key to continue...')

    if orientation is not None:
        pass
    else:
        if species == 'rodents' or species == 'rodent':  # for rodents
            orientation = 'RIA'  # orient to RIA
        else:  # for NHPs
            orientation = 'RPI'

    logs_predict_folder = predict_folder + '/logs'
    if not os.path.exists(logs_predict_folder):
        os.makedirs(logs_predict_folder)

    print('-' * 40)
    print('========= Input folder\t=========\n{}'.format(input_folder))
    print('========= Predict folder\t=========\n{}'.format(predict_folder))
    print('========= Logs predict folder\t=========\n{}'.format(logs_predict_folder))
    print('========= Species\t=========\n{}'.format(species))
    print('========= New orientation\t=========\n{}'.format(orientation))
    # print('========= Mode\t=========\n{}, {}'.format(mode, mode_illustration))
    print('-' * 40)

    ''' Set information table '''
    seg_metrics = OrderedDict()
    seg_metrics['Name'] = list()
    seg_metrics['Path'] = list()
    seg_metrics['Raw Orientation'] = list()
    seg_metrics['Display Orientation'] = list()
    seg_metrics['Spacing'] = list()
    seg_metrics['Slice'] = list()
    seg_metrics['Shape'] = list()
    seg_metrics['Brain Volume (mm3)'] = list()

    ''' Start processing '''
    filenames = glob(os.path.join(input_folder, '*.nii*'))
    filenames = sorted(filenames)
    predict_filenames = glob(os.path.join(predict_folder, '*.nii*'))
    num_file = len(filenames)

    for i, filename in tqdm(enumerate(filenames)):
        basename = os.path.basename(filename)
        basename_wo_ext = basename[:basename.find('.nii')]
        print('Processing: ', basename_wo_ext)

        ''' Process '''
        # load file
        img = get_itk_image(filename)
        original_orientation = sitk.DICOMOrientImageFilter_GetOrientationFromDirectionCosines(
            img.GetDirection())  # e.g. 'LPS'
        # load prediction
        pred = get_itk_image(predict_filenames[i])

        # orient
        reoriented_img = sitk.DICOMOrient(img, orientation)
        reoriented_img_array = sitk.GetArrayFromImage(reoriented_img)
        reoriented_pred = sitk.DICOMOrient(pred, orientation)
        reoriented_pred_array = sitk.GetArrayFromImage(reoriented_pred)

        # # combine img and pred to one masked RGB image
        # reoriented_img_pred = combine_data_seg_v2(reoriented_img_array, reoriented_pred_array)
        # reoriented_img_pred = np.transpose(reoriented_img_pred, [1, 0, 2, 3])  # todo: update confused orientation

        ''' Visual inspection output and Save '''
        save_name = str(logs_predict_folder) + '/' + basename_wo_ext + ".png"
        plot_segmentation_montage(_raw=reoriented_img_array, _pred=reoriented_pred_array, save_name=save_name)

        ''' Add information table '''
        spacing = reoriented_img.GetSpacing()
        brain_volume = reoriented_pred_array.sum() * spacing[0] * spacing[1] * spacing[2]
        seg_metrics['Name'].append(basename)
        seg_metrics['Path'].append(filename)
        seg_metrics['Raw Orientation'].append(original_orientation)
        seg_metrics['Display Orientation'].append(orientation)
        seg_metrics['Spacing'].append(spacing)
        seg_metrics['Slice'].append(reoriented_img_array.shape[0])
        seg_metrics['Shape'].append(reoriented_img.GetSize())
        seg_metrics['Brain Volume (mm3)'].append(brain_volume)

    dataframe = pd.DataFrame(seg_metrics)
    dataframe.to_csv(logs_predict_folder + '/info.csv', index=False, mode='w')  # mode='a'

    print('\n**********\t', 'Logs have been saved', '\t**********\n')

    return logs_predict_folder

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest='input_folder', required=True, type=str, help="input image folder")
    parser.add_argument("-predict", dest='predict_folder', default=None, type=str, help="predict image folder")
    parser.add_argument("-s", dest='species', default='rodents', type=str, help="species of input images")
    parser.add_argument("-check", dest='check_orientation',
                        help="Check input orientation. None for skipping. 'RIA' for rodents and 'RPI' for NHPs")

    args = parser.parse_args()

    # Define variables
    input_folder = args.input_folder
    predict_folder = args.predict_folder
    species = args.species
    check_orientation = args.check_orientation

    make_result_to_logs(input_folder, predict_folder, species, check_orientation)
