from Organisms.Plants.Plant import Plant
from EnumsAndConsts.Parameters import DANDELION, DANDELION_SPREAD_PROBABILITY
from EnumsAndConsts.ExtraStatusType import ExtraStatusType


class Dandelion(Plant):

    def __init__(self, power, symbol, currentStatus, position, world, probabilityOfSpreading, currentExtraStatus):
        super().__init__(power, symbol, currentStatus, position, world, probabilityOfSpreading, currentExtraStatus)

    # PRINT DANDELION'S LOG
    def printLog(self):
        positionToPrint = self.getPosition()
        return "[Dandelion (" + str(positionToPrint.getX()) + "," + str(positionToPrint.getY()) + ")]"

    # SPECIFY DANDELION'S ACTION
    def squareAction(self):
        counter = 0
        while counter < 3:
            if not self.spreading():
                print(self.printLog() + " spreading failed")
                counter += 1
            else:
                self.setNewExtraStatus(ExtraStatusType.AFTER_SPREAD)
                print(self.printLog() + " spreading was successful")
                counter += 1

    # SAME AS ON SQUARE GRID
    def hexAction(self):
        self.squareAction()

    # PRINT DANDELION'S SYMBOL
    def print(self):
        return DANDELION

    # GENERATE DANDELION'S COPY
    def generateCopy(self):
        return Dandelion(self.getPower(), DANDELION, self.getCurrentStatus(), self.getPosition(), self.getWorld(),
                         DANDELION_SPREAD_PROBABILITY, self.getCurrentExtraStatusType())
