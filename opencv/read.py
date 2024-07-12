
import cv2 as cv


#读取单张图片
# img = cv.imread("Photos/cats.jpg")

# cv.imshow('Cat',img)

# cv.waitKey(0)

#读取视频文件
capture = cv.VideoCapture('Videos/dog.mp4')#参数为int:0,1,2的话是表示调用摄像头id，如果是路径的话就是按路径获取资源

while True:
    isTrue, frame = capture.read()

    cv.imshow("dog", frame)

    # cv.waitKey(20):
    # 这个函数等待 20 毫秒，以检查是否有按键事件。
    # 它返回一个整数，代表按键的 ASCII 码，但可能包含额外的高位数据。
    # & 0xFF:

    # 0xFF 是一个二进制掩码，等于 255（十六进制表示）。
    # 它的二进制形式是 11111111，即 8 个二进制 1。
    # & 是按位与操作符。
    # 当我们使用 & 0xFF 时，实际上是保留了返回值的低 8 位（最低的 8 位二进制数），并将高 8 位屏蔽掉
    if cv.waitKey(20) & 0xFF==ord('d'):
        break


capture.release()
cv.destroyAllWindows()
