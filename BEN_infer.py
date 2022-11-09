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
    parser.add_argument("-model", dest='model', help="model weight path")

    parser.set_defaults(BN_list=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

    args = parser.parse_args()

    inference_pipeline(args.input, args.output, weight=args.model, BN_list=args.BN_list)
