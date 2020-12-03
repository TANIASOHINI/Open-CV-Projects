import cv2
import numpy as np
import time
from skimage.metrics import structural_similarity as ssim





def shortest_path_algorithm(m, startp, endp):
    w, h = 10, 10  # 10x10(blocks) is the dimension of the input images
    sx, sy = startp  # Start Point
    ex, ey = endp  # End Point
    # [parent node, x, y, g, f]
    node = [None, sx, sy, 0, abs(ex - sx) + abs(ey - sy)]
    closeList = [node]
    createdList = {}
    createdList[sy * w + sx] = node
    k = 0
    while (closeList):
        node = closeList.pop(0)
        x = node[1]
        y = node[2]
        l = node[3] + 1
        k += 1
        # find neighbours
        if k != 0:
            neighbours = ((x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y))
        else:
            neighbours = ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
        for nx, ny in neighbours:
            if nx == ex and ny == ey:
                path = [(ex, ey)]
                while node:
                    path.append((node[1], node[2]))
                    node = node[0]
                return list(reversed(path))
            if 0 <= nx < w and 0 <= ny < h and m[ny][nx] == 0:
                if ny * w + nx not in createdList:
                    nn = (node, nx, ny, l, l + abs(nx - ex) + abs(ny - ey))
                    createdList[ny * w + nx] = nn
                    # adding to closelist ,using binary heap
                    nni = len(closeList)
                    closeList.append(nn)
                    while nni:
                        i = (nni - 1) >> 1
                        if closeList[i][4] > nn[4]:
                            closeList[i], closeList[nni] = nn, closeList[i]
                            nni = i
                        else:
                            break


def traversal_window(image, stepSize, windowSize):
    ###############  slide a window across the image      #############################
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])

def astar(m,startp,endp):
    w,h = 10,10		# 10x10(blocks) is the dimension of the input images
    sx,sy = startp 	#Start Point
    ex,ey = endp 	#End Point
    #[parent node, x, y, g, f]
    node = [None,sx,sy,0,abs(ex-sx)+abs(ey-sy)]
    closeList = [node]
    createdList = {}
    createdList[sy*w+sx] = node
    k=0
    while(closeList):
        node = closeList.pop(0)
        x = node[1]
        y = node[2]
        l = node[3]+1
        k+=1
        #find neighbours
        if k!=0:
            neighbours = ((x,y+1),(x,y-1),(x+1,y),(x-1,y))
        else:
            neighbours = ((x+1,y),(x-1,y),(x,y+1),(x,y-1))
        for nx,ny in neighbours:
            if nx==ex and ny==ey:
                path = [(ex,ey)]
                while node:
                    path.append((node[1],node[2]))
                    node = node[0]
                return list(reversed(path))
            if 0<=nx<w and 0<=ny<h and m[ny][nx]==0:
                if ny*w+nx not in createdList:
                    nn = (node,nx,ny,l,l+abs(nx-ex)+abs(ny-ey))
                    createdList[ny*w+nx] = nn
                    #adding to closelist ,using binary heap
                    nni = len(closeList)
                    closeList.append(nn)
                    while nni:
                        i = (nni-1)>>1
                        if closeList[i][4]>nn[4]:
                            closeList[i],closeList[nni] = nn,closeList[i]
                            nni = i
                        else:
                            break
    return []


def main(image_filename, obstacles=[]):
    full_grids = []  # List to store coordinates of occupied grid
    expected_path = {}  # Dictionary to store information regarding path planning

    # load the image and define the window width and height
    image = cv2.imread(image_filename)
    (winW, winH) = (60, 60)  # Size of individual cropped images

    barrier = []  # List to store barrier (black tiles)
    index = [1, 1]
    blank_image = np.zeros((60, 60, 3), np.uint8)
    list_images = [[blank_image for i in range(10)] for i in range(10)]  # array of list of images
    maze = [[0 for i in range(10)] for i in range(10)]  # matrix to represent the grids of individual cropped images

    for (x, y, window) in traversal_window(image, stepSize=60, windowSize=(winW, winH)):
        # if the window does not meet our desired window size, ignore it
        if window.shape[0] != winH or window.shape[1] != winW:
            continue

        #	print index
        clone = image.copy()
        cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
        crop_img = image[x:x + winW, y:y + winH]  # crop the image
        list_images[index[0] - 1][index[1] - 1] = crop_img.copy()  # Add it to the array of images

        average_color_per_row = np.average(crop_img, axis=0)
        average_color = np.average(average_color_per_row, axis=0)
        average_color = np.uint8(average_color)  # Average color of the grids
        #	print (average_color)

        ##########     Check if grids are colored ie not majorly white and termed these grids as full_grids ######
        if (any(i <= 240 for i in average_color)):
            maze[index[1] - 1][index[0] - 1] = 1
            full_grids.append(tuple(index))
            print("occupied")

        ##########     Check if grids are black and add them to barrier list   ###########
        if (any(i <= 20 for i in average_color)):
            print("black obstacles")
            obstacles.append(tuple(index))

        cv2.imshow("Window", clone)
        cv2.waitKey(1)
        time.sleep(0.025)

        # Iterate
        index[1] = index[1] + 1
        if (index[1] > 10):
            index[0] = index[0] + 1
            index[1] = 1

    ####################       Write a statement to print the full_grids      ################
    print("Full Grids : ")
    print(full_grids)

    # Printing other info
    print("Total no of Occupied Grids : ")
    print(len(full_grids))
    print("Obstacles : ")
    print(obstacles)
    print("Map list: ")
    print(maze)
    print("Map : ")
    for x in range(10):
        for y in range(10):
            if (maze[x][y] == -1):
                print(str(maze[x][y])),
            else:
                print(" " + str(maze[x][y])),
        print("")

    # First part done
    ##############################################################################

    list_colored_grids = [n for n in full_grids if n not in barrier]  # Grids with objects (not black barrier)

    print("Colored Occupied Grids : ")
    print(list_colored_grids)
    print("Total no of Colored Occupied Grids : " + (str(len(list_colored_grids))))

    # Compare each image in the list of objects with every other image in the same list

    for startimage in list_colored_grids:
        key_startimage = startimage
        img1 = list_images[startimage[0] - 1][startimage[1] - 1]
        for grid in [n for n in list_colored_grids if n != startimage]:
            img = list_images[grid[0] - 1][grid[1] - 1]
            #		print "for {0} , other images are {1}".format(key_startimage, grid)
            image = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            image2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            s = ssim(image, image2)
            if s > 0.9:
                result = astar(maze, (startimage[0] - 1, startimage[1] - 1), (grid[0] - 1, grid[1] - 1))
                print(result)
                list2 = []
                for t in result:
                    x, y = t[0], t[1]
                    list2.append(tuple((x + 1, y + 1)))  # Contains min path + startimage + endimage
                    result = list(list2[1:-1])  # Result contains the minimum path required

                print("similarity :" + str(s))

                if not result:  # If no path is found;
                    expected_path[startimage] = list(["NO PATH", [], 0])
                expected_path[startimage] = list([str(grid), result, len(result) + 1])

    print("Dictionary Keys pf expected_path:")
    print(expected_path.keys())

    for obj in list_colored_grids:
        if not (obj in expected_path):  # If no matched object is found;
            expected_path[obj] = list(["NO MATCH", [], 0])

    ##############  Write a statement to print the expected_path ###################

    print("Excepted path: ")
    print(expected_path)

    return full_grids, expected_path


############  Second Part done                            ################

if _name_ == '_main_':
    # change filename to check for other images
    image_filename = "Path_4.jpg"  ### Add the image filename to the image_filename

    main(image_filename)

    cv2.waitKey(10000)
    cv2.destroyAllWindows()
