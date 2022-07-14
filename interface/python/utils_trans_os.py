from glob import glob
from tqdm import tqdm
import time
import sys

def run_main(input_folder=r'pipeline-afni-src/*', output_folder='Native-label-afni-brain', fixed_image=r'R2_SIGMA_Anatomical_Brain_Atlas.nii.gz', trans_mat_folder=r'ANTs-sigma-afni2brain'):
    # 2021/11/09 transform atlas label to native space
    t1 = time.time()
    
    ''' input moving nii'''
    # for CentOS
    # path = glob(r'/home1/yuzq/Music/src-macaque/dataset-2/*')
    # for Windows
    path = glob(input_folder)
    path.sort(reverse=False)
    outfolder = output_folder
    
    reference_image = fixed_image
    trans_root_folder = trans_mat_folder
    ''' above need change for each run '''
    
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
        print('Creating new folder:', outfolder)
        time.sleep(1)
    
    for i in tqdm(path):
    
        trans_matrix_prefix = os.path.basename(i)  # equal to filename
        print(trans_matrix_prefix)
    
        try:
            trans_mat1 = glob('{}/{}*{}'.format(trans_root_folder, trans_matrix_prefix, '0GenericAffine.mat'))[0]
            trans_mat2 = glob('{}/{}*{}'.format(trans_root_folder, trans_matrix_prefix, '1InverseWarp.nii.gz'))[0]
        except:
            print('lose trans mat!')
            continue
    
        outname = outfolder + '/' + trans_matrix_prefix
    
        # check
        trans_mat_name = os.path.basename(trans_mat1)
        if trans_matrix_prefix[4:10] != trans_mat_name[4:10]:
            input('Warning!!')
    
        # for src apply trans
        # os.system('antsApplyTransforms -d 3 -i {} -r {} -t {} -t {} -o {}'.format(i, reference_image, trans_mat1, trans_mat2, outname))
    
        # for label and binary mask/output (for interpolation NO new value?)
        os.system('antsApplyTransforms -d 3 -i {} -r {} -n NearestNeighbor -t [{}, 1] -t {} -o {}'.format(reference_image, i, trans_mat1, trans_mat2, outname))
        # only linear transformation
        # os.system('antsApplyTransforms -d 3 -i {} -r {} -n GenericLabel[Linear] -t [{}, 1] -o {}'.format(reference_image, i, trans_mat1, outname))
    
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
    parser.add_argument("-mat", dest='mat', help="transform mat")
    args = parser.parse_args()
    
    # if  'gz' not in os.listdir(args.input)[0]:
    #     print('\nThe path does not contain nii.gz format files.\n')
    # elif   not os.path.exists(args.input):
    #     print('\nThe path does not exist.\n')
    # else:
    #     run_main(input_folder=args.input, output_folder=args.output, fixed_image=args.ref, trans_mat_folder=args.mat)

    run_main(input_folder=args.input, output_folder=args.output, fixed_image=args.ref, trans_mat_folder=args.mat)
