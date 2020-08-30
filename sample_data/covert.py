# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
from os import listdir
from os.path import join
 
classes = [ "license-plate","number_plate"] # own data sets which classes which category to write, in the order
 
def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
 
def convert_annotation(image_id):
    in_file = open('images/valid/%s.xml'%(image_id), encoding = 'utf-8')
    out_file = open('labels/valid/%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
 
    for obj in root.iter('object'):
        #difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write("0" + " " + " ".join([str(a) for a in bb]) + '\n')
 
val_percent = 0.1 # test set proportion of the total data set, the default 0.1, if the test set and the training set have been demarcated, the corresponding code is modified
#data_path = 'data/images/train/'# darknet relative path folder, see description github, and they need to modify, according to note here the absolute path can also be used
data_path2 = 'data/images/valid/'
if not os.path.exists('labels/'):
    os.makedirs('labels/')
image_ids = [f for f in os.listdir ( 'images/valid')] # XML data storage folder
#train_file = open('train.txt', 'w')
val_file = open('valid.txt', 'w')
for i, image_id in enumerate(image_ids):
    
         #if image_id [-3:] == "xml": # Sometimes jpg and xml files are placed in the same folder, so to determine what suffixes
        #if i < (len(image_ids) * val_percent):
         #   val_file.write(data_path + '%s\n'%(image_id[:-3] + 'jpg'))
    if image_id[-3:] != "xml":
        val_file.write(data_path2 + '%s\n'%(image_id[:-3] + 'jpg'))
    convert_annotation(image_id[:-4])
    print(data_path2+image_id)
#train_file.close()
val_file.close()
