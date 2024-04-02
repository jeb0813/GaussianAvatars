import os 
import json
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

cam_dic_reverse={v:k for k,v in cam_dic.items()}

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--subject_path", type=str, default="/data/chenziang/codes/GaussianAvatars/data/my_074")
    parser.add_argument("--opt", type=str)
    args = parser.parse_args()
    return args

def write_trial(trial_path,cam_metadata_path):
    # we don't need know how these fucking params comes from so we borrow it 

    # "cx": 274.83734130859375,
    # "cy": 400.87847900390625,
    # "fl_x": 2048.657958984375,
    # "fl_y": 2048.683349609375,
    # "h": 802,
    # "w": 550,
    # "camera_angle_x": 0.26687315349380775,
    # "camera_angle_y": 0.3865834169367763,

    json_path_train=os.path.join(trial_path,"transforms_train.json")
    json_path_test=os.path.join(trial_path,"transforms_test.json")
    json_path_val=os.path.join(trial_path,"transforms_val.json")

    # 先为每个json写入上面注释里的内容
    with open(json_path_train, 'w') as f:
        json.dump({
            "cx": 274.83734130859375,
            "cy": 400.87847900390625,
            "fl_x": 2048.657958984375,
            "fl_y": 2048.683349609375,
            "h": 802,
            "w": 550,
            "camera_angle_x": 0.26687315349380775,
            "camera_angle_y": 0.3865834169367763
        }, f)

    # Write to transforms_test.json
    with open(json_path_test, 'w') as f:
        json.dump({
            "cx": 274.83734130859375,
            "cy": 400.87847900390625,
            "fl_x": 2048.657958984375,
            "fl_y": 2048.683349609375,
            "h": 802,
            "w": 550,
            "camera_angle_x": 0.26687315349380775,
            "camera_angle_y": 0.3865834169367763
        }, f)

    # Write to transforms_val.json
    with open(json_path_val, 'w') as f:
        json.dump({
            "cx": 274.83734130859375,
            "cy": 400.87847900390625,
            "fl_x": 2048.657958984375,
            "fl_y": 2048.683349609375,
            "h": 802,
            "w": 550,
            "camera_angle_x": 0.26687315349380775,
            "camera_angle_y": 0.3865834169367763
        }, f)

    # 为train和test写入"camera_indices":

    with open(json_path_train, 'r') as f:
        data = json.load(f)
        data["camera_indices"]=[0,1,2,3,4,5,6,7,9,10,11,12,13,14,15]
    with open(json_path_train, 'w') as f:
        json.dump(data, f)
    
    with open(json_path_test, 'r') as f:
        data = json.load(f)
        data["camera_indices"]=[0,1,2,3,4,5,6,7,9,10,11,12,13,14,15]
    with open(json_path_test, 'w') as f:
        json.dump(data, f)

    with open(json_path_val, 'r') as f:
        data = json.load(f)
        data["camera_indices"]=[8]
    with open(json_path_val, 'w') as f:
        json.dump(data, f)
    
    # 遍历flame_param文件夹，获取ply文件总数
    ply_path=os.path.join(trial_path,"flame_param")
    ply_files=os.listdir(ply_path)
    ply_files=[file for file in ply_files if file.endswith(".ply")]
    ply_files.sort()
    total_frames=len(ply_files)

    # 为train和val写入"timestep_indices"，range(0, total_frames*2//3)
    # test写入range(total_frames*2//3, total_frames)

    with open(json_path_train, 'r') as f:
        data = json.load(f)
        data["timestep_indices"]=list(range(0, total_frames*2//3))
    with open(json_path_train, 'w') as f:
        json.dump(data, f)
    
    with open(json_path_val, 'r') as f:
        data = json.load(f)
        data["timestep_indices"]=list(range(0, total_frames*2//3))
    with open(json_path_val, 'w') as f:
        json.dump(data, f)

    with open(json_path_test, 'r') as f:
        data = json.load(f)
        data["timestep_indices"]=list(range(total_frames*2//3, total_frames))
    with open(json_path_test, 'w') as f:
        json.dump(data, f)
    
    cam_metadata=json.load(open(cam_metadata_path))


    """
    这块需要重构，但是先用着吧
    """
    # 先读train
    with open(json_path_train, 'r') as f:
        data = json.load(f)
    timestep_indices=data["timestep_indices"]
    camera_indices=data["camera_indices"]

    # 创建frames列表
    frames=[]


    for timestep in timestep_indices:
        for camera_index in camera_indices:
            str_camera_index="{:02d}".format(camera_index)
            # print(str_camera_index)
            frame={
                "timestep_index":timestep,
                "camera_index":camera_index,
                # camera_index需要是两位数字，左侧补0
                "camera_id":cam_dic_reverse[str_camera_index],
                "cx":data["cx"],
                "cy":data["cy"],
                "fl_x":data["fl_x"],
                "fl_y":data["fl_y"],
                "h":data["h"],
                "w":data["w"],
                "camera_angle_x":data["camera_angle_x"],
                "camera_angle_y":data["camera_angle_y"],
                "transform_matrix":cam_metadata["world_2_cam"][cam_dic_reverse[str_camera_index]],
                "file_path":"images_raw/{:04d}_{:02d}.png".format(timestep,camera_index),
                "flame_param_path":"flame_param/{:02d}.ply".format(timestep)
            }
            frames.append(frame)

    # frames写入train
    data["frames"]=frames
    with open(json_path_train, 'w') as f:
        json.dump(data, f)

    # 读test
    with open(json_path_test, 'r') as f:
        data = json.load(f)
    timestep_indices=data["timestep_indices"]
    camera_indices=data["camera_indices"]

    # 创建frames列表
    frames=[]
    for timestep in timestep_indices:
        for camera_index in camera_indices:
            frame={
                "timestep_index":timestep,
                "camera_index":camera_index,
                "camera_id":cam_dic_reverse[str_camera_index],
                "cx":data["cx"],
                "cy":data["cy"],
                "fl_x":data["fl_x"],
                "fl_y":data["fl_y"],
                "h":data["h"],
                "w":data["w"],
                "camera_angle_x":data["camera_angle_x"],
                "camera_angle_y":data["camera_angle_y"],
                "transform_matrix":cam_metadata["world_2_cam"][cam_dic_reverse[str_camera_index]],
                "file_path":"images_raw/{:04d}_{:02d}.png".format(timestep,camera_index),
                "flame_param_path":"flame_param/{:02d}.ply".format(timestep)
            }
            frames.append(frame)
    
    # frames写入test
    data["frames"]=frames
    with open(json_path_test, 'w') as f:
        json.dump(data, f)
    
    # 读val
    with open(json_path_val, 'r') as f:
        data = json.load(f)
    timestep_indices=data["timestep_indices"]
    camera_indices=data["camera_indices"]

    # 创建frames列表
    frames=[]
    for timestep in timestep_indices:
        for camera_index in camera_indices:
            frame={
                "timestep_index":timestep,
                "camera_index":camera_index,
                "camera_id":cam_dic_reverse[str_camera_index],
                "cx":data["cx"],
                "cy":data["cy"],
                "fl_x":data["fl_x"],
                "fl_y":data["fl_y"],
                "h":data["h"],
                "w":data["w"],
                "camera_angle_x":data["camera_angle_x"],
                "camera_angle_y":data["camera_angle_y"],
                "transform_matrix":cam_metadata["world_2_cam"][cam_dic_reverse[str_camera_index]],
                "file_path":"images_raw/{:04d}_{:02d}.png".format(timestep,camera_index),
                "flame_param_path":"flame_param/{:04d}.ply".format(timestep)
            }
            frames.append(frame)
    
    # frames写入val
    data["frames"]=frames
    with open(json_path_val, 'w') as f:
        json.dump(data, f)
    







if __name__ == '__main__':
    args = get_args()
    subject_path=args.subject_path
    cam_metadata_path="/data/chenziang/codes/GaussianAvatars/data/my_074/camera_params.json"
    trial_paths=os.listdir(subject_path)

    for trial in trial_paths:
        if not (trial.startswith("EMO") or trial.startswith("EXP")):
            continue
        print(trial)
        write_trial(os.path.join(subject_path,trial),cam_metadata_path)
        # exit()
