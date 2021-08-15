import cv2 as cv
import csv
import numpy

def displayColor(color):
    int_averages = numpy.array(color, dtype=numpy.uint8)
    average_image = numpy.zeros((100, 100, 3), numpy.uint8)
    average_image[:] = int_averages

    cv.imshow("Image", average_image)
    cv.waitKey(0)

def attainData(fileName):
    global HSV_ranges
    global obstaclePositions

    obstaclePositions = []
    
    file = open(fileName)

    dataline = file.read()
    d = dataline.split(",")

    HSV_ranges = [[int(d[0]), int(d[1])], [int(d[2]), int(d[3])], [int(d[4]), int(d[5])]]

    d = d[6:-1]

    for i in range(int(len(d) / 4)):
        j = 4 * i
        obstacle = [[int(d[j]), int(d[j + 1])], [int(d[j + 2]), int(d[j + 3])]]
        obstaclePositions.append(obstacle)

    file.close()

def obstacleTest():
    global obstaclePositions
    global image
    global HSV_ranges
    global obstacleArray

    number = 0
    obstacleArray = [0,0,0,0]
    
    for obstacle in obstaclePositions:
        obstacle_sample = image[obstacle[1][0]:obstacle[1][1], obstacle[0][0]:obstacle[0][1]]
        avgColor = obstacle_sample.mean(axis=0).mean(axis=0)

        test = [0,0,0]
        
        for i in range(3):
            if HSV_ranges[i][0] <= avgColor[i] <= HSV_ranges[i][1]:
                print("Pass test: ", i)
                test[i] = 1
                print(test)

        if test == [1,1,1]:
            obstacleArray[number] = 1

        number += 1
            
##        cv.imshow("Image", obstacle_sample)
##        cv.waitKey(0)
##
##        displayColor(avgColor)

image = cv.imread("Slide2.JPG")
image = cv.cvtColor(image, cv.COLOR_BGR2HSV)

cv.namedWindow("Image")

attainData("datafile.txt")
obstacleTest()

print(obstaclePositions)
print(obstacleArray)
    
cv.destroyAllWindows()

        

    
