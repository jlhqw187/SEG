import numpy as np
import cv2

def overlap_filter(box1, box2):
    
    epsilon = 1e-9
    # 计算交集区域的左上角和右下角坐标
    x1_inter = max(box1[0], box2[0])
    y1_inter = max(box1[1], box2[1])
    x2_inter = min(box1[2], box2[2])
    y2_inter = min(box1[3], box2[3])
    
    # 计算交集区域的宽度和高度
    width_inter = max(0, x2_inter - x1_inter)
    height_inter = max(0, y2_inter - y1_inter)
    
    # 计算交并区域的面积
    area_inter = width_inter * height_inter
    area_box1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area_box2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    area_union = area_box1 + area_box2 - area_inter
    
    # 计算IoU
    iou = area_inter / area_union
    if abs(iou - min(area_box1, area_box2) / max(area_box1, area_box2)) < epsilon:
        return True
    return False


box1 = (100, 100, 200, 200)
box2 = (150, 150, 175, 175)

print("IoU:", overlap_filter(box1, box2))
