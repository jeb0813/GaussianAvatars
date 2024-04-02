import os
from PIL import Image
import argparse

cam_dic={
    "222200042":"00",
    "222200044":"01",
    "222200046":"02",
    "222200040":"03",
    "222200036":"04",
    "222200048":"05",
    "220700191":"06",
    "222200041":"07",
    "222200037":"08",
    "222200038":"09",
    "222200047":"10",
    "222200043":"11",
    "222200049":"12",
    "222200039":"13",
    "222200045":"14",
    "221501007":"15",
}

def bg_remove(video_path,img_path):
    # cam_id: camera id
    # img_path: path of the image
    # save_path: path to save the image
    cmd = "CUDA_VISIBLE_DEVICES=3 python /data/chenziang/codes/SplattingAvatar/preprocess/IMavatar/preprocess/submodules/RobustVideoMatting/segmentation_api.py --input {video_path} --output {img_path}".format(video_path=video_path, img_path=img_path)
    os.system(cmd)

def rename_and_change_bg(input_path,output_path, cam_id,bg_color="white"):
    # input_path: path of the image
    # output_path: path to save the image
    # bg_color: background color
    imgs=os.listdir(input_path)
    for img in imgs:
        img_path=os.path.join(input_path,img)
        new_image_path=os.path.join(output_path,img.split(".")[0]+"_"+cam_id+".png")
        # 打开图像
        image = Image.open(img_path)
        # 创建一个白色背景的新图像
        new_image = Image.new("RGB", image.size, bg_color)
    
        # 将原始图像粘贴到新图像上
        new_image.paste(image, (0, 0), image)
    
        # 保存新图像
        new_image.save(new_image_path)

        # 删除原图像
        os.remove(img_path)

def trial_handler(trial_path):
    vids=os.listdir(trial_path)
    images_raw_path=os.path.join(trial_path,"images_raw")
    if not os.path.exists(images_raw_path):
        os.mkdir(images_raw_path)
    for vid in vids:
        if not vid.startswith("cam"):
            continue
        # 去掉后缀
        cam_name=(vid.split(".")[0]).split("_")[1]
        cam_id=cam_dic[cam_name]
        video_path=os.path.join(trial_path,vid)
        img_path=os.path.join(trial_path,"bg_removed",cam_id)
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        bg_remove(video_path,img_path)

        rename_and_change_bg(img_path,images_raw_path,cam_id)

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--subject_path", type=str, default="/data/chenziang/codes/GaussianAvatars/data/my_074")
    args = parser.parse_args()
    return args

if __name__=="__main__":
    args=get_args()
    subject_path=args.subject_path

    # EMO1234EXP234589
    trial_path=os.listdir(subject_path)
    for trial in trial_path:
        if not (trial.startswith("EMO") or trial.startswith("EXP")):
            continue
        print(trial)
        trial_path=os.path.join(subject_path,trial)
        trial_handler(trial_path)


    # rename_and_change_bg("/data/chenziang/codes/GaussianAvatars/data/my_074/EXP-2-eyes/temp","00")