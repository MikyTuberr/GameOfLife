from Organisms.Plants.Plant import Plant
from EnumsAndConsts.Parameters import GUARANA, GUARANA_SPREAD_PROBABILITY, GUARANA_POWER_UP
from EnumsAndConsts.StatusType import StatusType


class Guarana(Plant):
    def __init__(self, power, symbol, currentStatus, position, world, probabilityOfSpreading, currentExtraStatus):
        super().__init__(power, symbol, currentStatus, position, world, probabilityOfSpreading, currentExtraStatus)

    # SPECIFY GUARANA'S COLLISION -> INCREASE BY GUARANA_POWER_UP ENEMY'S STRENGTH
    def collision(self, enemy):
        self.setNewStatus(StatusType.TO_BE_KILLED)
        print(self.printLog() + " was eaten by: " + enemy.printLog())
        enemy.setPower(enemy.getPower() + GUARANA_POWER_UP)
        print(enemy.printLog() + " has + " + str(GUARANA_POWER_UP) + " to power stat, due to eating ")
        return self

    # PRINT GUARANA'S LOG
    def printLog(self):
        positionToPrint = self.getPosition()
        return "[Guarana (" + str(positionToPrint.getX()) + "," + str(positionToPrint.getY()) + ")]"

    # PRINT GUARANA'S SYMBOL
    def print(self):
        return GUARANA

    # GENERATE GUARANA'S COPY
    def generateCopy(self):
        return Guarana(self.getPower(), GUARANA, self.getCurrentStatus(), self.getPosition(), self.getWorld(),
                       GUARANA_SPREAD_PROBABILITY, self.getCurrentExtraStatusType())
