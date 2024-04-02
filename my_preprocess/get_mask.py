import os
import argparse


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject_path", type=str, default="/data/chenziang/codes/GaussianAvatars/data/my_074")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = arg_parser()
    subject_path = args.subject_path
    trial_path = os.listdir(subject_path)
    for trial in trial_path:
        if not (trial.startswith("EMO") or trial.startswith("EXP")):
            continue
        print(trial)
        img_path = os.path.join(subject_path, trial, "images_raw")
        mask_path = os.path.join(subject_path, trial, "fg_masks")
        print(f"img_path: {img_path}")
        print(f"output_path: {mask_path}")
        cmd=f"python /data/chenziang/codes/SplattingAvatar/preprocess/IMavatar/preprocess/submodules/face-parsing.PyTorch/test.py --dspth {img_path} --respth {mask_path}"
        os.system(cmd)
        

