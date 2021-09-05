#Ultrasonic Sensor and Line follower Code
#TrustyTui - Assessment Code
#2021-08-16
import RPi.GPIO as GPIO
import time
 
#Remove warnings from the sensors
GPIO.setwarnings(False)

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#Line Followers Setup
GPIO.setup(22,GPIO.IN) #GPIO 23 -> Far Right IR out
GPIO.setup(23,GPIO.IN) #GPIO 23 -> Mid Right IR out
GPIO.setup(24,GPIO.IN) #GPIO 24 -> Mid Left IR out
GPIO.setup(25,GPIO.IN) #GPIO 24 -> Far Left IR out
 
#Ultrasonic Sensor Setup
GPIO_TRIGGER = 18
GPIO_ECHO = 17
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#Set a Maximum wait time (seconds) for Ultrasonic Sensor
maxTime = 0.04

#Calculate the distance from Ultrasonic Sensor
def distance():
    #Ensure the trigger is LOW before sending a pulse
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.01)

    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    #Prevent getting stuck in while loops with a timeout option
    StartTime = time.time()
    timeout = StartTime + maxTime 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0 and StartTime < timeout:
        StartTime = time.time()
 
    StopTime = time.time()
    timeout = StopTime + maxTime 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1 and StopTime < timeout:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because signal goes there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

#This method prints the values of the sensors, and the decision of direction
def printtoterminal():
    print('Left: ' + str(GPIO.input(24)) + ' Right: ' + str(GPIO.input(23)) + ' Direction: ' + direct + "    Barrier = %.1f cm     " % dist, end='\r')
  
#Decision Logic
def direction(dist):
    global direct
    if(dist < 0.1):
        direct = 'Crash!!!   '
    elif (GPIO.input(24)==1 and GPIO.input(23)==1):
        direct = 'Go Straight'
    elif (GPIO.input(24)==0 and GPIO.input(23)==1):
        direct = 'Turn Right '
    elif (GPIO.input(24)==1 and GPIO.input(23)==0):
        direct = 'Turn Left  '
    elif (GPIO.input(24)==0 and GPIO.input(23)==0):
        direct = 'Stop       '

#Actual Program
try:
    while True:
        dist = distance()
        direction(dist)
        printtoterminal()
        time.sleep(0.5)

    # Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
