import os
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject_path", type=str, default="/data/chenziang/codes/GaussianAvatars/data/my_074")
    args = parser.parse_args()
    return args


if __name__=="__main__":
    args=get_args()
    subject_path=args.subject_path

    for vid in os.listdir(subject_path):
        if not vid.endswith(".mp4"):
            continue
        video_path=os.path.join(subject_path,vid)
        down_sample_path=os.path.join(subject_path,vid.split(".")[0]+"_25.mp4")
        cmd="ffmpeg -i {} -r 25 {}".format(video_path,down_sample_path)
        os.system(cmd)
        # 删除原视频
        os.remove(video_path)
        # 重命名
        os.rename(down_sample_path,video_path)
    print(f"down sample {video_path} done!")
 