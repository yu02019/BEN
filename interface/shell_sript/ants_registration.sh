#------------ path ----------
input_path=/PATH/...
ben_output_path=/PATH/...
weight=/PATH/...
FIXED_IMAGE=/PATH/...
output_path=/PATH/...

# ------------ skull-stripping start ------------
python infer.py -i $input_path -o $ben_output_path -w $weight
# ------------ skull-stripping end ------------

#------------ registration script--------
cd $ben_output_path

for i in *
do
echo processing: $i
if [ ! -f "$output_path/$i" ];then
antsRegistrationSyN.sh -d 3 -n 10 -o $output_path/$i -f $FIXED_IMAGE -m $i
fi
done
