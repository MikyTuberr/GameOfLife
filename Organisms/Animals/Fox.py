import random
from EnumsAndConsts.Parameters import FOX_INITIATIVE, FOX
from Organisms.Animals.Animal import Animal
from GUI.Point import Point


class Fox(Animal):
    def __init__(self, power, currentStatus, position, world, currentExtraStatus):
        super().__init__(power, FOX_INITIATIVE, FOX, currentStatus, position, world,
                         currentExtraStatus)

    # PRINT FOXES SYMBOL
    def print(self):
        return FOX

    # PRINT FOXES LOG
    def printLog(self):
        positionToPrint = self.getPosition()
        return "[Fox (" + str(positionToPrint.getX()) + "," + str(positionToPrint.getY()) + ")]"

    # SPECIFY FOXES SQUARE ACTION -> FOX WILL NEVER MOVE TO THE FIELD THAT IS OCCUPIED BY STRONGER ORGANISM
    def squareAction(self):
        self.checkExtraStatus()
        newPosition = Point(-1, -1)
        position = self.getPosition()
        pX = position.getX()
        pY = position.getY()
        while True:
            newPosition.setX(pX + random.choice([-1, 0, 1]))
            newPosition.setY(pY + random.choice([-1, 0, 1]))
            if self.isValidMove(newPosition) and (pX != newPosition.getX() or pY != newPosition.getY()):
                break
        if not self.checkCoordinates(newPosition, self.getWorld()):
            newPosition = self.findFreeCoordinates(self.getPosition())
        if newPosition.getX() != -1 and newPosition.getY() != -1:
            self.setPosition(newPosition)
            print(str(self.printLog()) + "moved to:" + str(newPosition.getX()) + "," + str(newPosition.getY()))
        else:
            print(str(self.printLog()) + "couldn't move, due to lack of space")

    # SPECIFY FOXES HEX ACTION -> THE SAME AS ON THE SQUARE GRID
    def hexAction(self):
        self.squareAction()

    # FIND FREE FIELD IF DRAWN POSITION IS OCCUPIED BY STRONGER ORGANISM
    def findFreeCoordinates(self, position):
        newPosition = position
        world = self.getWorld()
        x = position.getX()
        y = position.getY()
        offsets = [[1, 0], [-1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]
        for offset in offsets:
            x += offset[0]
            y += offset[1]
            if self.isValidMove(Point(x, y)) and self.checkCoordinates(Point(x, y), world):
                newPosition = Point(x, y)
                break
        if newPosition == position:
            newPosition = Point(-1, -1)
        return newPosition

    # CHECK IF FOX CAN MOVE TO DRAWN POSITION
    def checkCoordinates(self, position, world):
        if world.findOrganism(position) is None:
            return True
        elif self.comparePower(world.findOrganism(position)):
            return True
        else:
            return False

    # COMPARE FOXES AND ENEMY'S POWER
    def comparePower(self, organism):
        if organism.getPower() > self.getPower():
            return False
        elif organism.getPower() <= self.getPower():
            return True
        return False

    # GENERATE COPY OF THE FOX
    def generateCopy(self):
        return Fox(self.getPower(), self.getCurrentStatus(), self.getPosition(), self.getWorld(),
                   self.getCurrentExtraStatusType())
