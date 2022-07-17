import os
import numpy as np
from utils.load_data import read_from_nii, read_from_nii_label
from model.models_network import backbone_network
import time
from model.loss import weighted_dice_with_CE, dice_coef
from utils.load_data import read_from_nii, read_from_nii_label

def update_weight(train_data='', label_data='',
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
                  ):
    """

    :param train_data:
    :param label_data:
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

    if not read_from_npy:
        all_src_data = read_from_nii(nii_path=nii_path, need_resize=256, Hu_window='auto',
                                     need_rotate=need_rotate, max_num=max_num)
        all_src_data = np.expand_dims(all_src_data, -1)

        if len(label_path) > 2:  # if label path is not empty. len('' + '/*') == 2
            all_label_data = read_from_nii_label(nii_path=label_path, need_resize=256, need_rotate=need_rotate,
                                                 interest_label=1, max_num=max_num)
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
        if freeze:
            models = backbone_network(256, 256, pretrained_weights=weight, need_complie=False, BN_list=BN_list,
                                      droprate=droprate)
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
        input('please check input.')

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
    train
    '''
    if freeze:
        models.fit(all_src_data, all_label_data, batch_size=batch_size, epochs=epochs, validation_split=0.1,
                   callbacks=callbacks_list)

    ''' if using label '''
    if len(label_path) > 2:  # if label path is not empty. len('' + '/*') == 2
        for layer in models.layers:
            layer.trainable = True
        models.compile(optimizer='adam', loss=[weighted_dice_with_CE], metrics=[dice_coef])
        models.fit(all_src_data, all_label_data, batch_size=batch_size, epochs=epochs, validation_split=0.1,
                   callbacks=callbacks_list)

    # del models

    # no need if use callback_list to save automatically
    if not os.path.exists(weight_path):
        os.makedirs(weight_path)
    models.save_weights(weight_path + '.hdf5')

    print('New model has trained and saved as:  ' + weight_path)

    return weight_path  # return new weight path for load to infer
