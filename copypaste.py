import cv2
import json
import os
import numpy as np
import utils
from tqdm import tqdm
# 定义标签映射关系
chinese_labels = [
    '签字笔', '手机', '钥匙', '水杯', '登机牌', '身份证', '银行卡', '名片', '充电宝', 
    '耳机', '钱包', '手环', '手表', '头绳', '皮筋', '戒指', '梳子', '其他', 
    '书包', '电脑', '货币', '口红', '耳钉', '硬币', '香烟', '护照', '鼠标', 
    '充电器', 'U盘', '线', '行李箱', '' , '' , '' ,'手'
]
chinese_to_number = {label: index for index, label in enumerate(chinese_labels) if label}

src_folder = './src'
bg_folder = './bg'
json_label_folder = './json'
output_folder = './output'
os.makedirs(output_folder, exist_ok=True)

bg_files = os.listdir(bg_folder)
src_files = os.listdir(src_folder)

times = 100
for times in tqdm(range(times)):
    times -= 1
    bg_name = bg_files[np.random.randint(0, len(bg_files))]
    bg = cv2.imread(os.path.join(bg_folder, bg_name))
    src_name = src_files[np.random.randint(0, len(src_files))]
    src = cv2.imread(os.path.join(src_folder, src_name))

    json_label = os.path.join(json_label_folder, src_name.replace('.jpg', '.json'))

    with open(json_label, 'r', encoding='utf-8') as file:
        label_data = json.load(file)

    src_path = os.path.join(src_folder, label_data['imagePath'])
    src = cv2.imread(src_path)
    new_img_name = f'result_{times}.jpg'

    result_image = bg.copy()
    edge2inpaint = []
    for label_info in label_data['shapes']:
        label_name = label_info['label']
        label_id = chinese_to_number.get(label_name, -1)  

        points = np.array(label_info['points'], np.int32).reshape((1, -1, 2))

        object_mask = np.zeros_like(src, dtype=np.uint8)
        edge_mask = np.zeros_like(src)

        line_width = 2
        cv2.drawContours(edge_mask, points, -1, (255, 255, 255), line_width)
        edge2inpaint.append(edge_mask)
        cv2.drawContours(object_mask, points, -1, (255, 255, 255), cv2.FILLED)
        # cv2.fillPoly(mask, [points], (255, 255, 255)) 


        object = cv2.bitwise_and(src, object_mask)
        edge = cv2.bitwise_and(src, edge_mask)


        result_image[object_mask == 255] = object[object_mask == 255]
                    

    for edge2inpaint_mask in edge2inpaint:
        result_image = cv2.inpaint(result_image, edge2inpaint_mask[:, :, 0], inpaintRadius=3, flags=cv2.INPAINT_TELEA)

    # cv2.imshow("src", src)
    # cv2.imshow("result", result_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite(os.path.join(output_folder, new_img_name), result_image)
