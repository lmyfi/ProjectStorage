import cv2 as cv

img = cv.imread("Photos/park.jpg")
cv.imshow("Park", img)

#图像处理函数
# Converting to grayscale,转成灰度图
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("Gray", gray)

# Blur，模糊化图片
blur = cv.blur(img, (7,7), cv.BORDER_DEFAULT) #ksize模糊核大小（7，7)
cv.imshow("Blur", blur)

# Edge Cascade,边缘级联（提取出图像中内容的轮廓）
canny = cv.Canny(blur,125,175) #threshold,阈值
cv.imshow("Canny", canny)

# Dilating the image,图像膨胀
dilated = cv.dilate(canny, (7,7), iterations=3)
cv.imshow("Dilate", dilated)

# Eroding, 图像腐蚀操作，可以将膨胀的效果抵消
eroded = cv.erode(dilated, (7,7), iterations=3)
cv.imshow("Erode", eroded)

# Resize, 修改尺寸
resized = cv.resize(img, (500,500), interpolation=cv.INTER_CUBIC)
cv.imshow("Resized", resized)

# Cropping，裁剪
cropped = img[50:200, 200:400]
cv.imshow('Cropped', cropped)
                 

cv.waitKey(0)
