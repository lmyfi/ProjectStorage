import os
import cv2 as cv
import numpy as np

people = ['Ben Afflek','Elton John','Jerry Seinfield','Madonna','Mindy Kaling']
DIR =r'E:\study\yotube\opencv_course_full_Tutorial_with_Python\opencv\Faces\train'

# face_detector
haar_cascade = cv.CascadeClassifier('haar_face.xml')
features = []
labels = []

def create_train():
    for person in people:
        path = os.path.join(DIR, person)
        label = people.index(person)

        print(f'peron:{person},path:{path},label:{label}')

        for img in os.listdir(path):
            img_path = os.path.join(path,img)

            img_array = cv.imread(img_path)
            gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

            faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

            for (x,y,w,h) in faces_rect:
                # 在图像处理中，图像的坐标系是以左上角为原点 (0, 0)，横向为 x 轴，纵向为 y 轴。
                # gray[y:y+h, x:x+w] 表示在灰度图像中从坐标 (x, y) 开始，宽度为 w，高度为 h 的矩形区域。
                # 在 NumPy 数组中，图像的第一个维度是行（对应 y 轴），第二个维度是列（对应 x 轴），因此要先指定 y 轴的范围再指定 x 轴的范围。
                faces_roi = gray[y:y+h, x:x+w] # faces_roi = gray[y:y+h, x:x+w]：

                features.append(faces_roi)
                labels.append(label)

create_train()
# print(f'features:{len(features)}')
# print(f'labels:{len(labels)}')

# Train the Recognizer on the features list and the labels list
face_recognizer = cv.face.LBPHFaceRecognizer_create()

features = np.array(features,dtype='object')
labels = np.array(labels)

face_recognizer.train(features,labels)
print('Traning Done----------------------------------')

face_recognizer.save('face_train.yml')
np.save('features.npy', features)
np.save('labels.npy',labels)
                

