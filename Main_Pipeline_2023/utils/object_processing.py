# import json
# import os


def filter_by_objects(images: list, obj_filter: list, Dict_Img2Objs: dict, mode_search = 'And', threshold: float = None):
    images_filtered = []
    
    for img in images:
        classes = list(map(lambda x: x.lower(), Dict_Img2Objs[img]['class_detected']))
        
        
        print('obj want to filter: ', obj_filter)
        print('classes: ', classes)
        
        if mode_search.lower() == 'and':
            if (set(obj_filter).issubset(classes)):
                images_filtered.append(img)
        else:
            for obj in obj_filter:
                if (obj in classes):
                    images_filtered.append(img)
                    break
    
    return images_filtered.copy()
