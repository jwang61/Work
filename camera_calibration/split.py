import cv2

cap = cv2.VideoCapture('newcap.avi')
for count in range(1000):
    ret, img = cap.read()
    cv2.imwrite('video2/img{}.jpg'.format(count), img)

