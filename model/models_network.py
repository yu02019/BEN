# encoding=utf-8
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Add, BatchNormalization
from tensorflow.keras.layers import Dropout

from tensorflow.keras.layers import Conv2D, Conv2DTranspose
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import concatenate
from tensorflow.keras import backend as K
from model.loss import weighted_dice_with_CE, dice_coef

from model.non_local import non_local_block

smooth = 0.001

K.set_image_data_format('channels_last')


def resconv(inputlayer, outdim, name, res_connet=True, droprate=0.0, is_batchnorm=True,
            BN_trainable=False, Drop_trainable=True, momentum=0.8):
    '''
    :param inputlayer:
    :param outdim:
    :param name:
    :param is_batchnorm:
    :return:
    '''
    kinit = 'he_normal'
    x = Conv2D(outdim, 3, activation='elu', padding='same', kernel_initializer=kinit, name=name + '_1')(inputlayer)
    x = Conv2D(outdim, 3, activation='elu', padding='same', kernel_initializer=kinit, name=name + '_2')(x)

    if is_batchnorm:
        ''' default setting '''
        # x = BatchNormalization(axis=-1, )(x)

        ''' Customized momentum. Note that there is NO trainable parameters here (center=False, scale=False)'''
        x = BatchNormalization(axis=-1, center=False, scale=False, momentum=momentum)(x)

    if droprate:
        x = Dropout(droprate, trainable=Drop_trainable)(x, training=True)

    if res_connet:
        x = Add()([inputlayer, x])

    return x


def backbone_network(IMG_WIDTH=256, IMG_HEIGHT=256, IMG_CHANNELS=1, pretrained_weights=False,
                     # opt = Adam(1e-4),
                     need_complie=True,
                     BN_list=None,
                     droprate=0.0,
                     NL_att=False,
                     momentum=0.8,
                     ):
    """

    :param IMG_WIDTH:
    :param IMG_HEIGHT:
    :param IMG_CHANNELS:
    :param pretrained_weights:
    :param need_complie:
    :param BN_list:
    :param droprate: If droprate=0, there will be No setting (do nothing).
    :param NL_att:
    :return:
    """
    inputs = Input((IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS))

    if BN_list != None:
        BN1, BN2, BN3, BN4, BN5, BN6, BN7, BN8, BN9, BN10 = BN_list
    else:
        BN1 = BN2 = BN3 = BN4 = BN5 = BN6 = BN7 = BN8 = BN9 = BN10 = 0

    if isinstance(droprate, list):
        droprate1, droprate2, droprate3, droprate4, droprate5, droprate6, droprate7, droprate8, droprate9, droprate10 = droprate
    elif droprate is None or droprate == False:  # 0.0 == False
        droprate = 0
        droprate1 = droprate2 = droprate3 = droprate4 = droprate5 = droprate6 = droprate7 = droprate8 = droprate9 = droprate10 = droprate
    else:
        droprate1 = droprate2 = droprate3 = droprate4 = droprate5 = droprate6 = droprate7 = droprate8 = droprate9 = droprate10 = droprate

    e1 = resconv(inputlayer=inputs, outdim=16, name='encoder1', is_batchnorm=BN1, res_connet=False, droprate=droprate1,
                 momentum=momentum)
    down1 = MaxPooling2D((2, 2))(e1)

    e2 = resconv(inputlayer=down1, outdim=32, name='encoder2', is_batchnorm=BN2, res_connet=False, droprate=droprate2,
                 momentum=momentum)
    down2 = MaxPooling2D((2, 2))(e2)

    e3 = resconv(inputlayer=down2, outdim=64, name='encoder3', is_batchnorm=BN3, res_connet=False, droprate=droprate3,
                 momentum=momentum)
    down3 = MaxPooling2D((2, 2))(e3)

    e4 = resconv(inputlayer=down3, outdim=128, name='encoder4', is_batchnorm=BN4, res_connet=False, droprate=droprate4,
                 momentum=momentum)
    down4 = MaxPooling2D((2, 2))(e4)

    bottlenect = resconv(inputlayer=down4, outdim=256, name='bottle_start', is_batchnorm=BN5, res_connet=False,
                         droprate=droprate5, momentum=momentum)

    # add non-local
    if NL_att:
        bottlenect = non_local_block(bottlenect)

    bottlenect = resconv(inputlayer=bottlenect, outdim=256, name='bottle_end', is_batchnorm=BN6, res_connet=False,
                         droprate=droprate6, momentum=momentum)

    bottlenect = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(bottlenect)
    bottlenect = concatenate([bottlenect, e4])

    d6 = resconv(inputlayer=bottlenect, outdim=128, name='decoder6', is_batchnorm=BN7, res_connet=False,
                 droprate=droprate7, momentum=momentum)
    u6 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(d6)
    u6 = concatenate([u6, e3])

    d7 = resconv(inputlayer=u6, outdim=64, name='decoder7', is_batchnorm=BN8, res_connet=False, droprate=droprate8,
                 momentum=momentum)
    u7 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(d7)
    u7 = concatenate([u7, e2])

    d8 = resconv(inputlayer=u7, outdim=32, name='decoder8', is_batchnorm=BN9, res_connet=False, droprate=droprate9,
                 momentum=momentum)
    u8 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(d8)
    u8 = concatenate([u8, e1])

    d9 = resconv(inputlayer=u8, outdim=16, name='decoder9', is_batchnorm=BN10, res_connet=False, droprate=droprate10,
                 momentum=momentum)

    outputs = Conv2D(1, (1, 1), activation='sigmoid')(d9)

    model = Model(inputs=[inputs], outputs=[outputs])

    if need_complie:
        model.compile(optimizer='adam', loss=[weighted_dice_with_CE], metrics=[dice_coef])

    if (pretrained_weights):
        model.load_weights(pretrained_weights)

    return model


if __name__ == '__main__':
    # test
    model = backbone_network(BN_list=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                             droprate=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], NL_att=True)
    model.summary()
