
from flask import Flask, render_template, Response, request, send_file, jsonify
import cv2
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import numpy as np
import pandas as pd
import json
import requests
from pathlib import Path
from posixpath import join

from utils.faiss_processing import MyFaiss
from utils.submit import write_csv, show_csv
from utils.bert_processing import BERTSearch
from utils.ocr_processing import fill_ocr_results, fill_ocr_df
from utils.sequence_search_processing import get_sequence_frame_order
from utils.object_processing import filter_by_objects

# http://0.0.0.0:5001/thumbnailimg?index=0

# app = Flask(__name__, template_folder='templates', static_folder='static')
app = Flask(__name__, template_folder='templates/front-end')

# Faiss
bin_file= 'dataset/clip-features-vit-b32/clip-features-vit-b32/'


json_path = 'dict/keyframes_id.json'
json_id2img_path = 'dict/dict_id2img_path.json'
json_img2id_path = 'dict/dict_img2id_path.json'
json_keyframe2id = 'dict/keyframe_path2id.json'

json_object_thr01 = 'dict/object_all_s_thr01.json'
json_object_thr02 = 'dict/object_all_s_thr02.json'
json_object_thr03 = 'dict/object_all_s_thr03.json'
json_object_thr05 = 'dict/object_all_s_thr05.json'
json_object_thr005 = 'dict/object_all_s_thr005.json'

# with open("dict/info_ocr.txt", "r", encoding="utf8") as fi:
#     ListOcrResults = list(map(lambda x: x.replace("\n",""), fi.readlines()))

# with open("dict/info_asr.txt", "r", encoding="utf8") as fi: 
#     ListASRResults = list(map(lambda x: x.replace("\n",""), fi.readlines()))
# df_asr = pd.read_csv("dict/info_asr.txt", delimiter=",", header=None)
# df_asr.columns = ["video_id", "frame_id", "asr"]    
        
with open(json_id2img_path, 'r') as f:
    DictId2Img = json.loads(f.read())

with open(json_img2id_path, 'r') as f:
    DictImg2Id = json.loads(f.read())

with open(json_keyframe2id, 'r') as f:
    DictKeyframe2Id = json.loads(f.read())
    
with open(json_path, 'r') as f:
    DictGlobalId2Path = json.loads(f.read())
    
# with open(json_object_thr01, 'r') as f:
#     Dict_Img2Objs_thr01 = json.loads(f.read())
    
thresholds = {}

with open(json_object_thr05, 'r') as f:
    thresholds['0.5'] = json.loads(f.read())

with open(json_object_thr03, 'r') as f:
    thresholds['0.3'] = json.loads(f.read())

with open(json_object_thr02, 'r') as f:
    thresholds['0.2'] = json.loads(f.read())

with open(json_object_thr01, 'r') as f:
    thresholds['0.1'] = json.loads(f.read())
    
with open(json_object_thr005, 'r') as f:
    thresholds['0.05'] = json.loads(f.read())

CosineFaiss = MyFaiss('Database', bin_file, json_path)
DictImagePath = CosineFaiss.id2img_fps
LenDictPath = len(CosineFaiss.id2img_fps)
print("LenDictPath: ", LenDictPath)
# CosineFaiss.id2img_fps

# BERT
# MyBert = BERTSearch(dict_bert_search='dict/keyframes_id_bert.json', bin_file='dict/faiss_bert.bin', mode='search')

@app.route('/thumbnailimg')
def thumbnailimg():
    print("load_iddoc")

    # remove old file submit 
    submit_path = join("submission", "submit.csv")
    old_submit_path = Path(submit_path)
    if old_submit_path.is_file():
        os.remove(submit_path)
        # open(submit_path, 'w').close()

    pagefile = []
    index = int(request.args.get('index'))
    if index == None:
        index = 0

    imgperindex = 100
    
    # imgpath = request.args.get('imgpath') + "/"
    pagefile = []

    page_filelist = []
    list_idx = []

    if LenDictPath-1 > index+imgperindex:
        first_index = index * imgperindex
        last_index = index*imgperindex + imgperindex

        tmp_index = first_index
        while tmp_index < last_index:
            page_filelist.append(DictImagePath[tmp_index]["image_path"])
            list_idx.append(tmp_index)
            tmp_index += 1    
    else:
        first_index = index * imgperindex
        last_index = LenDictPath

        tmp_index = first_index
        while tmp_index < last_index:
            page_filelist.append(DictImagePath[tmp_index]["image_path"])
            list_idx.append(tmp_index)
            tmp_index += 1    

    for imgpath, id in zip(page_filelist, list_idx):
        pagefile.append({'imgpath': imgpath, 'id': id})

    data = {'num_page': int(LenDictPath/imgperindex)+1, 'pagefile': pagefile}
    
    return render_template('index_thumb.html', data=data)

@app.route('/imgsearch')
def image_search():
    print("image search")
    k = int(request.args.get('k_value'))

    pagefile = []
    id_query = int(request.args.get('imgid'))
    _, list_ids, _, list_image_paths = CosineFaiss.image_search(id_query, k=k)

    imgperindex = 100 

    for imgpath, id in zip(list_image_paths, list_ids):
        pagefile.append({'imgpath': imgpath, 'id': int(id)})

    data = {'num_page': int(LenDictPath/imgperindex)+1, 'pagefile': pagefile}
    
    return render_template('index_thumb.html', data=data)


@app.route('/textsearch')
def text_search():
    print("text search")
    k = int(request.args.get('k_value'))
    pagefile = []
    text_query = request.args.get('textquery')
    _, list_ids, _, list_image_paths = CosineFaiss.text_search(text_query, k=k)

    print('text_query: ', text_query)

    imgperindex = 100 

    for imgpath, id in zip(list_image_paths, list_ids):
        # print(imgpath)
        if (int(imgpath[41:-4]) == 1): continue        
        pagefile.append({'imgpath': imgpath, 'id': int(id)})
        # print(imgpath)
# dataset/Keyframes_L19/keyframes/L19_V046/
    # data = {'num_page': int(LenDictPath/imgperindex)+1, 'pagefile': pagefile, 'mode': "Text", 'query': text_query}
    data = {'num_page': int(LenDictPath/imgperindex)+1, 'pagefile': pagefile, 'mode': "Text", 'query': text_query.replace(' ','_')}
    
    return render_template('index_thumb.html', data=data)

@app.route('/sequencesearch')
def sequence_search():
    print ('sequence search')
    print(request.args.get('k_value'))
    k = int(request.args.get('k_value'))
    pagefile = []
    images_start = []
    images_next = []
    
    text_query_start = request.args.get('text_start')
    text_query_next = request.args.get('text_nextframes')
    
    # list_ids_start
    scores_start, _, _, list_image_paths_start = CosineFaiss.text_search(text_query_start, k=k)
    scores_end, _, _, list_image_paths_next = CosineFaiss.text_search(text_query_next, k=k)
    
    # print('scores_start: ', scores_start)        

    imgperindex = 100 

    for imgpath in list_image_paths_start:
        images_start.append(imgpath[32:-4])
    for imgpath in list_image_paths_next:
        images_next.append(imgpath[32:-4])

    frames = get_sequence_frame_order(images_start, images_next, scores_start[0], scores_end[0])

    for i in frames:
        imgpath = f'dataset/Keyframes_{i[:3]}/keyframes/{i}.jpg'
        id = DictKeyframe2Id[imgpath]
        pagefile.append({'imgpath': imgpath, 'id': int(id)})
    
    data = {'num_page': int(LenDictPath/imgperindex)+1, 'pagefile': pagefile, 'mode': 'Sequence', 'query1': text_query_start.replace(' ','_'), 'query2': text_query_next.replace(' ','_')}
    
    return render_template('index_thumb.html', data=data)

    ################################################ brute force ################################################
    # pairs, weak_pairs, frames_in_both = get_sequence_frame(images_start, images_next)
    
    # for i in pairs + weak_pairs:
    #     tmp_imgpath_first = f'dataset/Keyframes_{i[0][:3]}/keyframes/{i[0]}.jpg'
    #     tmp_imgpath_last = f'dataset/Keyframes_{i[1][:3]}/keyframes/{i[1]}.jpg'
        
    #     tmp_id_first = DictKeyframe2Id[tmp_imgpath_first]
    #     tmp_id_last = DictKeyframe2Id[tmp_imgpath_last]
        
    #     tmp_imgpath_mids = []
    #     tmp_id_mids = []
    #     for midid in range(int(tmp_id_first), int(tmp_id_last)):
    #         midid = str(midid)
    #         tmp_id_mids.append(midid)
    #         tmp_imgpath_mids.append(DictGlobalId2Path[midid]["image_path"])
        
    #     for imgpath, id in zip([tmp_imgpath_first] + tmp_imgpath_mids + [tmp_imgpath_last], [tmp_id_first] + tmp_id_mids + [tmp_id_last]):
    #         pagefile.append({'imgpath': imgpath, 'id': int(id)})
            
    # for i in frames_in_both:
    #     imgpath = f'dataset/Keyframes_{i[:3]}/keyframes/{i}.jpg'
    #     id = DictKeyframe2Id[imgpath]
    #     pagefile.append({'imgpath': imgpath, 'id': int(id)})
    
    # data = {'num_page': int(LenDictPath/imgperindex)+1, 'pagefile': pagefile}
    
    # return render_template('index_thumb.html', data=data)
    ################################################ brute force ################################################

@app.route('/objectfilter')
def object_filter():
    print ('object filter')
    pagefile = []
    k = int(request.args.get('k_value'))
    images = []
    imgperindex = 100 
    
    text_query = request.args.get('textquery')
    obj_filter = list(map(lambda x: x.lower(), request.args.get('objects').split(',')))
    threshold = request.args.get('threshold')
    mode_search = request.args.get('operator')
    # threshold = 0.3
    dict_obj_thr = thresholds[threshold]
    
    _, _, _, list_image_paths = CosineFaiss.text_search(text_query, k=k)
    for imgpath in list_image_paths:
        if (int(imgpath[41:-4]) == 1): continue
        images.append(imgpath[32:-4])
    
    images_filtered = filter_by_objects(images, obj_filter, dict_obj_thr,  mode_search = mode_search)
    print('obj want to filter: ', obj_filter)
    
    for i in images_filtered:
        imgpath = f'dataset/Keyframes_{i[:3]}/keyframes/{i}.jpg'
        id = DictKeyframe2Id[imgpath]
        pagefile.append({'imgpath': imgpath, 'id': int(id)})

    data = {'num_page': int(LenDictPath/imgperindex)+1, 'pagefile': pagefile}
    
    return render_template('index_thumb.html', data=data)

# @app.route('/asrsearch')
# def asrsearch():
#     print("asr search")
#      # remove old file submit 

#     pagefile = []
#     text_query = request.args.get('text_asr')
#     _, list_ids, _, list_image_paths = MyBert.bert_search(text_query, k=100)

#     imgperindex = 100 

#     for imgpath, id in zip(list_image_paths, list_ids):
#         imgpath = imgpath.replace("\\","/")
#         pagefile.append({'imgpath': imgpath, 'id': int(DictKeyframe2Id[imgpath])})

#     data = {'num_page': int(LenDictPath/imgperindex)+1, 'pagefile': pagefile}
    
#     return render_template('index_thumb.html', data=data)

# @app.route('/ocrfilter')
# def ocrfilter():
#     print("ocr search")

#     pagefile = []
#     text_query = request.args.get('text_ocr')

#     list_all = fill_ocr_results(text_query, ListOcrResults)
#     list_all.extend(fill_ocr_results(text_query, ListASRResults))

#     # list_all = fill_ocr_df(text_query, df_ocr)
#     # list_all = np.vstack((list_all, fill_ocr_df(text_query, df_ocr)))
    
#     print("list results of ocr + asr: ", list_all)

#     imgperindex = 100 

#     for frame in list_all:
#         list_frame_name = frame.split("/")
#         keyframe_dir = list_frame_name[0][:7]
#         video_dir = list_frame_name[0]
#         new_frame_name = list_frame_name[-1]
#         frame_in_video_path =  join("Database", "KeyFrames"+keyframe_dir, video_dir, new_frame_name)
#         frame_in_video_path =  frame_in_video_path.replace("\\","/")
#         # print("frame_in_video_path: ", frame_in_video_path)
#         if frame_in_video_path in DictKeyframe2Id:
#             print("frame_in_video_path: ", frame_in_video_path)
#             frame_id_in_video_path = DictKeyframe2Id[frame_in_video_path]
#             pagefile.append({'imgpath': frame_in_video_path, 'id': int(frame_id_in_video_path)})

#     data = {'num_page': int(LenDictPath/imgperindex)+1, 'pagefile': pagefile}
    
#     return render_template('index_thumb.html', data=data)

@app.route('/showsegment')
def show_segment():
    print("showsegment")
    id_query = int(request.args.get('imgid'))
    img_path = DictGlobalId2Path[str(id_query)]["image_path"][32:-4]
    print(img_path)
    
    return(search_image_path(img_path))
    
    # pagefile = []

    # list_shot_path = DictImagePath[id_query]['list_shot_path']
    
    # imgperindex = 100 
    # for shot_info in list_shot_path:
    #     pagefile.append({'imgpath': shot_info['shot_path'], 'id': int(DictKeyframe2Id[shot_info['shot_path']])})

    # # show  around 200 key image
    # frame_path = DictImagePath[id_query]["image_path"]
    # list_split = frame_path.split("/")
    # keyframe_dir = list_split[1][-7:]
    # video_dir = list_split[2]
    # image_name = list_split[3]


    # total_image_in_video = int(DictImg2Id[keyframe_dir][video_dir]["total_image"])
    # number_image_id_in_video = int(DictImg2Id[keyframe_dir][video_dir][image_name])

    # first_index_in_video = number_image_id_in_video-40 if number_image_id_in_video-40>0 else 0
    # last_index_in_video = number_image_id_in_video+40 if number_image_id_in_video+40<total_image_in_video else total_image_in_video
    # frame_index = first_index_in_video
    # while frame_index < last_index_in_video:
    #     new_frame_name = DictId2Img[keyframe_dir][video_dir][str(frame_index)]
    #     frame_in_video_path =  join("Database", "KeyFrames"+keyframe_dir, video_dir, new_frame_name)
    #     frame_in_video_path =  frame_in_video_path.replace("\\","/")
    #     if frame_in_video_path in DictKeyframe2Id:
    #         frame_id_in_video_path = DictKeyframe2Id[frame_in_video_path]
    #         pagefile.append({'imgpath': frame_in_video_path, 'id': int(frame_id_in_video_path)})

    #     frame_index += 1

    # data = {'num_page': int(LenDictPath/imgperindex)+1, 'pagefile': pagefile}
    
    # return render_template('index_thumb.html', data=data)

@app.route('/writecsv')
def submit():
    print("writecsv")
    info_key = request.args.get('info_key')
    mode_write_csv = request.args.get('mode')
    print("info_key", info_key)
    print("mode: ", mode_write_csv)
    info_key = info_key.split(",")

    id_query = int(info_key[0])
    selected_image = info_key[1]
    
    number_line, list_frame_id = write_csv(DictImagePath, mode_write_csv, selected_image, id_query, "submission")
    
    str_fname = ",".join(list_frame_id[:])
    # str_fname += " #### number csv line: {}".format(number_line)

    info = {
        "str_fname": str_fname,
        "number_line": str(number_line)
    }

    return jsonify(info)

@app.route('/get_img')
def get_img():
    # print("get_img")
    fpath = request.args.get('fpath')
    # fpath = fpath
    list_image_name = fpath.split("/")
    image_name = "/".join(list_image_name[-2:])

    if os.path.exists(fpath):
        img = cv2.imread(fpath)
    else:
        print("load 404.jph")
        img = cv2.imread("./static/images/404.jpg")

    img = cv2.resize(img, (1280,720))

    # print(img.shape)
    img = cv2.putText(img, image_name, (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 
                   3, (255, 0, 0), 4, cv2.LINE_AA)

    ret, jpeg = cv2.imencode('.jpg', img)
    return  Response((b'--frame\r\n'
                     b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/dowload_submit_file', methods=['GET'])
def dowload_submit_file():
    print("dowload_submit_file")
    filename = request.args.get('filename')
    fpath = join("submission", filename)
    print("fpath", fpath)

    return send_file(fpath, as_attachment=True)

@app.route('/get_first_row')
def getFirstRowOfCsv():
    csv_path = "submission/submit.csv"
    result = {
        'video_id':"None",
        'frame_id':"None"
    }
    if os.path.exists(csv_path):
        lst_frame = show_csv(csv_path)[0]
        video_id, frame_id = lst_frame.split("/")[-2:]
        result["video_id"] = video_id
        result["frame_id"] = int(frame_id[:-4])

    return result

@app.route('/visualize')
def visualize():
    number_of_query = int(request.args.get('number_of_query'))
    csv_path = join("submission", "query-{}.csv".format(number_of_query))

    query_path = join("query","query-{}.txt".format(number_of_query))
    if os.path.exists(query_path):
        with open(query_path, "rb") as fi:
            query_content = fi.read().decode("utf-8").replace(" ","_")

    pagefile = []
    lst_frame = show_csv(csv_path)
    for frame_path in lst_frame:
        frame_id = DictKeyframe2Id[frame_path]
        pagefile.append({'imgpath': frame_path, 'id': int(frame_id)})
    if query_content is not None:
        data = {'num_page': 1, 'pagefile': pagefile, 'query': query_content}
    else:
        data = {'num_page': 1, 'pagefile': pagefile}

    return render_template('index_thumb.html', data=data)

@app.route('/search_image_path')
def search_image_path(frame_path = None):
    pagefile = []
    frame_path = request.args.get('frame_path') if not(frame_path) else frame_path
    query = frame_path
    if (len (frame_path) <= 9):
        
        pass
    else:
        frame_path_origin = frame_path
        
        list_frame_split = frame_path.split("/")

        video_dir = list_frame_split[0]
        image_name = list_frame_split[1] + ".jpg"
        keyframe_dir = video_dir[:-2]

        frame_path = join("dataset", "Keyframes"+ "_" + keyframe_dir.split("_")[0],"keyframes", video_dir, image_name)
        frame_path = frame_path.replace("\\","/")
        frame_id = DictKeyframe2Id[frame_path]
        print("frame_id: ", frame_id)
        
        imgperindex = 100 
        pagefile.append({'imgpath': frame_path, 'id': int(frame_id)})
        # print(pagefile)
        # print (frame_path)
        
        # pass
        
        # TODO Show img_padding before and after
        img_padding = 40
        
        list_split = frame_path.split("/")
        keyframe_dir = list_split[1]
        video_dir = list_split[-2]
        image_name = list_split[-1]

        # total_image_in_video = int(DictImg2Id[keyframe_dir][video_dir]["total_image"])        
        # frame_ids = [i for i in range(max(1, int(list_frame_split[1]) - img_padding), min(int(list_frame_split[1]) + img_padding + 1, total_image_in_video))]        
        # tmp_append = [{'imgpath': frame_path[:-8] + DictId2Img[keyframe_dir][video_dir][str(i)], 'id': int(DictKeyframe2Id[frame_path[:-8] + DictId2Img[keyframe_dir][video_dir][str(i)]])} for i in frame_ids]
        
        frame_ids = [i for i in range(max(1, int(frame_id) - img_padding), min(int(frame_id) + img_padding + 1, 328829))]   
        tmp_append = [{'imgpath': DictGlobalId2Path[str(i)]['image_path'], 'id': i} for i in frame_ids]
        
        # print(keyframe_dir)
        # print (image_name)
        # print (tmp_append)
        
        pagefile += tmp_append
        
        

        # dataset/Keyframes_L01/L01_V001/0001.jpg
        # dataset/Keyframes_L01/keyframes/L01_V001/0001.jpg

        # # show  around 30 key image
        # total_image_in_video = int(DictImg2Id[keyframe_dir][video_dir]["total_image"])
        # number_image_id_in_video = int(DictImg2Id[keyframe_dir][video_dir][image_name])

        # # print(DictKeyframe2Id)

        # first_index_in_video = number_image_id_in_video-40 if number_image_id_in_video-40>0 else 0
        # last_index_in_video = number_image_id_in_video+40 if number_image_id_in_video+40<total_image_in_video else total_image_in_video

        # frame_index = first_index_in_video
        # while frame_index < last_index_in_video:
        #     new_frame_name = DictId2Img[keyframe_dir][video_dir][str(frame_index)]
        #     frame_in_video_path =  join("Database", "KeyFrames"+keyframe_dir, video_dir, new_frame_name)
        #     frame_in_video_path = frame_in_video_path.replace("\\","/")
        #     if frame_in_video_path in DictKeyframe2Id:
        #         frame_id_in_video_path = DictKeyframe2Id[frame_in_video_path]
        #         pagefile.append({'imgpath': frame_in_video_path, 'id': int(frame_id_in_video_path)})

        id_query = video_dir
        # id_query = frame_path_origin
        #     frame_index += 1
        print('query =', query)
        link, keyframe = get_url(query)
        print(link)
        print(keyframe)
        data = {'num_page': int(LenDictPath/imgperindex)+1, 'pagefile': pagefile, 'youtube_url': link, 'keyframe_id': int(keyframe), 'mode': 'Image' , 'query': query}
    
    return render_template('index_thumb.html', data=data)


def get_url(query):
    # to do after
    print(query)
    folder, id = query.split('/')
    print(folder)
    id = int(id)
    print(id)
    path = folder.split('_')[0]
    csv_path = f'map_frame_id/MapKeyframe_{path}/{folder}.csv'
    json_path = f'dataset/New_Metadata/{folder}.json'

    if not os.path.exists(csv_path) or not os.path.exists(json_path):
        print("CSV/json file does not exist.")
        print(csv_path)
        print(json_path)
        return

    df = pd.read_csv(csv_path)
    df.set_index('n', inplace=True)

    try:
        output = df.at[id, 'frame_idx']
        pts_time = df.at[id, 'pts_time']
    except KeyError:
        print('except key error')
        return

    with open(json_path, 'r', encoding="utf8") as json_file:
        json_data = json.load(json_file)
    watch_url = json_data.get('watch_url', '')

    minutes = int(pts_time // 60)  # Get the whole minutes
    seconds = int(pts_time % 60)  # Get the remaining seconds

    link = f"{watch_url}&t={minutes}m{seconds}s"

    return link, output

@app.route('/submit_img')
def submit_img(session = "node0daps0nu1p57w1xda7c5bybauu3047"):
    id = request.args.get('id')
    item = id.split("/")[0]
    frame = request.args.get('frame')
    url = f"https://eventretrieval.one/api/v1/submit?item={item}&frame={frame}&session={session}"
    print(url)
    r = requests.get(url=url)
    response_data = r.json()  # Get the JSON content from the response
    return jsonify(response_data)

if __name__ == '__main__':
    submit_dir = "submission"
    if not os.path.exists(submit_dir):
        os.mkdir(submit_dir)

    app.run(debug=True, host="0.0.0.0", port=5001)
