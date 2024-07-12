import cv2 as cv
import numpy as np

img = cv.imread('Photos/park.jpg')
cv.imshow('Imgae',img)

gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow('gray',gray)

# 边缘检测 Edge Detection

# Laplacian,拉普拉斯算子
lap = cv.Laplacian(gray, cv.CV_64F) #cv.CV_64F: 输出图像的数据类型，使用 64 位浮点数以防止负数截断。
lap = np.uint8(np.absolute(lap)) #计算结果的绝对值，并转换为 8 位无符号整数。
cv.imshow('Laplacian', lap)

# Sobel算子，结合了高斯平滑和微分求导，一阶导数的边缘检测算子
sobelx = cv.Sobel(gray, cv.CV_64F, 1, 0) #1, 0: x 方向的导数为 1，y 方向的导数为 0。
sobely = cv.Sobel(gray, cv.CV_64F, 0, 1) #0, 1: x 方向的导数为 0，y 方向的导数为 1。
combined_sobel = cv.bitwise_or(sobelx,sobely) # 将 x 方向和 y 方向的边缘检测结果进行按位或操作，得到综合的边缘检测结果。

cv.imshow('Sobel x', sobelx)
cv.imshow('Sobel y', sobely)
cv.imshow('Combined_sobel', combined_sobel)

# canny算子，寻找梯度的局部最大值。
canny = cv.Canny(gray, 150, 175) #150, 175: 较低的阈值和较高的阈值，用于连接边缘。
cv.imshow('Canny', canny)

cv.waitKey(0)