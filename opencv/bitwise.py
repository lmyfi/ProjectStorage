import cv2 as cv
import numpy as np

blank = np.zeros((500,500),dtype='uint8')
cv.imshow("Blank",blank)

# Rectangle 矩形，将矩形区域填充为白色255
rectangle = cv.rectangle(blank.copy(),(30,30),(440,440),255,-1)
cv.imshow("Rectangle", rectangle)

# Circle 圆形，将圆形填充为白色
circle = cv.circle(blank.copy(),(250,250),250,255,-1)
cv.imshow("Circle", circle)

# AND, 按位与，找出交叉的区域
bitwise_and = cv.bitwise_and(rectangle,circle)
cv.imshow("AND", bitwise_and)

# OR, 按位或，  找出相交和没相交的区域
bitwise_or = cv.bitwise_or(rectangle,circle)
cv.imshow("AND", bitwise_or)

# XOR, 异或， 找出没相交的区域
bitwise_xor = cv.bitwise_xor(rectangle, circle)
cv.imshow("XOR", bitwise_xor)

cv.waitKey(0)