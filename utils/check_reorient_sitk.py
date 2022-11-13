"""
2022/10
Reorient and check MR images
2022/11/06 (find bug when processing 4D array)
todo: sitk.DICOMOrient doesn't support 4D array (e.g., fMRI, ASL) currently. To address 4D array:
1. If you want to reorient these 4D data, please use functions provided by FSL, AFNI to reorient them first
2. If you don't need reorientation, just use BEN with parameter [modality='epi'] for all 4D arrays.
"""
import argparse
import os
from glob import glob
from tqdm import tqdm
import SimpleITK as sitk
import matplotlib.pyplot as plt
from utils.load_data import get_itk_image, write_itk_image
import warnings


def visual_inspection_orientation(_img, _reoriented_img, _orientation, _original_orientation):
    """
        Visual inspection output. Results will be saved as 'png'.
    The output image view is the same as the network input view. Please check if the network is given the correct view.
    :param _img:
    :param _reoriented_img:
    :return: None
    """
    img_data = sitk.GetArrayFromImage(_img)
    reoriented_img_data = sitk.GetArrayFromImage(_reoriented_img)

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.suptitle('{} @ Slice: {}/{} \nRaw orientation: {}\nNew orientation: {}'.format(basename, img_data.shape[0] // 2,
                                                                                       img_data.shape[0],
                                                                                       _original_orientation,
                                                                                       _orientation), fontsize=16)

    plt.imshow(img_data[img_data.shape[0] // 2], cmap='gray'), plt.title('Before')
    plt.subplot(1, 2, 2)
    plt.imshow(reoriented_img_data[reoriented_img_data.shape[0] // 2], cmap='gray'), plt.title('After / Network input')
    plt.tight_layout()
    plt.savefig(os.path.join(args.logs_output_folder, basename_wo_ext + '.png'))

    # plt.show()  # for debug only

    return None


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest='input_folder', required=True, type=str, help="input image folder")
    parser.add_argument("-o", dest='output_folder', default=None, type=str, help="output image folder")
    parser.add_argument("-s", dest='species', default='rodents', type=str, help="species of input images")
    parser.add_argument("-mode", dest='mode', default=0, type=int,
                        help="0-Only do visual inspection; 1-Only do orientation; 2:Do both")
    args = parser.parse_args()

    if args.output_folder is not None:
        if not os.path.exists(args.output_folder):
            os.makedirs(args.output_folder)
    if args.input_folder == args.output_folder:
        warnings.warn('input_folder and output_folder are consistent, input files will be overwritten!')
        input('Overwrite input files? Press any key to continue...')

    if args.species == 'rodents' or args.species == 'rodent':  # for rodents
        orientation = 'RIA'  # orient to RIA
    else:  # for NHPs
        orientation = 'RPI'

    if args.mode == 2:
        mode_illustration = 'Do both orientation and visual inspection'
        assert args.output_folder is not None  # please provide output_folder
    elif args.mode == 1:
        mode_illustration = 'Only do orientation'
        assert args.output_folder is not None  # please provide output_folder
    elif args.mode == 0:
        mode_illustration = 'Only do visual inspection'
        args.output_folder = args.input_folder
    else:
        input('Please check the mode code!')
        mode_illustration = 'Wrong mode code'

    args.logs_output_folder = args.output_folder + '/logs'
    if not os.path.exists(args.logs_output_folder):
        os.makedirs(args.logs_output_folder)

    print('-' * 40)
    print('========= Input folder\t=========\n{}'.format(args.input_folder))
    print('========= Output folder\t=========\n{}'.format(args.output_folder))
    print('========= Logs output folder\t=========\n{}'.format(args.logs_output_folder))
    print('========= Species\t=========\n{}'.format(args.species))
    print('========= New orientation\t=========\n{}'.format(orientation))
    print('========= Mode\t=========\n{}, {}'.format(args.mode, mode_illustration))
    print('-' * 40)

    filenames = glob(os.path.join(args.input_folder, '*.nii*'))
    filenames = sorted(filenames)
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
        # orient
        reoriented_img = sitk.DICOMOrient(img, orientation)
        # write file
        if args.mode == 1 or args.mode == 2:  # do orientation
            # test start
            # from myutils.read_all_data_from_nii_pipe import get_itk_array
            # img_data = get_itk_array(filename)

            # test end
            write_itk_image(reoriented_img, os.path.join(args.output_folder, basename))

        ''' Visual inspection output '''
        if args.mode != 1:  # do visual inspection
            visual_inspection_orientation(img, reoriented_img, orientation, original_orientation)
