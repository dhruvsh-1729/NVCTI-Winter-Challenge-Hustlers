import cv2
import cv2.aruco as aruco
import time
import math as m
import requests as rq
import numpy as np

url='192.168.43.194'

capture=cv2.VideoCapture(0)

def get_frame():
    ret,frame=capture.read()
    return frame

def findAruco(img, marker_size=7,total_markers=250,draw=True):
    center_list=[]
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key=getattr(aruco,f'DICT_ARUCO_ORIGINAL')
    arucoDict=aruco.Dictionary_get(key)
    arucoParam=aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(img, arucoDict,
	parameters=arucoParam)

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
            
        if len(corners)==2:
            [x,y]=[m.fabs(center_list[0][0])-m.fabs(center_list[1][0]),m.fabs(center_list[0][1]-center_list[1][1])]
            while(angle<357 and angle>3):
                if angle<357:
                    r=rq.get(url="http://"+url+"/sright")
                    print("SR")
                elif angle>3:
                    r=rq.get(url="http://"+url+"/sleft")
                    print("SL")
                    
                
