import cv2 as cv
import numpy as np

cats = cv.imread("Photos/cats.jpg")
cv.imshow("Cats", cats)

# Gray 灰度图
gray = cv.cvtColor(cats,cv.COLOR_BGR2GRAY)
cv.imshow('Gray',gray)

# Simple thresholding
threshold, thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)
cv.imshow("Simple Thresholded", thresh)
print(threshold)

threshold2, thresh_Inv = cv.threshold(gray, 150, 255, cv.THRESH_BINARY_INV)
cv.imshow("Simple Thresholded Inverse", thresh_Inv)

# Adaptive thresholding,这段代码使用自适应阈值方法对灰度图像进行二值化处理

# ### 自适应阈值方法的原理
# 自适应阈值方法与全局阈值方法不同，它会根据图像的不同区域计算不同的阈值，使得在光照不均匀的条件下能够更好地处理图像。自适应阈值方法对每个像素计算阈值，这个阈值取决于其周围一定区域的像素值。
# OpenCV 提供了两种自适应阈值方法：
# 1. `cv.ADAPTIVE_THRESH_MEAN_C`: 阈值是区域内像素的平均值减去常数 C。
# 2. `cv.ADAPTIVE_THRESH_GAUSSIAN_C`: 阈值是区域内像素值的加权和（权重是一个高斯窗口）减去常数 C。

# ### 参数解释
# 1. `gray`:
#    - 输入图像，必须是单通道（灰度图像）。   
# 2. `255`:
#    - 阈值化后的最大值。如果一个像素值大于计算出的阈值，则将该像素值设置为该最大值（即 255）。
# 3. `cv.ADAPTIVE_THRESH_MEAN_C`:
#    - 自适应阈值方法。在这种情况下，阈值是区域内像素的平均值减去常数 C。
# 4. `cv.THRESH_BINARY`:
#    - 阈值化类型。这里选择二值化，即大于阈值的像素值设置为 `maxValue`（255），小于等于阈值的像素值设置为 0。
# 5. `11`:
#    - 阈值计算过程中使用的区域大小（即窗口大小）。这个窗口大小是一个奇数，表示在计算阈值时要考虑的邻域大小。在这种情况下，是 11x11 的区域。
# 6. `9`:
#    - 常数 C，在计算阈值时从区域的平均值或加权平均值中减去的值。这个常数用于调整阈值的灵敏度。
# ### 代码执行步骤
# 1. **计算邻域内的像素平均值**：
#    对于图像中的每个像素，以其为中心的 11x11 区域内的像素计算平均值。
# 2. **减去常数 C**：
#    将上一步计算的平均值减去常数 C（即 9）。
# 3. **比较并二值化**：
#    将每个像素值与上述计算出的自适应阈值进行比较。如果像素值大于阈值，则将其设置为 255，否则设置为 0。
# ### 具体的应用场景
# 自适应阈值化在处理具有不均匀光照或复杂背景的图像时非常有用，例如：
# - 文档图像处理，特别是扫描的文档可能会有阴影或光线不均匀的部分。
# - 车牌识别，在不同光照条件下拍摄的车牌图像。
# - 医学图像处理，例如在处理X射线或CT扫描图像时。
# 通过使用自适应阈值方法，可以更加鲁棒地提取图像中的重要特征，避免由于光照变化而导致的错误检测。
adaptive_thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 9)
cv.imshow('Adaptive Thresholding', adaptive_thresh)

cv.waitKey(0)


