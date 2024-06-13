import json
import time
import torch
import numpy as np


from build_utils import img_utils, utils
from yolo_models import Darknet



class YOLOv3Detector:
    def __init__(self, cfg_path, weights_path, json_path, img_size=512):
        self.cfg_path = cfg_path
        self.weights_path = weights_path
        self.json_path = json_path
        self.img_size = img_size

        # Load class labels from json file
        with open(json_path, 'r') as f:
            self.class_dict = json.load(f)
        self.category_index = {str(v): str(k) for k, v in self.class_dict.items()}

        # Initialize the YOLOv3 model
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = self.load_model()

        #
        self.faceTracker = {}

    def load_model(self):
        model = Darknet(self.cfg_path, self.img_size)
        weights_dict = torch.load(self.weights_path, map_location='cpu')
        weights_dict = weights_dict["model"] if "model" in weights_dict else weights_dict
        model.load_state_dict(weights_dict)
        model.to(self.device)
        model.eval()
        with torch.no_grad():
            img = torch.zeros((1, 3, self.img_size, self.img_size), device=self.device)
            model(img)  # Initialize model
        return model

    def yolov3_detect(self, frame):
        img_o = frame  # BGR

        img = img_utils.letterbox(img_o, new_shape=(self.img_size, self.img_size), auto=True, color=(0, 0, 0))[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device).float() / 255.0
        img = img.unsqueeze(0)  # Add batch dimension


        with torch.no_grad():
            time_start = time.time()
            pred = self.model(img)[0]
            pred = utils.non_max_suppression(pred, conf_thres=0.1, iou_thres=0.6, multi_label=True)[0]
            time_end = time.time()
            print(f"inference+NMS time: {time_end - time_start}")

        if pred is None:
            print("No target detected.")
            return

        pred[:, :4] = utils.scale_coords(img.shape[2:], pred[:, :4], img_o.shape).round()

        bboxes = pred[:, :4].detach().cpu().numpy()
        scores = pred[:, 4].detach().cpu().numpy()
        classes = pred[:, 5].detach().cpu().numpy().astype(np.int) + 1

        results = []
        # 遍历每个检测结果
        for i in range(len(bboxes)):
            # 提取边界框的四个坐标
            bbox = tuple(bboxes[i].astype(int))  # 转换为整数并转换为元组
            # 获取类别名称
            class_name = self.category_index[str(classes[i])]  # 减去1是因为类别从1开始
            # 创建置信度的tensor
            score_tensor = torch.tensor(scores[i])
            # 创建一个元组来存储每个检测结果的信息
            result = (bbox[0], bbox[1], bbox[2], bbox[3], class_name, score_tensor)
            results.append(result)

        return results


