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

    # json_path_train=os.path.join(trial_path,"transforms_train.json")
    # json_path_test=os.path.join(trial_path,"transforms_test.json")
    # json_path_val=os.path.join(trial_path,"transforms_val.json")
    json_path = os.path.join(trial_path,"transforms.json")
    with open(json_path, 'w') as f:
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

    # 写入"camera_indices":

    with open(json_path, 'r') as f:
        data = json.load(f)
        data["camera_indices"]=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    with open(json_path, 'w') as f:
        json.dump(data, f)

    # 遍历flame_param文件夹，获取ply文件总数
    ply_path=os.path.join(trial_path,"flame_param")
    ply_files=os.listdir(ply_path)
    ply_files=[file for file in ply_files if file.endswith(".ply")]
    ply_files.sort()
    total_frames=len(ply_files)

    # l写入"timestep_indices"，range(0, total_frames)
    with open(json_path, 'r') as f:
        data = json.load(f)
        data["timestep_indices"]=list(range(0, total_frames))
    with open(json_path, 'w') as f:
        json.dump(data, f)

    cam_metadata=json.load(open(cam_metadata_path))



    with open(json_path, 'r') as f:
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
                "flame_param_path":"flame_param/{:04d}.ply".format(timestep)
            }
            frames.append(frame)

    # frames写入
    data["frames"]=frames
    with open(json_path, 'w') as f:
        json.dump(data, f)

    

def write_union_trainval(trainval_trials,union_path,subject_path):
    """
    除了cam08全写入train，cam08写入val
    """
    global cnt
    union_train_json_path=os.path.join(union_path,"transforms_train.json")
    union_val_json_path=os.path.join(union_path,"transforms_val.json")

    with open(union_train_json_path, 'w') as f:
        json.dump({
            "cx": 274.83734130859375,
            "cy": 400.87847900390625,
            "fl_x": 2048.657958984375,
            "fl_y": 2048.683349609375,
            "h": 802,
            "w": 550,
            "camera_angle_x": 0.26687315349380775,
            "camera_angle_y": 0.3865834169367763,
            "camera_indices": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                9,
                10,
                11,
                12,
                13,
                14,
                15
            ]
        }, f)
    
    with open(union_val_json_path, 'w') as f:
        json.dump({
            "cx": 274.83734130859375,
            "cy": 400.87847900390625,
            "fl_x": 2048.657958984375,
            "fl_y": 2048.683349609375,
            "h": 802,
            "w": 550,
            "camera_angle_x": 0.26687315349380775,
            "camera_angle_y": 0.3865834169367763,
            "camera_indices": [
                8
            ]
        }, f)

    for trial in trainval_trials:
        trial_path=os.path.join(subject_path,trial)
        trial_json_path=os.path.join(trial_path,"transforms.json")



        with open(trial_json_path, 'r') as f:
            data = json.load(f)
        trial_frames=data["frames"]
        trial_timestep_indices=data["timestep_indices"]

        n=len(trial_timestep_indices)

        # time_indices 要根据cnt做偏移
        trial_timestep_indices=[i+cnt for i in trial_timestep_indices]

        # frames的timestep_index也要做偏移
        # frames的file_path和flame_param_path要补全到绝对路径

        # 判断是写入train还是val
        frames_train=[]
        frames_val=[]
        # timestep_indices是一样的

        for frame in trial_frames:
            frame["timestep_index"]+=cnt
            frame["file_path"]=os.path.join(trial_path,frame["file_path"])
            frame["flame_param_path"]=os.path.join(trial_path,frame["flame_param_path"])

            if frame["camera_index"]==8:
                frames_val.append(frame)
            else:
                frames_train.append(frame)

        
        cnt+=n



        # 写入union的json
        with open(union_train_json_path, 'r') as f:
            data = json.load(f)
        # 先判断是否存在frames字段
        if "frames" in data:
            data["frames"].extend(frames_train)
        else:
            data["frames"]=frames_train
        # 再判断是否存在timestep_indices字段
        if "timestep_indices" in data:
            data["timestep_indices"].extend(trial_timestep_indices)
        else:
            data["timestep_indices"]=trial_timestep_indices
        with open(union_train_json_path, 'w') as f:
            json.dump(data, f)
        
        with open(union_val_json_path, 'r') as f:
            data = json.load(f)
        # 先判断是否存在frames字段
        if "frames" in data:
            data["frames"].extend(frames_val)
        else:
            data["frames"]=frames_val
        # 再判断是否存在timestep_indices字段
        if "timestep_indices" in data:
            data["timestep_indices"].extend(trial_timestep_indices)
        else:
            data["timestep_indices"]=trial_timestep_indices
        with open(union_val_json_path, 'w') as f:
            json.dump(data, f)


def write_union_test(test_trials,union_path,subject_path):
    """
    写入所有帧
    """
    global cnt
    union_test_json_path=os.path.join(union_path,"transforms_test.json")
    # 先写入固定的部分
    with open(union_test_json_path, 'w') as f:
        json.dump({
            "cx": 274.83734130859375,
            "cy": 400.87847900390625,
            "fl_x": 2048.657958984375,
            "fl_y": 2048.683349609375,
            "h": 802,
            "w": 550,
            "camera_angle_x": 0.26687315349380775,
            "camera_angle_y": 0.3865834169367763,
            "camera_indices": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
            ]
        }, f)
    
    for trial in test_trials:
        trial_path=os.path.join(subject_path,trial)
        test_json_path=os.path.join(trial_path,"transforms.json")

        with open(test_json_path, 'r') as f:
            data = json.load(f)
        test_frames=data["frames"]
        test_timestep_indices=data["timestep_indices"]

        n=len(test_timestep_indices)

        # # 这里的indice不是从0开始的，再做一次shift
        # shift=test_timestep_indices[0]
        # time_indices 要根据cnt做偏移
        test_timestep_indices=[i+cnt for i in test_timestep_indices]

        # frames的timestep_index也要做偏移
        # frames的file_path和flame_param_path要补全到绝对路径

        for frame in test_frames:
            frame["timestep_index"]+=cnt
            frame["file_path"]=os.path.join(trial_path,frame["file_path"])
            frame["flame_param_path"]=os.path.join(trial_path,frame["flame_param_path"])

        cnt+=n

        # 写入union的json
        with open(union_test_json_path, 'r') as f:
            data = json.load(f)
        # 先判断是否存在frames字段
        if "frames" in data:
            data["frames"].extend(test_frames)
        else:
            data["frames"]=test_frames

        # 再判断是否存在timestep_indices字段
        if "timestep_indices" in data:
            data["timestep_indices"].extend(test_timestep_indices)
        else:
            data["timestep_indices"]=test_timestep_indices
        with open(union_test_json_path, 'w') as f:
            json.dump(data, f)
        
    







if __name__ == '__main__':
    args = get_args()
    subject_path=args.subject_path
    cam_metadata_path="/data/chenziang/codes/GaussianAvatars/data/my_074/camera_params.json"
    trial_paths=os.listdir(subject_path)


    # 这里实际应该写入所有的数据，不需要划分，但是不想改了
    # 更新了，只写一个文件，划分交给下一步做
    for trial in trial_paths:
        if not (trial.startswith("EMO") or trial.startswith("EXP")):
            continue
        print(trial)
        write_trial(os.path.join(subject_path,trial),cam_metadata_path)
        # exit()

    # 写入Union的json
    # train中是除了trial的除了08的所有camera
    # test中是trial的所有camera
    # val中是除了trial的camera 08
    
    # 先读txt
    Union_path=os.path.join(subject_path,"Union_074")
    test_txt_path=os.path.join(Union_path,"sequences_test.txt")
    trainval_txt_path=os.path.join(Union_path,"sequences_trainval.txt")

    
    cnt=0

    with open(trainval_txt_path,"r") as f:
        trainval_trials=f.readlines()
        trainval_trials=[trial.strip() for trial in trainval_trials]
    

    with open(test_txt_path,"r") as f:
        test_trials=f.readlines()
        test_trials=[trial.strip() for trial in test_trials]
    
    write_union_trainval(trainval_trials,Union_path,subject_path)
    write_union_test(test_trials,Union_path,subject_path)
    