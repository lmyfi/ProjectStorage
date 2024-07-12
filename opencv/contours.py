import cv2 as cv
import numpy as np

img = cv.imread("Photos/cats.jpg")
cv.imshow("Cats",img)

# 创建空白图像，大小与img一样
blank = np.zeros(img.shape, dtype='uint8')
cv.imshow("Blank", blank)

# 将bgt图转换为灰度图gray。减少图像信息，灰度图像里的信息已经足够了，加快计算速度
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow('Gray',gray)

# 边缘级联，提取出图片内容的轮廓
canny = cv.Canny(img, 125, 175)
cv.imshow('Canny Edges', canny)

# 将图像进行类似二值化操作
ret, thresh = cv.threshold(gray, 125, 255, cv.THRESH_BINARY)
cv.imshow('Thresh', thresh)

# 查找轮廓：
# contours, hierarchies = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)：在二值图像中查找轮廓。
# thresh：输入的二值图像。
# cv.RETR_LIST：轮廓检索模式，检索所有轮廓。
# cv.CHAIN_APPROX_SIMPLE：轮廓近似方法，仅保存轮廓的拐点。
# print(f'{len(contours)} contour(s) found')：打印找到的轮廓数量。
contours, hierachies = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
print(f'{len(contours)} contour(s) found')

# 将找到的轮廓信息绘制到空白窗口上
# 绘制轮廓：
# cv.drawContours(blank, contours, -1, (0, 0, 255), 1)：在空白图像上绘制找到的所有轮廓。
# blank：绘制轮廓的目标图像。
# contours：要绘制的轮廓列表。
# -1：绘制所有轮廓。
# (0, 0, 255)：轮廓颜色（红色）。
# 1：轮廓线条宽度。
# cv.imshow('Contours Drawn', blank)：显示绘制了轮廓的空白图像。
cv.drawContours(blank, contours, -1, (0,0,255), 1)
cv.imshow('Contours Drawn', blank)

cv.waitKey(0)


