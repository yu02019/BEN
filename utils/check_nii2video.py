import cv2
import itertools
import numpy as np
import nibabel as nib
# from matplotlib import pyplot as plt
import os
from skimage import transform

join = os.path.join


# %%


def run_main(img_path, seg_path, save_path, render_num=-1):
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

    def seg_norm(seg_volume):
        # assign the RGB channels and intensity for each seg of organs
        channels_candidate_list = []
        for i in range(1, 4):
            channels_candidate_list += itertools.combinations('012', i)
        print(channels_candidate_list)
        base_color = 128
        color_stride = (255 - base_color) * 3 // np.max(seg_volume)
        for i in range(1, np.max(seg_volume) + 1):
            color = color_stride * (i - 1)
            intensity = color % (255 - base_color) + base_color
            channels = channels_candidate_list[(i - 1) % len(channels_candidate_list)]
            channels = [int(x) for x in channels]
            print(i, intensity, channels)
            for j in range(3):
                if j in channels:
                    seg_volume[:, :, j, :][seg_volume[:, :, j, :] == i] = intensity
                else:
                    seg_volume[:, :, j, :][seg_volume[:, :, j, :] == i] = 0

        return seg_volume

    COLOR_LIST = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]

    def assign_color(seg_volume):
        # assign the RGB for each organ based on predefined color (COLOR_LIST)
        for i in range(1, np.max(seg_volume) + 1):
            for j in range(3):
                seg_volume[:, :, j, :][seg_volume[:, :, j, :] == i] = COLOR_LIST[i - 1][j]

        return seg_volume

    def combine_data_seg(data_volume, seg_volume):
        data_volume = data_norm(data_volume)
        data_volume = toRGB(data_volume)
        seg_volume = toRGB(seg_volume)
        seg_volume = seg_norm(seg_volume)
        data_seg_volume = np.zeros(shape=data_volume.shape, dtype=np.uint8)
        for i in range(data_volume.shape[-1]):
            rate_for_image = 0.7
            data_seg_volume[..., i] = cv2.addWeighted(data_volume[..., i], rate_for_image,
                                                      seg_volume[..., i], 1 - rate_for_image, 0)

        return data_seg_volume

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

    def imgs2video(imgs, zmin, show_name, save_name, fps=5):
        # define font
        font = cv2.FONT_HERSHEY_SIMPLEX
        # fps = 2 frames per second
        # size = (imgs.shape[0], imgs.shape[1])  # wrong setting
        size = (imgs.shape[1], imgs.shape[0])

        video_writer = cv2.VideoWriter(save_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, size)

        for i in range(imgs.shape[-1]):
            # put text to image
            img_temp = np.fliplr(imgs[..., i])
            frame = img_temp.copy()
            # img, text, coord, font, size, color, wide +1 aims to match the index in ITK-SNAP
            cv2.putText(frame, "%s: %d" % (show_name, zmin + i + 1), (40, 40), font, 0.5, (255, 255, 255), 2)
            # video_writer.write(imgs[..., i])
            video_writer.write(frame)

        video_writer.release()

    def find_seg_region(seg, shift=2):
        # identify the z_min and z_max of a segmentation
        # seg.shape = (x,y,z); z should be the number of axial slices
        if np.max(seg) > 0:
            z_index = np.where(seg_volume > 0)[2]
        else:
            z_index = np.where(seg_volume > 0)[2]
        z_min = np.max([np.min(z_index) - shift, 0])
        z_max = np.min([np.max(z_index) + shift, seg.shape[2]])

        return z_min, z_max

    ''' Run '''
    names = os.listdir(seg_path)
    names.sort()
    names_img = os.listdir(img_path)
    names_img.sort()

    if render_num != -1:  # num to address
        list_to_address = names[0:render_num]
    else:
        list_to_address = names
    for i, name in enumerate(list_to_address):
        data_volume = nib.load(join(img_path, names_img[i])).get_fdata()
        seg_volume = nib.load(join(seg_path, name)).get_fdata()
        z_min, z_max = find_seg_region(seg_volume)
        data_volume[data_volume < 0] = 0

        # if i < 10:   # for Cor data
        #     pass
        # else:  # for Radio data
        #     data_volume = transform.resize(data_volume, (512,512, seg_volume.shape[-1]))
        #     seg_volume = transform.resize(seg_volume, (512,512, seg_volume.shape[-1]), 0)

        # combine data and seg to one volume
        # data_volume: mouse: (200, 280, 128) float64
        data_seg_volume = combine_data_seg_v2(data_volume[:, :, z_min:z_max], seg_volume[:, :, z_min:z_max])
        # data_seg_volume: mouse: (280, 200, 3, 113[time])
        imgs2video(data_seg_volume, z_min, show_name=name, save_name=join(save_path, name.split(".nii.gz")[0] + ".mp4"))

    # img_path = r'H:\TCIA-Lung\Task020_NSCLCLung\imagesTr'
    # seg_path = r'H:\TCIA-Lung\Task020_NSCLCLung\labelsTr'
    # save_path = r'H:\TCIA-Lung\LungVideos'

    # for name in names[0:1]:
    #    data_volume = nib.load(join(img_path, name.split('.nii.gz')[0]+'_0000.nii.gz')).get_fdata()
    #    seg_volume = nib.load(join(seg_path, name)).get_fdata()
    #    z_min, z_max = find_seg_region(seg_volume)
    #
    #    data_volume[data_volume>150] = 150
    #    data_volume[data_volume<-1350] = -1350
    #
    #    # combine data and seg to one volume
    #    data_seg_volume = combine_data_seg_v2(data_volume[:,:, z_min:z_max], seg_volume[:,:, z_min:z_max])
    #    imgs2video(data_seg_volume, z_min, show_name=name, save_name=join(save_path, name.split(".nii.gz")[0] +".mp4"))


if __name__ == '__main__':
    img_path = r'E:\New\Data_repo\doi_10.5061_dryad.1vhhmgqv8__v2\dataset\train-all'
    seg_path = r'E:\New\Data_repo\doi_10.5061_dryad.1vhhmgqv8__v2\dataset\pred-pipe_30epoch_11090153'
    save_path = r'E:\New\Data_repo\doi_10.5061_dryad.1vhhmgqv8__v2\dataset'
    render_num = 1  # num to address. Set -1 to address all

    run_main(img_path, seg_path, save_path, render_num)
