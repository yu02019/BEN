import os
import numpy as np
# from utils.load_data import read_from_nii, read_from_nii_label
from model.models_network import backbone_network
import time
from model.loss import weighted_dice_with_CE, dice_coef
from utils.load_data import read_from_nii, read_from_nii_label


def update_weight(train_data='', label_data='', target_data='',
                  need_mkdir=False,
                  weight=None,
                  need_rotate=True,
                  model_name='model_',
                  BN_list=None,
                  droprate=0.0,
                  freeze=True,
                  momentum=0.8,
                  batch_size=32,
                  epochs=30,
                  max_num=-1,
                  check_orientation=None,
                  ):
    """

    :param train_data: folder path for raw target MR scans (with labels in another folder)
    :param label_data: folder path for labels of target scans
    :param target_data: folder path for all target raw MR scans (with or without labels)
    :param need_mkdir:
    :param weight:
    :param need_rotate:
    :param model_name:
    :param BN_list:
    :param droprate:
    :param freeze:
    :param momentum:
    :param batch_size:
    :param epochs:
    :param max_num:
    :return:
    """

    '''
    read / load cross_domain
    '''
    read_from_npy = False
    nii_path = train_data + '/*'
    label_path = label_data + '/*'
    target_path = target_data + '/*'  # 2022/11/11 update

    if not read_from_npy:
        all_src_data = read_from_nii(nii_path=nii_path, need_resize=256, Hu_window='auto',
                                     need_rotate=need_rotate, max_num=max_num, check_orientation=check_orientation)
        all_src_data = np.expand_dims(all_src_data, -1)

        if len(label_path) > 2:  # if label path is not empty. len('' + '/*') == 2
            all_label_data = read_from_nii_label(nii_path=label_path, need_resize=256, need_rotate=need_rotate,
                                                 interest_label=1, max_num=max_num, check_orientation=check_orientation)
            all_label_data = np.expand_dims(all_label_data, -1)
        else:
            all_label_data = np.zeros_like(all_src_data)  # create empty label matrix
            print('Create empty label matrix!')
    elif read_from_npy:
        all_src_data = np.load(r'D:\\polyic_src.npy')
        all_src_data = all_src_data[:]
        all_label_data = np.load(r'D:\\polyic_label.npy')
        all_label_data = all_label_data[:]

    print('\n**********\tInferring CT/MRI scans:\t**********\n')

    # tf.keras.backend.clear_session()

    if weight:
        models = backbone_network(256, 256, pretrained_weights=weight, need_complie=False, BN_list=BN_list,
                                  droprate=droprate)
        if freeze:
            for layer in models.layers:
                if 'batch_normalization' not in layer.name:
                    layer.trainable = False
                else:
                    print('Trainable lay: ', layer.name)

            models.compile(optimizer='adam', loss=[weighted_dice_with_CE], metrics=[dice_coef])
            print('Only finetune BN on target domain!')
        else:
            models = backbone_network(256, 256, pretrained_weights=weight, need_complie=False, BN_list=BN_list,
                                      droprate=droprate, momentum=momentum)
            models.compile(optimizer='adam', loss=[weighted_dice_with_CE], metrics=[dice_coef])
            print('finetune all layers on target domain!')
    else:
        # input('please check input.')
        print('Note: no pretrained weight used.')
        models = backbone_network(256, 256, pretrained_weights=None, need_complie=False, BN_list=BN_list,
                                  droprate=droprate)
        if freeze:
            for layer in models.layers:
                if 'batch_normalization' not in layer.name:
                    layer.trainable = False
                else:
                    print('Trainable lay: ', layer.name)
        models.compile(optimizer='adam', loss=[weighted_dice_with_CE], metrics=[dice_coef])

    '''
    setting
    '''
    from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping, ReduceLROnPlateau

    time_id = np.int64(time.strftime('%Y%m%d%H%M', time.localtime(time.time())))
    time_id = str(time_id)[-8:]
    # no need if use callback_list to save automatically
    # model_id = 'weight/' + model_name + '_' + time_id + '/'
    # if not os.path.exists(model_id):
    #     os.makedirs(model_id)

    weight_path = 'weight/' + model_name + '_' + time_id + '/'  # save model (tf)

    reduceLROnPlat = ReduceLROnPlateau(monitor='val_loss', factor=0.2, min_lr=1e-6, patience=5, verbose=1, epsilon=1e-4,
                                       mode='min')  # lr*factor
    # reduceLROnPlat = ReduceLROnPlateau(monitor='val_loss', factor=0.8, patience=10, verbose=1, mode='auto', epsilon=0.0001, cooldown=5, min_lr=0.00001)
    # epsilon=0.0001，min_lr=0.00001

    early = EarlyStopping(monitor="val_loss",
                          mode="min",
                          patience=10)

    checkpoint = ModelCheckpoint(weight_path, monitor='val_loss', verbose=1,
                                 save_best_only=True, mode='min', save_weights_only=True)

    callbacks_list = [  # feel free to change as needed.
        # checkpoint,  # save model
        # early,
        # reduceLROnPlat
    ]

    '''
    Train
    '''
    ''' Step 1: Use limited-label raw MR images (around 3–10, depending on the quality of scans). Update BN layers. '''
    if freeze:
        models.fit(all_src_data, all_label_data, batch_size=batch_size, epochs=epochs, validation_split=0,  # or 0.1
                   callbacks=callbacks_list)

    ''' Step 2: If have labels, update all layers (both Conv and BN layers). Otherwise, skip (zero-shot inference). '''
    if len(label_path) > 2:  # if label path is not empty. len('' + '/*') == 2
        for layer in models.layers:
            layer.trainable = True
        models.compile(optimizer='adam', loss=[weighted_dice_with_CE], metrics=[dice_coef])
        models.fit(all_src_data, all_label_data, batch_size=batch_size, epochs=epochs, validation_split=0,  # or 0.1
                   callbacks=callbacks_list)

    ''' Step 2 (Optional): Update all layers with augmentation (Not recommended) '''
    # if len(label_path) > 2:  # if label path is not empty. len('' + '/*') == 2
    #     for layer in models.layers:
    #         layer.trainable = True
    # from keras.preprocessing.image import ImageDataGenerator
    # datagen = ImageDataGenerator(
    #     # rotation_range=20,
    #     width_shift_range=0.2,
    #     height_shift_range=0.2,
    #     horizontal_flip=True,
    #     # vertical_flip=True,
    #     zoom_range=0.2,
    #     shear_range=0.2,
    #     # fill_mode='reflect',
    # )
    # # Fit the model using batch data with real-time augmentation
    # models.fit_generator(datagen.flow(all_src_data, all_label_data, batch_size=32),
    #                     steps_per_epoch=len(all_src_data) / 32, epochs=200)  # epochs=epochs

    ''' Step 3: Freeze all layers except the BN layers and adapt them to raw MR scans from the target domain. (no labeling needed) '''
    if freeze and len(target_path) > 2:  # if target path is not empty. len('' + '/*') == 2:
        for layer in models.layers:
            if 'batch_normalization' not in layer.name:
                layer.trainable = False
            else:
                print('Trainable lay: ', layer.name)
        models.compile(optimizer='adam', loss=[weighted_dice_with_CE], metrics=[dice_coef])
        print('Only finetune BN on target domain!')
        # load target raw MR scans
        all_src_data = read_from_nii(nii_path=target_path, need_resize=256, Hu_window='auto',
                                     need_rotate=need_rotate, max_num=max_num, check_orientation=check_orientation)
        all_src_data = np.expand_dims(all_src_data, -1)
        all_label_data = np.zeros_like(all_src_data)  # create empty label matrix
        # adaptation
        models.fit(all_src_data, all_label_data, batch_size=batch_size, epochs=epochs, validation_split=0,  # or 0.1
                   callbacks=callbacks_list)

    # no need following codes if you have used callback_list earlier to save automatically
    if not os.path.exists(weight_path):
        os.makedirs(weight_path)
    models.save_weights(weight_path + '.hdf5')

    print('New model has trained and saved as:  ' + weight_path)

    del models  # release RAM

    return weight_path  # return new weight path for load to infer
