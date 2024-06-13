import os
import json
import time

import torch
from PIL import Image
import transforms
from src import SSD300, Backbone


def create_model(num_classes):
    backbone = Backbone()
    model = SSD300(backbone=backbone, num_classes=num_classes)

    return model

class SSDDetector:
    def __init__(self, weights_path, json_path, device):
        self.device = device
        self.num_classes = 20 + 1  # VOC dataset has 20 classes + background

        # create model
        self.model = create_model(self.num_classes)
        self.model.to(self.device)

        # load train weights
        self.weights_path = weights_path
        self.load_weights()

        # read class index
        self.json_path = json_path
        self.category_index = self.read_class_index()

        # create data transform
        self.data_transform = transforms.Compose([
            transforms.Resize((300, 300)),  # SSD300 needs 300x300 input
            transforms.ToTensor(),
            transforms.Normalization(),
        ])

        self.faceTracker = {}

    def load_weights(self):
        weights_dict = torch.load(self.weights_path, map_location=self.device)
        weights_dict = weights_dict["model"] if "model" in weights_dict else weights_dict
        self.model.load_state_dict(weights_dict)

    def read_class_index(self):
        assert os.path.exists(self.json_path), f"file '{self.json_path}' does not exist."
        with open(self.json_path, 'r') as json_file:
            class_dict = json.load(json_file)
        return {str(v): str(k) for k, v in class_dict.items()}

    def ssd_detect(self, frame):
        # convert frame to PIL image and preprocess
        original_img = Image.fromarray(frame)
        img, _ = self.data_transform(original_img)
        img = torch.unsqueeze(img, dim=0).to(self.device)

        self.model.eval()
        with torch.no_grad():
            # initial model
            init_img = torch.zeros((1, 3, 300, 300), device=self.device)
            self.model(init_img)
            # print("ssd loading succeeded")

            time_start = time.time()
            predictions = self.model(img)[0]  # bboxes_out, labels_out, scores_out
            time_end = time.time()
            print(f"inference+NMS time: {time_end - time_start}")

            predict_boxes = predictions[0].to("cpu").numpy()
            predict_boxes[:, [0, 2]] = predict_boxes[:, [0, 2]] * original_img.size[0]
            predict_boxes[:, [1, 3]] = predict_boxes[:, [1, 3]] * original_img.size[1]
            predict_classes = predictions[1].to("cpu").numpy()
            predict_scores = predictions[2].to("cpu").numpy()


            # create detection results
            detections = []
            for i, score in enumerate(predict_scores):
                if score > 0.5:  # only consider predictions with confidence > 0.5
                    box = predict_boxes[i]
                    label_id = predict_classes[i]
                    label_name = self.category_index[str(label_id)]  # 使用类别 ID 获取类别名称

                    detections.append((box, label_name, score))

            print("SSD目标检测器")

            return detections

# # Usage:
# # Initialize the SSDDetector with the path to the trained weights and the device ('cpu' or 'cuda:0')
# ssd_detector = SSDDetector(
#     weights_path="./save_weights/ssd300-14.pth",
#     json_path='./pascal_voc_classes.json',
#     device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# )
#
# # Detect objects in a frame from a video
# frame = cv2.imread('../test.jpg')  # Open the frame using OpenCV
# detections = ssd_detector.detect(frame)
# #
# # Print the detections
# for detection in detections:
#     print(detection)