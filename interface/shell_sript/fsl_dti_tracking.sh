#------------ path ----------
input_path=/PATH/...
ben_output_path=/PATH/...
weight=/PATH/...

# ------------ skull-stripping start ------------
python infer.py -i $input_path -o $ben_output_path -w $weight
# ------------ skull-stripping end ------------

# ---input------
datadir=/PATH/...
g_table=/PATH/...
# this gradient table should made by bvecs,such like b30.txt ,see more in onenote.
bval=1000
b0=1
nex=2
pref=dtk

#-----core code-----
cd $datadir
for i in *
do
echo dtk recon:$i
if [ ! -f "${datadir}/${i}/${pref}_tensor.nii" ];then
dti_recon "${datadir}/${i}/data.nii.gz" "${datadir}/${i}/${pref}" -gm "${g_table}" -b ${bval} -b0 $b0 -nex $nex -sn 1 -ot nii
fi
done

#------------input--------

datadir=/PATH
pref=dtk
param=' -fact -l 0.5 -at 60  -it nii -iz'
# fact:tracking arithmetic. 60 angle. see more open console type 'dti_tracker' for help
# -iz:-invert z compoent(s) of vector(in this demo use -iz,normolly,should try 3 times for best results)
ref=/PATH/MNI152_T1_2mm_brain.nii.gz

#-----core code-------
cd $datadir
for i in *
do echo Fiber tracking:$i
if [ ! -f "${datadir}/${i}/${pref}.trk" ];then
dti_tracker "${datadir}/${i}/${pref}" "${datadir}/${i}/${pref}.trk" -m "${datadir}/${i}/${pref}_dwi.nii"  -m2 "${datadir}/${i}/${pref}_fa.nii" 0.2 1 $param
fi
echo Normalize fiber into standard space:${i}
if [ ! -f "${datadir}/${i}/MNI_${pref}.trk" ];then
track_transform ${datadir}/${i}/${pref}.trk  ${datadir}/${i}/MNI_${pref}.trk -src  ${datadir}/${i}/${pref}_b0.nii -ref $ref -reg  ${datadir}/${i}/diff2standard.mat
fi
done