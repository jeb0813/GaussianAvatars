pwd="/data/chenziang/codes/GaussianAvatars"
subject_path="/data/chenziang/codes/GaussianAvatars/data/my_074"
frame_path="/images_raw"
mask_path="/fg_masks"

# # downsample vids before running
# echo "downsample videos"
# python /data/chenziang/codes/GaussianAvatars/my_preprocess/down_smaple.py --subject_path=$subject_path

# # step1: background/foreground segmentation
# source deactivate
# source activate splatting

# echo "background/foreground segmentation"  
# python bg_remove.py --subject_path=$subject_path

# source deactivate

# # step2: mask/senmantic segmentation
# echo "semantic segmentation with face parsing"
# source deactivate
# source activate splatting
# python get_mask.py --subject_path=$subject_path
# source deactivate

# step3: 3D face reconstruction
# source deactivate
# source activate mtracker

# python MICA_helper.py --subject_path=$subject_path --opt="pre_opt"

# cd "/data/chenziang/codes/metrical-tracker/MICA"
# python demo.py
# cd $pwd

# python MICA_helper.py --subject_path=$subject_path --opt="post_opt"

# # run mtracker
# python MICA_helper.py --subject_path=$subject_path --opt="mtracker"

# # cp and rename
# python MICA_helper.py --subject_path=$subject_path --opt="cp"

# source deactivate


# step4: write json
source deactivate
source activate gaussian-avatars
python json_writer.py --subject_path=$subject_path

source deactivate
