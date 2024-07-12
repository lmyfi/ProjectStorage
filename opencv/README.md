# OpenCV 学习与实现

## 项目简介
学习和掌握 OpenCV，从基础概念到高级应用，并在实践中开发了多个项目。

Faces:人脸识别数据集

Photos:图像处理数据集

Videos:视频数据集

人脸检测: face_detect.py

人脸识别：faces_train.py(人脸识别模型训练)+face_recognition.py(人脸识别模型调用运行使用)

## 项目结构
1. **图像处理**:
   - **图像读取与显示**: 使用 `cv.imread` 读取图像，使用 `cv.imshow` 显示图像。
   - **图像转换**: 颜色空间转换、图像旋转、缩放等。

2. **边缘检测**:
   - **Laplacian 边缘检测**: 使用 `cv.Laplacian` 进行边缘检测。
   - **Sobel 边缘检测**: 使用 `cv.Sobel` 分别在 x 和 y 方向进行边缘检测，并结合结果。
   - **Canny 边缘检测**: 使用 `cv.Canny` 进行高级边缘检测。

3. **直方图**:
   - **灰度直方图**: 使用 `cv.calcHist` 计算灰度直方图，并使用 `matplotlib` 绘制直方图。
   - **彩色直方图**: 计算 BGR 三个通道的直方图，并在同一图表中绘制。

4. **图像分割与阈值化**:
   - **简单阈值化**: 使用 `cv.threshold` 进行固定阈值处理。
   - **自适应阈值化**: 使用 `cv.adaptiveThreshold` 进行局部阈值处理。

5. **人脸检测**:
   - **Haar 特征级联分类器**: 使用预训练的 `haar_face.xml` 模型进行人脸检测。

6. **项目实现**:
   - **人脸检测与识别系统**: 使用 Haar Cascade 进行人脸检测，并提取 ROI 进行训练和识别。

## 依赖项
- Python 3.8.5
- OpenCV
- NumPy
- Matplotlib