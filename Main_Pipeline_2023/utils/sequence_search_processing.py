from functools import reduce
import numpy as np


def get_sequence_frame_order(l1: list, l2: list, scores1: list, scores2: list):
    # l1_unique = l1.copy()    
    # l2_unique = l2.copy()
    
    dict_fr2id_l1 = {}
    dict_fr2score_l1 = {}
    dict_fr2score_l2 = {}
    for i, fr in enumerate(l1):
        dict_fr2id_l1[fr] = i
        dict_fr2score_l1[fr] = scores1[i]
        
    for i, fr in enumerate(l2):
        dict_fr2score_l2[fr] = scores2[i]
    
    l1.sort()
    l2.sort()
    
    vid_l1 = [i[:8] for i in l1]
    vid_l2 = [i[:8] for i in l2]

    vid_l1_unique = list(np.unique(vid_l1))
    vid_l2_unique = list(np.unique(vid_l2))
    vid_all_unique = []
    dict_vid2imgs = {}
    # dict_vid2scores = {}
    dict_vid_2_avgscore = {}
    # fr_l1 = [int(i[9:]) for i in l1]
    # fr_l2 = [int(i[9:]) for i in l2]
    
    images_all_unique = l1+l2
    images_all_unique.sort()
    images_all_unique = list(np.unique(images_all_unique))
    
    images_all_a2z = []
    for i in images_all_unique:
        tmp_vid = i[:8]
        if (tmp_vid in vid_l1_unique and tmp_vid in vid_l2_unique):
            images_all_a2z.append(i)
            
            if not(tmp_vid in dict_vid2imgs.keys()):
                if not(i in l1):
                    continue
                
                vid_all_unique.append(tmp_vid)
                dict_vid_2_avgscore[tmp_vid] = 0
                dict_vid2imgs[tmp_vid] = []
                
            dict_vid2imgs[tmp_vid].append(i)
            
            tmp_score = 0
            if (i in l1 and i in l2):
                tmp_score = (dict_fr2score_l1[i] + dict_fr2score_l2[i]) / 2
            elif (i in l1):
                tmp_score = dict_fr2score_l1[i]
            else:
                tmp_score = dict_fr2score_l2[i]
                
            dict_vid_2_avgscore[tmp_vid] += tmp_score
            
        else:
            print ("appear in only 1 query:", i)

    for v in dict_vid2imgs:
        dict_vid_2_avgscore[v] /= len(dict_vid2imgs[v])
        
    vids_ordered_by_score = sorted(dict_vid_2_avgscore, key=lambda i: dict_vid_2_avgscore[i])
    
    dict_vid2imgs_ordered = {}
    for i in vids_ordered_by_score:
        dict_vid2imgs_ordered[i] = dict_vid2imgs[i]
    images_ordered_by_score = reduce(lambda x, y: x + y, dict_vid2imgs_ordered.values())

    return images_ordered_by_score
    


def get_sequence_frame(l1: list, l2: list):
    l1_orig = l1.copy()    
    dict_fr2id_l1 = {}
    for i, fr in enumerate(l1):
        dict_fr2id_l1[fr] = i
    
    l1.sort()
    l2.sort()
    
    vid_l1 = [i[:8] for i in l1]
    vid_l2 = [i[:8] for i in l2]

    # fr_l1 = [int(i[9:]) for i in l1]
    # fr_l2 = [int(i[9:]) for i in l2]
    
    # Get first frame of each video in L1
    l1_min = [l1[0]]    
    curr_vid = vid_l1[0]

    i = 0
    for f in l1[1:]:
        i += 1
        if (curr_vid != vid_l1[i]):
            l1_min.append(f)
            curr_vid = vid_l1[i]

    # Get last frame of each video in L1
    l2_reserve = l2
    l2_reserve.reverse()

    curr_vid = vid_l2[-1]
    l2_max = [l2[-1]]

    i = len(l2) - 1
    for f in l2_reserve[1:]:
        i -= 1
        if (curr_vid != vid_l2[i]):
            l2_max[:0] = [f]
            curr_vid = vid_l2[i]        
    del(l2_reserve)

    pairs, weak_pairs, frames_in_both = mapping_two_framelist(l1_min, l2_max)
        
    print (len(pairs))
    print (pairs[:10])
    print (weak_pairs)
    print (frames_in_both)
    
    dict_pairs2order = {}
    for i in pairs:
        dict_pairs2order[i] = dict_fr2id_l1[i[0]]
    
    pairs = sorted(dict_pairs2order, key=lambda i: dict_pairs2order[i])
    # print (len(pairs))
    # print (pairs[:10])
    
    return pairs.copy(), weak_pairs.copy(), frames_in_both.copy()
    

# def mapping_two_framelist_bruteforce(l1_min, l2_max):
def mapping_two_framelist(l1_min, l2_max):
    i2 = 0
    v2 = l2_max[i2][:8]
    f2 = l2_max[i2][9:]
    
    pairs = []
    weak_pairs = []
    frames_in_both = []

    for i1 in range(len(l1_min)):
        v1 = l1_min[i1][:8]
        if (v1 < v2): continue
            
        while (i2 < len(l2_max) and v1 > l2_max[i2]):
            i2 += 1
            
        if (i2 >= len(l2_max)): break
        
        v2 = l2_max[i2][:8]
        if (v1 < v2): continue
        
        f1 = int(l1_min[i1][9:])
        f2 = int(l2_max[i2][9:])
        
        if (f1 < f2):
            pairs.append ((l1_min[i1], l2_max[i2]))
        elif (f1 == f2):
            frames_in_both.append(l1_min[i1])
        elif (f1 > f2 - 2):
            # weak_pairs.append ((l2_max[i2], l1_min[i1]))
            pass
        
    return pairs, weak_pairs, frames_in_both
            
    print (len(pairs))
    print (pairs)
    print (frames_in_both)
        