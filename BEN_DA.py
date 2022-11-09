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
    parser.add_argument("-l", dest='label', required=True, type=str, help="label data folder")
    parser.add_argument("-source", dest='source', type=str, help="source model weight path")
    parser.add_argument("-prefix", dest='prefix', help="new model name prefix")

    parser.set_defaults(BN_list=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

    args = parser.parse_args()

    # for Linux/Colab
    new_weight = update_weight(args.train, args.label, weight=args.source,
                               model_name=args.prefix, BN_list=args.BN_list,
                               )
    # # for Windows
    # new_weight = update_weight(args.train, args.label, weight=eval(args.source),
    #               model_name=args.prefix, BN_list=args.BN_list,
    #               )

    print('\n**********\t New weight saved as:\t**********\n')
    print(new_weight)
