import cv2 as cv
import numpy as np
import os

# 构建人脸识别对象列表，列表中存放它们的名字
people = []
DIR = r'E:\study\yotube\opencv_course_full_Tutorial_with_Python\opencv\Faces\train'
for path in os.listdir(DIR):
    people.append(path)
print(people)

# 构建haarcascade人脸检测器
haar_cascade = cv.CascadeClassifier('haar_face.xml')

# 加载保存的faces_roi(脸部region of interest)和标签labels,以及保存的训练好的人脸识别模型
features = np.load('features.npy', allow_pickle=True)
labels = np.load('labels.npy')

face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_train.yml')

# 测试
img = cv.imread(r"E:\study\yotube\opencv_course_full_Tutorial_with_Python\opencv\Faces\val\ben_afflek\2.jpg")
cv.imshow("Images", img)

# gray
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow("Gray", gray)

# Detect the face in the image
faces_rect = haar_cascade.detectMultiScale(gray,1.1,4)

for (x,y,w,h) in faces_rect:
    # 裁剪出脸部
    faces_roi = gray[y:y+h,x:x+w]
    # 对脸部进行识别预测
    label, confidence = face_recognizer.predict(faces_roi)
    print(f'Label = {people[label]} whith a confidence = {confidence}')

    cv.putText(img, str(people[label]), (20,20), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), thickness=2)

    cv.rectangle(img, (x,y),(x+w,y+h), (0,255,0),2)

cv.imshow("Face Recognition",img)

cv.waitKey(0)
