source activate gaussian-avatars

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