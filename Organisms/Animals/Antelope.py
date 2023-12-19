import random
from Organisms.Animals.Animal import Animal
from GUI.Point import Point
from EnumsAndConsts.Parameters import ANTELOPE_INITIATIVE, ANTELOPE


class Antelope(Animal):
    def __init__(self, power, currentStatus, position, world, currentExtraStatus):
        super().__init__(power, ANTELOPE_INITIATIVE, ANTELOPE, currentStatus, position, world,
                         currentExtraStatus)

    # PRINT ANTELOPE'S SYMBOL
    def print(self):
        return ANTELOPE

    # PRINT ANTELOPE'S LOG
    def printLog(self):
        positionToPrint = self.getPosition()
        return "[Antelope (" + str(positionToPrint.getX()) + "," + str(positionToPrint.getY()) + ")]"

    # SPECIFY SQUARE ACTION OF ANTELOPE -> ANTELOPE MOVES TWO FIELDS
    def squareAction(self):
        self.checkExtraStatus()
        self.getWorld().setTmpPoint(self.getPosition())
        pX = self.getPosition().getX()
        pY = self.getPosition().getY()

        while True:
            x = self.getPosition().getX() + 2 * random.choice([-1, 0, 1])
            y = self.getPosition().getY() + 2 * random.choice([-1, 0, 1])
            if self.isValidMove(Point(x, y)) and pX != x or pY != y:
                break

        tmpPosition = Point(x, y)
        self.setPosition(tmpPosition)
        print(str(self.printLog()) + " moved to: " + str(tmpPosition.getX()) + "," + str(tmpPosition.getY()))

    # SPECIFY HEX ACTION -> THE SAME AS SQUARE ACTION
    def hexAction(self):
        self.squareAction()

    # CHECK IF ANTELOPE ESCAPED
    def wasEscapeSuccesfull(self):
        lottery = random.choice([0, 1])
        return lottery == 1

    # GENERATE ANTELOPE'S COPY
    def generateCopy(self):
        return Antelope(self.getPower(), self.getCurrentStatus(), self.getPosition(), self.getWorld(),
                        self.getCurrentExtraStatusType())
