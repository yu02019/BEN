#------------ path ----------
input_path=/PATH/...
ben_output_path=/PATH/...
weight=/PATH/...

# ------------ skull-stripping start ------------
python infer.py -i $input_path -o $ben_output_path -w $weight
# ------------ skull-stripping end ------------

# ------ input --------
datadirs=/PATH
ref=/PATH/MNI152_T2_2mm_brain.nii.gz
prefix=dti20160803
# ------ core code -------
cd $datadirs
for s in *
do
echo coregristration of the diffusion indices to MNI space: $s
if [ ! -f "$s/diff2standard.mat" ];then
# estimate
flirt  -in $s/nodif_brain -ref $ref -omat $s/diff2standard.mat
# invert the affine matrix
convert_xfm -omat $s/standard2diff.mat -inverse $s/diff2standard.mat
# write
flirt -in $s/nodif_brain -ref $ref -out $s/MNI_nodif_brain -applyxfm -init $s/diff2standard.mat
flirt -in $s/${prefix}_FA -ref $ref -out $s/MNI_${prefix}_FA -applyxfm -init $s/diff2standard
flirt -in $s/${prefix}_MD -ref $ref -out $s/MNI_${prefix}_MD -applyxfm -init $s/diff2standard
flirt -in $s/${prefix}_L1 -ref $ref -out $s/MNI_${prefix}_L1 -applyxfm -init $s/diff2standard
flirt -in $s/${prefix}_L2 -ref $ref -out $s/MNI_${prefix}_L2 -applyxfm -init $s/diff2standard
flirt -in $s/${prefix}_L3 -ref $ref -out $s/MNI_${prefix}_L3 -applyxfm -init $s/diff2standard
fslmaths $s/${prefix}_L3 -add ${s}/${prefix}_L2 -div 2 ${s}/${prefix}_L23
flirt -in $s/${prefix}_L23 -ref $ref -out $s/MNI_${prefix}_L23 -applyxfm -init $s/diff2standard
fi
done