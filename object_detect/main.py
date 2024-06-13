#导入相关包
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QComboBox, \
    QGridLayout, QCheckBox, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QMutex, QMutexLocker
import torch
import cv2
import time
import json

# 导入目标检测器模型和相关函数
from models.ssd.predict_test import SSDDetector
from models.faster_rcnn.predict import FasterRCNNDetector
from models.yolov3_spp.predict_test import YOLOv3Detector
from trackers import plot_bboxes, update_tracker_fasterrcnn, update_tracker_ssd, \
    update_tracker_yolov3, image_object_detection, reset_tracker, video_object_detection

#支持的目标检测器字典
DETECTORS = {
    'faster_rcnn': FasterRCNNDetector,
    'ssd': SSDDetector,
    'yolov3spp': YOLOv3Detector
}

# 自定义线程类，用于执行目标检测任务
class ObjectDetectThread(QThread):
    # 定义信号
    change_pixmap_signal = pyqtSignal(QImage)
    send_raw = pyqtSignal(QImage)
    pause_signal = pyqtSignal()
    send_statistic = pyqtSignal(dict) #统计检测结果
    update_status_signal = pyqtSignal(str) #状态信息
    send_fps_signal = pyqtSignal(dict)

    def __init__(self, file_path, detector_type, weights_path, json_path, cfg_path, data_type):
        super().__init__()
        # 初始化线程参数
        self.file_path = file_path
        self.detector_type = detector_type
        self.weights_path = weights_path
        self.json_path = json_path
        self.cfg_path = cfg_path
        self.stopped = False
        self.paused = False
        self.filter_detect_cls = 'person' #如果要启用过滤功能，即只检测指定类别，默认为人
        self.filter_detect = False #是否开启过滤
        self.data_type = data_type
        self.detector = None
        self.update_tracker = None
        self.mutex = QMutex()
        self.set_detector_and_tracker()
        self.use_deepsort = False
        self.fps = 0
        self.last_time = time.time()

    def run(self):
        # 根据数据类型实现主要的检测处理过程
        try:
            if self.data_type == 'video':
                self.process_video()
            elif self.data_type == 'camera':
                self.process_camera()
            elif self.data_type == 'image':
                self.process_image()
        except Exception as e:
            print(f"检测线程中发生错误：{e}")
        finally:
            self.cleanup_resources()

    def cleanup_resources(self):
        # 清理资源，如释放视频捕获资源
        if hasattr(self, 'video_capture') and self.video_capture:
            self.video_capture.release()


    def set_detector_and_tracker(self):
        # 根据选择的目标检测器类型设置对应的模型和跟踪器
        if self.detector_type == 'faster_rcnn':
            self.detector = FasterRCNNDetector(self.weights_path, self.json_path,
                                               device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))
            self.update_tracker = update_tracker_fasterrcnn
        elif self.detector_type == 'ssd':
            self.detector = SSDDetector(self.weights_path, self.json_path,
                                        device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))
            self.update_tracker = update_tracker_ssd
        elif self.detector_type == 'yolov3spp':
            self.detector = YOLOv3Detector(self.cfg_path, self.weights_path, self.json_path)
            self.update_tracker = update_tracker_yolov3

    def process_video(self):
        # 处理视频文件
        if not self.file_path:
            self.update_status_signal.emit("Error: No video path provided.")
            return

        video_capture = cv2.VideoCapture(self.file_path)
        reset_tracker()
        video_capture.set(cv2.CAP_PROP_FPS,10)


        try:
            fps = int(video_capture.get(cv2.CAP_PROP_FPS))
            # 打印出帧率
            print("Frames per second (FPS):", fps)
            t = int(1000 / fps)
            # 打印出每帧的时间间隔
            print("Time per frame (ms):", t)

            while not self.stopped:
                if not self.paused:
                    _, im = video_capture.read()
                    if im is None:
                        break

                    current_time = time.time()
                    self.fps = 1.0 / (current_time - self.last_time)
                    self.last_time = current_time
                    self.send_fps_signal.emit({'fps': self.fps})  # 发送FPS

                    raw_qimage = self.convert_cv2_to_qimage(im)

                    if self.use_deepsort:
                        time_start = time.time()
                        # 使用DeepSort
                        image, new_id, bboxes2draw = self.update_tracker(self.detector, im)
                        time_end = time.time()
                        print(f"Detector+DeepSort runtime: {time_end - time_start}")

                        #只检测指定类别
                        if self.filter_detect:
                            bboxes2draw = [item for item in bboxes2draw if item[4] == self.filter_detect_cls]
                            result = plot_bboxes(im, bboxes2draw)
                        else:
                            result = plot_bboxes(im, bboxes2draw)

                        # 检测结果，统计信息
                        if bboxes2draw:
                            class_counts = {}
                            for bbox in bboxes2draw:
                                class_name = bbox[4]
                                if class_name in class_counts:
                                    class_counts[class_name] += 1
                                else:
                                    class_counts[class_name] = 1

                            self.send_statistic.emit(class_counts)



                        result_qimage = self.convert_cv2_to_qimage(result)

                    else:
                        time_start = time.time()
                        # 仅使用目标检测器
                        result_image, results = video_object_detection(self.detector, im, self.filter_detect, self.filter_detect_cls)
                        time_end = time.time()
                        print(f"Only Detector runtime: {time_end - time_start}")
                        if results:
                            class_counts = {}
                            for bbox in results:
                                class_name = bbox[4]
                                if class_name in class_counts:
                                    class_counts[class_name] += 1
                                else:
                                    class_counts[class_name] = 1

                            self.send_statistic.emit(class_counts)


                        result_qimage = self.convert_cv2_to_qimage(result_image)

                    self.change_pixmap_signal.emit(result_qimage)
                    self.send_raw.emit(raw_qimage)

                    self.msleep(t)
                else:
                    self.msleep(100)

        finally:
            video_capture.release()

    def process_camera(self):
        # 处理摄像头输入
        # video_capture = cv2.VideoCapture(0)
        video_capture = cv2.VideoCapture(1)
        reset_tracker()

        # 获取摄像头的FPS，如果失败则设置为30作为默认值
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        if fps != int(fps):
            fps = 30
        else:
            fps = int(fps)

        # 计算每帧的时间间隔（以毫秒为单位）
        t = int(1000 / fps)

        # 打印出帧率和每帧的时间间隔
        print("Frames per second (FPS) from camera:", fps)
        print("Time per frame (ms) from camera:", t)

        try:
            fps = int(video_capture.get(cv2.CAP_PROP_FPS))
            # 打印出帧率
            print("Frames per second (FPS):", fps)
            t = int(1000 / fps)
            # 打印出每帧的时间间隔
            print("Time per frame (ms):", t)

            while not self.stopped:
                if not self.paused:
                    _, im = video_capture.read()
                    if im is None:
                        break

                    current_time = time.time()
                    self.fps = 1.0 / (current_time - self.last_time)
                    self.last_time = current_time
                    self.send_fps_signal.emit({'fps': self.fps})  # 发送FPS

                    raw_qimage = self.convert_cv2_to_qimage(im)

                    if self.use_deepsort:
                        time_start = time.time()
                        # 使用DeepSort
                        image, new_id, bboxes2draw = self.update_tracker(self.detector, im)
                        time_end = time.time()
                        print(f"Detector+DeepSort runtime: {time_end - time_start}")

                        # 只检测指定类别
                        if self.filter_detect:
                            bboxes2draw = [item for item in bboxes2draw if item[4] == self.filter_detect_cls]
                            result = plot_bboxes(im, bboxes2draw)
                        else:
                            result = plot_bboxes(im, bboxes2draw)

                        # 检测结果，统计信息
                        if bboxes2draw:
                            class_counts = {}
                            for bbox in bboxes2draw:
                                class_name = bbox[4]
                                if class_name in class_counts:
                                    class_counts[class_name] += 1
                                else:
                                    class_counts[class_name] = 1

                            self.send_statistic.emit(class_counts)

                        result_qimage = self.convert_cv2_to_qimage(result)

                    else:
                        time_start = time.time()
                        # 仅使用目标检测器
                        result_image, results = video_object_detection(self.detector, im, self.filter_detect,
                                                                       self.filter_detect_cls)
                        time_end = time.time()
                        print(f"Only Detector runtime: {time_end - time_start}")
                        if results:
                            class_counts = {}
                            for bbox in results:
                                class_name = bbox[4]
                                if class_name in class_counts:
                                    class_counts[class_name] += 1
                                else:
                                    class_counts[class_name] = 1

                            self.send_statistic.emit(class_counts)

                        result_qimage = self.convert_cv2_to_qimage(result_image)

                    self.change_pixmap_signal.emit(result_qimage)
                    self.send_raw.emit(raw_qimage)

                    self.msleep(30)
                else:
                    self.msleep(100)
        except Exception as e:
            print(f"检测线程中发生错误：{e}")
        finally:
            video_capture.release()


    # 处理静态图像文件
    def process_image(self):
        reset_tracker()
        if not self.file_path:
            self.update_status_signal.emit("Error: No image path provided.")
            return

        try:
            image = cv2.imread(self.file_path)
            if image is None:
                self.update_status_signal.emit(f"Error: Failed to load image from path: {self.file_path}")
                return

            raw_qimage = self.convert_cv2_to_qimage(image)
            self.send_raw.emit(raw_qimage)  # 发送原始图像

            # 进行图像目标检测
            result_image = image_object_detection(self.detector, image, self.filter_detect, self.filter_detect_cls)

            if result_image is None:
                self.update_status_signal.emit("Error: Failed to process image.")
            else:
                result_qimage = self.convert_cv2_to_qimage(result_image)
                self.change_pixmap_signal.emit(result_qimage)  # 发送处理后的图像
                print("正常执行")

        except Exception as e:
            # 发送异常信息到主线程并在控制台打印
            self.update_status_signal.emit(f"Error: An exception occurred while processing the image: {e}")
            print(f"An error occurred while processing the image: {e}")

        finally:
            # 释放图像资源，如果有必要的话
            # 如果图像是通过cv2.imread加载的，通常不需要手动释放资源
            # 如果图像是其他方式创建的，可能需要根据实际情况释放资源
            pass

    # 将OpenCV格式的图像转换为QImage格式
    def convert_cv2_to_qimage(self, cv_image):
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_image.shape
        bytes_per_line = channel * width
        return QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)

    # 停止process_video或process_camera中循环处理数据序列
    # 停止线程
    def stop(self):
        self.update_status_signal.emit("停止线程")
        self.stopped = True
        self.wait()

    # 暂停线程
    def pause(self):
        self.update_status_signal.emit("暂停检测")
        self.paused = True


    # 恢复线程
    def resume(self):
        self.update_status_signal.emit("继续检测")
        self.paused = False
        self.pause_signal.emit()

    #停止线程并重置参数
    def pause_and_restart(self):
        self.update_status_signal.emit("停止线程并重置参数")
        # 停止线程并重置参数
        self.stop()
        self.file_path = None
        self.detector_type = None
        self.weights_path = None
        self.json_path = None
        self.start()

    # 重置线程类
    def restart(self):
        self.update_status_signal.emit("重置线程")
        self.stopped = True
        self.wait()
        self.file_path = None
        self.detector_type = None
        self.weights_path = None
        self.json_path = None
        self.cfg_path = None
        self.start()

# 主窗口类
class ObjectDetectorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.detector_type = 'faster_rcnn'
        self.weights_path = ''
        self.json_path = ''
        self.file_path = ''
        self.cfg_path = ''
        self.detect_thread = None
        self.initUI()
        self.use_deepsort_checkbox = None  # 新增属性

    # 初始化UI界面
    # 创建各种控件和布局
    # 设置信号和槽连接
    def initUI(self):
        self.detectorLabel = QLabel('选择目标检测器:', self)
        self.detectorComboBox = QComboBox(self)
        self.detectorComboBox.addItems(DETECTORS.keys())
        self.detectorComboBox.currentIndexChanged.connect(self.switchDetector)

        self.dataTypeLabel = QLabel('选择检测类型:', self)
        self.dataTypeComboBox = QComboBox(self)
        self.dataTypeComboBox.addItems(['video', 'image', 'camera'])
        self.dataTypeComboBox.currentIndexChanged.connect(self.setDataType)

        self.videoLabel = QLabel('选择文件:', self)
        self.videoButton = QPushButton('文件', self)
        self.videoButton.clicked.connect(self.switchFile)

        self.startButton = QPushButton('开始检测', self)
        self.startButton.clicked.connect(self.startDetection)

        self.pauseButton = QPushButton('暂停/继续', self)
        self.pauseButton.clicked.connect(self.pauseDetection)

        self.resetButton = QPushButton('重置', self)
        self.resetButton.clicked.connect(self.resetDetection)

        self.outputLabel = QLabel('输出信息：', self)

        self.filterLabel = QLabel('固定检测类别:', self)
        self.filterComboBox = QComboBox(self)
        # 读取并解析JSON文件
        with open('models/faster_rcnn/pascal_voc_classes.json', 'r') as file:
            categories_data = json.load(file)
        # 提取类别名称列表
        self.categories_list = list(categories_data.keys())
        self.filterComboBox.addItems(self.categories_list)
        self.filterComboBox.currentIndexChanged.connect(self.setDetectClass)

        self.filterCheckBox = QCheckBox('开启检测过滤功能', self)
        self.filterCheckBox.stateChanged.connect(self.setFilterDetect)

        self.originalVideoLabel = QLabel('原始', self)
        self.detectedVideoLabel = QLabel('检测后', self)

        self.statisticsLabel = QLabel('检测结果统计：', self)
        self.statisticsLabel.setFixedSize(300,200)


        self.statusLabel = QLabel('程序状态：', self)


        self.originalVideoWidget = QLabel(self)
        self.originalVideoWidget.setFixedSize(600, 500)
        self.detectedVideoWidget = QLabel(self)
        self.detectedVideoWidget.setFixedSize(600, 500)

        # 新增DeepSort选项框
        self.use_deepsort_checkbox = QCheckBox('使用DeepSort', self)
        self.use_deepsort_checkbox.setChecked(False)  # 默认不选中
        self.use_deepsort_checkbox.stateChanged.connect(self.toggleDeepSort)

        # 新增显示DeepSort状态和检测过滤功能的QLabel
        self.deepsortStatusLabel = QLabel('DeepSort: 不使用', self)
        self.filterStatusLabel = QLabel('检测过滤: 关闭', self)

        # 新增FPS显示用的QLabel
        self.fpsLabel = QLabel('FPS: N/A', self)  # N/A 表示“不适用”


        layout = QGridLayout()
        layout.addWidget(self.detectorLabel, 0, 0)
        layout.addWidget(self.detectorComboBox, 0, 1)
        layout.addWidget(self.dataTypeLabel, 1, 0)
        layout.addWidget(self.dataTypeComboBox, 1, 1)
        layout.addWidget(self.videoLabel, 2, 0)
        layout.addWidget(self.videoButton, 2, 1)
        layout.addWidget(self.startButton, 3, 0)
        layout.addWidget(self.pauseButton, 3, 1)
        layout.addWidget(self.resetButton, 4, 0)  # 添加重置按钮
        layout.addWidget(self.outputLabel, 4, 1, 1, 2)

        layout.addWidget(self.originalVideoLabel, 5, 0)
        layout.addWidget(self.detectedVideoLabel, 5, 1)

        layout.addWidget(self.originalVideoWidget, 6, 0, 1, 2)
        layout.addWidget(self.detectedVideoWidget, 6, 1, 1, 2)
        layout.setRowStretch(6, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        layout.addWidget(self.filterLabel, 7, 0)
        layout.addWidget(self.filterComboBox, 7, 1)
        layout.addWidget(self.filterCheckBox, 8, 0, 1, 2)
        layout.addWidget(self.use_deepsort_checkbox, 8, 1)  # 添加到布局中

        layout.addWidget(self.statisticsLabel, 9, 0, 1, 3)
        layout.addWidget(self.statusLabel, 10, 0, 1, 2)

        layout.addWidget(self.deepsortStatusLabel, 11, 0)
        layout.addWidget(self.filterStatusLabel, 11, 1)

        # 添加FPS显示到布局中，这里以添加到第12行，第1列为例
        layout.addWidget(self.fpsLabel, 12, 0, 1, 2)


        self.setFixedSize(1280, 1024)
        self.setLayout(layout)


    def startDetection(self):
        selected_detector = self.detectorComboBox.currentText()
        self.choose_cfg(selected_detector)


        # 检查是否已有运行中的检测线程
        if self.detect_thread and self.detect_thread.isRunning():
            if (self.detect_thread.detector_type != selected_detector or
                    self.detect_thread.file_path != self.file_path):
                # 如果检测器类型或文件路径发生变化，则暂停并重置现有线程
                self.detect_thread.pause_and_restart()
            else:
                # 否则只是继续已有的线程，无需重新开始
                self.detect_thread.resume()
                return

        # 创建新的检测线程（或重用已有线程）
        if not self.detect_thread or not self.detect_thread.isRunning():
            self.detect_thread = ObjectDetectThread(self.file_path, selected_detector,
                                                    self.weights_path, self.json_path,
                                                    self.cfg_path, self.dataTypeComboBox.currentText())
            self.detect_thread.change_pixmap_signal.connect(self.updateAfterDetectedLabels)
            self.detect_thread.send_raw.connect(self.updateOriginalLabels)
            self.detect_thread.send_statistic.connect(self.updateDetectionStatistics)
            self.detect_thread.update_status_signal.connect(self.updateStatus)
            # 在 ObjectDetectorApp 类的 initUI 方法中
            self.detect_thread.send_fps_signal.connect(self.updateFPS)
            self.detect_thread.start()

    # 切换目标检测器时调用，更新参数后重新开始检测
    def switchDetector(self):
        selected_detector = self.detectorComboBox.currentText()
        if not self.file_path:
            return


    # 设置数据类型
    def setDataType(self):
        if self.detect_thread and self.detect_thread.isRunning():
            # self.detect_thread.stop()
            self.detect_thread.pause_and_restart()

    # 切换文件时调用，更新文件路径后重新开始检测
    def switchFile(self):
        if self.dataTypeComboBox.currentText() == 'image':
            dialog_title = '选择图片文件'
            filter_str = 'Image files (*.jpg *.png *.bmp);;All Files (*)'
        else:
            dialog_title = '选择视频文件'
            filter_str = 'Video files (*.mp4 *.avi);;All Files (*)'

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getOpenFileName(self, dialog_title, '', filter_str, options=options)
        if file_path:
            self.file_path = file_path
            self.outputLabel.setText('已选择文件: ' + self.file_path)
        else:
            self.outputLabel.setText('取消选择文件')

    # 暂停/继续目标检测
    def pauseDetection(self):
        if self.detect_thread and self.detect_thread.isRunning():
            if not self.detect_thread.paused:
                self.detect_thread.pause()
                self.pauseButton.setText('继续')
            else:
                self.detect_thread.resume()
                self.pauseButton.setText('暂停')

    # 选择模型配置文件
    def choose_cfg(self, selected_detector):
        if selected_detector == 'faster_rcnn':
            self.weights_path = 'models/faster_rcnn/fasterrcnn_voc2012.pth'
            self.json_path = 'models/faster_rcnn/pascal_voc_classes.json'
        elif selected_detector == 'ssd':
            self.weights_path = 'models/ssd/save_weights/ssd300-14.pth'
            self.json_path = 'models/ssd/pascal_voc_classes.json'
        elif selected_detector == 'yolov3spp':
            self.cfg_path = 'models/yolov3_spp/cfg/yolov3-spp.cfg'
            self.weights_path = 'models/yolov3_spp/weigths/yolov3spp-14.pt'
            self.json_path = 'models/yolov3_spp/data/pascal_voc_classes.json'

    # 更新原始图像标签
    def updateOriginalLabels(self, q_image):
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(self.originalVideoWidget.size(), Qt.KeepAspectRatio)
        self.originalVideoWidget.setPixmap(scaled_pixmap)

    # 更新检测后图像标签
    def updateAfterDetectedLabels(self, q_image):
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(self.detectedVideoWidget.size(), Qt.KeepAspectRatio)
        self.detectedVideoWidget.setPixmap(scaled_pixmap)


    # 设置固定检测类别
    def setDetectClass(self):
        if self.detect_thread:
            self.detect_thread.filter_detect_cls = self.filterComboBox.currentText()

    # 设置检测过滤功能
    def setFilterDetect(self, state):
        if self.detect_thread:
            self.detect_thread.filter_detect = (state == Qt.Checked)
        # 更新检测过滤功能状态显示
        self.filterStatusLabel.setText('检测过滤: ' + ('开启' if state else '关闭'))

    def updateFPS(self, fps_data):
        # 更新FPS显示
        self.fpsLabel.setText(f'FPS: {fps_data["fps"]:.2f}')

    def updateDetectionStatistics(self, class_counts):
        # 更新检测结果统计信息显示
        statistic_text = "检测结果统计：\n"
        for class_name, count in class_counts.items():
            statistic_text += f"{class_name}: {count}\n"

        self.statisticsLabel.setText(statistic_text)


    #显示程序状态
    def updateStatus(self, status):
        # 更新状态信息显示
        self.statusLabel.setText('程序状态：'+status)

    def resetDetection(self):
        if self.detect_thread and self.detect_thread.isRunning():
            self.detect_thread.pause_and_restart()  # 暂停线程并重置参数
            self.detect_thread.quit()  # 退出线程
            self.detect_thread.wait()  # 等待线程结束

        # 清空文件路径和检测器类型
        self.file_path = ''
        self.detector_type = ''

        # 重新设置视频控件的大小
        self.originalVideoWidget.setFixedSize(600, 500)
        self.detectedVideoWidget.setFixedSize(600, 500)

        # 更新界面状态
        self.outputLabel.setText('已重置')
        self.statisticsLabel.setText('检测结果统计：')
        self.statusLabel.setText('程序状态：已重置')


        # 清除视频控件中的图像
        self.originalVideoWidget.clear()
        self.detectedVideoWidget.clear()


    # 在 ObjectDetectorApp 类中
    def toggleDeepSort(self, state):
        # 用户改变DeepSort选项时调用的槽函数
        if self.detect_thread:
            self.detect_thread.use_deepsort = (state == Qt.Checked)
        self.deepsortStatusLabel.setText('DeepSort: ' + ('使用' if state == Qt.Checked else '不使用'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ObjectDetectorApp()
    ex.show()
    sys.exit(app.exec_())
