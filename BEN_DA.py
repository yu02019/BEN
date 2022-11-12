from utils.update_model import update_weight

import os
import logging
import warnings
import tensorflow as tf

warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # tf log errors only
logging.getLogger('tensorflow').setLevel(logging.ERROR)
print(tf.__version__)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", dest='train', required=True, type=str, help="train data folder")
    parser.add_argument("-l", dest='label', required=True, type=str,
                        help="label data folder; if No label used, set it to None or '' ")
    parser.add_argument("-r", dest='raw', required=True, type=str, help="raw target data folder (only raw scans need)")
    parser.add_argument("-weight", dest='weight', type=str,
                        default=r'weight/unet_fp32_all_BN_NoCenterScale_polyic_epoch15_bottle256_04012056/',
                        help="source model pretrained weight path")
    parser.add_argument("-prefix", dest='prefix', required=True, help="new model name prefix")
    parser.add_argument("-check", dest='check_orientation', default=None,
                        help="Check input orientation. 'RIA' for rodents and 'RPI' for NHPs")

    parser.set_defaults(BN_list=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

    args = parser.parse_args()

    # Check the path string for compatibility with different operating systems (Windows, Linux, and Collab)
    if args.weight == 'None':
        args.weight = None
        print('args.weight: None')
    if args.label == 'None' or args.label == "''":
        args.label = ''
        print('args.label: None')

    new_weight = update_weight(args.train, args.label, target_data=args.raw,
                               weight=args.weight,
                               model_name=args.prefix, BN_list=args.BN_list, check_orientation=args.check_orientation,
                               )

    print('\n**********\t New weight saved as:\t**********\n')
    print(new_weight)
