import random
from abc import ABC, abstractmethod

from EnumsAndConsts.ExtraStatusType import *
from EnumsAndConsts.StatusType import *
from EnumsAndConsts.Parameters import PLANTS_INITIATIVE
from Organisms.Organism import Organism
from GUI.Point import Point


# ABSTRACT CLASS FOR PLANTS
class Plant(Organism, ABC):
    def __init__(self, power, symbol, currentStatus, position, world, probabilityOfSpreading, currentExtraStatus):
        super().__init__(power, PLANTS_INITIATIVE, symbol, currentStatus, position, world, currentExtraStatus)
        self.probabilityOfSpreading = probabilityOfSpreading

    # GETTERS
    def getProbabilityOfSpreading(self):
        return self.probabilityOfSpreading

    # SETTERS
    def setProbabilityOfSpreading(self, probabilityOfSpreading):
        self.probabilityOfSpreading = probabilityOfSpreading

    # ACTION ON THE SQUARE GRID -> TRY TO SPREAD
    def squareAction(self):
        if not self.spreading():
            print(self.printLog() + "spreading failed")
        else:
            self.setNewExtraStatus(ExtraStatusType.AFTER_SPREAD)
            print(self.printLog() + "spreading was succesful")

    # THE SAME ACTION AS ON THE SQUARE GRID
    def hexAction(self):
        self.squareAction()

    # PRINT SYMBOL
    @abstractmethod
    def print(self):
        pass

    # PRINT LOG
    @abstractmethod
    def printLog(self):
        pass

    # GENERATE COPY OF PLANT
    @abstractmethod
    def generateCopy(self):
        pass

    def wasEscapeSuccesfull(self):
        return False

    # EVERY PLANT IS IMMUNE TO SOSNOWSKY'S HOGWEED
    def isImmuneToSosnowskysHogweed(self):
        return True

    # SPECIFY COLLISION OF PLANT
    def collision(self, enemy):
        self.setNewStatus(StatusType.TO_BE_KILLED)
        print(f"{self.printLog()} was eaten by: {enemy.printLog()}")
        return self

    # SPREADING FUNCTION
    def spreading(self):
        fortune = random.random()

        if fortune > self.probabilityOfSpreading:
            return False

        newPosition = Point(-1, -1)
        width = self.getWorld().getWidth()
        height = self.getWorld().getHeight()
        newPosition.setX(random.randint(0, width - 1))
        newPosition.setY(random.randint(0, height - 1))

        if self.getWorld().findOrganism(newPosition) is not None:
            return False

        newOrganism = self.generateCopy()
        newOrganism.setPosition(newPosition)
        self.getWorld().addOrganism(newOrganism)
        newOrganism.setNewStatus(StatusType.RECENTLY_SPAWNED)
        return True
