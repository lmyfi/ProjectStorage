import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

img = cv.imread("Photos/park.jpg")
cv.imshow("Park", img)

blank = np.zeros(img.shape[:2],dtype='uint8')

# 提取三通道，b-蓝色，g-绿色，r-红色
b,g,r = cv.split(img)

cv.imshow("Blue_single",b)
cv.imshow("Green_single",g)
cv.imshow('Red_single',r)

# 将其他两个通道置为blank（空），构建三通道的b,g,r图像
blue = cv.merge([b,blank,blank])
green = cv.merge([blank,g,blank])
red = cv.merge([blank,blank,r])

cv.imshow("Blue",blue)
cv.imshow("Green",green)
cv.imshow('Red',red)

cv.waitKey(0)