from Organisms.Animals.Animal import Animal
from EnumsAndConsts.Parameters import SHEEP_INITIATIVE, SHEEP


class Sheep(Animal):
    def __init__(self, power, currentStatus, position, world, currentExtraStatus):
        super().__init__(power, SHEEP_INITIATIVE, SHEEP, currentStatus, position, world,
                         currentExtraStatus)

    # PRINT SHEEP'S SYMBOL
    def print(self):
        return SHEEP

    # PRINT SHEEP'S LOG
    def printLog(self):
        positionToPrint = self.getPosition()
        return "[Sheep (" + str(positionToPrint.getX()) + "," + str(positionToPrint.getY()) + ")]"

    # GENERATE SHEEP'S COPY
    def generateCopy(self):
        return Sheep(self.getPower(), self.getCurrentStatus(), self.getPosition(), self.getWorld(),
                     self.getCurrentExtraStatusType())
