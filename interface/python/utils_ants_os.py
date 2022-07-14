import os
from glob import glob
from tqdm import tqdm
import time
import sys


def run_main(input_folder=r'pipeline-BEN-src/*', output_folder='ANTs-sigma-brain-colab/', fixed_image=r'Atlas-brain/SIGMA_InVivo_Brain_Template_Masked.nii.gz'):
    t1 = time.time()

    path = glob(input_folder)
    path.sort(reverse=False)

    patch = sys.argv[1]  # get first param
    patch = int(patch)
    print('get param', patch)
    time.sleep(2)

    out_folder = output_folder  # if no used, keep ''.

    if patch>=0:
        path = path[patch*10 : patch*10 + 10]
    else:
        path = path

    # fixed_image = r'Atlas-brain/SIGMA_InVivo_Brain_Template_Masked.nii.gz'

    for i in tqdm(path):

        trans_matrix_prefix = os.path.basename(i)
        # print(out_folder + trans_matrix_prefix)

        # check if the output already exists!
        check_output = glob(out_folder + trans_matrix_prefix + '*')
        print(check_output)
        if check_output != []:
            print('already exists! continue!')
            time.sleep(0.3)
            if len(check_output)<5:
                input('Warnning!!!')
            continue

        os.system('antsRegistrationSyN.sh -d 3 -n 10 -o {} -f {} -m {}'.format(out_folder + trans_matrix_prefix, fixed_image, i))

        # break

    print('Done!')
    t2 = time.time()

    print('total time:', t2-t1)
    print('avg time:', (t2-t1)/len(path))


if __name__ == '__main__':
    import os
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest='input', required=True, type=str, help="Input folder")
    parser.add_argument("-o", dest='output', required=True, type=str, help="Output folder")
    parser.add_argument("-ref", dest='ref', help="Reference/fixed image")
    args = parser.parse_args()

    # if not os.path.exists(args.input.replace('*', '')):
    #     print('\nThe path does not exist.\n')
    # elif 'gz' not in os.listdir(args.input)[0]:
    #     print('\nThe path does not contain nii.gz format files.\n')
    # else:
    #     run_main(input_folder=args.input, output_folder=args.output, fixed_image=args.ref)

    run_main(input_folder=args.input, output_folder=args.output, fixed_image=args.ref)
