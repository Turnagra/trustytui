##=====================================================
# INITIALISING THE DIFFERENT STATES

#Creating the states for the veering FSM
class veer_in():
    def __init__(self, FSM):
        self.FSM = FSM

    def execute(self):
        if follow_side == 0:
            print("--> Veering in")
        elif follow_side == 1:
            print("<-- Veering in")

class veer_out():
    def __init__(self, FSM):
        self.FSM = FSM

    def execute(self):
        if follow_side == 0:
            print("<-- Veering out")
        elif follow_side == 1:
            print("--> Veering out")
        
class straight():
    def __init__(self, FSM):
        self.FSM = FSM

    def execute(self):
        print("^^^ Going straight")

#Creating the states for the side selection FSM
class right():
    def __init__(self, FSM):
        self.FSM = FSM
        self.state_name = "Right"

    def execute(self):
        print("Following the right line")

class left():
    def __init__(self, FSM):
        self.FSM = FSM
        self.state_name = "Left"

    def execute(self):
        print("Following the left line")

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

class veering():
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


class side_selection():
    def __init__(self):
        self.FSM = FSM(self)

        #Initialising states
        self.FSM.add_state("Left", left(self.FSM))
        self.FSM.add_state("Right", right(self.FSM))

        #Setting the first state
        self.FSM.set_state("Right")

    #Defining behaviour for when this FSM is executed
    def execute(self):
        if follow_side == 1:
            self.FSM.set_state("Right")
        elif follow_side == 0:
            self.FSM.set_state("Left")
            
        self.FSM.execute()

##=====================================================
# THE ACTUAL CODE BIT

print("\nSide inputs:     left = 0    right = 1")
print("Sensor inputs:   black = 0   white = 1\n")

sensor = [0,1,1,0]

veer = veering()
side = side_selection()

raw_side = input("Which side is being followed: ")
follow_side = int(raw_side[0])

side.execute()

while (sensor[0] != 2):
    raw_sensor = input("What are the sensors sending: ")

    side.FSM.current_state.state_name

    if follow_side == 0:
        sensor = [int(raw_sensor[0]), int(raw_sensor[1])]
    elif follow_side == 1:
        sensor = [int(raw_sensor[3]), int(raw_sensor[2])]
    elif follow_side == 2:
        sensor = raw_sensor

    veer.execute()
