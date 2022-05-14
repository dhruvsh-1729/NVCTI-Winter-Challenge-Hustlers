import cv2
import cv2.aruco as aruco
import time
import math as m
import requests as rq
import numpy as np

url='192.168.0.7'

capture=cv2.VideoCapture(1)

def findAruco(img, marker_size=7,total_markers=250,draw=True):
    center_list=[]
    angle_dic={}
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key=getattr(aruco,f'DICT_ARUCO_ORIGINAL')
    arucoDict=aruco.Dictionary_get(key)
    arucoParam=aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(img, arucoDict,
	parameters=arucoParam)

    # print(ids)
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
            angle_dic[markerID]=angle
            cv2.putText(img,f'{angle}',(cX-10,cY-10),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2,cv2.LINE_AA) 
            
        # print(center_list)
        # print(angle_dic)
        
        if len(ids)==2:
            [x,y]=[int(m.fabs(center_list[0][0]-center_list[1][0])),int(m.fabs(center_list[0][1]-center_list[1][1]))]
            print(x,y)
            if(x>150 or y>150):
                dis=m.sqrt(m.pow(x,2)+m.pow(y,2))
                dis=int(dis)
                print(dis)
                theta=m.degrees(m.atan2(y,x))
                theta=int(theta)
                if theta<0:
                    theta+=360
                print(angle_dic[164],theta)

                if(angle_dic[164]<(theta-5)):
                    r=rq.get(url="http://"+url+"/sright")
                    print('SR')
                    time.sleep(0.5)
                elif(angle_dic[164]>(theta+5)):
                    r=rq.get(url="http://"+url+"/sleft")
                    print('SL')
                    time.sleep(0.5)
                elif(angle_dic[164]>(theta-5) or angle_dic[164]<(theta+5)):
                    r=rq.get(url="http://"+url+"/Forward")
                    print('F') 
                    time.sleep(0.5)   
            else:
                if(angle_dic[164]<354 and angle_dic[164]>300):
                    r=rq.get(url="http://"+url+"/sright")
                    print('SR')
                    time.sleep(0.5)
                elif(angle_dic[164]>6 and angle_dic[164]<60):
                    r=rq.get(url="http://"+url+"/sleft")
                    print('SL')
                    time.sleep(0.5)
                elif(angle_dic[164]<=6 and angle_dic[164]>=354):
                    r=rq.get(url="http://"+url+"/Forward")
                    print('F')
                    time.sleep(0.5)
while True:
    ret,img=capture.read()
    # img=cv2.resize(img,(0,0),fx=0.5,fy=0.5)
    findAruco(img)
    
    if cv2.waitKey(1) & 0xFF== ord('q'):
        break
    cv2.imshow('Webcam',img)

capture.release()
cv2.destroyAllWindows()                      
                