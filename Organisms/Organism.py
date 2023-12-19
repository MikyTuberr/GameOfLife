from abc import ABC, abstractmethod


# ABSTRACT CLASS FOR ALL ORGANISMS
class Organism(ABC):

    def __init__(self, power, initiative, symbol, currentStatus, position, world, ExtraStatus):
        self.position = position
        self.power = power
        self.initiative = initiative
        self.symbol = symbol
        self.currentStatus = currentStatus
        self.currentExtraStatusType = ExtraStatus
        self.world = world
        self.age = 0
        self.tourCounter = 0

    # GETTERS
    def getPosition(self):
        return self.position

    def getPower(self):
        return self.power

    def getInitiative(self):
        return self.initiative

    def getSymbol(self):
        return self.symbol

    def getTour(self):
        return self.tourCounter

    def getCurrentStatus(self):
        return self.currentStatus

    def getCurrentExtraStatusType(self):
        return self.currentExtraStatusType

    def getWorld(self):
        return self.world

    def getAge(self):
        return self.age

    # SETTERS
    def setPosition(self, newPosition):
        self.position = newPosition

    def setPower(self, newPower):
        self.power = newPower

    def setInitiative(self, newInitiative):
        self.initiative = newInitiative

    def setAge(self, newAge):
        self.age = newAge

    def setTour(self, newTour):
        self.tourCounter = newTour

    def setSymbol(self, newSymbol):
        self.symbol = newSymbol

    def setWorld(self, newWorld):
        self.world = newWorld

    def setNewStatus(self, newStatusType):
        self.currentStatus = newStatusType

    def setNewExtraStatus(self, newExtraStatus):
        self.currentExtraStatusType = newExtraStatus

    # MAKE ACTION ON SQUARE FIELDS
    @abstractmethod
    def squareAction(self):
        pass

    # MAKE ACTION ON HEX FIELDS
    @abstractmethod
    def hexAction(self):
        pass

    # COLLISION BETWEEN TWO ORGANISMS THAT HAVE MET ON THE SAME FIELD
    @abstractmethod
    def collision(self, enemy):
        pass

    # PRINT SYMBOL OF ORGANISM
    @abstractmethod
    def print(self):
        pass

    # PRINT LOG OF ORGANISM
    @abstractmethod
    def printLog(self):
        pass

    # GENERATE COPY OF ORGANISM
    @abstractmethod
    def generateCopy(self):
        pass

    # CHECK ESCAPE
    @abstractmethod
    def wasEscapeSuccesfull(self):
        pass
    # CHECK IF ORGANISM IS IMMUNE TO SOSNOWSKY HOGWEED
    def isImmuneToSosnowskysHogweed(self):
        return False

    # SAVE ORGANISM PARAMETERS TO STRING
    def saveToString(self):
        string = ""

        string += str(self.getSymbol()) + " "
        string += str(self.getPosition().getX()) + " "
        string += str(self.getPosition().getY()) + " "
        string += str(self.getPower()) + " "
        string += str(self.getCurrentStatus().value) + " "
        string += str(self.getCurrentExtraStatusType().value) + "\n"

        return string
