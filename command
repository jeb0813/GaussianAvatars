source activate gaussian-avatars
conda deactivate

git clone https://github.com/ShenhanQian/GaussianAvatars.git --recursive

# Install CUDA and ninja for compilation
conda install -c "nvidia/label/cuda-11.6" cuda-toolkit ninja

# ==== for Linux ====
ln -s "$CONDA_PREFIX/lib" "$CONDA_PREFIX/lib64"  # to avoid error "/usr/bin/ld: cannot find -lcudart"

# re-activate the environment to make the above eonvironment variables effective
conda deactivate
source activate gaussian-avatars

# Install PyTorch (make sure the CUDA version match with the above)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu116

# or
conda install pytorch torchvision pytorch-cuda=11.6 -c pytorch -c nvidia
# make sure torch.cuda.is_available() returns True

# Install the rest pacakges (can take a while to compile diff-gaussian-rasterization, simple-knn, and nvdiffrast)
pip install -r requirements.txt

# hipconfig error
https://github.com/microsoft/DeepSpeed/issues/3814#issuecomment-1764849256


CUDA_VISIBLE_DEVICES=3 bash train.sh

Optimizing output/UNION10EMOEXP_306_eval_600k
Output folder: output/UNION10EMOEXP_306_eval_600k [23/03 19:39:08]



CUDA_VISIBLE_DEVICES=2 bash train_gpu2.sh
CUDA_VISIBLE_DEVICES=3 bash train_gpu3.sh
CUDA_VISIBLE_DEVICES=3 python my_train.py -s /data/chenziang/codes/GaussianAvatars/data/074/cluster/ikarus/sqian/project/dynamic-head-avatars/code/multi-view-head-tracker/export/UNION10_074_EMO1234EXP234589_v16_DS2-0.5x_lmkSTAR_teethV3_SMOOTH_offsetS_whiteBg_maskBelowLine -m /data/chenziang/codes/GaussianAvatars/output/UNION10EMOEXP_074_eval_600k --port 60000 --eval --white_background --bind_to_mesh

CUDA_VISIBLE_DEVICES=2 python my_train.py \
-s /data/chenziang/codes/GaussianAvatars/data/074/cluster/ikarus/sqian/project/dynamic-head-avatars/code/multi-view-head-tracker/export/UNION10_074_EMO1234EXP234589_v16_DS2-0.5x_lmkSTAR_teethV3_SMOOTH_offsetS_whiteBg_maskBelowLine \
-m output/UNION10EMOEXP_074_eval_600k \
--port 60000 --eval --white_background --bind_to_mesh