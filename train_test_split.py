import os
import shutil
import random
import sys
import xml.etree.cElementTree as ET
import imgaug.augmenters as iaa
import numpy
import cv2

seq = iaa.OneOf([
    # Add gaussian noise
    iaa.AdditiveGaussianNoise(scale=(30, 60)),
    # Resize each image to something between 50 and 100% of its original size
    iaa.Resize((0.5, 1.0)),
    # Change images to grayscale and overlay them with the original image by varying strengths, effectively removing 0 to 100% of the color
    iaa.Grayscale(alpha=(0.0, 1.0)),
    # Median blur
    iaa.MedianBlur(k=(3, 7)),
    # Motion Blur
    iaa.MotionBlur(angle=(0, 288)),
    # Add a value to all pixels in an image
    iaa.Add((-45, 45)),
    # Making the image darker or brighter
    iaa.Multiply((0.5, 1.5)),
    # Add salt an pepper noise
    iaa.SaltAndPepper((0.03, 0.05))
])


def train_test_split(ratio):
    images = os.listdir('images/')
    labels = os.listdir('c_annotations/')
    all_data = list(zip(sorted(images), sorted(labels)))
    random.shuffle(all_data)
    for element in all_data[:int(ratio*len(images))]:
        tree = ET.parse('c_annotations/'+element[1])
        childs = tree.getroot().getchildren()
        for ch in childs:
            if ch.tag == 'object' and ch.getchildren()[0].text in ['balise', 'varioussignals', 'trafficsignals']:
                # augment image
                im = cv2.imread('images/'+element[0])
                augs = [seq.augment_image(im) for i in range(10)]
                for idx, aug in enumerate(augs):  # save augs
                    cv2.imwrite('train-images/'+'aug'+str(idx)+element[0], aug)
                    shutil.copy('c_annotations/' +
                                element[1], 'train-labels/'+'aug'+str(idx)+element[1])
                break
        shutil.copy('images/'+element[0], 'train-images/')
        shutil.copy('c_annotations/' + element[1], 'train-labels/')
    for element in all_data[int(ratio*len(images)):]:
        shutil.copy('images/'+element[0], 'test-images/')
        shutil.copy('c_annotations/'+element[1], 'test-labels/')


if __name__ == "__main__":
    train_test_split(float(sys.argv[1]))
