import cv2 as cv
import numpy as np

blank = np.zeros((500,500,3),dtype='uint8') #创建一个numpy.ndarray类型数组
print(type(blank))
cv.imshow("Blank",blank)

# 1. paint the image a certain colour（将图像画成一定的颜色）
blank[300:400,300:400] = 0,0,255 ##绘制一个红色的正方块
cv.imshow("green",blank[:])

# 2. Draw A Rectangle(画一个红色矩形)
cv.rectangle(blank,(0,0),(250,250),(0,0,255),thickness=-1)
cv.imshow("Rectangle Blank", blank)

# 3. Draw A Circle(画一个圆)
cv.circle(blank,(250,250),40,(0,255,0),thickness=3)
cv.imshow("cirle",blank)

# 4. Draw A line
cv.line(blank,(125,125),(500,500),(0,0,255),thickness=3)
cv.imshow("Line", blank)

# 5. Put A Text
cv.putText(blank, 'Hello my name is Ming',(0,255),cv.FONT_HERSHEY_COMPLEX,1.0, 
           (0,255,0), 2)
cv.imshow("Text",blank)
cv.waitKey(0)