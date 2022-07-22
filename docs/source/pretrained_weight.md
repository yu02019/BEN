# Pretained weight

We provide all trained weight here via [Google Drive](https://drive.google.com/file/d/1aBrvDWtXRcLbwj3lKCln9SIcF-WWOt1D/view?usp=sharing). Users can deploy BEN as an out-of-the-box tool instantly if their data domain are contained within the after-mentioned lists.

In detail, for the introduction of a new dataset, we suggest that the user do as follows.
1) First, use BEN to load the pretrained weights for the closest corresponding species.
2) Consider labeling several scans to fine-tune the model if the pretrained weights do not yield satisfactory performance or the target species is beyond the scope of our datasets. The domain transfer procedures will be performed automatically, without human intervention.

Pretrained weight list:

| Mouse            | Rat            | Marmoset           | Macaque           | Human                                          |
|------------------|----------------|--------------------|-------------------|------------------------------------------------|
| Mouse-T2WI-11.7T | Rat-T2WI-11.7T | Marmoset-T2WI-9.4T | Macaque-T1WI-4.7T | Human-T1WI-3T <br/>(trained on three datasets) |
| Mouse-T2WI-9.4T  | Rat-T2WI-9.4T  | Marmoset-EPI-9.4T  | Macaque-T1WI-3T   | Human-T1WI-ABCD-3T                             |
| Mouse-T2WI-7T    | Rat-T2WI-7T    |                    | Macaque-T1WI-1.5T | Human-T1WI-UKB-3T                              |
| Mouse-EPI-11.7T  | Rat-EPI-9.4T   |                    |                   | Human-T1WI-ZIB-3T                              |
| Mouse-EPI-9.4T   |                |                    |                   |                                                |
| Mouse-SWI-11.7T  |                |                    |                   |                                                |
| Mouse-ASL-11.7T  |                |                    |                   |                                                |


(T2WI: Anatomical MRI; EPI: Functional MRI.)
