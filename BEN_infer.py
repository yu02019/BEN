import os
import logging
import warnings
import tensorflow as tf
from utils.inference import inference_pipeline

# warnings.filterwarnings("ignore")
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # tf log errors only
# logging.getLogger('tensorflow').setLevel(logging.ERROR)
# print(tf.__version__)

# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# tf.Session(config=config)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest='input', required=True, type=str, help="Input folder")
    parser.add_argument("-o", dest='output', required=True, type=str, help="Output folder")
    parser.add_argument("-model", dest='model', help="model weight path")
    args = parser.parse_args()

    inference_pipeline(args.input, args.output, weight=source_domain_weight,)

