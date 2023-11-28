import numpy as np
import cv2
import os

image_folder = "./"
label_folder = "./"

for label_file in os.listdir(label_folder):
    if label_file.endswith('.txt'):
        image_name = label_file.split(".")[0] + '.jpg'
        image = cv2.imread(os.path.join(image_folder, image_name))
        image_height, image_width, _ = image.shape
        x_image_center = image_width // 2
        y_image_center = image_height // 2

        with open(label_file, 'r') as labels:
            label_lines = labels.readlines()
        for label_line in label_lines:
            parts = label_line.strip().split()  
            class_id = int(parts[0])

            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])


            x_center_pixel = int(x_center * image_width)
            y_center_pixel = int(y_center * image_height)
            width_pixel = int(width * image_width)
            height_pixel = int(height * image_height)


            angle_degrees = 300  
            angle_radians = np.radians(angle_degrees)
            new_x = (x_center_pixel - x_image_center) * np.cos(angle_radians) - (y_center_pixel - y_image_center) * np.sin(angle_radians) + x_image_center
            new_y = (x_center_pixel - x_image_center) * np.sin(angle_radians) + (y_center_pixel - y_image_center) * np.cos(angle_radians) + y_image_center
          
            new_x = new_x / image_width
            new_y = new_y / image_height


            # 计算边界框的左上角和右下角坐标
            x1 = x_center_pixel - width_pixel // 2
            y1 = y_center_pixel - height_pixel // 2
            x2 = x_center_pixel + width_pixel // 2
            y2 = y_center_pixel + height_pixel // 2
            
            # x3 x4分别是 右上 左下
            x3, y3 = x2, y1
            x4, y4 = x1, y2


            new_x1 = (x1 - x_image_center) * np.cos(angle_radians) - (y1 - y_image_center) * np.sin(angle_radians) + x_image_center
            new_y1 = (x1 - x_image_center) * np.sin(angle_radians) + (y1 - y_image_center) * np.cos(angle_radians) + y_image_center
            new_x2 = (x2 - x_image_center) * np.cos(angle_radians) - (y2 - y_image_center) * np.sin(angle_radians) + x_image_center
            new_y2 = (x2 - x_image_center) * np.sin(angle_radians) + (y2 - y_image_center) * np.cos(angle_radians) + y_image_center
            new_x3 = (x3 - x_image_center) * np.cos(angle_radians) - (y3 - y_image_center) * np.sin(angle_radians) + x_image_center
            new_y3 = (x3 - x_image_center) * np.sin(angle_radians) + (y3 - y_image_center) * np.cos(angle_radians) + y_image_center
            new_x4 = (x4 - x_image_center) * np.cos(angle_radians) - (y4 - y_image_center) * np.sin(angle_radians) + x_image_center
            new_y4 = (x4 - x_image_center) * np.sin(angle_radians) + (y4 - y_image_center) * np.cos(angle_radians) + y_image_center
            
            width = max(new_x1, new_x2, new_x3, new_x4) - min(new_x1, new_x2, new_x3, new_x4)
            height = max(new_y1, new_y2, new_y3, new_y4) - min(new_y1, new_y2, new_y3, new_y4)
            new_x = min(new_x1, new_x2, new_x3, new_x4) + width // 2
            new_y = max(new_y1, new_y2, new_y3, new_y4) - height // 2

            new_x = new_x / image_width
            new_y = new_y / image_height
            width = width / image_width
            height = height / image_height
            new_label_list = []
            new_label_list.append(str(class_id))
            new_label_list.append(str(new_x))
            new_label_list.append(str(new_y))
            new_label_list.append(str(width))
            new_label_list.append(str(height))
            new_label_line = " ".join(new_label_list) + "\n"
            with open('rotated_image.txt', 'w') as file:
    # 写入文本内容
                file.write(new_label_line)
            # cv2.rectangle(image, (x1, y1), (x2, y2), color_mapping[class_id], thickness)

            # 保存带有边界框的图像
            # cv2.imwrite('output_image.jpg', image)

            # cv2.imshow("result", image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()









