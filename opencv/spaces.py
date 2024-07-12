import cv2 as cv

#颜色空间转换
#BGR 
img = cv.imread("Photos/park.jpg")
cv.imshow('BGR', img)
#GRAY
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow('Gray',gray)
#HSV
hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
cv.imshow('HSV',hsv)
#Lab
lab = cv.cvtColor(img,cv.COLOR_BGR2Lab)
cv.imshow("Lab",lab)

cv.waitKey(0)