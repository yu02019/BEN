from utils.inference import inference_pipeline

import os
import logging
import warnings
import tensorflow as tf

warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # tf log errors only
logging.getLogger('tensorflow').setLevel(logging.ERROR)
print(tf.__version__)

# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# tf.Session(config=config)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest='input', required=True, type=str, help="Input folder")
    parser.add_argument("-o", dest='output', required=True, type=str, help="Output folder")
    parser.add_argument("-weight", dest='weight', help="model weight path",
                        default=r'weight/unet_fp32_all_BN_NoCenterScale_polyic_epoch15_bottle256_04012056/')
    parser.add_argument("-check", dest='check_orientation',
                        help="Check input orientation. None for skipping. 'RIA' for rodents and 'RPI' for NHPs")
    parser.add_argument("-mkdir", dest='is_mkdir', default=True, help="If the output folder doesn't exist, creat it")

    parser.set_defaults(BN_list=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

    args = parser.parse_args()

    ''' Run inference '''
    inference_pipeline(args.input, args.output, weight=args.weight, BN_list=args.BN_list,
                       check_orientation=args.check_orientation, is_mkdir=args.is_mkdir)

    ''' (Optional) Run post-processing '''
    # from utils.postprocess import remove_small_objects_v1
    # from utils.postprocess_crf import crf_2D

    # remove_small_objects_v1(input_path=args.output, output_path=args.output)  # in-place rewrite
    # crf_2D(img_dir=args.input, predict_dir=args.output, output_folder=args.output)  # in-place rewrite

    ''' Generate visual report '''
    from utils.check_result import make_result_to_logs
    from utils.check_html import make_logs_to_html

    logs_folder = make_result_to_logs(input_folder=args.input, predict_folder=args.output, species='rodents')
    make_logs_to_html(log_folder=logs_folder)  # HTML logs will be saved in this folder

    print('\n**********\t', 'Pipeline finished.', '\t**********\n')
