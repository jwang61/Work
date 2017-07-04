import cv2
import sys


cap = cv2.VideoCapture(sys.argv[1])
for count in range(1000):
    ret, img = cap.read()
    cv2.imwrite('video2/img{}.jpg'.format(count), img)

