import cv2
import numpy as np
import cv2.aruco as aruco
import sys

CAMERAMATRIX = [2079.8, 0, 960, 0, 2079.8, 540, 0, 0, 1]
DISTORTION = [0.05235, 2.277, 0, 0, -11.87] 

cap = cv2.VideoCapture(sys.argv[1])
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)
parameters =  aruco.DetectorParameters_create()
cam_reshaped = np.reshape(CAMERAMATRIX, (3,3))
dist_reshaped = np.reshape(DISTORTION, (5,))
while (cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('other', cv2.resize(gray, (0,0), fx=0.5, fy=0.5))
    if len(sys.argv) > 2:
        blur = cv2.GaussianBlur(gray, (0,0), 3)
        gray = cv2.addWeighted(gray, 4, blur, -3, 0)
    #print(parameters)

    #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    rvec, tvec, objpoints = aruco.estimatePoseSingleMarkers(corners, 16, cam_reshaped, dist_reshaped)
    print tvec
    if (tvec != None):
        aruco.drawAxis(gray, cam_reshaped, dist_reshaped, rvec, tvec, 10)
    gray = aruco.drawDetectedMarkers(gray, corners)

    #print(rejectedImgPoints)
    # Display the resulting frame
    cv2.imshow('frame',cv2.resize(gray, (0,0), fx=0.5, fy=0.5))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
