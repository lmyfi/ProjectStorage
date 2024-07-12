import cv2 as cv

img = cv.imread("Photos/cats.jpg")
cv.imshow("Park",img)

#图像增强--图像平滑操作
# Averaging 均值滤波
averaged = cv.blur(img,(3,3))
cv.imshow('Averaging', averaged)

# Gaussian 高斯滤波
gaussian = cv.GaussianBlur(img, (3,3), 0)
cv.imshow("Gussian",gaussian)

# Median 中值滤波
median = cv.medianBlur(img,3)
cv.imshow("Median", median)

# bilateral 双边滤波
bilateral = cv.bilateralFilter(img, 10, 35,25)
cv.imshow('Bilateral', bilateral)

cv.waitKey(0)
