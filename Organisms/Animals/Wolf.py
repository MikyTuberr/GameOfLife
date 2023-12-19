from Organisms.Animals.Animal import Animal
from EnumsAndConsts.Parameters import WOLF, WOLF_INITIATIVE


class Wolf(Animal):
    def __init__(self, power, currentStatus, position, world, currentExtraStatus):
        super().__init__(power, WOLF_INITIATIVE, WOLF, currentStatus, position, world,
                         currentExtraStatus)

    # PRINT WOLF'S SYMBOL
    def print(self):
        return WOLF

    # PRINT WOLF'S LOG
    def printLog(self):
        positionToPrint = self.getPosition()
        return "[Wolf (" + str(positionToPrint.getX()) + "," + str(positionToPrint.getY()) + ")]"

    # GENERATE WOLF'S COPY
    def generateCopy(self):
        return Wolf(self.getPower(), self.getCurrentStatus(), self.getPosition(), self.getWorld(),
                    self.getCurrentExtraStatusType())
