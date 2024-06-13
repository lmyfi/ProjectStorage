import time
import json
import torch
from torchvision import transforms
from network_files import FasterRCNN
from backbone import resnet50_fpn_backbone


class FasterRCNNDetector:
    def __init__(self, weights_path, json_path, device):
        self.device = device
        self.num_classes = 21  # VOC dataset has 20 classes + background
        self.category_index = self.read_class_index(json_path)
        self.model = self.create_model()
        self.load_weights(weights_path)
        self.data_transform = transforms.Compose([transforms.ToTensor()])
        self.model.to(device)

        self.faceTracker = {}

    def create_model(self):
        # resNet50+fpn+faster_RCNN
        backbone = resnet50_fpn_backbone(norm_layer=torch.nn.BatchNorm2d)
        model = FasterRCNN(backbone=backbone, num_classes=self.num_classes, rpn_score_thresh=0.5)
        return model

    def load_weights(self, weights_path):
        weights_dict = torch.load(weights_path, map_location=self.device)
        weights_dict = weights_dict["model"] if "model" in weights_dict else weights_dict
        self.model.load_state_dict(weights_dict)

    def read_class_index(self, json_path):
        with open(json_path, 'r') as json_file:
            class_dict = json.load(json_file)
        return {str(v): str(k) for k, v in class_dict.items()}

    def fasterrcnn_detect(self, image):
        original_img = image
        img = self.data_transform(original_img)
        img = torch.unsqueeze(img, dim=0)

        self.model.eval()
        # print("faster_rcnn loading succeeded")
        with torch.no_grad():
            t_start = time.time()
            predictions = self.model(img.to(self.device))[0]
            t_end = time.time()
            print("inference+NMS time: {}".format(t_end - t_start))

            predict_boxes = predictions["boxes"].to("cpu").numpy()
            predict_classes = predictions["labels"].to("cpu").numpy()
            predict_scores = predictions["scores"].to("cpu").numpy()

            # 将类别 ID 转换为对象名称
            predict_class_names = [self.category_index[str(class_id)] for class_id in predict_classes]
            if len(predict_boxes) == 0:
                print("没有检测到任何目标!")
                return []

        return predict_boxes, predict_class_names, predict_scores



