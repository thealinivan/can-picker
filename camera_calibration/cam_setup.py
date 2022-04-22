import cv2
vc = cv2.VideoCapture(2)
vc.set(3, 960)
vc.set(4, 1280)
while vc.isOpened():
	val, frame = vc.read()
	#frame = frame[100:450, 300:550]
	cv2.imshow("stream", frame)
	k=cv2.waitKey(1)
	if k==27: break
vc.release()