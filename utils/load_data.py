'''
load nii cross_domain
'''
import os
import cv2
import numpy as np
from glob import glob
import SimpleITK as itk
import matplotlib.pyplot as plt
import warnings

# from skimage.transform import resize
# from scipy.misc.pilutil import imresize


def get_itk_image(filename):
    ''' Get an itk image given an image filename of extionsion *TIFF, JPEG,
    PNG, BMP, DICOM, GIPL, Bio-Rad, LSM, Nifti, Analyze, SDT/SPR (Stimulate),
    Nrrd or VTK images*.'''

    reader = itk.ImageFileReader()
    reader.SetFileName(filename)

    image = reader.Execute()

    return image


def get_itk_array(filenameOrImage, normalize=False):
    ''' Get an image array given an image filename of extension *TIFF, JPEG,
    PNG, BMP, DICOM, GIPL, Bio-Rad, LSM, Nifti, Analyze, SDT/SPR (Stimulate),
    Nrrd or VTK images*.'''

    if isinstance(filenameOrImage, str):
        image = get_itk_image(filenameOrImage)
    else:
        image = filenameOrImage

    imageArray = itk.GetArrayFromImage(image)
    if normalize:
        imageArray = imageArray - np.min(imageArray)
        imageArray = imageArray * 1.0 / np.max(imageArray)

    return imageArray


def make_itk_image(imageArray, protoImage=None):
    ''' Create an itk image given an image numpy ndarray (imageArray) and an
    itk proto-image (protoImage) to provide Origin, Spacing and Direction.'''

    image = itk.GetImageFromArray(imageArray)
    if protoImage != None:
        image.CopyInformation(protoImage)

    return image


def write_itk_image(image, filename):
    ''' Write an itk image to a specified filename.'''

    writer = itk.ImageFileWriter()
    writer.SetFileName(filename)

    if filename.endswith('.nii'):
        Warning('You are converting nii, be careful with type conversions')

    writer.Execute(image)

    return


def write_itk_imageArray(imageArray, filename, src_nii=None):
    img = make_itk_image(imageArray, src_nii)
    write_itk_image(img, filename)


def read_from_nii(nii_path=r'E:\data\src/*', need_rotate=True,
                  need_resize=256, Hu_window=(-1000, 512), modality=None, max_num=-1, keyword=None, check_orientation=None):
    '''
    read nii/nii.gz files in one folder
    :param nii_path: path of folder
    :param need_rotate: dependent on
    :param need_resize:
    :param Hu_window:
    :param modality:
    :param max_num:
    :param keyword:
    :param check_orientation:

    :return:
    '''

    nii_path = [_nii_path for _nii_path in glob(nii_path) if _nii_path.endswith('nii') or _nii_path.endswith('nii.gz')]
    if keyword != None:
        nii_path = [i for i in nii_path if keyword in i]

    nii_path.sort()
    print('Finding ', len(nii_path), ' nii.gz format files.\t')
    tag = 1
    total_list = []
    shape_list = []

    for name in nii_path:
        if check_orientation is None:
            nii = get_itk_array(name, False)
        elif check_orientation == 'RIA':
            nii = get_itk_image(name)
            nii = itk.DICOMOrient(nii, 'RIA')
            nii = itk.GetArrayFromImage(nii)
        elif check_orientation == 'RPI':
            nii = get_itk_image(name)
            nii = itk.DICOMOrient(nii, 'RPI')
            nii = itk.GetArrayFromImage(nii)


        '''
        add shape to list
        '''
        if modality == 'epi':
            if nii.ndim == 4:  # check ndim
                if nii.shape[0] >= 4:  # check timepoint
                    nii = nii[4]  # default: 4th timepoint (However, some fMRI only have 2 timepoints)
                else:
                    nii = nii[-1]  # if length < 4, select the last timepoint
            else:
                warnings.warn('the ndim of EPI/fMRI nii data is {}. Please check data!'.format(nii.ndim))

        elif nii.ndim >= 4:
            raise Exception("Please check the modality of your data.")

        shape_list.append(nii.shape)

        print('Reading:\t', name.split('/')[-1])  # e.g. (301, 512, 512)
        print(nii.shape)

        if Hu_window == 'auto':
            Hu_max = np.percentile(nii, 99)  # 1-99%
            Hu_min = np.percentile(nii, 1)
        elif type(Hu_window).__name__ == 'tuple':
            Hu_min = Hu_window[0]
            Hu_max = Hu_window[1]
        else:
            input('Please check Hu_window parameter!')
        nii[nii < Hu_min] = Hu_min
        nii[nii > Hu_max] = Hu_max

        # normalise to 0-1
        nii = nii - np.min(nii)
        nii = nii * 1.0 / np.max(nii)
        # print(np.max(nii))  # norm to 0~1
        # print(np.min(nii))

        # 05/07 for public cross_domain which have shape like (42,512,512,3), e.g. from Cell
        if len(nii.shape) >= 4:
            nii = nii[:, :, :, 0]

        '''
        rotate and resize
        '''
        slices = nii.shape[0]
        if need_rotate:
            for i in range(slices):
                nii[i, :, :] = np.flip(nii[i, :, :])
                nii[i, :, :] = np.flip(nii[i, :, :], axis=1)  # rotate 180

        if need_resize:
            total_data = np.zeros((slices, need_resize, need_resize))  # init
            for i in range(slices):
                total_data[i] = cv2.resize(nii[i], (need_resize, need_resize))
        else:
            total_data = nii

        tag = tag + 1
        total_list.append(total_data)
        if tag > max_num and max_num != -1:  # max num nii to read
            break

    total = total_list.pop(0)  # init
    for i in total_list:
        total = np.concatenate((total, i), 0)

    total_all = total
    if np.max(total_all) > 1:
        # normalise to 0-1
        total_all = total_all - np.min(total_all)
        total_all = total_all * 1.0 / np.max(total_all)

    print('Done.')

    if modality == 'epi':
        return total_all, shape_list

    return total_all


def read_from_nii_label(nii_path=r'E:\Lung\covid_data0424\label_V2_lung/*', need_rotate=True,
                        need_resize=256, interest_label=1, max_num=-1, keyword=None, check_orientation=None):
    '''

    :param nii_path:
    :param need_rotate:
    :param need_resize:
    :param interest_label:
    :param max_num:
    :param keyword:
    :param check_orientation:

    :return:

    '''

    nii_path = [_nii_path for _nii_path in glob(nii_path) if _nii_path.endswith('nii') or _nii_path.endswith('nii.gz')]

    if keyword != None:
        nii_path = [i for i in nii_path if keyword in i]

    nii_path.sort()
    print('len of nii_path:\t', len(nii_path))
    tag = 1
    total_list = []

    for name in nii_path:
        if check_orientation is None:
            nii = get_itk_array(name, False)
        elif check_orientation == 'RIA':
            nii = get_itk_image(name)
            nii = itk.DICOMOrient(nii, 'RIA')
            nii = itk.GetArrayFromImage(nii)
        elif check_orientation == 'RPI':
            nii = get_itk_image(name)
            nii = itk.DICOMOrient(nii, 'RPI')
            nii = itk.GetArrayFromImage(nii)

        print('Reading:\t', name.split('/')[-1])  # e.g. (301, 512, 512)
        print(nii.shape)

        nii[nii != interest_label] = 0  # interest label
        nii[nii == interest_label] = 1

        slices = nii.shape[0]
        if need_rotate:
            for i in range(slices):
                nii[i, :, :] = np.flip(nii[i, :, :])
                nii[i, :, :] = np.flip(nii[i, :, :], axis=1)  # rotate 180

        if need_resize:
            total_data = np.zeros((slices, need_resize, need_resize))  # init
            for i in range(slices):
                total_data[i] = cv2.resize(nii[i], (need_resize, need_resize))  # 512*512 / 256*256
        else:
            total_data = nii

        tag = tag + 1
        total_list.append(total_data)
        if tag > max_num and max_num != -1:  # max num nii to read
            break

    total = total_list.pop(0)  # init
    for i in total_list:
        total = np.concatenate((total, i), 0)

    total_all = total
    if np.max(total_all) > 1:
        print('sacle of nii is changed after imresize!\n Now, normlise:')
        # for label:
        total_all[total_all < 128] = 0
        total_all[total_all >= 128] = 1

        # normalise to 0-1
        total_all = total_all - np.min(total_all)
        total_all = total_all * 1.0 / np.max(total_all)

    print('Done.')

    return total_all


def save_pred_to_nii(pred=None, save_path=r'E:\Lung\covid_data0424\label_V1pred/',ref_path=r'E:\Lung\covid_data0424\src/*',
                     need_rotate=True, need_resize=True, need_threshold=True, shape_list=None, keyword=None, check_orientation=None):
    '''
    :param pred:
    :param save_path:
    :param ref_path:
    :param need_rotate:
    :param need_resize:
    :param need_threshold:
    :param shape_list:
    :param keyword:
    :param check_orientation
    :return:
    '''
    nii_path = [_nii_path for _nii_path in glob(ref_path) if _nii_path.endswith('nii') or _nii_path.endswith('nii.gz')]
    if keyword != None:
        nii_path = [i for i in nii_path if keyword in i]

    nii_path.sort()
    print('\n**********\t', len(nii_path), 'file(s) to save:', '\t**********\n')

    tag = 0

    for index, name in enumerate(nii_path):

        if shape_list:
            nii_shape = shape_list[index]
            slices = nii_shape[0]
            matrix = nii_shape[1:]
        else:
            nii_ref = get_itk_image(name)
            original_orientation = itk.DICOMOrientImageFilter_GetOrientationFromDirectionCosines(nii_ref.GetDirection())  # e.g. 'LPS'
            if check_orientation is None:
                nii_matrix = get_itk_array(name)
            elif check_orientation == 'RIA':
                nii_ref_reorient = itk.DICOMOrient(nii_ref, 'RIA')
                nii_matrix = itk.GetArrayFromImage(nii_ref_reorient)
            elif check_orientation == 'RPI':
                nii_ref_reorient = itk.DICOMOrient(nii_ref, 'RPI')
                nii_matrix = itk.GetArrayFromImage(nii_ref_reorient)
            slices = nii_matrix.shape[0]
            matrix = nii_matrix.shape[1:3]

        # 05/04
        if tag + slices > pred.shape[0]:
            cut = tag + slices - pred.shape[0]
            H = pred.shape[1]  # 256
            W = pred.shape[2]  # 256
            temp = np.zeros((cut, H, W))
            pred = np.concatenate((pred, temp), 0)

        nii_one = pred[tag:tag + slices]

        if need_rotate:
            for i in range(slices):
                nii_one[i, :, :] = np.flip(nii_one[i, :, :])
                nii_one[i, :, :] = np.flip(nii_one[i, :, :], axis=1)

        if need_resize:
            total_data = np.zeros((slices, matrix[0], matrix[1]))  # init
            for i in range(slices):
                total_data[i] = cv2.resize(nii_one[i], (matrix[1], matrix[0]), interpolation=cv2.INTER_NEAREST)

        else:
            total_data = nii_one

        if need_threshold:
            if total_data.max() >= 200:
                retVal, total_data = cv2.threshold(total_data, thresh=0.5, maxval=256, type=cv2.THRESH_BINARY)
            elif total_data.max() <= 1.0001:
                retVal, total_data = cv2.threshold(total_data, thresh=0.5, maxval=1, type=cv2.THRESH_BINARY)
            else:
                input('Please check the results! \n total_data.max():', total_data.max())

        print('Saving:\t', total_data.shape)  # save each one nii
        if '\\' in save_path:  # if using Windows：
            if shape_list:
                write_itk_imageArray(total_data, save_path + os.path.split(name)[-1],
                                     src_nii=None)  # Windows : '\\', ( or '/', easily confusable when using Linux PC）
            else:
                if check_orientation is None:
                    write_itk_imageArray(total_data, save_path + os.path.split(name)[-1], nii_ref)  # Windows : '\\', ( or '/', easily confusable when using Linux PC）
                else:
                    new_nii = itk.GetImageFromArray(total_data)
                    new_nii.SetDirection(nii_ref_reorient.GetDirection())
                    new_nii_to_Original_orientation = itk.DICOMOrient(new_nii, original_orientation)
                    write_itk_image(new_nii_to_Original_orientation, save_path + os.path.split(name)[-1])


        else:
            if shape_list:
                write_itk_imageArray(total_data, save_path + os.path.split(name)[-1],
                                     src_nii=None)
            else:
                if check_orientation is None:
                    write_itk_imageArray(total_data, save_path + name.split('/')[-1], nii_ref)
                else:
                    new_nii = itk.GetImageFromArray(total_data)
                    new_nii.SetDirection(nii_ref_reorient.GetDirection())
                    new_nii_to_Original_orientation = itk.DICOMOrient(new_nii, original_orientation)
                    write_itk_image(new_nii_to_Original_orientation, save_path + os.path.split(name)[-1])

        tag = tag + slices

    print('\n**********\t', 'Done.', '\t**********\n')
    return None


def save_matrix_to_nii(pred=None, save_path=r'E:\Lung\covid_data0424\label_V1pred/',
                       ref_path=r'E:\Lung\covid_data0424\src/*',
                       need_rotate=True, need_resize=True, need_threshold=True, meta=None):
    '''
    :param pred:
    :param save_path:
    :param ref_path:
    :param need_rotate:
    :param need_resize:
    :param need_threshold:
    :param meta:
    :return:
    '''

    meta_thin = meta[meta['slice'] > 300]  # select thin scans

    tag = 0  # current slice
    for index, row in meta_thin.iterrows():
        filename = row['filename']
        filename = os.path.basename(filename)
        slices = row['slice']
        origin_shape = eval(row['shape'])  # e.g. (382, 512, 512)
        matrix = origin_shape[1:]

        nii_one = pred[tag:tag + slices]

        if need_rotate:
            for i in range(slices):
                nii_one[i, :, :] = np.flip(nii_one[i, :, :])
                nii_one[i, :, :] = np.flip(nii_one[i, :, :], axis=1)  #

        if need_resize:
            total_temp = np.zeros((slices, matrix[0], matrix[1]))  # init
            for i in range(slices):
                total_temp[i] = imresize(nii_one[i], (matrix[0], matrix[1]), interp='nearest')  # 512*512 / 256*256
        else:
            total_temp = nii_one

        if need_threshold:
            if total_temp.max() >= 200:
                total_temp[total_temp < 128] = 0
                total_temp[total_temp >= 128] = 1

        print('Saving:\t', total_temp.shape)  # save each one nii
        if '\\' in save_path:  # if using Windows：
            write_itk_imageArray(total_temp, save_path + filename,
                                 # nii_ref
                                 )

        else:
            write_itk_imageArray(total_temp, save_path + filename,
                                 # nii_ref
                                 )

        tag = tag + slices
        print('tag:', tag)

        print('\n**********\t', 'Done.', '\t**********\n')
        return None


def save_npy_to_nii(pred=None, save_path=r'E:\Lung\covid_data0424\label_V1pred/',
                    # ref_path=r'E:\Lung\covid_data0424\src/*',
                    nii_name_id=None,
                    save_type=None,
                    need_rotate=True, need_resize=True, need_threshold=True):
    '''
    :param pred:
    :param save_path:
    :param ref_path:
    :param need_rotate:
    :param need_resize:
    :param need_threshold:
    :param save_type
    :return:
    '''

    print('\n**********\t save one npy to nii.gz', '\t**********\n')

    tag = 0

    slices = pred.shape[0]
    matrix = (512, 512)  #

    # 05/04
    if tag + slices > pred.shape[0]:
        cut = tag + slices - pred.shape[0]
        H = pred.shape[1]  # 256
        W = pred.shape[2]  # 256
        temp = np.zeros((cut, H, W))
        pred = np.concatenate((pred, temp), 0)

    nii_one = pred[tag:tag + slices]

    if need_rotate:
        for i in range(slices):
            nii_one[i, :, :] = np.flip(nii_one[i, :, :])
            nii_one[i, :, :] = np.flip(nii_one[i, :, :], axis=1)

    if need_resize:
        total_temp = np.zeros((slices, matrix[0], matrix[1]))  # init
        for i in range(slices):
            total_temp[i] = imresize(nii_one[i], (matrix[0], matrix[1]), interp='nearest')  # 512*512 / 256*256

    else:
        total_temp = nii_one

    if need_threshold:
        if total_temp.max() >= 200:
            total_temp[total_temp < 128] = 0
            total_temp[total_temp >= 128] = 1

    print('Saving:\t', total_temp.shape)  # save each one nii

    if save_type is not None:
        save_path = os.path.join(save_path + nii_name_id).replace('.nii.gz', '_' + save_type + '.nii.gz')
        try:
            if not os.path.exists(os.path.dirname(save_path)):
                os.makedirs(os.path.dirname(save_path))
        except:
            print('Failed to mkdir :', os.path.dirname(save_path))

    else:
        save_path = save_path + nii_name_id

    if '\\' in save_path:  # if using Windows：
        write_itk_imageArray(total_temp, save_path, )

    else:
        write_itk_imageArray(total_temp, save_path, )

    print('\n**********\t', 'Done.', '\t**********\n')
    return None


'''
other utils
'''


def crop_volume(volume, crop):
    volume_ = volume.copy()
    volume_[:crop[0]] = 0
    volume_[-crop[1]:] = 0
    return volume_


def resize(data, shape):
    mask = np.zeros(shape)
    for i in range(shape[0]):
        mask[i, :, :] = cv2.resize(data[i, :, :], (shape[1], shape[2]))
    return mask


def save_nii(raw, lung, lesion, meta, crop=[0, 0]):
    """ Save raw cross_domain, raw segmentation, lesion segmentation as .nii.gz file
    """
    # the path in this function is used for saving gz file.
    # raw_root = './cross_domain'
    # lung_root = './raw'
    # lesion_root = './lesion'
    # meta_root = './meta'

    lung_root = '2020035365_output/raw/'
    lesion_root = '2020035365_output/lesion/'

    former_slice = 0
    for index, row in meta.iterrows():
        filename = row['filename']
        filename = os.path.basename(filename)  # '2020035365_0204_3050_20200204184413_2.nii.gz'
        slices = row['slice']  # 65
        origin_shape = eval(row['shape'])
        total_slice = lung.shape[0]
        current_slice = np.min([former_slice + slices, total_slice])

        # raw_volume = raw[former_slice:current_slice]
        lung_volume = lung[former_slice:current_slice]
        lesion_volume = lesion[former_slice:current_slice]
        lesion_volume = lesion_volume * lung_volume
        if crop[0] > 0:
            lung_volume = crop_volume(lung_volume, (np.array(crop) * slices).astype('int'))
            lesion_volume = crop_volume(lesion_volume, (np.array(crop) * slices).astype('int'))

        lung_volume = resize(lung_volume, origin_shape)
        lesion_volume = resize(lesion_volume, origin_shape)
        # raw_volume = resize(raw_volume, origin_shape)

        lung_path = os.path.join(lung_root, filename)
        lesion_path = os.path.join(lesion_root, filename)
        # raw_path = os.path.join(raw_root, filename)
        print(lung_path)
        print(lesion_path)
        # print(raw_path)

        write_itk_imageArray(lung_volume, lung_path)
        write_itk_imageArray(lesion_volume, lesion_path)
        # write_itk_imageArray(raw_volume, raw_path)
        former_slice = current_slice


if __name__ == '__main__':
    pass
