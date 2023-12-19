from abc import ABC, abstractmethod
import random
from Organisms.Organism import Organism
from GUI.Point import Point
from EnumsAndConsts.ExtraStatusType import *
from EnumsAndConsts.StatusType import *
from EnumsAndConsts.Parameters import MULTIPLICATION_DELAY


# ANIMALS ABSTRACT CLASS
class Animal(Organism, ABC):
    def __init__(self, power, initiative, symbol, currentStatus, position, world, currentExtraStatus):
        super().__init__(power, initiative, symbol, currentStatus, position, world, currentExtraStatus)

    # CHECK IF MOVE IS VALID
    def isValidMove(self, position):
        return 0 <= position.getX() < self.getWorld().getWidth() and \
            0 <= position.getY() < self.getWorld().getHeight()

    # CHECK RULES OF MULTIPLICATION
    def checkExtraStatus(self):
        if 1 <= self.getTour() < MULTIPLICATION_DELAY:
            self.setTour(self.getTour() + 1)
        elif self.getTour() == MULTIPLICATION_DELAY:
            self.setNewExtraStatus(ExtraStatusType.DEFAULT)
            self.setTour(0)
        elif self.getCurrentExtraStatusType() == ExtraStatusType.AFTER_BREED:
            self.setTour(1)

    # ANIMAL ACTION ON SQUARE GRID
    def squareAction(self):
        self.checkExtraStatus()
        self.getWorld().setTmpPoint(self.getPosition())
        pX = self.getPosition().getX()
        pY = self.getPosition().getY()

        while True:
            x = self.getPosition().getX() + random.choice([-1, 0, 1])
            y = self.getPosition().getY() + random.choice([-1, 0, 1])
            if self.isValidMove(Point(x, y)) and pX != x or pY != y:
                break

        tmpPosition = Point(x, y)
        self.setPosition(tmpPosition)
        print(self.printLog() + " moved to: (" + str(tmpPosition.getX()) + "," + str(tmpPosition.getY()) + ")")

    # ANIMAL ACTION ON HEX GRID
    def hexAction(self):
        self.squareAction()

    # COMPARE ANIMALS STRENGTH
    def compareStrength(self, enemy):
        if self.getPower() > enemy.getPower():
            enemy.setNewStatus(StatusType.TO_BE_KILLED)
            print(self.printLog() + " killed: " + enemy.printLog())
            return enemy

        elif self.getPower() < enemy.getPower():
            self.setNewStatus(StatusType.TO_BE_KILLED)
            print(enemy.printLog() + " killed: " + self.printLog())
            return self

    # SPECIFY COLLISION OF ANIMALS
    def collision(self, enemy):
        if self.getCurrentExtraStatusType() != ExtraStatusType.IMMORTAL and \
                enemy.getCurrentExtraStatusType() != ExtraStatusType.IMMORTAL:

            if enemy.wasEscapeSuccesfull:
                tmpWorld = self.getWorld()
                newPosition = tmpWorld.findFreePosition(enemy.getPosition())
                print(enemy.printLog() + " has escaped attack from: " + self.printLog())
                enemy.setPosition(newPosition)
                print(
                    enemy.printLog() + " due to escape, has moved to: (" + str(newPosition.getX()) + "," +
                    str(newPosition.getY()) + ")")

            elif not enemy.didHeReflectTheAttack(self):
                return self.compareStrength(enemy)
            else:
                tmpWorld = self.getWorld()
                position = tmpWorld.getTmpPoint()
                print(enemy.printLog() + " has reflected the attack from " + self.printLog())
                self.setPosition(position)
                print(
                    self.printLog() + " due to reflection, goes back to: (" + str(position.getX()) + ","
                    + str(position.getY()) + ")")
                return None
        else:
            if self.getCurrentExtraStatusType() == ExtraStatusType.IMMORTAL and self.getPower() < enemy.getPower():
                world = self.getWorld()
                position = world.getTmpPoint()
                print(self.printLog() + " survived fight (because of immortality) against: " + enemy.printLog())
                self.setPosition(position)
                print(
                    self.printLog() + " due to losing fight, goes back to: (" + str(position.getX()) + ","
                    + str(position.getY()) + ")")
                return None

            elif enemy.getCurrentExtraStatusType() == ExtraStatusType.IMMORTAL and self.getPower() > enemy.getPower():
                world = self.getWorld()
                position = world.getTmpPoint()
                print(enemy.printLog() + " survived fight (because of immortality) against: " + self.printLog())
                self.setPosition(position)
                print(
                    self.printLog() + " due to immortality of human,needs to go back to: (" + str(position.getX())
                    + "," + str(position.getY()) + ")")
                return None

            else:
                return self.compareStrength(enemy)

        return None

    # CHECK IF ATTACK WAS REFLECTED
    def didHeReflectTheAttack(self, enemy):
        return False

    # CHECK IF ANIMAL ESCAPED
    def wasEscapeSuccesfull(self):
        return False

    # PRINT SYMBOL
    @abstractmethod
    def print(self):
        pass

    # PRINT LOG
    @abstractmethod
    def printLog(self):
        pass

    # NORMALLY ANIMALS AREN'T IMMUNE TO SOSNOWSKY'S HOGWEED
    def isImmuneToSosnowskysHogweed(self):
        return False

    # SPECIFY MULTIPLICATION
    def multiplication(self, partner):
        partner.setNewExtraStatus(ExtraStatusType.AFTER_BREED)
        world = partner.getWorld()
        newOrganism = partner.generateCopy()
        newPosition = world.findFreePosition(partner.getPosition())
        newOrganism.setPosition(newPosition)

        if newPosition.getX() != -1 and newPosition.getY() != -1:
            world.addOrganism(newOrganism)
            newOrganism.setNewStatus(StatusType.RECENTLY_SPAWNED)
            positionOfMultiplication = partner.getPosition()
            print(
                newOrganism.printLog() + " recently spawned, due to multiplication, on position: (" +
                str(positionOfMultiplication.getX()) + "," + str(positionOfMultiplication.getY()) + ")")
        else:
            print(self.printLog() + " and " + partner.printLog() + "couldn't multiplicate, due to lack of "
                                                                   "space, for child")
