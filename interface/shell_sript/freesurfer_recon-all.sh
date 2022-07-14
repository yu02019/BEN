#------------ path ----------
input_path=/PATH/...
ben_output_path=/PATH/...
weight=/PATH/...

# ------------ skull-stripping start ------------
python infer.py -i $input_path -o $ben_output_path -w $weight
# ------------ skull-stripping end ------------

#------------ recon-all script--------
export SUBJECTS_DIR=/PATH/TO/DATA
recon-all -s OUTPUT_DIR -i INPUT_DATA

# Note: User could also implement a single step in the reconstruction process or use -autorecon1 directive to
# check mask quality. (for more details, please refer to https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all)