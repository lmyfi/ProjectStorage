import cv2 as cv

def rescaling(frame, scale=0.75):

    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width,height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

def changeRes(width,height):
    capture.set(3,width)
    capture.set(4,height)

capture = cv.VideoCapture("Videos/dog.mp4")

while True:

    isTrue, frame = capture.read()

    rescale_frame = rescaling(frame,scale=.2)

    cv.imshow("Video", frame)
    cv.imshow("Video rescale", rescale_frame)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()


    
