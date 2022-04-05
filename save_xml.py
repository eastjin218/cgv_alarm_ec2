import os, glob
import cv2
from PIL import Image

import carla
from carla import ColorConverter as cc

SEG_INPUT = '/home/carla_client/carla/add-aas/aas/utils/dataset/tesla_train_50'
TRAIN_INPUT = '/home/carla_client/carla/add-aas/aas/utils/train/tf_object_detection_api/single_model/train'
TEST_INPUT = '/home/carla_client/carla/add-aas/aas/utils/train/tf_object_detection_api/single_model/test'
rend_path = glob.glob(os.path.join(TRAIN_INPUT,'*.jpg'), recursive=True)
seg_path = glob.glob(os.path.join(SEG_INPUT,'segmented-img/**/*.png'), recursive=True)


def get_bbox(img_path):
    array = cv2.imread(img_path)
    array = array[:,:,:3]
    mask = cv2.inRange(array, (141,0,0),(143,0,0))

    _, thresh = cv2.threshold(mask, 127,255,0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boundRect = [None]*len(contours)
    total_area = 0
    for i, c in enumerate(contours):
        contours_poly = cv2.approxPolyDP(c, 3, True)
        boundRect[i] = cv2.boundingRect(contours_poly)
        total_area += cv2.contourArea(c)
    
    if total_area > 2500.0:
        x_min = min([int(boundRect[i][0]) for i in range(len(contours))])
        y_min = min([int(boundRect[i][1]) for i in range(len(contours))])

        x_max = max([int(boundRect[i][0]+boundRect[i][2]) for i in range(len(contours))])
        y_max = max([int(boundRect[i][1]+boundRect[i][3]) for i in range(len(contours))])
    return y_min, y_max, x_min, x_max

def save_xml(img_path, y_min, y_max, x_min, x_max):
    from xml.etree.ElementTree import Element, SubElement, ElementTree
    
    filename = os.path.basename(img_path).split(".")[0]
    root = Element("annotation")
    folder = img_path.split('/')[-2]
    SubElement(root,"folder").text = folder
    SubElement(root,"filename").text = os.path.basename(img_path)
    SubElement(root,"path").text = img_path
    source = SubElement(root,"source")
    SubElement(source, "database").text = "Unknown"

    size = SubElement(root,"size")
    SubElement(size, "width").text = str(1280)
    SubElement(size, "height").text = str(720)
    SubElement(size, "depth").text = "3"
    SubElement(root, 'segmented').text = '0'

    obj = SubElement(root, 'object')
    SubElement(obj, 'name').text = "car"
    SubElement(obj, 'pose').text = 'Unspecified'
    SubElement(obj, 'truncated').text = '0'
    SubElement(obj, 'difficult').text = '0'
    bbox = SubElement(obj, 'bndbox')
    SubElement(bbox, 'xmin').text = str(x_min)
    SubElement(bbox, 'ymin').text = str(y_min)
    SubElement(bbox, 'xmax').text = str(x_max)
    SubElement(bbox, 'ymax').text = str(y_max)

    tree = ElementTree(root)
    output_dir = os.path.join(os.path.split(img_path)[0])
    # print('output_dir: ',output_dir)
    tree.write(f'{output_dir}/{filename}.xml')

for seg_img in seg_path:
    y_min, y_max, x_min, x_max = get_bbox(seg_img)
    tmp_name = os.path.basename(seg_img).split('.')[0]
    file_name = seg_img.split('/')[-2]
    for num in range(0,50):
        raw = os.path.join(TRAIN_INPUT, tmp_name+'_'+file_name+'_'+str(num)+'.jpg')
        if raw in rend_path:
            save_xml(raw, y_min, y_max, x_min, x_max)
        else:
            raw = os.path.join(TEST_INPUT, tmp_name+'_'+file_name+'_'+str(num)+'.jpg')
            save_xml(raw, y_min, y_max, x_min, x_max)

