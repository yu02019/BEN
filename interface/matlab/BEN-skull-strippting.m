function BEN_infer(input_path, ben_output_path, weight)

command = ['python infer.py -i ', input_path, ' -o ', ben_output_path, ' -w ', weight];
system(command);

end
