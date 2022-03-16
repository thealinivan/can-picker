import cv2

vc = cv2.VideoCapture(0)
while vc.isOpened():
    rval, frame = vc.read()
    cv2.imshow("stream", frame)
    if key ==27:
        break
cv2.destroyWindow("stream")
vc.release()
