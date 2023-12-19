from Organisms.Plants.Plant import Plant
from EnumsAndConsts.Parameters import GRASS, GRASS_SPREAD_PROBABILITY


class Grass(Plant):

    def __init__(self, power, symbol, currentStatus, position, world, probabilityOfSpreading, currentExtraStatus):
        super().__init__(power, symbol, currentStatus, position, world, probabilityOfSpreading, currentExtraStatus)

    # PRINT GRASS LOG
    def printLog(self):
        positionToPrint = self.getPosition()
        return "[Grass (" + str(positionToPrint.getX()) + "," + str(positionToPrint.getY()) + ")]"

    # PRINT GRASS SYMBOL
    def print(self):
        return GRASS

    # GENERATE GRASS COPY
    def generateCopy(self):
        return Grass(self.getPower(), GRASS, self.getCurrentStatus(), self.getPosition(), self.getWorld(),
                     GRASS_SPREAD_PROBABILITY, self.getCurrentExtraStatusType())
