import os

import numpy as np
from glob import glob
from utils.load_data import get_itk_array
from utils.transparent_imshow import transp_imshow
import matplotlib.pyplot as plt


def load_slice_cross_species(raw_path='', zeroshot_path='', ft_path='', DA_path='', gt_path='',
                             scans_num=0, disp_num=6):
    """

    :param raw_path:
    :param zeroshot_path:
    :param ft_path:
    :param DA_path:
    :param gt_path:
    :param scans_num:
    :param disp_num:
    :return:
    """
    os.chdir(r'G:\\2020_01_17\\G\\gmycode\\unet-BET_pm2.5\\unet-github')  # for debug only
    raw = glob(raw_path + '/*');
    raw.sort()
    zeroshot = glob(zeroshot_path + '/*');
    zeroshot.sort()
    ft = glob(ft_path + '/*');
    ft.sort()
    DA = glob(DA_path + '/*');
    DA.sort()
    gt = glob(gt_path + '/*');
    gt.sort()

    raw = get_itk_array(raw[scans_num])
    zeroshot = get_itk_array(zeroshot[scans_num])
    ft = get_itk_array(ft[scans_num])
    DA = get_itk_array(DA[scans_num])
    gt = get_itk_array(gt[scans_num])

    disp_num_list = list(range(0, raw.shape[0], raw.shape[0] // (disp_num)))

    # extract slices
    raw = raw[disp_num_list]
    zeroshot = zeroshot[disp_num_list]
    ft = ft[disp_num_list]
    DA = DA[disp_num_list]
    gt = gt[disp_num_list]

    return raw, zeroshot, ft, DA, gt


def load_slice(raw_path='', zeroshot_path='', DA_path='', scans_num=0, disp_num=6):
    """

    :param raw_path:
    :param zeroshot_path:
    :param DA_path:
    :param scans_num:
    :param disp_num:
    :return:
    """
    os.chdir(r'G:\\2020_01_17\\G\\gmycode\\unet-BET_pm2.5\\unet-github')  # for debug only
    raw = glob(raw_path + '/*');
    raw.sort()
    zeroshot = glob(zeroshot_path + '/*');
    zeroshot.sort()
    DA = glob(DA_path + '/*');
    DA.sort()

    raw = get_itk_array(raw[scans_num])
    zeroshot = get_itk_array(zeroshot[scans_num])
    DA = get_itk_array(DA[scans_num])

    disp_num_list = list(range(0, raw.shape[0], raw.shape[0] // (disp_num)))

    # extract slices
    raw = raw[disp_num_list]
    zeroshot = zeroshot[disp_num_list]
    DA = DA[disp_num_list]

    return raw, zeroshot, DA


def plot_segmentation_cross_species(raw, zeroshot, ft, DA, gt, task, hspace=-0.6):
    """

    :param raw:
    :param zeroshot:
    :param ft:
    :param DA:
    :param gt:
    :param task:
    :param hspace: float, optional. The height of the padding between subplots, as a fraction of the average axes height.
    :return:
    """

    fig = plt.figure(
        # figsize=(16, 9)
    )

    timepoint_count = raw.shape[0]

    for i in range(timepoint_count):
        plt.subplot(5, timepoint_count, i + 1)
        plt.imshow(raw[i], cmap='gray')
        # plt.title('No.{} scan\n'.format(i + 1), fontsize=8)
        plt.xticks([]), plt.yticks([])

    for i in range(timepoint_count):
        plt.subplot(5, timepoint_count, timepoint_count + i + 1)
        plt.imshow(raw[i], cmap='gray')
        transp_imshow(zeroshot[i], cmap='Reds', alpha=0.6)
        # plt.title('No.{} scan lung\n'.format(i + 1), fontsize=8)
        plt.xticks([]), plt.yticks([])

    for i in range(timepoint_count):
        plt.subplot(5, timepoint_count, timepoint_count * 2 + i + 1)
        plt.imshow(raw[i], cmap='gray')
        transp_imshow(ft[i], cmap='Reds', alpha=0.6)
        # plt.title('No.{} scan lung\n'.format(i + 1), fontsize=16)
        plt.xticks([]), plt.yticks([])

    for i in range(timepoint_count):
        plt.subplot(5, timepoint_count, timepoint_count * 3 + i + 1)
        plt.imshow(raw[i], cmap='gray')
        transp_imshow(DA[i], cmap='Reds', alpha=0.6)
        # plt.title('No.{} scan lesion\n'.format(i + 1), fontsize=16)
        plt.xticks([]), plt.yticks([])

    # gt
    for i in range(timepoint_count):
        plt.subplot(5, timepoint_count, timepoint_count * 4 + i + 1)
        plt.imshow(raw[i], cmap='gray')
        transp_imshow(gt[i], cmap='Oranges', alpha=0.6)
        # plt.title('No.{} scan lesion\n'.format(i + 1), fontsize=16)
        plt.xticks([]), plt.yticks([])

    plt.subplots_adjust(hspace=hspace, wspace=0.0)
    # plt.tight_layout()
    fig.suptitle('Plot of different methods on cross-{} task'.format(task), fontsize=14)
    plt.savefig('result.png', dpi=300)
    plt.show()


def plot_segmentation(raw, zeroshot, DA, task, hspace=-0.7):
    """
    Each 'methods' need a set of slices for plot
    Displays the segmentation results.
    Parameters
    ----------
    raw:
    lung: green
    lesion: red (color_map)
    color_map:
    task:
    hspace: float, optional. The height of the padding between subplots, as a fraction of the average axes height.
    """
    fig = plt.figure(
        # figsize=(8, 4)
    )

    timepoint_count = raw.shape[0]

    for i in range(timepoint_count):
        plt.subplot(3, timepoint_count, i + 1)
        plt.imshow(raw[i], cmap='gray')
        # plt.title('No.{} scan\n'.format(i + 1), fontsize=8)
        plt.xticks([]), plt.yticks([])

    for i in range(timepoint_count):
        plt.subplot(3, timepoint_count, timepoint_count + i + 1)
        plt.imshow(raw[i], cmap='gray')
        transp_imshow(zeroshot[i], cmap='Reds', alpha=0.6)
        # plt.title('No.{} scan lung\n'.format(i + 1), fontsize=8)
        plt.xticks([]), plt.yticks([])

    for i in range(timepoint_count):
        plt.subplot(3, timepoint_count, timepoint_count * 2 + i + 1)
        plt.imshow(raw[i], cmap='gray')
        transp_imshow(DA[i], cmap='Reds', alpha=0.6)
        # plt.title('No.{} scan lesion\n'.format(i + 1), fontsize=16)
        plt.xticks([]), plt.yticks([])

    plt.subplots_adjust(hspace=hspace, wspace=0.0)
    # plt.tight_layout()
    fig.suptitle('Plot of different methods on cross-{} task'.format(task), fontsize=14)
    # plt.savefig('result.png', dpi=300)
    plt.show()


if __name__ == '__main__':
    ''' cross species '''
    # raw, zeroshot, ft, DA, gt = load_slice_cross_species(raw_path=r'cross_domain\rat\src',
    #                                                      zeroshot_path=r'cross_domain\\rat\\pred-Rat-42d-2022-%0-ft',
    #                                                      ft_path=r'cross_domain\\rat\\pred-Rat-42d-2022-%1-ft',
    #                                                      DA_path=r'cross_domain\\rat\\pred-Rat-42d-2022-%1-DA',
    #                                                      gt_path=r'cross_domain\\rat\\gt', scans_num=2)
    # plot_segmentation_cross_species(raw, zeroshot, ft, DA, gt, task='species')

    ''' cross species - postprocessing'''
    # raw, zeroshot, ft, DA, gt = load_slice_cross_species(raw_path=r'cross_domain\rat\src',
    #                                                      zeroshot_path=r'cross_domain\\rat\\pred-Rat-42d-2022-%0-ft',
    #                                                      ft_path=r'cross_domain\\rat\\pred-Rat-42d-2022-%1-ft-post',
    #                                                      DA_path=r'cross_domain\\rat\\pred-Rat-42d-2022-%1-DA-post',
    #                                                      gt_path=r'cross_domain\\rat\\gt', scans_num=2)
    # plot_segmentation_cross_species(raw, zeroshot, ft, DA, gt, task='species')

    ''' cross modality / field strengh '''
    # raw, zeroshot, DA = load_slice(raw_path=r'cross_domain\epi\src',
    #                                zeroshot_path=r'cross_domain\\epi\\pred-zeroshot',
    #                                DA_path=r'cross_domain\\epi\\pred-02162151',
    #                                scans_num=1)
    # plot_segmentation(raw, zeroshot, DA, task='modality', hspace=-0.7)
    #
    # raw, zeroshot, DA = load_slice(raw_path=r'cross_domain\7T\src',
    #                                zeroshot_path=r'cross_domain\\7T\\pred-zeroshot',
    #                                DA_path=r'cross_domain\\7T\\pred-02162151',
    #                                scans_num=1)
    # plot_segmentation(raw, zeroshot, DA, task='field strength', )
