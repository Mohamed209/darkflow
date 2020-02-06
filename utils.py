import xml.etree.cElementTree as ET


def box_to_yolo(size: tuple, box: tuple):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x, y, w, h)


def create_voc_annotations(w, h, annotation_dir: str, image_name: str, objects: list, res_folder: str, dims: tuple, other=False):
    root = ET.Element("annotations")
    ET.SubElement(root, "folder").text = "images"
    ET.SubElement(root, "filename").text = image_name
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(w)
    ET.SubElement(size, "height").text = str(h)
    ET.SubElement(size, "depth").text = "3"
    for sobj in objects:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = sobj
        bbox = ET.SubElement(obj, "bndbox")
        if not other:
            ET.SubElement(bbox, "xmin").text = str(dims[0])
            ET.SubElement(bbox, "ymin").text = str(dims[1])
            ET.SubElement(bbox, "xmax").text = str(dims[2])
            ET.SubElement(bbox, "ymax").text = str(dims[3])
        else:
            ET.SubElement(bbox, "xmin").text = str(dims[0]-100)
            ET.SubElement(bbox, "ymin").text = str(dims[1]-100)
            ET.SubElement(bbox, "xmax").text = str(dims[2]+100)
            ET.SubElement(bbox, "ymax").text = str(dims[3]+100)
    tree = ET.ElementTree(root)
    tree.write(annotation_dir+image_name.split('.')[0]+'.xml')
