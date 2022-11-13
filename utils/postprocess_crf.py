"""
Adapted from the original C++ example: densecrf/examples/dense_inference.cpp
http://www.philkr.net/home/densecrf Version 2.2

2022/11
Reference: How to use CRF in pixel-level binary classification problem?
https://github.com/lucasb-eyer/pydensecrf/issues/63

"""

"""
2020/01
(Test in the Windows console) Input: raw image[.bmp] + mask(rough-seg)[.png]; Output: fine-seg results[.png]
2022/11/12
    1. Update interface (nii format input).
    2. Add 3D CRF implementation.

Installation:
It seems that the "pydensecrf" folder included in the raw project needs to be compiled before being used.
Use the following command instead in Windows:
    conda install -c conda-forge pydensecrf

"""
import os
import cv2
import sys
import numpy as np
import pydensecrf.densecrf as dcrf  # in mrcnn
from skimage.segmentation import relabel_sequential

# 2022/11/12
from glob import glob
from myutils.read_all_data_from_nii_pipe import get_itk_image, get_itk_array, write_itk_imageArray
from pydensecrf.utils import unary_from_softmax, create_pairwise_bilateral, create_pairwise_gaussian


# if len(sys.argv) != 4:
#     print("Usage: python {} IMAGE ANNO OUTPUT".format(sys.argv[0]))
#     print("")
#     print("IMAGE and ANNO are inputs and OUTPUT is where the result should be written.")
#     sys.exit(1)

# sys.argv[1]='im1.png'
# sys.argv[2]='anno1.png'
# sys.argv[3]='ooo1.png'

def batch_crf(img_name, label_name, out_name):
    # img = cv2.imread(img_name, 1)  # cv2.IMREAD_COLOR: 1, load RGB image
    # # (160, 224, 3)
    # labels = relabel_sequential(cv2.imread(label_name, 0))[0].flatten()
    # #  (35840,)
    # labels = labels+1  # 2020/01/16 标签0表示不确定的分类
    # output = out_name
    # M = labels.max() + 1  # number of labels  # 2 for mouse
    # print(M)

    img = img_name
    img = np.uint8(255 * img)
    img = np.expand_dims(img, -1)
    img = np.concatenate([img, img, img], axis=-1)

    labels = relabel_sequential(label_name)[0].flatten()
    labels = labels + 1  # 2020/01/16 标签0表示不确定的分类

    output = out_name

    M = labels.max() + 1  # number of labels  # 2 for mouse
    # print(M)

    '''
    # Setup the CRF model
    '''
    # Setup the CRF model
    d = dcrf.DenseCRF2D(img.shape[1], img.shape[0], M)

    # Certainty that the ground truth is correct
    GT_PROB = 0.5  # 0.5

    # Simple classifier that is 50% certain that the annotation is correct
    u_energy = -np.log(1.0 / M)
    n_energy = -np.log((1.0 - GT_PROB) / (M - 1))
    p_energy = -np.log(GT_PROB)

    U = np.zeros((M, img.shape[0] * img.shape[1]), dtype='float32')
    U[:, labels > 0] = n_energy
    U[labels, np.arange(U.shape[1])] = p_energy
    U[:, labels == 0] = u_energy
    d.setUnaryEnergy(U)

    # d.addPairwiseGaussian(sxy=3, compat=3)
    # d.addPairwiseBilateral(sxy=80, srgb=13, rgbim=img, compat=10)

    d.addPairwiseGaussian(sxy=3, compat=3)
    d.addPairwiseBilateral(sxy=180, srgb=113, rgbim=img, compat=1)

    # Do the inference
    res = np.argmax(d.inference(5), axis=0).astype('float32')

    # if save to drive.
    # res *= 255 / res.max()

    res = res.reshape(img.shape[:2])
    # cv2.imwrite(output, res.astype('uint8'))  # When using cv2 to save, it is not a black-white image, but a gray-white image
    # plt.imsave(output, res, cmap='gray')  # Black-white binary image

    return res  # output post-processing


def batch_3D_crf(image, probs):
    # probs of shape 3d image per class: Nb_classes x Height x Width x Depth
    # assume the image has shape (69, 51, 72)
    shape = image.shape
    new_image = np.empty(shape)
    d = dcrf.DenseCRF(np.prod(shape), probs.shape[0])
    U = unary_from_softmax(probs)
    d.setUnaryEnergy(U)
    feats = create_pairwise_gaussian(sdims=(1.0, 1.0, 1.0), shape=shape)
    d.addPairwiseEnergy(feats, compat=3, kernel=dcrf.FULL_KERNEL, normalization=dcrf.NORMALIZE_SYMMETRIC)

    Q = d.inference(5)
    new_image = np.argmax(Q, axis=0).reshape((shape[0], shape[1], shape[2]))  # take about 10 seconds

    # plot
    # plt.imshow(new_image[64,]); plt.show()
    print(new_image.shape)

    return new_image


def crf_2D(img_dir, predict_dir, output_folder):
    scan_num = len(img_dir)
    for i in tqdm(range(scan_num)):
        filename = os.path.basename(predict_dir[i])
        out_name = output_folder + '\\' + filename

        ''' Method 1: 2D slice-level crf '''
        image = get_itk_array(img_dir[i])  # (128, 280, 200)
        image[image < 0] = 0
        image = image - image.min()
        image = image * 1.0 / image.max()

        ref = get_itk_image(predict_dir[i])
        predict = get_itk_array(predict_dir[i])  # (128, 280, 200)
        predict_post = np.zeros_like(predict)
        for slice_id in range(image.shape[0]):
            image_slice = image[slice_id]
            predict_slice = predict[slice_id]

            post_slice = batch_crf(img_name=image_slice,
                                   label_name=predict_slice,
                                   out_name=None,
                                   )
            post_slice[post_slice < 2] = 0  # only save the class of 2
            post_slice[post_slice == 2] = 1
            predict_post[slice_id] = post_slice

        ''' Method 2: 3D crf '''
        # image = get_itk_array(img_dir[i])  # (128, 280, 200)
        #
        # ref = get_itk_image(predict_dir[i])
        # predict = get_itk_array(predict_dir[i])  # (128, 280, 200)
        # predict = np.expand_dims(predict, 0)  # (1, 128, 280, 200)
        # probs = np.concatenate([np.zeros_like(predict), predict], axis=0)  # 2 class (不确定的类 + foreground)
        #
        # predict_post = batch_3D_crf(image, probs)

        # save to nii
        predict_post = predict_post.astype('float')
        write_itk_imageArray(predict_post, out_name, ref)  # ref


def crf_3D(img_dir, predict_dir, output_dir):
    scan_num = len(img_dir)
    for i in tqdm(range(scan_num)):
        filename = os.path.basename(predict_dir[i])
        out_name = output_folder + '\\' + filename

        # # 2D slice-level crf
        # batch_crf(img_name=img_dir[i],
        #           label_name=predict_dir[i],
        #           out_name=out_name)

        # 3D crf
        image = get_itk_array(img_dir[i])  # (128, 280, 200)

        ref = get_itk_image(predict_dir[i])
        predict = get_itk_array(predict_dir[i])  # (128, 280, 200)
        predict = np.expand_dims(predict, 0)  # (1, 128, 280, 200)
        probs = np.concatenate([np.zeros_like(predict), 1 - predict, predict],
                               axis=0)  # 3 class (Uncertain class + background + foreground)

        predict_post = batch_3D_crf(image, probs)

        # save to nii
        predict_post = predict_post.astype('float')
        write_itk_imageArray(predict_post, out_name, ref)


if __name__ == '__main__':
    from tqdm import tqdm
    import matplotlib.pyplot as plt

    img_dir = glob(r'E:\New\Data_repo\doi_10.5061_dryad.1vhhmgqv8__v2\dataset\train-all\*.nii*')
    predict_dir = glob(r'E:\New\Data_repo\doi_10.5061_dryad.1vhhmgqv8__v2\dataset\pred-pipe_30epoch_11090153\*.nii*')
    output_folder = r'E:\New\Data_repo\doi_10.5061_dryad.1vhhmgqv8__v2\dataset\pred-CRF'

    # main_3D(img_dir, predict_dir, output_folder)

    crf_2D(img_dir, predict_dir, output_folder)
