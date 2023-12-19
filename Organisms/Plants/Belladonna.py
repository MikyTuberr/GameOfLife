from Organisms.Plants.Plant import Plant
from EnumsAndConsts.Parameters import BELLADONNA, BELLADONNA_SPREAD_PROBABILITY
from EnumsAndConsts.ExtraStatusType import ExtraStatusType
from EnumsAndConsts.StatusType import StatusType


class Belladonna(Plant):
    def __init__(self, power, symbol, currentStatus, position, world, probabilityOfSpreading, currentExtraStatus):
        super().__init__(power, symbol, currentStatus, position, world, probabilityOfSpreading, currentExtraStatus)

    # PRINT BELLADONNA'S SYMBOL
    def print(self):
        return BELLADONNA

    # PRINT BELLADONNA'S LOG
    def printLog(self):
        positionToPrint = self.getPosition()
        return "[Belladonna (" + str(positionToPrint.getX()) + "," + str(positionToPrint.getY()) + ")]"

    # SPECIFY COLLISION OF BELLADONNA -> ONLY IMMORTAL HUMAN CAN SURVIVE AFTER EATING BELLADONNA
    def collision(self, enemy):
        print(self.printLog() + " was eaten by: " + enemy.printLog())
        if enemy.getCurrentExtraStatusType() != ExtraStatusType.IMMORTAL:
            enemy.setNewStatus(StatusType.TO_BE_KILLED)
            print(enemy.printLog() + " dies, due to eating " + self.printLog())
            return enemy
        else:
            self.setNewStatus(StatusType.TO_BE_KILLED)
            return self

    # GENERATE BELLADONNA'S COPY
    def generateCopy(self):
        return Belladonna(self.getPower(), BELLADONNA, self.getCurrentStatus(), self.getPosition(), self.getWorld(),
                          BELLADONNA_SPREAD_PROBABILITY, self.getCurrentExtraStatusType())
