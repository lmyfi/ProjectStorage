from deep_sort.utils.parser import get_config
from deep_sort.deep_sort import DeepSort
import torch
import cv2

import models

# palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)
# cfg = get_config()
# cfg.merge_from_file("deep_sort/configs/deep_sort.yaml")
# deepsort = DeepSort(cfg.DEEPSORT.REID_CKPT,
#                     max_dist=cfg.DEEPSORT.MAX_DIST, min_confidence=cfg.DEEPSORT.MIN_CONFIDENCE,
#                     nms_max_overlap=cfg.DEEPSORT.NMS_MAX_OVERLAP, max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
#                     max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
#                     use_cuda=False)

def reset_tracker():
    global deepsort  # 声明 deepsort 是全局变量，以便在函数中修改
    cfg = get_config()
    cfg.merge_from_file("deep_sort/configs/deep_sort.yaml")
    deepsort = DeepSort(cfg.DEEPSORT.REID_CKPT,
                        max_dist=cfg.DEEPSORT.MAX_DIST, min_confidence=cfg.DEEPSORT.MIN_CONFIDENCE,
                        nms_max_overlap=cfg.DEEPSORT.NMS_MAX_OVERLAP, max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                        max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                        use_cuda=False)



#faster rcnn tracker
def update_tracker_fasterrcnn(target_detector, image):

    new_ids = []
    faster_rcnn_results = target_detector.fasterrcnn_detect(image)
    # print("faster rcnn : {}", faster_rcnn_results)
    predict_boxes, class_names, scores = faster_rcnn_results

    # 获取所有目标的 xmin 坐标
    xmin = predict_boxes[:, 0]

    # 获取所有目标的 ymin 坐标
    ymin = predict_boxes[:, 1]

    # 获取所有目标的 xmax 坐标
    xmax = predict_boxes[:, 2]

    # 获取所有目标的 ymax 坐标
    ymax = predict_boxes[:, 3]

    # 转换边界框坐标为 YOLO 格式
    bbox_xywh = []
    confs = []
    clss = []

    for i in range(len(xmin)):
        # 计算中心点坐标
        x_center = (xmin[i] + xmax[i]) / 2
        y_center = (ymin[i] + ymax[i]) / 2

        # 计算宽度和高度
        width = xmax[i] - xmin[i]
        height = ymax[i] - ymin[i]

        # 添加到列表中
        bbox_xywh.append([x_center, y_center, width, height])
        confs.append(scores[i])
        clss.append(class_names[i])

    # 将列表转换为 torch.Tensor
    bbox_xywh_tensor = torch.tensor(bbox_xywh, dtype=torch.float32)
    confs_tensor = torch.tensor(confs, dtype=torch.float32)
    # clss_tensor = torch.tensor(clss)

    # 更新 DeepSort 跟踪器
    outputs = deepsort.update(bbox_xywh_tensor, confs_tensor, clss, image)

    bboxes2draw = []
    detect_id_bboxes = []
    current_ids = []
    for value in list(outputs):
        x1, y1, x2, y2, cls_, track_id = value
        bboxes2draw.append(
            (x1, y1, x2, y2, cls_, track_id)
        )
        current_ids.append(track_id)
        if cls_ == 'face':
            if not track_id in target_detector.faceTracker:
                target_detector.faceTracker[track_id] = 0
                face = image[y1:y2, x1:x2]
                new_ids.append((face, track_id))
            detect_id_bboxes.append(
                (x1, y1, x2, y2)
            )

    ids2delete = []
    for history_id in target_detector.faceTracker:
        if not history_id in current_ids:
            target_detector.faceTracker[history_id] -= 1
        if target_detector.faceTracker[history_id] < -5:
            ids2delete.append(history_id)

    for ids in ids2delete:
        target_detector.faceTracker.pop(ids)
        print('-[INFO] Delete track id:', ids)

    # image = draw_detection_results(image, faster_rcnn_results)

    return image, new_ids, bboxes2draw



def convert_fasterrcnn_to_yolo(faster_rcnn_results):
    # 将提供的数据格式转换为目标检测结果的数据格式
    detections = []
    for bbox, cls_id, score in zip(faster_rcnn_results[0], faster_rcnn_results[1], faster_rcnn_results[2]):
        x1, y1, x2, y2 = bbox
        detections.append((x1, y1, x2, y2, cls_id, score))
    return detections


#ssd tracker
def convert_ssd_to_yolo(ssd_detections):
    yolo_detections = []
    for detection in ssd_detections:
        # 解包SSD检测结果
        bbox, cls_id, conf = detection

        # 从NumPy数组中提取边界框坐标
        x1, y1, x2, y2 = bbox

        # 创建YOLO格式的检测结果
        yolo_detection = [
            x1, y1, x2, y2,  # bbox
            cls_id,  # cls_id
            conf  # conf
        ]
        yolo_detections.append(yolo_detection)

    return yolo_detections

def update_tracker_ssd(target_detector, image):

    new_ids = []
    # 使用SSD目标检测器进行目标检测
    ssd_results = target_detector.ssd_detect(image)
    # print("ssd_datection : {}", ssd_results)
    bboxes = convert_ssd_to_yolo(ssd_results)

    bbox_xywh = []
    confs = []
    clss = []

    for x1, y1, x2, y2, cls_id, conf in bboxes:

        obj = [
            int((x1+x2)/2), int((y1+y2)/2),
            x2-x1, y2-y1
        ]
        bbox_xywh.append(obj)
        confs.append(conf)
        clss.append(cls_id)

    xywhs = torch.Tensor(bbox_xywh)
    confss = torch.Tensor(confs)

    outputs = deepsort.update(xywhs, confss, clss, image)

    bboxes2draw = []
    detect_id_bboxes = []
    current_ids = []
    for value in list(outputs):
        x1, y1, x2, y2, cls_, track_id = value
        bboxes2draw.append(
            (x1, y1, x2, y2, cls_, track_id)
        )
        current_ids.append(track_id)
        if cls_ == 'car':
            if not track_id in target_detector.faceTracker:
                target_detector.faceTracker[track_id] = 0
                face = image[y1:y2, x1:x2]
                new_ids.append((face, track_id)) #新检测出的指定类别对象
            detect_id_bboxes.append(
                (x1, y1, x2, y2)
            ) #检测过的所有类别的位置信息

    ids2delete = []
    for history_id in target_detector.faceTracker:
        if not history_id in current_ids:
            target_detector.faceTracker[history_id] -= 1
        if target_detector.faceTracker[history_id] < -5:
            ids2delete.append(history_id)

    for ids in ids2delete:
        target_detector.faceTracker.pop(ids)
        print('-[INFO] Delete track id:', ids)

    # image = plot_bboxes(image, bboxes2draw)
    # image = draw_detection_results(image, ssd_results)

    return image, new_ids, bboxes2draw

#yolov3 tracker
def update_tracker_yolov3(target_detector, image):

    new_ids = []
    bboxes = target_detector.yolov3_detect(image)
    # print("yolov3 results : ", bboxes)

    bbox_xywh = []
    confs = []
    clss = []

    for x1, y1, x2, y2, cls_id, conf in bboxes:

        obj = [
            int((x1+x2)/2), int((y1+y2)/2),
            x2-x1, y2-y1
        ]
        bbox_xywh.append(obj)
        confs.append(conf)
        clss.append(cls_id)

    xywhs = torch.Tensor(bbox_xywh)
    confss = torch.Tensor(confs)

    outputs = deepsort.update(xywhs, confss, clss, image)

    bboxes2draw = []
    detect_id_bboxes = []
    current_ids = []
    for value in list(outputs):
        x1, y1, x2, y2, cls_, track_id = value
        bboxes2draw.append(
            (x1, y1, x2, y2, cls_, track_id)
        )
        current_ids.append(track_id)
        if cls_ == 'face':
            if not track_id in target_detector.faceTracker:
                target_detector.faceTracker[track_id] = 0
                face = image[y1:y2, x1:x2]
                new_ids.append((face, track_id))
            detect_id_bboxes.append(
                (x1, y1, x2, y2)
            )

    ids2delete = []
    for history_id in target_detector.faceTracker:
        if not history_id in current_ids:
            target_detector.faceTracker[history_id] -= 1
        if target_detector.faceTracker[history_id] < -5:
            ids2delete.append(history_id)

    for ids in ids2delete:
        target_detector.faceTracker.pop(ids)
        print('-[INFO] Delete track id:', ids)

    # image = plot_bboxes(image, cars_only)
    # image = draw_detection_results(image, bboxes)

    return image, new_ids, bboxes2draw

def plot_bboxes(image, bboxes, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(
        0.002 * (image.shape[0] + image.shape[1]) / 2) + 1  # line/font thickness
    #bboxes数据格式为[(294, 470, 394, 541, 'car', 1), (425, 491, 518, 582, 'car', 2)]
    for (x1, y1, x2, y2, cls_id, pos_id) in bboxes:
        if cls_id in ['person']:
            color = (0, 0, 255)
        else:
            color = (0, 255, 0)
        c1, c2 = (x1, y1), (x2, y2)
        cv2.rectangle(image, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(cls_id, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(image, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(image, '{} ID-{}'.format(cls_id, pos_id), (c1[0], c1[1] - 2), 0, tl / 3,
                    [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

    return image

def draw_detection_results(image, detections):
    """
    绘制目标检测结果（边界框和标签）到图像上，只绘制置信度大于0.45的结果。

    Args:
        image: 原始图像。
        detections: 目标检测结果，每个元素为一个元组，包含 (x1, y1, x2, y2, cls_id, score)。

    Returns:
        绘制了检测结果的图像。
    """
    confidence_threshold = 0.45  # 设置置信度阈值
    #detections数据格式为: [(316.92523, 82.44391, 384.64835, 288.55475, 'person', 0.08015221)]
    #cls_id为(str)如'person'
    for x1, y1, x2, y2, cls_id, score in detections:
        if score > confidence_threshold:  # 检查置信度是否大于阈值
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(image, f'{cls_id}: {score:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)

    return image



def image_object_detection(target_detector, image, filter_detect, filter_detect_cls):
    if isinstance(target_detector, models.ssd.predict_test.SSDDetector):
        # 使用 SSD 目标检测器进行目标检测
        ssd_results = target_detector.ssd_detect(image)
        print("ssd",ssd_results)
        ssd_results = convert_ssd_to_yolo(ssd_results)  #转化为yolo格式
        # 将 SSD 检测结果绘制到图片上
        image_with_detection = draw_detection_results(image, ssd_results)
    elif isinstance(target_detector, models.faster_rcnn.predict.FasterRCNNDetector):  # 这里请替换为 FasterRCNN 类的实际名称
        # 使用 Faster R-CNN 目标检测器进行目标检测
        faster_rcnn_results = target_detector.fasterrcnn_detect(image) #faster rcnn目标检测结果
        print("faster rcnn", faster_rcnn_results)
        faster_rcnn_results = convert_fasterrcnn_to_yolo(faster_rcnn_results) #转换为yolo格式
        image_with_detection = draw_detection_results(image, faster_rcnn_results)
    elif isinstance(target_detector, models.yolov3_spp.predict_test.YOLOv3Detector):  # 这里请替换为 YOLOv3 类的实际名称
        # 使用 YOLOv3 目标检测器进行目标检测
        yolov3_results = target_detector.yolov3_detect(image) #目标检测结果
        print("yolov3", yolov3_results)
        image_with_detection = draw_detection_results(image, yolov3_results)
    else:
        # 如果 target_detector 不是已知类型的目标检测器，则抛出异常或执行其他操作
        raise ValueError("Unknown target detector type")

    return image_with_detection

#只有目标检测器进行视频序列的检测
def video_object_detection(target_detector, image, filter_detect, filter_detect_cls):
    results = []
    if isinstance(target_detector, models.ssd.predict_test.SSDDetector):
        # 使用 SSD 目标检测器进行目标检测
        ssd_results = target_detector.ssd_detect(image)
        print("ssd",ssd_results)
        ssd_results = convert_ssd_to_yolo(ssd_results)  #转化为yolo格式
        results = ssd_results
    elif isinstance(target_detector, models.faster_rcnn.predict.FasterRCNNDetector):  # 这里请替换为 FasterRCNN 类的实际名称
        # 使用 Faster R-CNN 目标检测器进行目标检测
        faster_rcnn_results = target_detector.fasterrcnn_detect(image) #faster rcnn目标检测结果
        print("faster rcnn", faster_rcnn_results)
        faster_rcnn_results = convert_fasterrcnn_to_yolo(faster_rcnn_results) #转换为yolo格式
        results = faster_rcnn_results

    elif isinstance(target_detector, models.yolov3_spp.predict_test.YOLOv3Detector):  # 这里请替换为 YOLOv3 类的实际名称
        # 使用 YOLOv3 目标检测器进行目标检测
        yolov3_results = target_detector.yolov3_detect(image) #目标检测结果
        print("yolov3", yolov3_results)
        results = yolov3_results
    else:
        # 如果 target_detector 不是已知类型的目标检测器，则抛出异常或执行其他操作
        raise ValueError("Unknown target detector type")

    if filter_detect:
        results = [item for item in results if item[4] == filter_detect_cls]
    image_with_detection = draw_detection_results(image, results)

    return image_with_detection, results