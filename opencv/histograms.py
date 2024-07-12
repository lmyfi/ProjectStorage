import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img = cv.imread("Photos/Cats.jpg")
cv.imshow("Image",img)

# 空白数字矩阵
blank = np.zeros(img.shape[:2],dtype='uint8')


# 灰度图
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("Gray",gray)

# circle
circle = cv.circle(blank,(blank.shape[1]//2,blank.shape[0]//2), 100, 255, -1)
cv.imshow("Mask", circle)

# Grayscale histogram
gray_hist = cv.calcHist([gray], [0], None, [256], [0,256])

# plt.figure()
# plt.title("Grayscale Histogram")
# plt.xlabel("bins")
# plt.ylabel('# of pixels')
# plt.plot(gray_hist)
# plt.xlim([0,256])
# plt.show()

# plt.figure(): 创建一个新的图像。
# plt.title("Colour Histogram"): 设置图像的标题。
# plt.xlabel("Bins"): 设置 x 轴的标签。
# plt.ylabel("# of pixels"): 设置 y 轴的标签。
# colors = ('b', 'g', 'r'): 定义颜色通道的元组，分别为蓝色、绿色和红色。
# for i,col in enumerate(colors): 遍历每个颜色通道。
# i 是通道的索引，col 是颜色。
# hist = cv.calcHist([img], [i], circle, [256], [0,256]): 计算每个颜色通道的直方图。参数解释如下：
# [img]: 输入图像，是一个列表。
# [i]: 当前通道的索引。
# circle: 掩码，用于只计算图像中的某些部分（这里是圆形掩码）。
# [256]: 直方图的维度，即直方图的 bin 数量。
# [0,256]: 像素值的范围。
# plt.plot(hist, col): 绘制颜色直方图。
# plt.xlim([0,256]): 设置 x 轴的范围。
# plt.show(): 显示图像。
plt.figure()
plt.title("Colour Histogram")
plt.xlabel("Bins")
plt.ylabel("# of pixels")
colors = ('b', 'g', 'r')
for i,col in enumerate(colors):
    # 使用circle图形去遮掩img
    hist = cv.calcHist([img], [i], circle, [256], [0,256])
    plt.plot(hist,col)
    plt.xlim([0,256])
plt.show()

cv.waitKey(0)