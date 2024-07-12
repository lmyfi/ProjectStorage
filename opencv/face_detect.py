import cv2 as cv

img = cv.imread("Photos/group 1.jpg")
cv.imshow('People', img)

gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow('Gray People', gray)

# 基于haar特征的分类器
haar_cascade = cv.CascadeClassifier('haar_face.xml')

# 人脸检测
# haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)：
# 使用级联分类器在灰度图像中检测人脸。
# gray：输入的灰度图像。
# scaleFactor=1.1：图像缩放系数，用于创建图像金字塔。每次图像缩放后，图像尺寸缩小 10%，这样可以检测不同尺寸的人脸。
# minNeighbors=3：表示每一个候选矩形应该保留多少个邻近矩形，值越大，检测越严格，误检越少，但漏检可能增加。
# 参数解释
# gray：
# 输入的灰度图像。人脸检测通常在灰度图像上进行，因为颜色信息对于人脸检测的影响不大，而且灰度图像计算更快。
# scaleFactor：
# 图像缩放系数。这个参数决定了图像在多尺度搜索时的缩放程度。值越大，搜索的尺度越少，检测速度越快，但可能漏检小尺寸的人脸；值越小，搜索的尺度越多，检测速度越慢，但检测精度更高。
# minNeighbors：
# 每个候选矩形必须保留的最小邻居数。这个参数影响检测结果的质量。值越大，只有那些被更多邻近矩形检测到的区域才会被认为是人脸，误检减少，但漏检可能增加；值越小，检测更灵敏，误检可能增加。
face_detect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7)

print(f'Number of faces found = {len(face_detect)}')

for (x,y,w,h) in face_detect:
    cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),thickness=3)

cv.imshow("Face Detect", img)

cv.waitKey(0)