from Organisms.Animals.Animal import Animal
import random
from EnumsAndConsts.Parameters import CYBER_SHEEP, CYBER_SHEEP_INITIATIVE
from GUI.Point import Point


class Cybersheep(Animal):

    def __init__(self, power, currentStatus, position, world, currentExtraStatus):
        super().__init__(power, CYBER_SHEEP_INITIATIVE, CYBER_SHEEP, currentStatus, position, world,
                         currentExtraStatus)

    # PRINT CYBER_SHEEP SYMBOL
    def print(self):
        return CYBER_SHEEP

    # CYBER SHEEP IS IMMUNE TO SOSNOWSKY'S HOGWEED
    def isImmuneToSosnowskysHogweed(self):
        return True

    # PRINT CYBER SHEEP LOG
    def printLog(self):
        positionToPrint = self.getPosition()
        return "[CyberSheep (" + str(positionToPrint.getX()) + "," + str(positionToPrint.getY()) + ")]"

    # SPECIFY SQUARE ACTION -> FIND CLOSES SOSNOWSKY'S HOGWEED AND FOLLOW IT'S DIRECTION
    def squareAction(self):
        self.checkExtraStatus()
        world = self.getWorld()
        world.setTmpPoint(self.getPosition())
        pX = self.getPosition().getX()
        pY = self.getPosition().getX()
        while True:
            positionOfClosestSosnowskyHogweed = world.findClosestSosnowskyHogweed(self.getPosition())
            if positionOfClosestSosnowskyHogweed.getX() != -1 and positionOfClosestSosnowskyHogweed.getY() != -1:
                x_diff = pX - positionOfClosestSosnowskyHogweed.getX()
                y_diff = pY - positionOfClosestSosnowskyHogweed.getY()
                if x_diff > 0:
                    x = pX - 1
                else:
                    x = pX + 1
                if y_diff > 0:
                    y = pY - 1
                else:
                    y = pY + 1
            else:
                x = pX + random.choice([-1, 0, 1])
                y = pY + random.choice([-1, 0, 1])
            newPosition = Point(x, y)
            if self.isValidMove(newPosition) and pX != x or pY != y:
                break

        newPosition = Point(x, y)
        self.setPosition(newPosition)
        print(str(self.printLog()) + "moved to: " + str(newPosition.getX()) + "," + str(newPosition.getY()))

    # HEX ACTION
    def hexAction(self):
        self.squareAction()

    # GENERATE CYBER SHEEP COPY
    def generateCopy(self):
        return Cybersheep(self.getPower(), self.getCurrentStatus(), self.getPosition(), self.getWorld(),
                          self.getCurrentExtraStatusType())
