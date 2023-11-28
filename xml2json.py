import xml.etree.ElementTree as ET
import json
import os

# 解析XML文件
tree = ET.parse(r'semantic_annotation\annotations_2.xml')
root = tree.getroot()
# os.makedirs(output_dir, exist_ok=True)
output_folder = "json_all"
os.makedirs(output_folder, exist_ok=True)
# 创建一个空列表，用于存储解析后的形状数据

# 遍历XML中的所有<image>元素
for image_element in root.findall('image'):
    shapes = []
    xml_dict = {}
    image_name = image_element.get('name')
    image_width = image_element.get('width')
    image_height = image_element.get('height')
    xml_dict = {
        'version' : r"5.2.1",
        "flags" : {},
        'imagePath' : image_name,
        'imageData' : None,
        'imageHeight' : int(image_height),
        'imageWidth' : int(image_width),
    }
    for polygon_element in image_element.findall('polygon'):
        polygon_label = polygon_element.get('label')
        polygon_points = polygon_element.get('points')
        polygon_group_id = None
        polygon_description = ""
        polygon_shape_type = "polygon"
        polygon_flags = {}

        # 创建一个形状字典
        shape = {
            'label': polygon_label,
            'points': [],
            'group_id': polygon_group_id,
            'description': polygon_description,
            'shape_type': polygon_shape_type,
            'flags': polygon_flags
        }

        # 解析多边形点坐标并添加到形状字典中
        for point in polygon_points.split(';'):
            x, y = map(float, point.split(','))
            shape['points'].append([x, y])

        # 将形状字典添加到形状列表中
        shapes.append(shape)

    xml_dict["shapes"] = shapes
    # json_data = {'shapes': shapes}
    json_string = json.dumps(xml_dict, indent=2,ensure_ascii=False)
    output_path = output_folder +"/"+ image_name.split('.')[0] + ".json"
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_string)
# 打印或保存JSON字符串
# print(json_string)
