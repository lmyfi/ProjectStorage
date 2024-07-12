import cv2 as cv
import numpy as np

img = cv.imread("Photos/cats.jpg")
cv.imshow("Cats",img)

blank = np.zeros(img.shape[:2],dtype='uint8')
cv.imshow("Blank", blank)

circle = cv.circle(blank,(blank.shape[1]//2,blank.shape[0]//2),100,255,-1)
cv.imshow("Circle", circle)

# 按位操作是masked遮掩的基础
masked = cv.bitwise_and(img,img,mask=circle)
cv.imshow("Masked",masked)

cv.waitKey(0)