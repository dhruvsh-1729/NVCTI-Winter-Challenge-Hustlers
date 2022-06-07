# NVCTI Winter Challenge-Warehouse Automation Prototype

Team Members
1. Ashutosh Singh
2. Arunim Basak
3. Dhruv Shah
4. Ayush Gupta
# *PATH ALGORITHM*

The path algorithm used for estimating the shortest path that will be followed by the bot to reach from one stack to another stack is A-Star.
A* Search algorithm is one of the best and popular techniques used in path-finding and graph traversals.Unlike other traversal approaches, A* Search algorithms have brains. What this means is that it is a sophisticated algorithm that distinguishes itself from other algorithms. 
It's also worth noting that many games and web-based maps employ this approach to effectively locate the shortest path (approximation).

Consider a square grid with numerous obstacles, as well as a starting and target cell. We aim to go to the target cell as rapidly as possible from the starting cell. Here The A* Search Algorithm saves the day.
At each stage, the A* Search Algorithm selects a node based on a value-'f,' which is a parameter equal to the sum of two other parameters – 'g' and 'h.' At each step, it selects the node/cell with the lowest 'f' and processes it.
We define 'g' and 'h' as simply as possible: 
g = the cost of moving from the starting point to a specific square on the grid using the path generated to get there.
h = the estimated movement cost to move from that given square on the grid to the final destination. This is often referred to as the Heuristic. Heuristic can be calculated using numerous methods like Euclidean distance, Manhattan distance etc.

# *SETUP OF THE ENVIRONMENT*

We will be having a mobile camera(in this case we are using the open-source DroidCam Client connected through common wifi network between mobile device and laptop) mounted on the top of the arena (here on the stair of a ladder) which will be taking live feed of the dynamic environment of the arena and feed each frames to the path algorithm code. In each frames, we will be having some obstacles in the arena and two arucos, one representing the robot and the other representing the stack.

# *WORKING OF THE PATH PLANNING ALGORITHM*

In the path algorithm code, first we will be using powerful Computer vision library called as OpenCV. Using the library,
the code would convert those images into a num_rows by num_cols grid and then detect the coordinates of obstacles in the arena and also the coordinates of two arucos ,according to the grid and then feed those coordinates into the A-Star (path-finding) algorithm. The A-Star ,then returns the coordinates of all those points which will be forming a shortest path from the robot to the stack, avoiding the obstacles.

# *WORKING OF ARUCO MARKER*

Two Aruco markers of known ids were generated and printed from an online resource. Then, using the opencv-contrib-python library which has the cv2.aruco library, programming it for the ORIGINAL_ARUCO markers, we are able to identify the markers in the frame received and are able to write code to get the coordinates of the corners, centers of the markers and the orientation or the polar angle of the markers in degrees. Using all of this data we have written the code such that aruco on the robot makes the robot chase the aruco on the stacks in the same frame. Hence, making the movement of the robot autonomous.

# *HANDLING THE DYNAMIC ENVIRONMENT*

Using the A-Star algorithm , we would be handling the dynamic environment of the arena. Suppose during the robot movement ,following the shortest path, an obstacle suddenly comes in its path.
Then an emergency command will run which will stop the robot immediately and then the robot waits for some specific time for the obstacle to get away. If the obstacle gets away then the robot will follow the same path to reach its destination. But if it doesnt move , then the path finding code will run again and calculates a new shortest path and then the robot will follow that new path. Thus , in this way we will be handling the dynamic environment. 

# *PICKING UP THE STACKS*
Once the robot reaches the destination stack Aruco, it goes underneath the stack stool and lifts it up using the automated scissor jack, which is made from welding the gear motor shaft to the double threaded screw of the scissor jack. Though we could not implement this before the deadline since it was not possible for us to make a custom stool such that our robot goes underneath it and lifts it up but still we have automated the entire process so if we had the stool and the stacks kept over it the system would still work perfectly fine.


1. 
  ![p1](https://user-images.githubusercontent.com/96870948/168494970-9ce14182-3b30-4502-b7bd-4468c915e881.png)

The arena depicted above. Red dot representing the starting point and Blue dot representing the destination point and the other objects are the obstacles.



2. 
  ![p2](https://user-images.githubusercontent.com/96870948/168494995-21a272da-ee06-47d3-bd64-134ad73f6df9.png)

Using Opencv, the obstacles are detected and rectangles are drawn around them.



3. 
  ![p3](https://user-images.githubusercontent.com/96870948/168495013-76d2fe3a-287a-4e45-959e-4df1dd9e8833.png)

After getting the coordinates of the obstacles and feeding to the path finding algorithm , the shortest path is found out and then drawn it into the image.



4. 
  ![p4](https://user-images.githubusercontent.com/96870948/168495026-34cc66cd-3565-4044-a68c-b4742e3d30e2.png)

These are the coordinates of the routes that are found out using the path finding algorithm.

