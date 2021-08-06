import cv2 as cv
import numpy

def showImage(image):
    cv.imshow("Image", image)
    cv.waitKey(0)

def momentImage(image_in, image_overlay):
    m = cv.moments(image_in)

    cx = int(m["m10"] / m["m00"])
    cy = int(m["m01"] / m["m00"])

    cv.circle(image_overlay, (cx, cy), 5, (255, 0, 255), -1)

    centroidPosition = [cx, cy]
    return centroidPosition

def hsvFilter(val):
    global image_mask
    
    hueCentre = cv.getTrackbarPos("Hue Centre", "HSV")
    hueAccuracy = cv.getTrackbarPos("Hue Accuracy", "HSV")

    hueMin = int(hueCentre - hueAccuracy)
    hueMax = int(hueCentre + hueAccuracy)

    satCentre = cv.getTrackbarPos("Sat Centre", "HSV")
    satAccuracy = cv.getTrackbarPos("Sat Accuracy", "HSV")

    satMin = int(satCentre - satAccuracy)
    satMax = int(satCentre + satAccuracy)

    valCentre = cv.getTrackbarPos("Val Centre", "HSV")
    valAccuracy = cv.getTrackbarPos("Val Accuracy", "HSV")

    valMin = int(valCentre - valAccuracy)
    valMax = int(valCentre + valAccuracy) 

    image_mask = cv.inRange(image_hsv, (hueMin, satMin, valMin), (hueMax, satMax, valMax))
    cv.imshow("Image", image_mask)

def makeSliders(slider_window):
    cv.namedWindow(slider_window)

    cv.createTrackbar("Hue Centre", slider_window, 20, 180, hsvFilter)
    cv.createTrackbar("Hue Accuracy", slider_window, 10, 90, hsvFilter)

    cv.createTrackbar("Sat Centre", slider_window, 128, 255, hsvFilter)
    cv.createTrackbar("Sat Accuracy", slider_window, 128, 128, hsvFilter)

    cv.createTrackbar("Val Centre", slider_window, 128, 255, hsvFilter)
    cv.createTrackbar("Val Accuracy", slider_window, 128, 128, hsvFilter)

    cv.waitKey(0)
    cv.destroyWindow(slider_window)

def getContours(mask):
    global contours
    
    contours, heirarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(image, contours, -1, (0, 255, 0), 3)

    showImage(image)

def identifyContours(size, contour):
    global moment_list
    moment_list = []
    
    for c in contour:
        contourArea = cv.contourArea(c)
        if contourArea > size:
            moment_list.append(momentImage(c, image))
            
    showImage(image)

def definePositions(val):
    global moment_tolerance_list
    global moment_list
    moment_tolerance_list = []

    tolerance = cv.getTrackbarPos("Tolerance", "Tolerance")

    for position in moment_list:
        obstacle = []
    
        for coordinate in position:
            coordinateMin = coordinate - tolerance
            coordinateMax = coordinate + tolerance

            obstacle.append([coordinateMin, coordinateMax])

        moment_tolerance_list.append(obstacle)

    showTolerance(1)

def showTolerance(val):
    global moment_tolerance_list

    image_drawn = image[:]
    
    for obstacle in moment_tolerance_list:
        cv.rectangle(image_drawn, (obstacle[0][0], obstacle[1][0]), (obstacle[0][1], obstacle[1][1]), (255, 0, 255), 5)

    cv.imshow("Image", image_drawn)

image = cv.imread("5.jpg")
image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

showImage(image)
showImage(image_hsv)

makeSliders("HSV")

getContours(image_mask)
identifyContours(2000, contours)

cv.namedWindow("Tolerance")
cv.createTrackbar("Tolerance", "Tolerance", 50, 100, definePositions)
cv.waitKey(0)

cv.destroyAllWindows()

