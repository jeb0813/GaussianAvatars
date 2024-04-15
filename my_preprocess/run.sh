pwd="/data/chenziang/codes/GaussianAvatars"
subject_path="/data/chenziang/codes/GaussianAvatars/data_mead/M003/neutral"
frame_path="/images_raw"

# # downsample vids before running
# echo "downsample videos"
# python /data/chenziang/codes/GaussianAvatars/my_preprocess/down_smaple.py --subject_path=$subject_path


# step1: background/foreground segmentation
source deactivate
source activate splatting

echo "background/foreground segmentation"  
python bg_remove.py --subject_path=$subject_path

source deactivate

# step2: 3D face reconstruction
source deactivate
source activate mtracker

# python MICA_helper.py --subject_path=$subject_path --opt="pre_opt"

# cd "/data/chenziang/codes/metrical-tracker/MICA"
# python demo.py
# cd $pwd

# python MICA_helper.py --subject_path=$subject_path --opt="post_opt"

# run mtracker
python MICA_helper.py --subject_path=$subject_path --opt="mtracker"

# cp and rename
# python MICA_helper.py --subject_path=$subject_path --opt="cp"

source deactivate