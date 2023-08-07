import cv2
import cv2.aruco as aruco
import numpy as np
import math as m
import requests as rq

capture=cv2.VideoCapture(0)

# dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_250)
# parameters =  cv.aruco.DetectorParameters()
# detector = cv.aruco.ArucoDetector(dictionary, parameters)

# frame = cv.imread(...)

# markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)


def findAruco(img, marker_size=7,total_markers=250,draw=True):
    center_list=[]
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    parameters =  aruco.DetectorParameters()
    detector = aruco.ArucoDetector(dictionary, parameters)

    corners, ids, rejected = detector.detectMarkers(gray)

    print(ids)
    if len(corners) > 0:
	# flatten the ArUco IDs list
        ids = ids.flatten()
        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
            # extract the marker corners (which are always returned in
            # top-left, top-right, bottom-right, and bottom-left order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            center=[cX,cY]
            center_list.append(center)
            cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
            mX = int((topRight[0] + bottomRight[0]) / 2.0)
            mY = int((topRight[1] + bottomRight[1]) / 2.0)
            x=mX-cX
            angle=m.degrees(m.atan2(mY-cY,mX-cX))
            angle=int(angle)
            if angle<0:
                angle+=360
            cv2.putText(img,f'{angle}',(cX-10,cY-10),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2,cv2.LINE_AA)    

img_path='arucos.png'
while True:
    ret,img=capture.read()
    # img=cv2.resize(img,(0,0),fx=0.5,fy=0.5)
    findAruco(img)
    
    if cv2.waitKey(1) & 0xFF== ord('q'):
        break
    cv2.imshow('Webcam',img)

capture.release()
cv2.destroyAllWindows()    
