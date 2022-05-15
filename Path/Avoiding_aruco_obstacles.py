import cv2 as cv
import cv2.aruco as aruco
import numpy as np
import math as m
import requests as rq

url='192.168.43.194'



def findAruco(img, marker_size=7,total_markers=250,draw=True):
    center_list=[]
    gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    key=getattr(aruco,f'DICT_ARUCO_ORIGINAL')
    arucoDict=aruco.Dictionary_get(key)
    arucoParam=aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv.aruco.detectMarkers(img, arucoDict,
	parameters=arucoParam)
    aruco_corners = []
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
            # cv.circle(img,topRight,5,(0,0,255),2)
            # cv.circle(img,bottomRight,5,(0,0,255),2)
            # cv.circle(img,topLeft,5,(0,0,255),2)
            # cv.circle(img,bottomLeft,5,(0,0,255),2)
            center=[cX,cY]
            center_list.append(center)
            cv.circle(img, (cX, cY), 4, (0, 0, 255), -1)
            mX = int((topRight[0] + bottomRight[0]) / 2.0)
            mY = int((topRight[1] + bottomRight[1]) / 2.0)
            x=mX-cX
            angle=m.degrees(m.atan2(mY-cY,mX-cX))
            angle=int(angle)
            if angle<0:
                angle+=360
            cv.putText(img,f'{angle}',(cX-10,cY-10),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),2,cv.LINE_AA)
            if (angle>45 and angle<135):
                aruco_corners.append([bottomLeft,topLeft,topRight,bottomRight,markerID])
            elif (angle>135 and angle<225):
                aruco_corners.append([bottomRight,bottomLeft,topLeft,topRight,markerID])
            elif (angle>225 and angle<315):
                aruco_corners.append([topRight,bottomRight,bottomLeft,topLeft,markerID])
            else:
                aruco_corners.append([topLeft,topRight,bottomRight,bottomLeft,markerID])
    return aruco_corners
def converting_to_pixel_coordinate_form(aruco_corner):
    for i in range(4):
        aruco_corner[i] = list(aruco_corner[i])
        aruco_corner[i][0],aruco_corner[i][1] = aruco_corner[i][1],aruco_corner[i][0]
    return aruco_corner
def aruco_rectangle_corner_one_point(aruco_corner): # pass pixel coordinate form
    m1 = min(aruco_corner[0][0],aruco_corner[1][0])
    aruco_corner[0][0] = m1
    aruco_corner[1][0] = m1

    m2 = max(aruco_corner[1][1],aruco_corner[2][1])
    aruco_corner[1][1] = m2
    aruco_corner[2][1] = m2

    m3 = max(aruco_corner[2][0],aruco_corner[3][0])
    aruco_corner[2][0] = m3
    aruco_corner[3][0] = m3

    m4 = min(aruco_corner[3][1],aruco_corner[0][1])
    aruco_corner[3][1] = m4
    aruco_corner[0][1] = m4

    return aruco_corner
def aruco_rectangle_corner_points(aruco_corners): # no need to pass pixel coordinate form
    for i in range(len(aruco_corners)):
        aruco_corner = aruco_corners[i]
        aruco_corner = converting_to_pixel_coordinate_form(aruco_corner)
        aruco_corner = aruco_rectangle_corner_one_point(aruco_corner)
    return aruco_corners #it will return each rectangle corner points enclosing each arucos
# def one_aruco_boundary(aruco_corner):
#     boundary = []
#     for i in range(aruco_corner[0][1],aruco_corner[1][1]+1):
#         boundary.append([aruco_corner[0][0],i])
#         boundary.append([aruco_corner[3][0],i])
#     for j in range(aruco_corner[0][0],aruco_corner[3][0]+1):
#         boundary.append([j,aruco_corner[0][1]])
#         boundary.append([j,aruco_corner[1][1]])
#     return boundary # pass pixel coordinate form and rectangle corner points enclosing an aruco

def one_aruco_area(aruco_corner):
    aruco_area = []
    for i in range(aruco_corner[0][0],aruco_corner[2][0]+2):
        for j in range(aruco_corner[0][1],aruco_corner[1][1]+2):
            aruco_area.append([i,j])
    return aruco_area
def whole_aruco_area(aruco_corners):
    aruco_corners = aruco_rectangle_corner_points(aruco_corners)
    # print("aruco_corners ",aruco_corners)
    arucos_areas = []
    for i in range(len(aruco_corners)):
        aruco_corner = aruco_corners[i]
        # print(aruco_corner)
        x = one_aruco_area(aruco_corner)
        # print(x)
        # print(x)
        arucos_areas.extend(x)
    return arucos_areas # # no need to pass (pixel coordinate form and rectangle corner points enclosing an aruco)

def find_aruco_grid_coord(i,j,coord,image_row,image_col,num_row,num_col):
    cr = image_row//num_row
    cl = image_col//num_col
    r = i//cr
    c = j//cl
    if (i%cr!=0 and j%cl!=0):
        # print(1)
        # print(r)
        # print(c)
        coord[r][c] = 0
        coord[r+1][c] = 0
        coord[r][c+1] = 0
        coord[r+1][c+1] = 0
    elif (i%cr==0 and j%cl!=0):
        # print(2)
        coord[r][c] = 0
        coord[r-1][c] = 0
        coord[r+1][c] = 0
        coord[r][c+1] = 0
        coord[r+1][c+1] = 0
        coord[r-1][c+1] = 0
    elif (i%cr!=0 and j%cl==0):
        # print(3)
        coord[r][c] = 0
        coord[r][c-1] = 0
        coord[r][c+1] = 0
        coord[r+1][c] = 0
        coord[r+1][c-1] = 0
        coord[r+1][c+1] = 0
    else:
        # print(i,j)
        # print(r,c)
        # print(coord.shape)
        # print(4)
        coord[r][c] = 0
        coord[r][c-1] = 0
        coord[r][c+1] = 0
        coord[r+1][c] = 0
        coord[r+1][c-1] = 0
        coord[r+1][c+1] = 0
        coord[r-1][c] = 0
        coord[r-1][c-1] = 0
        coord[r-1][c+1] = 0  # this function will find all those points which are near to i,j and make their values one in coord matrix
# img_path = "aruco2.jpeg"
# img = cv.imread(img_path)
# aruco_corners = findAruco(img)
# print(aruco_corners)
# print("whole ")
# print(whole_aruco_boundary(aruco_corners))
# [[(351, 204), (721, 204), (724, 567), (355, 575), 164]]
# [[204, 351], [204, 721], [567, 724], [575, 355], 164]
# print(converting_to_pixel_coordinate_form([(351, 204), (721, 204), (724, 567), (355, 575), 164]))
# print(aruco_rectangle_corner_one_point([[204, 351], [204, 721], [567, 724], [575, 355], 164]))
# print(aruco_rectangle_corner_points([[(351, 204), (721, 204), (724, 567), (355, 575), 164]]))
# [[[204, 355], [204, 724], [575, 724], [575, 355], 164]]
# print(whole_aruco_boundary([[[204, 355], [204, 724], [575, 724], [575, 355], 164]]))
# rect = whole_aruco_boundary([[(351, 204), (721, 204), (724, 567), (355, 575), 164]])
# print(rect) #[[[204, 351], [204, 724], [575, 724], [575, 351], 164]]
# cv.rectangle(img,(351,204),(724,575),(0,0,255),1)
# print(whole_aruco_boundary([[(577, 179), (405, 178), (408, 85), (576, 88), 164]]))

# print(one_aruco_boundary([[178, 576], [178, 408], [88, 408], [88, 576], 164]))
# aruco_boundary = whole_aruco_boundary(aruco_corners)
#
# for i in aruco_boundary:
#
#     find_grid_coord(i[0],i[1],the_map,image_row,image_col)















# cv.imshow("img",img)
# cv.waitKey(0)
