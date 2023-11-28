import cv2
import numpy as np
import json
import os

chinese_labels = [
    '签字笔', '手机', '钥匙', '水杯', '登机牌', '身份证', '银行卡', '名片', '充电宝', 
    '耳机', '钱包', '手环', '手表', '头绳', '皮筋', '戒指', '梳子', '其他', 
    '书包', '电脑', '货币', '口红', '耳钉', '硬币', '香烟', '护照', '鼠标', 
    '充电器', 'U盘', '线', '行李箱', '' , '' , '' ,'手'
]
chinese_to_number = {label: index for index, label in enumerate(chinese_labels) if label}

source_image_folder = './'

target_image_folder = './'

target_image = cv2.imread(os.path.join(target_image_folder, "bg.jpg"))

label_json_file = './Video_20230813090234284__0001669500.json'
with open(label_json_file, 'r', encoding='utf-8') as file:
    label_data = json.load(file)
source_image_path = os.path.join(source_image_folder, label_data['imagePath'])
source_image = cv2.imread(source_image_path)
result_image = target_image.copy()

for label_info in label_data['shapes']:
    label_name = label_info['label']
    label_id = chinese_to_number.get(label_name, -1)  
    points = np.array(label_info['points'], np.int32).reshape((-1, 1, 2))

    # 获取原来物体的掩码
    mask = np.zeros_like(source_image)
    color = (255, 255, 255)
    cv2.fillPoly(mask, [points], color)
    # cv2.imshow("1", mask)

    # 使用旋转矩阵进行旋转
    angle_degrees = 60
    rotation_matrix = cv2.getRotationMatrix2D((mask.shape[1] // 2, mask.shape[0] // 2), angle_degrees, 1)
    rotated_source_image = cv2.warpAffine(source_image, rotation_matrix, (source_image.shape[1], source_image.shape[0]))
    rotated_mask = cv2.warpAffine(mask, rotation_matrix, (mask.shape[1], mask.shape[0]))
    rotated_object = cv2.bitwise_and(rotated_source_image, rotated_mask)

    # 添加透明度逐渐减小的像素来平滑边缘
    alpha = np.linspace(1.0, 0.0, 10)  # 透明度从1到0逐渐减小
    for a in alpha:
        smoothed_object = cv2.addWeighted(rotated_object, a, rotated_mask, 1 - a, 0)


    result_image[rotated_mask == 255] = smoothed_object[rotated_mask == 255]

    # result_image[rotated_mask == 255] = rotated_source_image[rotated_mask == 255]

# cv2.imwrite('rotated_image.jpg', result_image)
cv2.namedWindow("result", cv2.WINDOW_NORMAL)
cv2.imshow("result", result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()