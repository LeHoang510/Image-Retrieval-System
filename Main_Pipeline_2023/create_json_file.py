import os
import json

# ====================================================================================================


id2img_json_path = 'dict_/dict_id2img_path.json'
img2id_json_path = 'dict_/dict_img2id_path.json'
keyframe_path2id_path = 'dict_/keyframe_path2id.json'
keyframe_id_path = 'dict_/keyframes_id.json'

KEYFRAME_LST = [folder for folder in os.listdir('dataset/') if 'Keyframes' in folder]
KEYFRAME_LST.sort()
# KEYFRAME_LST = ['Keyframes_L01']

# ====================================================================================================

def to_dict(keyframe_path, type):
    original_path = 'dataset/' + keyframe_path + '/keyframes'

    folder_lst = os.listdir(original_path)

    dict_keyframe = {}
    for folder in folder_lst:
        folder_path = os.path.join(original_path, folder)
        file_lst = os.listdir(folder_path)

        dict_keyframe_sub = {}
        total_images = 0

        for i, file in enumerate(file_lst):
            if type == 'id2img':
                dict_keyframe_sub[int(total_images)] = str(i).zfill(4) + '.jpg'
            else:
                dict_keyframe_sub[str(i).zfill(4) + '.jpg'] = int(total_images)
            total_images += 1

        dict_keyframe_sub['total_image'] = total_images
        dict_keyframe[folder] = dict_keyframe_sub

    return {keyframe_path: dict_keyframe}

# ====================================================================================================

def run_all_keyframe(type):
    dict_keyframe = {}
    for keyframe_path in KEYFRAME_LST:
        dict_keyframe.update(to_dict(keyframe_path, type))
    return dict_keyframe

# ====================================================================================================


def keyframe_path2id():
    dict_keyframe = {}
    count = 0
    for keyframe_path in KEYFRAME_LST:
        original_path = 'dataset/' + keyframe_path + '/keyframes'

        folder_lst = os.listdir(original_path)

        for folder in folder_lst:
            folder_path = os.path.join(original_path, folder)
            file_lst = os.listdir(folder_path)
            for file in file_lst:
                file_path = os.path.join(folder_path, file)
                dict_keyframe[file_path] = str(count)
                count += 1

    print(len(dict_keyframe))
    return dict_keyframe

# ====================================================================================================

def keyframe_id():
    dict_keyframe = {}
    count = 0
    for keyframe_path in KEYFRAME_LST:
        original_path = 'dataset/' + keyframe_path + '/keyframes'

        folder_lst = os.listdir(original_path)

        for folder in folder_lst:
            folder_path = os.path.join(original_path, folder)
            file_lst = os.listdir(folder_path)
            for file in file_lst:
                file_path = os.path.join(folder_path, file)
                dict_keyframe[str(count)] = {"image_path":file_path}
                count += 1

    print(len(dict_keyframe))
    return dict_keyframe

# ====================================================================================================

dict_keyframe_path2id = keyframe_path2id()
with open(keyframe_path2id_path, 'w') as json_file:
    json.dump(dict_keyframe_path2id, json_file, indent=4)

dict_id2img = run_all_keyframe(type='id2img')
with open(id2img_json_path, 'w') as json_file:
    json.dump(dict_id2img, json_file, indent=4)

dict_img2id = run_all_keyframe(type='img2id')
with open(img2id_json_path, 'w') as json_file:
    json.dump(dict_img2id, json_file, indent=4)

dict_keyframe_id = keyframe_id()
with open(keyframe_id_path, 'w') as json_file:
    json.dump(dict_keyframe_id, json_file, indent=4)