'''
inference
'''
import tensorflow as tf
import numpy as np
# import keras
from model.models_network import backbone_network

from utils.load_data import read_from_nii, save_pred_to_nii

# import cv2

import os

# os.environ['CUDA_VISIBLE_DEVICES'] = '1'
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
tf.Session(config=config)


def inference_pipeline(nii_filename='',
                  save_filename='',
                  label_filename='',
                  # sample_value=10,
                  # label_filename='',
                  # uc_chosen='Predictive',
                  threshold_value=0.5, sform='Other',
                  queue1=None,
                  uncertainty=0,
                  is_mkdir=False,
                  save_multi_samples=False,
                  weight=None,
                  need_rotate=True,
                  modality=None,
                  BN_list=None,
                  NL_att=None,
                  droprate=None,
                  max_num=-1,
                  specific=None,
                  keyword=None,
                  check_orientation=None
                  ):
    if is_mkdir and not os.path.exists(save_filename):
        print('Makedir:\t', save_filename)
        os.makedirs(save_filename)
    print('Object will save in (Existing) folder/print(save_filename):\t', save_filename)

    if specific:
        save_path = save_filename + '/{}'.format(specific)
        nii_path = nii_filename + '/{}'.format(specific)
    else:
        save_path = save_filename + '/*'
        nii_path = nii_filename + '/*'

    ''' read / load src cross_domain '''
    read_from_npy = False
    if not read_from_npy:
        shape_list = None
        if modality != 'epi':
            all_src_data = read_from_nii(nii_path=nii_path, need_resize=256, Hu_window='auto', need_rotate=need_rotate,
                                         modality=modality, max_num=max_num, keyword=keyword, check_orientation=check_orientation)
        elif modality == 'epi':
            all_src_data, shape_list = read_from_nii(nii_path=nii_path, need_resize=256, Hu_window='auto',
                                                     need_rotate=need_rotate, modality=modality)

        all_src_data = np.expand_dims(all_src_data, -1)
    elif read_from_npy:
        all_src_data = np.load(r'D:\\polyic_src.npy')

    print('\n**********\tInferring CT/MRI scans:\t**********\n')

    tf.keras.backend.clear_session()

    weight = 'model_NLunet_epoch20_12131942.hdf5' if not weight else weight

    models = backbone_network(256, 256, pretrained_weights=weight, BN_list=BN_list, droprate=droprate, NL_att=NL_att)

    pred = models.predict(all_src_data, batch_size=16)  # (slice,160,160,1)

    pred = np.squeeze(np.array(pred))

    if modality != 'epi':
        shape_list = None

    save_pred_to_nii(pred=pred, save_path=save_path.replace('*', ''), ref_path=nii_path,
                     need_resize=True, need_rotate=need_rotate, shape_list=shape_list, need_threshold=True,
                     keyword=keyword, check_orientation=check_orientation)


def main():
    # usage
    inference_pipeline(r'D:\raw_rc10_data\D\DATA\mouse_BET\Rat_Wangfei_dataset\88-total-dataset\src',
                       r'D:\raw_rc10_data\D\DATA\mouse_BET\Rat_Wangfei_dataset\88-total-dataset\88-day_2022-BN-train42test42d',
                       is_mkdir=True, weight=r'weight\BEN42day\.hdf5', need_rotate=True,
                       BN_list=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], droprate=0.0)


if __name__ == '__main__':
    main()
