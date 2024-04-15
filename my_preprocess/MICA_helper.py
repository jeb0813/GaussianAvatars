import os
import argparse

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--subject_path", type=str, default="/data/chenziang/codes/GaussianAvatars/data/my_074")
    parser.add_argument("--opt", type=str)
    args = parser.parse_args()
    return args

def pre_opt(subject_path,path):
    # 先保存第一帧提取identity.npy
    for vid in os.listdir(subject_path):
        if not vid.endswith(".mp4"):
            continue
        vid_path=os.path.join(subject_path,vid)
        pic_path=os.path.join(path,vid[:-4]+".png")
        cmd=f"ffmpeg -i {vid_path}  -vframes 1 {pic_path}"
        os.system(cmd)



def post_opt(subject_path,path):
    """
    将视频和identity.npy放入mtracker_path，然后先写yml，再call mtracker
    """
    mtracker_path="/data/chenziang/codes/metrical-tracker/input"
    yml_path="/data/chenziang/codes/metrical-tracker/configs/actors"
    _identity_path="/data/chenziang/codes/metrical-tracker/MICA/demo/output"

    for vid in os.listdir(subject_path):
        if not vid.endswith(".mp4"):
            continue
        vid_path=os.path.join(subject_path,vid)
        identity_path=os.path.join(_identity_path,vid[:-4],"identity.npy")

        # 在input目录下创建目录
        mtracker_vid_path=os.path.join(mtracker_path,vid[:-4])
        if not os.path.exists(mtracker_vid_path):
            os.makedirs(mtracker_vid_path)
        # 将视频和identity.npy放入mtracker_path
        # 视频重命名为video.mp4
        video_path=os.path.join(mtracker_vid_path,"video.mp4")
        cmd=f"cp {vid_path} {video_path}"
        os.system(cmd)

        # 复制identity.npy
        cmd=f"cp {identity_path} {mtracker_vid_path}"
        os.system(cmd)

        # 写yml
        yml_file=os.path.join(yml_path,vid[:-4]+".yml")
        template="actor: './input/{}'\nsave_folder: './output/'\noptimize_shape: true\noptimize_jaw: true\nbegin_frames: 1\nkeyframes: [ 0, 1 ]"
        with open(yml_file,"w") as f:
            f.write(template.format(vid[:-4]))


def mtracker(subject_path,path):
    yml_path="/data/chenziang/codes/metrical-tracker/configs/actors"

    for vid in os.listdir(subject_path):
        if not vid.endswith(".mp4"):
            continue
        yml_file=os.path.join(yml_path,vid[:-4]+".yml")
        print(yml_file)
        # change directory
        os.chdir("/data/chenziang/codes/metrical-tracker")
        cmd=f"python tracker.py --cfg {yml_file}"
        os.system(cmd)


def cp(subject_path,path):
    for vid in os.listdir(subject_path):
        if not vid.endswith(".mp4"):
            continue
        ply_path=os.path.join(subject_path,"flame_param")
        if not os.path.exists(ply_path):
            os.makedirs(ply_path)

        



    trial_path=os.listdir(subject_path)


    for trial in trial_path:
        if not (trial.startswith("EMO") or trial.startswith("EXP")):
            continue

        ply_path=os.path.join(subject_path,trial,"flame_param")
        if not os.path.exists(ply_path):
            os.makedirs(ply_path)

        ori_path=os.path.join("/data/chenziang/codes/metrical-tracker/output",trial[:5]+"_cam_222200037","mesh")
        canonical_path=os.path.join("/data/chenziang/codes/metrical-tracker/output",trial[:5]+"_cam_222200037","canonical.obj")
        cmd=f"cp {canonical_path} {os.path.join(subject_path,trial,'canonical_flame_param.obj')}"
        os.system(cmd)

        for file in os.listdir(ori_path):
            if file.endswith(".ply"):
                # 五位数字文件名变四位数字，去掉一个前导0
                new_file=file[1:]
                cmd=f"cp {os.path.join(ori_path,file)} {os.path.join(ply_path,new_file)}"
                os.system(cmd)
                



if __name__=="__main__":
    args=get_args()
    subject_path=args.subject_path
    opt=args.opt
    path="/data/chenziang/codes/metrical-tracker/MICA/demo/input"
    if opt=="pre_opt":
        print("pre_opt")
        pre_opt(subject_path,path)
    elif opt=="post_opt":
        print("opt")
        post_opt(subject_path,path)
    elif opt=="mtracker":
        print("mtracker")
        mtracker(subject_path,path)
    elif opt=="cp":
        print("cp")
        cp(subject_path,path)
        
        
        