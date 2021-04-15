import cv2
import numpy

def hp(x):
    print("")


cap = cv2.VideoCapture(0)
bars = cv2.namedWindow("bars")
#Person using this can set the HSV values as per his/her requirements 
cv2.createTrackbar("upper hue","bars",160,180,hp)
cv2.createTrackbar("upper saturation","bars",100, 255, hp)
cv2.createTrackbar("upper value","bars",100, 255, hp)
cv2.createTrackbar("lower hue","bars",30,255,hp)
cv2.createTrackbar("lower saturation","bars",100, 255, hp)
cv2.createTrackbar("lower value","bars",100, 255, hp)

#Capturing the first frame in order to use that as background 
while(True):
	cv2.waitKey(1000)
	ret,init_frame = cap.read()

	if(ret):
		break

 
while(True):
	ret,frame = cap.read()
	inspect = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	
	upper_hue = cv2.getTrackbarPos("upper hue", "bars")
	upper_saturation = cv2.getTrackbarPos("upper saturation", "bars")
	upper_value = cv2.getTrackbarPos("upper value", "bars")
	lower_value = cv2.getTrackbarPos("lower value","bars")
	lower_hue = cv2.getTrackbarPos("lower hue","bars")
	lower_saturation = cv2.getTrackbarPos("lower saturation","bars")

	
	kernel = numpy.ones((3,3),numpy.uint8)

	upper_hsv = numpy.array([upper_hue,upper_saturation,upper_value])
	lower_hsv = numpy.array([lower_hue,lower_saturation,lower_value])

	mask = cv2.inRange(inspect, lower_hsv, upper_hsv)
	mask = cv2.medianBlur(mask,3)
	mask_inv = 255-mask 
	mask = cv2.dilate(mask,kernel,5)
	
	
	b = frame[:,:,0]
	g = frame[:,:,1]
	r = frame[:,:,2]
	b = cv2.bitwise_and(mask_inv, b)
	g = cv2.bitwise_and(mask_inv, g)
	r = cv2.bitwise_and(mask_inv, r)
	frame_inv = cv2.merge((b,g,r))

	b = init_frame[:,:,0]
	g = init_frame[:,:,1]
	r = init_frame[:,:,2]
	b = cv2.bitwise_and(b,mask)
	g = cv2.bitwise_and(g,mask)
	r = cv2.bitwise_and(r,mask)
	blanket_area = cv2.merge((b,g,r))

	final = cv2.bitwise_or(frame_inv, blanket_area)

	cv2.imshow("Invisibility Cloak",final)

	if(cv2.waitKey(3) == ord('q')):
		break;

cv2.destroyAllWindows()
cap.release()




