% run skull-stripping before analysis
BEN_infer(input_path, ben_output_path, weight)

% 1) use GUI window of spm
run('spm');

% 2) use customized function
spm_batch(...)