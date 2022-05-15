import numpy as np
import cv2 as cv
from A_STAR import *
from Avoiding_aruco_obstacles import *
def find_grid_coord(i,j,coord,image_row,image_col):
    cr = image_row//num_row
    cl = image_col//num_col
    r = i//cr
    c = j//cl
    if (r==num_row):
        r = num_row-1
    if (c == num_col):
        c = num_col-1
    if (i%cr!=0 and j%cl!=0):
        # print(1)
        # print(r)
        # print(c)
        coord[r][c] = 1
        coord[r+1][c] = 1
        coord[r][c+1] = 1
        coord[r+1][c+1] = 1
    elif (i%cr==0 and j%cl!=0):
        # print("2th")
        # print(i,j)
        # print(r,c)
        coord[r][c] = 1
        coord[r-1][c] = 1
        coord[r+1][c] = 1
        coord[r][c+1] = 1
        coord[r+1][c+1] = 1
        coord[r-1][c+1] = 1
    elif (i%cr!=0 and j%cl==0):
        # print(3)
        coord[r][c] = 1
        coord[r][c-1] = 1
        coord[r][c+1] = 1
        coord[r+1][c] = 1
        coord[r+1][c-1] = 1
        coord[r+1][c+1] = 1
    else:
        # print(i,j)
        # print(r,c)
        # print(coord.shape)
        # print(4)
        coord[r][c] = 1
        coord[r][c-1] = 1
        coord[r][c+1] = 1
        coord[r+1][c] = 1
        coord[r+1][c-1] = 1
        coord[r+1][c+1] = 1
        coord[r-1][c] = 1
        coord[r-1][c-1] = 1
        coord[r-1][c+1] = 1  # this function will find all those points which are near to i,j and make their values one in coord matrix
def optimise_route(route_coordinates):
    route_coordinates.append([-1,-1])
    i = 0
    j = 1
    Nroute_coordinates = []
    while (j<len(route_coordinates)):
        if route_coordinates[i][1]==route_coordinates[j][1]:
            while (route_coordinates[j][1]==route_coordinates[i][1]):
                j+=1
            Nroute_coordinates.append(route_coordinates[i])
            i = j-1
            if (j==len(route_coordinates)-1):
                Nroute_coordinates.append(route_coordinates[i])
                break
        else:
            while route_coordinates[i][0]==route_coordinates[j][0]:
                j+=1
            Nroute_coordinates.append(route_coordinates[i])
            i = j - 1
            if (j==len(route_coordinates)-1):
                Nroute_coordinates.append(route_coordinates[i])
                break
    route_coordinates.pop(len(route_coordinates)-1)
    return Nroute_coordinates
image_row = 600
image_col = 600
num_row = 10
num_col = 10

# I WILL HAVE THE COORDINATES OF BOUNDARIES OF RECTANGLE ENCLOSING THE ROBOT
# FOR SOURCE , I NEED THE CENTROID OF THOSE ABOVE POINTS
rowA,colA = 1,1
rowB,colB = 9,8
image_specifications = [image_row,image_col]
map_specifications = [num_row,num_col]
source = [rowA,colA]
destination = [rowB,colB]
def path_algorithm(image_specifications,map_specifications,image_path,source,destination):

    rowA,colA = source[0],source[1]
    rowB,colB = destination[0],destination[1]

    image_row = image_specifications[0]
    image_col = image_specifications[1]

    num_row = map_specifications[0]
    num_col = map_specifications[1]
    cr = image_row//num_row
    cl = image_col//num_col

    img_init = cv.imread(image_path)

    img = cv.resize(img_init, (image_col,image_row),interpolation = cv.INTER_NEAREST)
    img2 = img.copy()
    # cv.imshow("img2",img2)
    # cv.waitKey(0)
    cv.circle(img,(colA*cl,rowA*cr),10,(0,0,255),2)
    cv.circle(img,(colB*cl,rowB*cr),10,(255,0,0),2)
    cv.imshow("img",img)
    cv.waitKey(0)
    resize = cv.GaussianBlur(img,(11,11),cv.BORDER_DEFAULT)

    gray = cv.cvtColor(resize,cv.COLOR_BGR2GRAY)

    gray = cv.fastNlMeansDenoising(gray,None)

    _,threshold = cv.threshold(gray,100,255,cv.THRESH_BINARY)


    temp,contours = cv.findContours(threshold,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)

    corner_points = []
    for cnt in temp:
        (x,y,w,h) = cv.boundingRect(cnt)
        cv.rectangle(img,(x-10,y-10),(x+w+10,y+h+10),(255,0,0))
        if (x!=0 and y!=0):
            corner_points.append([x,y,w,h])

    cv.imshow("img",img)
    cv.waitKey(0)
    print(corner_points)
    def inside_or_not(source,destination,corner_points):
        for corner in corner_points:
            x,y,w,h = corner[0],corner[1],corner[2],corner[3]
            iss = False
            # [a,b]
            [s1,s2] = source[1],source[0]
            [d1,d2] = destination[1],destination[0]

            if (s1>x and s2> y and s1<(x+w) and s2<(y+h)):
                return True
            if (d1>x and d2> y and d1<(x+w) and d2<(y+h)):
                return True
    iss = inside_or_not(source,destination,corner_points)
    if iss==True:
        print("Invalid Points")
        return
    else:
        boundary = []
        for i in range(len(corner_points)):
            start = [corner_points[i][1],corner_points[i][0]]
            end = [corner_points[i][1]+corner_points[i][3],corner_points[i][0]+corner_points[i][2]]

            for j in range(start[0],end[0]+1):
                boundary.append([j,start[1]])
                boundary.append([j,end[1]])
            for k in range(start[1],end[1]+1):
                boundary.append([start[0],k])
                boundary.append([end[0],k])

        the_map = []
        horizontal_size_of_map = num_col + 1
        vertical_size_of_map = num_row + 1
        row = [0] * horizontal_size_of_map
        for i in range(vertical_size_of_map):
            the_map.append(list(row))


        # print("boundary ",boundary)

        for i in boundary:

            find_grid_coord(i[0],i[1],the_map,image_row,image_col)

        # print(np.array(the_map))
        # if findAruco(img2)!=None:
        aruco_corners = findAruco(img2)
        # print("aruco_corners ",aruco_corners)
        # cv.imshow("img2_2",img2)
        # cv.waitKey(0)
        if len(aruco_corners)>0:
            arucos_areas = whole_aruco_area(aruco_corners)
            print("arucos_areas ",arucos_areas)
            for i in arucos_areas:
                find_aruco_grid_coord(i[0],i[1],the_map,image_row,image_col,num_row,num_col)

        # print(np.array(the_map))

        rowA,colA = source[0],source[1]
        rowB,colB = destination[0],destination[1]
        xA,yA = colA,rowA
        xB,yB = colB,rowB
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        possible_directions = 4

        route = pathFind(the_map, horizontal_size_of_map, vertical_size_of_map,possible_directions, dx, dy, xA, yA, xB, yB)

        route_coordinates = []
        # print(route_coordinates)
        if len(route) > 0:
            x = xA
            y = yA
            the_map[y][x] = 2
            route_coordinates.append([y,x])
            for i in range(len(route)):
                j = int(route[i])
                x += dx[j]
                y += dy[j]
                the_map[y][x] = 3
                route_coordinates.append([y,x])
            the_map[y][x] = 4

        cr = image_row//num_row
        cl = image_col//num_col
        route_coordinates_converted = [[route_coordinates[0][0]*cr,route_coordinates[0][1]*cl]]
        for i in range(1,len(route_coordinates)):
            [a,b] = route_coordinates[i][0]*cr,route_coordinates[i][1]*cl
            route_coordinates_converted.append([a,b])
        for i in range(1,len(route_coordinates_converted)):
            a2 = route_coordinates_converted[i]
            a1 = route_coordinates_converted[i-1]
            cv.line(img,(a1[1],a1[0]),(a2[1],a2[0]),(0, 210, 0), 2)


        # route_coordinates_converted = []
        # for i in range(1,len(route_coordinates)):
        #     a,b = route_coordinates[i][0]*cr,route_coordinates[i][1]*cl
        #     route_coordinates_converted.append([a,b])

        new_route_coordinates_converted = optimise_route(route_coordinates_converted)
        return img,new_route_coordinates_converted


img,route_coordinates = path_algorithm(image_specifications,map_specifications,"Object3.jpeg",source,destination)
print(route_coordinates)
print("showing img..")
cv.imshow("img",img)
cv.waitKey(0)
