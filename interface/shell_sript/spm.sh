#------------ path ----------
input_path=/PATH/...
ben_output_path=/PATH/...
weight=/PATH/...

# ------------ skull-stripping start ------------
python infer.py -i $input_path -o $ben_output_path -w $weight
# ------------ skull-stripping end ------------

#------------ spm script--------
matlab -r 'run spm_batch.m'
