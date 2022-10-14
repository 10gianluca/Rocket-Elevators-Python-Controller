from webbrowser import get
elevatorID = 1
FloorRequestButtonID = 1
callButtonID = 1
class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id
        self.status = ''
        self.elevatorList = []
        self.callButtonList = []
    
        self.createElevator(_amountOfFloors, _amountOfElevators)
        self.createCallButtons(_amountOfFloors)
    def createCallButtons(self, _amountOfFloors):
        buttonFloor = 1
        callButtonID = 1
        for i in range(_amountOfFloors):
                if (buttonFloor < _amountOfFloors):
                    callButton = CallButton(callButtonID, buttonFloor, "Up")
                    self.callButtonList.append(callButton)
                    callButtonID+=1
                if (buttonFloor > 1):
                    callButton = CallButton(callButtonID, buttonFloor, "Down")
                    self.callButtonList.append(callButton)
                    callButtonID+=1
                buttonFloor+=1
        i+=1
    def createElevator(self, _amountOfFloors, _amountOfElevators):
        global elevatorID
        for i in range( _amountOfElevators):
            elevator = Elevator(elevatorID, _amountOfFloors)
            self.elevatorList.append(elevator)
            elevatorID+=1
            i+=1
    def requestElevator(self, floor, direction):
        elevator = self.findElevator(floor, direction)
        elevator.floorRequestList.append(floor)
        elevator.move()
        elevator.operateDoors()
        return elevator
    def findElevator(self, requestedFloor, requestedDirection):
        bestElevator = None
        bestScore = 5
        referenceGap = 10000000 
        for i in range(len(self.elevatorList)):
            elevator = self.elevatorList[i]
            if requestedFloor == elevator.currentFloor and elevator.status == "stopped" and requestedDirection == elevator.direction:
                bestElevator, bestScore, referenceGap  = self.checkIfElevatorIsBetter(1, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            elif requestedFloor > elevator.currentFloor and elevator.direction == "Up" and requestedDirection == elevator.direction:
                bestElevator, bestScore, referenceGap = self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            elif requestedFloor < elevator.currentFloor and elevator.direction == "Down" and requestedDirection == elevator.direction:
                bestElevator, bestScore, referenceGap = self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            elif elevator.status == "idle":
                bestElevator, bestScore, referenceGap = self.checkIfElevatorIsBetter(3, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            else:
                bestElevator, bestScore, referenceGap = self.checkIfElevatorIsBetter(4, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
        i+=1
        return bestElevator
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
class Elevator:
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id
        self.status = ''
        self.currentFloor = 1
        self.direction = ''
        self.door = Door(_id)
        self.floorRequestButtonList = []
        self.floorRequestList = []
        self.createFloorRequestButtons(_amountOfFloors)
    def createFloorRequestButtons(self, _amountOfFloors):
        floorRequestButtonID = 1
        buttonFloor = 1
        for i in range(_amountOfFloors):
            floorRequestButton = FloorRequestButton(floorRequestButtonID, buttonFloor)
            self.floorRequestButtonList.append(floorRequestButton)
            buttonFloor+=1
            floorRequestButtonID+=1
        i+=1
    def requestFloor(self, floor):
        self.floorRequestList.append(floor) 
        self.move()
        self.operateDoors()
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
    def sortFloorList(self):
        if self.direction == "Up":
            self.floorRequestList.sort()
        else:
            self.floorRequestList.sort(reverse=True)
    def operateDoors(self):
        self.door.status = 'opened'
        if self != 'overweight':
            self.door.status = 'closing'
            if self != 'no obstruction':
                self.door.status = 'closed'
            else:
                self.operateDoors()
        else:
            while self =="overweight":
                print("Activate overweight alarm")
            self.operateDoors()
class CallButton:
    def __init__(self, _id, _floor, _direction):
        self.ID = _id
        self.status =''
        self.floor = _floor
        self.direction = _direction

class FloorRequestButton:
    def __init__(self, _id, _floor):
        self.ID = _id
        self.status =''
        self.floor = _floor

class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status =''
        