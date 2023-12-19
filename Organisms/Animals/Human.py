from Organisms.Animals.Animal import Animal
from EnumsAndConsts.Parameters import HUMAN, HUMAN_INITIATIVE, TIME_OF_SPECIAL_ABILITY
from EnumsAndConsts.KeyAction import KeyAction
from EnumsAndConsts.StatusType import StatusType
from EnumsAndConsts.ExtraStatusType import ExtraStatusType
from GUI.Point import Point
import pygame
from pygame.locals import *
import sys


class Human(Animal):
    def __init__(self, power, currentStatus, position, world, currentExtraStatus):
        super().__init__(power, HUMAN_INITIATIVE, HUMAN, currentStatus, position, world,
                         currentExtraStatus)

    # PRINT HUMAN'S SYMBOL
    def print(self):
        return HUMAN

    # PRINT HUMAN'S LOG
    def printLog(self):
        positionToPrint = self.getPosition()
        return "[Human (" + str(positionToPrint.getX()) + "," + str(positionToPrint.getY()) + ")]"

    # UPDATE POSITION AFTER MOVE
    def setPositionAndStatus(self, position, status):
        self.position = position
        self.setNewStatus(status)

    # UPDATE IMORTALITY CONTROLER
    def updateImmortalityControl(self):
        immortality_controler = self.world.getImmortalityControler()
        if 0 < immortality_controler < TIME_OF_SPECIAL_ABILITY:
            self.world.setImmortalityControler(immortality_controler + 1)
        elif immortality_controler == TIME_OF_SPECIAL_ABILITY:
            self.world.setImmortalityControler(0)
            self.setNewExtraStatus(ExtraStatusType.DEFAULT)

    # PRINT MOVE LOG
    def printMove(self, position_to_print):
        print(
            "[Human (" + str(position_to_print.x) + "," + str(position_to_print.y) + ")]" + " moved to: " + "(" + str(
                self.position.x) + "," + str(self.position.y) + ")")

    def moveDirection(self, position, new_position):
        if self.isValidMove(new_position):
            position = new_position
            self.setPosition(position)
            self.setNewStatus(StatusType.ALREADY_MOVED)
        else:
            print("CANT MOVE OUT OF THE BOARD!")

    def useSpecialAbility(self):
        world = self.getWorld()
        if world.getImmortalityControler() == 0:
            self.setNewExtraStatus(ExtraStatusType.IMMORTAL)
            self.setNewStatus(StatusType.ALREADY_MOVED)
            world.setImmortalityControler(world.getImmortalityControler() + 1)
            print(self.printLog() + " uses special ability (immortality)")
        else:
            print("U NEED TO WAIT " + str(TIME_OF_SPECIAL_ABILITY - world.getImmortalityControler() + 1) +
                  " BEFORE YOU USE SPECIAL ABILITY AGAIN")

    # SPECIFY SQUARE ACTION
    def squareAction(self):
        world = self.getWorld()
        position = self.getPosition()
        world.setTmpPoint(position)

        self.updateImmortalityControl()
        oldPosition = position
        action = None

        while not action:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_UP:
                        action = KeyAction.UP
                    elif event.key == pygame.K_DOWN:
                        action = KeyAction.DOWN
                    elif event.key == pygame.K_RIGHT:
                        action = KeyAction.RIGHT
                    elif event.key == pygame.K_LEFT:
                        action = KeyAction.LEFT
                    elif event.key == pygame.K_p:
                        action = KeyAction.SPECIAL_ABILITY

        if action == KeyAction.UP:
            self.moveDirection(position, Point(position.getX(), position.getY() - 1))
        elif action == KeyAction.DOWN:
            self.moveDirection(position, Point(position.getX(), position.getY() + 1))
        elif action == KeyAction.RIGHT:
            self.moveDirection(position, Point(position.getX() + 1, position.getY()))
        elif action == KeyAction.LEFT:
            self.moveDirection(position, Point(position.getX() - 1, position.getY()))
        elif action == KeyAction.SPECIAL_ABILITY:
            self.useSpecialAbility()
        else:
            print("PRESS RIGHT KEY!")

        world.setPositionOfHuman(self.position)
        print("[Human (" + str(oldPosition.getX()) + "," + str(oldPosition.getY()) + ")]" + " moved to: " + "(" + str(
            self.position.getX()) + "," + str(self.position.getY()) + ")")

    # SPECIFY HEX GRID ACTION
    def hexAction(self):
        pass

    # GENERATE HUMAN'S COPY
    def generateCopy(self):
        return Human(self.getPower(), self.getCurrentStatus(), self.getPosition(), self.getWorld(),
                     self.getCurrentExtraStatusType())
