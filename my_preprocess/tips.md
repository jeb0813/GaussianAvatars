# 生成json反而是最后一步  

# 首先需要camera_params.json  
这里先直接套用数据集里的，没有标注的数据再说  

# 背景分割  
/data/chenziang/codes/SplattingAvatar/preprocess/IMavatar/preprocess/my_preprocess_v2.sh  
echo "background/foreground segmentation"  
cd $path_rvm  
python -m segmentation_api --input $video_path --output $img_path  
 