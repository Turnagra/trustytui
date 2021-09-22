import Servo as servo
import Ultrasonic as ultrasonic

##=====================================================
# INITIALISING THE DIFFERENT STATES

#Creating the states for the veering FSM
class veer_in():
    def __init__(self, FSM):
        self.FSM = FSM

    def execute(self):
        if follow_side == 0:
            servo.right_turn()
        elif follow_side == 1:
            servo.left_turn()

class veer_out():
    def __init__(self, FSM):
        self.FSM = FSM

    def execute(self):
        if follow_side == 0:
            servo.left_turn()
        elif follow_side == 1:
            servo.right_turn()
        
class straight():
    def __init__(self, FSM):
        self.FSM = FSM

    def execute(self):
        servo.straighten()

#Creating the states for the ultrasonic FSM
class forward():
    def __init__(self, FSM):
        self.FSM = FSM
        self.state_name = "Forward"

    def execute(self):
        ultrasonic.drive()

class backward():
    def __init__(self, FSM):
        self.FSM = FSM
        self.state_name = "Backward"

    def execute(self):
        ultrasonic.reverse()

##=====================================================
# SETTING UP A FINITE STATE MACHINE

class FSM(object):
    #Initialises the FSM with the following set of values
    def __init__(self, character):
        self.char = character
        self.states = {}
        self.current_state = None

    def add_state(self, state_name, state):
        self.states[state_name] = state

    def set_state(self, state_name):
        self.current_state = self.states[state_name]

    def execute(self):
        self.current_state.execute()
        
##=====================================================
# IMPLEMENTING THE FSMS

class veering_FSM():
    def __init__(self):
        self.FSM = FSM(self)

        #Initialising states
        self.FSM.add_state("Veer in", veer_in(self.FSM))
        self.FSM.add_state("Veer out", veer_out(self.FSM))
        self.FSM.add_state("Straight", straight(self.FSM))

        #Setting the first state
        self.FSM.set_state("Straight")

    #Defining behaviour for when this FSM is executed
    def execute(self):
        if sensor == [0,1]:
            self.FSM.set_state("Straight")
        elif sensor == [0,0]:
            self.FSM.set_state("Veer in")
        elif sensor == [1,1]:
            self.FSM.set_state("Veer out")

        self.FSM.execute()


class ultrasonic_FSM():
    def __init__(self):
        self.FSM = FSM(self)

        #Initialising states
        self.FSM.add_state("Forward", forward(self.FSM))
        self.FSM.add_state("Backward", backward(self.FSM))

        #Setting the first state
        self.FSM.set_state("Forward")

    #Defining behaviour for when this FSM is executed
    def execute(self):
        if obstacle == 1:
            self.FSM.set_state("Backward")
        elif obstacle == 0:
            self.FSM.set_state("Forward")
            
        self.FSM.execute()

##=====================================================
# THE ACTUAL CODE BIT

print("\nSide inputs:     left = 0    right = 1")
print("Sensor inputs:   black = 0   white = 1\n")

sensor = [0,1,1,0]
intersection = 0

directions_raw = input("Where should the car go?: ")
directions = [int(directions_raw[0]),int(directions_raw[1])]
follow_side = directions[0]

veer = veering_FSM()
ultra = ultrasonic_FSM()

while (sensor[0] != 2):
    raw_sensor = input("What are the sensors sending: ")
    obstacle = int(input("Obstacle?: "))

    if (int(raw_sensor[0]) + int(raw_sensor[1]) + int(raw_sensor[2]) + int(raw_sensor[3])) >= 3:
        print("INTERSECTION")
        intersection += 1
        if intersection == 3:
            follow_side = directions[1]

    if follow_side == 0:
        sensor = [int(raw_sensor[0]), int(raw_sensor[1])]
    elif follow_side == 1:
        sensor = [int(raw_sensor[3]), int(raw_sensor[2])]
    elif follow_side == 2:
        sensor = raw_sensor

    ultra.execute()
    veer.execute()
