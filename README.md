# SEG：利用语义分割生成新的目标检测数据集
## 具体的任务是

- input1：背景图片文件夹bg

- input2：正常图片文件夹src

- input3：正常图片的目标检测标签文件夹txt

- input4：正常图片的语义分割标签文件夹json

- output1：新生成的众多图片output

- output2：新目标检测标签文件夹output_label

## 做法：正常图片里的物体通过语义分割被提取出来，通过随机的平移、翻转、旋转后生成新的数据集

## 实现细节：

step1：提取分割的物体（done）

step2：对物体进行平移、翻转、旋转（done）
- 相关文件:copypaste.py（复制粘贴）, translate.py(平移), rotate_seg.py（旋转）

step3：判读操作后的物体是否还在框中(通过计算IoU实现)*（to do）*
- 相关文件：count_iou.py

step4：计算并生成新的label（done）
- 相关文件：generate_rotated_corrd_txt.py(旋转的)，复制粘贴的没写直接复制原来的txt即可。

## 注意点：格式转换
1. 类别名称，语义分割数据集是中文，目标检测数据集是数字，需要进行一一对应。但是在此之前应该先完成目标检测数据集的种类压缩。
2. 外包发送的是xml，labelme使用的是json，目标检测用的是txt。xml2json.py对应外包转labelme形式
3. 通过inpaint方法来柔和边缘不那么突兀
4. json_all里是所有的分割数据集。semantic_annotation里是外包交付时的数据集样式。