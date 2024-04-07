import numpy as np
import os

npy_path="E:/Data/Datasets/GA/NeRSemble/104/cluster/ikarus/sqian/project/dynamic-head-avatars/code/multi-view-head-tracker/export/104_EXP-2_v16_DS2-0.5x_lmkSTAR_teethV3_SMOOTH_offsetS_whiteBg_maskBelowLine/flame_param/00000.npz"

npz=np.load(npy_path)
print(npz.files)
# ['translation', 'rotation', 'neck_pose', 'jaw_pose', 'eyes_pose', 'shape', 'expr', 'static_offset']

# 遍历所有数据，打印shape
for key in npz.files:
    print(key, npz[key].shape)
    if key=="rotation":
        print(npz[key])

    