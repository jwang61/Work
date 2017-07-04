import numpy as np
import cv2
import cv2.aruco as aruco

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)
img = aruco.drawMarker(aruco_dict, 23, 700)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyWindow('img')
cv2.imwrite('aruco.bmp', img)

