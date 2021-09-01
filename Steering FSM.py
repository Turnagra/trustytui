##=====================================================
# SETTING UP THE TRANSITIONS
#Creates a class of methods to deal with transitioning between states

class transition(object):
    def __init__(self, to_state):
        self.to_state = to_state

    def execute(self):
        print("Transitioning...")

##=====================================================
# INITIALISING THE DIFFERENT STATES

#This code is used to create the veer inwards state
class veer_in():
    def __init__(self, FSM):
        self.FSM = FSM

    def execute(self):
        print("Veering inwards >>>")
        

#This code is used to create the veer outwards state
class veer_out():
    def __init__(self, FSM):
        self.FSM = FSM

    def execute(self):
        print("Veering outwards <<<")
        

#This code is used to create the straight state
class straight():
    def __init__(self, FSM):
        self.FSM = FSM

    def execute(self):
        print("Going straight ^^^")

##=====================================================
# SETTING UP A FINITE STATE MACHINE

class FSM(object):
    #Initialises the FSM with the following set of values
    def __init__(self, character):
        self.char = character
        self.states = {}
        self.transitions = {}
        self.current_state = None
        self.transition = None

    #Creating some useful basic methods for the FSM
    def add_transition(self, transition_name, transition):
        self.transitions[transition_name] = transition

    def add_state(self, state_name, state):
        self.states[state_name] = state

    def set_state(self, state_name):
        self.current_state = self.states[state_name]

    def to_transition(self, to_transition):
        self.transition = self.transitions[to_transition]

    #repeatedly iterating through a state until there is a next state
    def execute(self):
        if (self.transition):
            #Transition to the new state
            self.transition.execute()
            #Change the state on the FSM
            self.set_state(self.transition.to_state)
            #Reseting the next state to a default
            self.transition = None
        self.current_state.execute()
        
##=====================================================
#IMPLEMENTING THE FSM

class trusty_tui():
    def __init__(self):
        self.FSM = FSM(self)

        #Initialising states
        self.FSM.add_state("Veer in", veer_in(self.FSM))
        self.FSM.add_state("Veer out", veer_out(self.FSM))
        self.FSM.add_state("Straight", straight(self.FSM))

        #Initialising transitions
        self.FSM.add_transition("Inwards", transition("Veer in"))
        self.FSM.add_transition("Outwards", transition("Veer out"))
        self.FSM.add_transition("Straighten", transition("Straight"))

        #Setting the first state
        self.FSM.set_state("Straight")

    #Defining behaviour for when this FSM is executed
    def begin(self):
        sensor = external
        
        while (sensor != "2"):
            sensor = input("What are the sensors sending: ")
            
            if sensor == "01" or sensor == "10":
                self.FSM.to_transition("Straighten")
            elif sensor == "00":
                self.FSM.to_transition("Inwards")
            elif sensor == "11":
                self.FSM.to_transition("Outwards")

            self.FSM.execute()

##=====================================================
# THE ACTUAL CODE BIT

external = "00"

veer = trusty_tui()
veer.begin()
