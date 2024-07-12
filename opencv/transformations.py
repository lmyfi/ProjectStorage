import cv2 as cv
import numpy as np

img = cv.imread("Photos/park.jpg")
cv.imshow("Park", img)

# 图像位置移动--平移操作
def translate(img, x, y):
    # transMat 是一个 2x3 的浮点数矩阵，用来描述平移变换。
    # [1, 0, x] 表示在 x 方向上的平移量。
    # [0, 1, y] 表示在 y 方向上的平移量。
    transMat  = np.float32(([1,0,x],[0,1,y]))
    # cv.warpAffine() 是 OpenCV 中的函数，用于应用仿射变换到图像上。
    # 它接受三个主要参数：
    # img：输入的图像。
    # transMat：变换矩阵，描述了要应用的仿射变换类型。
    # dimensions：输出图像的尺寸，通常与输入图像相同。
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)

# -x --> Left
# -y --> Up
# x  --> Right
# y --> Down
shift = translate(img,100,100)
cv.imshow("Sift",shift)

#图像旋转
def rotate(img, angle, rotPoint=None):
    (height, width) = img.shape[:2]

    if rotPoint is None:
        rotPoint = (width//2,height//2)
    
    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width, height)

    return cv.warpAffine(img, rotMat, dimensions)

rotated = rotate(img, -45)
cv.imshow("Rotate", rotated)

rotated_rotated = rotate(rotated, -45)
cv.imshow('Rotated Rotated', rotated_rotated)

# Resizing
resized = cv.resize(img, (500,500), interpolation=cv.INTER_CUBIC)
cv.imshow('Resized', resized)

# Flipping 翻转
flip = cv.flip(img, -1)
cv.imshow("Flip",flip)

# Cropping,裁剪
cropped = img[200:400, 300:400]
cv.imshow("Cropped",cropped)

cv.waitKey(0)