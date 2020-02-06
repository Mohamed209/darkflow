from PIL import Image
from utils import create_voc_annotations
import json
import os
import cv2
import xml.etree.cElementTree as ET
'''
convert images and json format data into YOLOv2 (VOC) training format image,box file pairs

'''


class DataPreprocessor:
    def __init__(self, elctrification_pole_path='../raw_data/cantilever/', other_path='../raw_data/other/', output_path='../processed_data/train/'):
        self.elctrification_pole_path = elctrification_pole_path
        self.other_path = other_path
        self.output_path = output_path
        self._classes = {'electric_poles': 0, 'balise': 1,
                         'trafficsignals': 2, 'varioussignals': 3}

    def process_electrification_poles_data(self):
        path = self.elctrification_pole_path
        image_path = path+'frames/'
        label_path = path+'labels/'
        all_data = zip(sorted(os.listdir(image_path)),
                       sorted(os.listdir(label_path)))
        for (png, annot) in all_data:
            with open(label_path+annot)as file:
                label = json.load(file)
            points = label['output']['objects'][0]['bndbox']
            xmin, xmax, ymin, ymax = points[1][1], points[1][0], points[3][1], points[3][0]
            if int(xmin) > int(xmax) or int(ymin) > int(ymax):
                continue
            im = Image.open(image_path+png)
            w = int(im.size[0])
            h = int(im.size[1])
            # im.save(self.output_path+'images/'+png.split('.')[0]+'.jpg')
            create_voc_annotations(w, h, annotation_dir=self.output_path+'labels/',
                                   objects=['electric_poles'],
                                   image_name=png.split('.')[0]+'.jpg', res_folder=self.output_path+'images/', dims=(int(xmin), int(ymin), int(xmax), int(ymax)))

    def process_other_data(self):
        path = self.other_path
        image_path = path + 'frames/'
        label_path = path + 'labels/'
        all_data = zip(sorted(os.listdir(image_path)),
                       sorted(os.listdir(label_path)))
        for (png, annot) in all_data:
            im = Image.open(image_path+png)
            w = int(im.size[0])
            h = int(im.size[1])
            with open(label_path+annot)as file:
                label = json.load(file)
            for obj in label['output']['objects']:
                if obj['classTitle'] == 'sleepers' or obj['classTitle'] == 'sleeper':
                    continue
                xmin, xmax, ymin, ymax = obj['points']['exterior'][0][0], obj['points']['exterior'][
                    1][0], obj['points']['exterior'][0][1], obj['points']['exterior'][1][1]
                if int(xmin) > int(xmax) or int(ymin) > int(ymax):
                    continue
                try:
                    # append annotations
                    tree = ET.parse(self.output_path+'labels/' +
                                    annot.split('.')[0]+'.xml')
                    root = tree.getroot()
                    sobj = ET.SubElement(root, "object")
                    ET.SubElement(sobj, "name").text = obj['classTitle']
                    bbox = ET.SubElement(sobj, "bndbox")
                    ET.SubElement(bbox, "xmin").text = str(int(xmin-100))
                    ET.SubElement(bbox, "ymin").text = str(int(ymin-100))
                    ET.SubElement(bbox, "xmax").text = str(int(xmax+100))
                    ET.SubElement(bbox, "ymax").text = str(int(ymax+100))
                    tree.write(self.output_path+'labels/' +
                               annot.split('.')[0]+'.xml')
                except FileNotFoundError:
                    # copy new image and write new xml annotations
                    im.save(self.output_path+'images/' +
                            png.split('.')[0]+'.jpg')
                    create_voc_annotations(w, h, annotation_dir=self.output_path+'labels/',
                                           objects=[obj['classTitle']],
                                           image_name=png.split('.')[0]+'.jpg', res_folder=self.output_path+'images/', dims=(int(xmin), int(ymin), int(xmax), int(ymax)), other=True)

                # txt_outfile.write(
                #    str(self._classes[obj['classTitle']]) + " " + " ".join([str(a) for a in bb]) + '\n')


if __name__ == "__main__":
    processor = DataPreprocessor()
    processor.process_electrification_poles_data()
    processor.process_other_data()
