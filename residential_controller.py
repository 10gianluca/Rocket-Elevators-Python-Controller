from webbrowser import get
#Setting the global variables to be used throughout the code
elevatorID = 1
FloorRequestButtonID = 1
callButtonID = 1
class Column:#Create the class that defines the columns that allow the elevator elevators to run
    #give them the properties to be used later such as id numbers so they can be idenitfied also set the amount of floors and amount of elevators and create arrays to be called and pulled from later
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id
        self.status = ''
        self.elevatorList = []
        self.callButtonList = []
        self.createElevator(_amountOfFloors, _amountOfElevators)
        self.createCallButtons(_amountOfFloors)
    #function that creates buttons for every floor that is in the array _amountOfFloors
    def createCallButtons(self, _amountOfFloors):
        buttonFloor = 1
        callButtonID = 1
        for i in range(_amountOfFloors):
                if (buttonFloor < _amountOfFloors): #If it's not the last floor
                    callButton = CallButton(callButtonID, buttonFloor, "Up")#id, floor, direction
                    self.callButtonList.append(callButton)
                    callButtonID+=1
                if (buttonFloor > 1):#If it's not the first floor
                    callButton = CallButton(callButtonID, buttonFloor, "Down")#id, floor, direction
                    self.callButtonList.append(callButton)
                    callButtonID+=1
                buttonFloor+=1
        i+=1
    #create an elevator based on the amount of elevators set, and give them a seperate id and push it to the array elevatorList
    def createElevator(self, _amountOfFloors, _amountOfElevators):
        global elevatorID
        for i in range( _amountOfElevators):
            elevator = Elevator(elevatorID, _amountOfFloors)#id, amountOfFloors
            self.elevatorList.append(elevator)
            elevatorID+=1
            i+=1
    #Simulate when a user press a button outside the elevator
    def requestElevator(self, floor, direction):
        elevator = self.findElevator(floor, direction)
        elevator.floorRequestList.append(floor)
        elevator.move()
        elevator.operateDoors()
        return elevator
    #We use a score system depending on the current elevators state. Since the bestScore and the referenceGap are 
    #higher values than what could be possibly calculated, the first elevator will always become the default bestElevator, 
    #before being compared with to other elevators. If two elevators get the same score, the nearest one is prioritized.
    def findElevator(self, requestedFloor, requestedDirection):
        bestElevator = None
        bestScore = 5
        referenceGap = 10000000 
        for i in range(len(self.elevatorList)):
            elevator = self.elevatorList[i]
            #The elevator is at my floor and going in the direction I want
            if requestedFloor == elevator.currentFloor and elevator.status == "stopped" and requestedDirection == elevator.direction:
                bestElevator, bestScore, referenceGap  = self.checkIfElevatorIsBetter(1, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            #The elevator is lower than me, is coming up and I want to go up
            elif requestedFloor > elevator.currentFloor and elevator.direction == "Up" and requestedDirection == elevator.direction:
                bestElevator, bestScore, referenceGap = self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            #The elevator is higher than me, is coming down and I want to go down
            elif requestedFloor < elevator.currentFloor and elevator.direction == "Down" and requestedDirection == elevator.direction:
                bestElevator, bestScore, referenceGap = self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            #The elevator is idle
            elif elevator.status == "idle":
                bestElevator, bestScore, referenceGap = self.checkIfElevatorIsBetter(3, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            #The elevator is not available, but still could take the call if nothing better is found
            else:
                bestElevator, bestScore, referenceGap = self.checkIfElevatorIsBetter(4, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
        i+=1
        return bestElevator
    #This function compares the current score to the best score and returns the best option   
    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestScore, referenceGap, bestElevator, floor):
        if scoreToCheck < bestScore:
            bestScore = scoreToCheck
            bestElevator = newElevator
            referenceGap = abs((newElevator.currentFloor) - (floor))
        elif bestScore == scoreToCheck:
            gap = abs((newElevator.currentFloor) - (floor))
            if referenceGap > gap:
                bestElevator = newElevator
                referenceGap = gap
        return bestElevator, bestScore, referenceGap
#This is the class that defines teh Elevators and what properties they need
class Elevator:
    #give properties like id, current floor, direction and sets the floor request arrays
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id
        self.status = ''
        self.currentFloor = 1
        self.direction = ''
        self.door = Door(_id)
        self.floorRequestButtonList = []
        self.floorRequestList = []
        self.createFloorRequestButtons(_amountOfFloors)
    #creates floor requst buttons based on the amount of floors and set them with id and floor properties 
    def createFloorRequestButtons(self, _amountOfFloors):
        floorRequestButtonID = 1
        buttonFloor = 1
        for i in range(_amountOfFloors):
            floorRequestButton = FloorRequestButton(floorRequestButtonID, buttonFloor)#id, floor
            self.floorRequestButtonList.append(floorRequestButton)
            buttonFloor+=1
            floorRequestButtonID+=1
        i+=1
    #Simulate when a user press a button inside the elevator
    def requestFloor(self, floor):
        self.floorRequestList.append(floor) 
        self.move()
        self.operateDoors()
    # takes the request from the floor request list and determins which direction to go then once it finishes the request gets rid of the request from the array
    def move(self):
        while len(self.floorRequestList) != 0:
            destination = self.floorRequestList[0]
            self.status = "moving"
            if self.currentFloor < destination:
                self.direction = "Up"
                self.sortFloorList()
                while self.currentFloor < destination:
                    self.currentFloor+=1
            elif self.currentFloor > destination:
                self.direction = "Down"
                self.sortFloorList()
                while self.currentFloor > destination:
                    self.currentFloor-=1
            self.status = "stopped"
            self.floorRequestList.pop()
            self.status = "idle"
    #sorts the floor request list based on the direction of the elevators
    def sortFloorList(self):
        if self.direction == "Up":
            self.floorRequestList.sort()
        else:
            self.floorRequestList.sort(reverse=True)
    #allows the doors to be opened or closed based on obstructions or max capacity
    def operateDoors(self):
        self.door.status = 'opened'
        if self != 'overweight':
            self.door.status = 'closing'
            if self != 'no obstruction':
                self.door.status = 'closed'
            else:
                self.operateDoors()#only operate if not obstructed and not overweight
        else:
            while self =="overweight":
                print("Activate overweight alarm")
            self.operateDoors()
class CallButton:#give the call buttons properties to check later like id, floor, and direction
    def __init__(self, _id, _floor, _direction):
        self.ID = _id
        self.status =''
        self.floor = _floor
        self.direction = _direction
class FloorRequestButton:#gives the floor request button properties to be check later like id, and floor
    def __init__(self, _id, _floor):
        self.ID = _id
        self.status =''
        self.floor = _floor
class Door:#gives the doors properties to be check later like id, and status
    def __init__(self, _id):
        self.ID = _id
        self.status =''
        