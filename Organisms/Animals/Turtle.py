from Organisms.Animals.Animal import Animal
from EnumsAndConsts.Parameters import TURTLE, TURTLE_INITIATIVE, TURTLE_REFLECTS_BELOW
import random
from GUI.Point import Point


class Turtle(Animal):

    def __init__(self, power, currentStatus, position, world, currentExtraStatus):
        super().__init__(power, TURTLE_INITIATIVE, TURTLE, currentStatus, position, world,
                         currentExtraStatus)

    # PRINT TURTLE'S SYMBOL
    def print(self):
        return TURTLE

    # PRINT TURTLE'S LOG
    def printLog(self):
        positionToPrint = self.getPosition()
        return "[Turtle (" + str(positionToPrint.getX()) + "," + str(positionToPrint.getY()) + ")]"

    # GENERATE TURTLE'S COPY
    def generateCopy(self):
        return Turtle(self.getPower(), self.getCurrentStatus(), self.getPosition(), self.getWorld(),
                      self.getCurrentExtraStatusType())

    # CHECK IF TURTLE REFLECTED THE ATTACK
    def didHeReflectTheAttack(self, enemy):
        if enemy.getPower() < TURTLE_REFLECTS_BELOW:
            return True
        return False

    # SPECIFY TURTLE'S ACTION
    def squareAction(self):
        super().checkExtraStatus()
        lottery = random.randint(0, 3)
        if lottery == 0:
            while True:
                position = self.getPosition()
                x = position.getX() + random.choice([-1, 0, 1])
                y = position.getY() + random.choice([-1, 0, 1])
                if self.isValidMove(position) and position.getX() != x or position.getY() != y:
                    position = Point(x, y)
                    break
            newPosition = Point(x, y)
            self.setPosition(newPosition)
            print(str(self.printLog()) + "moved to: " + str(newPosition.getX()) + "," + str(newPosition.getY()))
        else:
            print(str(self.printLog()) + "decides to take a break")
