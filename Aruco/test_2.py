import cv2
import cv2.aruco as aruco
import time
import math as m
import requests as rq
import numpy as np

url='192.168.43.16'

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
            [x,y]=[int(m.fabs(center_list[0][0]-center_list[1][0])-100),int(m.fabs(center_list[0][1]-center_list[1][1]))]
            print(x,y)

            if x>150 and y>=30:
                
                if angle_dic[164]>10 and angle_dic[164]<30:
                    print(angle_dic[164])
                    while angle_dic[164]>10:
                        r=rq.get(url="http://"+url+"/sleft")
                        print('SL')
                        time.sleep(0.2)
                elif angle_dic[164]<=350 and angle_dic[164]>330:
                    print(angle_dic[164])
                    while angle_dic[164]<=350:
                        r=rq.get(url="http://"+url+"/sright")
                        print('SR')
                        time.sleep(0.2)
                else: 
                    print(angle_dic[164])       
                    r=rq.get(url="http://"+url+"/Forward") 
                    print('F')  
                    print('Going straight')    
            elif x<=150 and y>=30:
                print(x,y)
                if angle_dic[164]>100 and angle_dic[164]<120:
                    print(angle_dic[164])
                    while angle_dic[164]>100:
                        r=rq.get(url="http://"+url+"/sleft")
                        print('SL')
                        time.sleep(0.2)
                elif angle_dic[164]<80 and angle_dic[164]>60:
                    print(angle_dic[164])
                    while angle_dic[164]<80:
                        r=rq.get(url="http://"+url+"/sright")
                        print('SR')
                        time.sleep(0.2)
                else:        
                    print(angle_dic[164])
                    r=rq.get(url="http://"+url+"/Forward") 
                    print('F')  
            elif x<0 and y<=30 and x>-60:
                
                if angle_dic[164]>10 and angle_dic[164]<70:
                    print(angle_dic[164])
                    while angle_dic[164]>5:
                        r=rq.get(url="http://"+url+"/sleft")
                        print('SL')
                        time.sleep(0.2)
                    r=rq.get(url="http://"+url+"/Forward")
                    print('F')
                    time.sleep(0.2)
                    r=rq.get(url="http://"+url+"/Forward")
                    print('F')
                    time.sleep(0.2)
                    for i in range(20):
                        r=rq.get(url="http://"+url+"/DOWN")
                    time.sleep(4)
                    for i in range(20):
                        r=rq.get(url="http://"+url+"/UP")
                    
                else:        
                    print(angle_dic[164])
                    r=rq.get(url="http://"+url+"/Forward")    
                    print('F')
                    
            

while True:
    ret,img=capture.read()
    # img=cv2.resize(img,(0,0),fx=0.5,fy=0.5)
    findAruco(img)
    
    if cv2.waitKey(1) & 0xFF== ord('q'):
        break
    cv2.imshow('Webcam',img)

capture.release()
cv2.destroyAllWindows()                      
                                      
                