# Obstacle Detection and Shortest Route Planning
Contains the python code for identifying shortest route and presence of obstacle using Open CV and Image Processing.
The file shortest_path_code using OpenCV and Shortest-Route(Detailed) contains python code consisting of required functions to detect the shortest route between the origin and the destination(denoted by blue box) as well as detect presence of obstacles if any, on the path supposed to be traversed by the Robot using Image processing and Open CV.
The code checks for different sample cases uploaded in path.jpeg and main_image.jpeg file. The file labelled delatiled shows the output in a detailed and self explinable manner.
## Control-O-Bot
This project developes a mechanism to identify the shortest path leading to the destination and avoiding any kind of obstacle during robot’s traversal route. This is the first step of our Open CV project which aims at simulating our Control-O-Bot.
### Given:

A set of test images, each containing

1. 10x10 grid, making 100 squares
2. Obstacles marked as black square
3. Starting and ending point of route marked in blue boxes.



The squares are identified by the coordinate (x,y) where x is the column and y is the row to which the square belongs. Each square
can be empty or have an Obstacle or have an Object.

### The command window shall display the following parameters: 
1. Process points 
2. Total Number of occupied grids 
3. Coloured occupied grids 
4. Total Number of coloured occupied grids 
5. Dictionary keys of planned path 
6. Coordinates of planned path 
