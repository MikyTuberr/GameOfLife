from Organisms.Plants.Plant import Plant
from EnumsAndConsts.Parameters import SOSNOWSKYS_HOGWEED, SOSNOWSKYS_HOGWEED_SPREAD_PROBABILITY
from EnumsAndConsts.ExtraStatusType import ExtraStatusType
from GUI.Point import Point
from EnumsAndConsts.StatusType import StatusType


class SosnowskysHogweed(Plant):
    def __init__(self, power, symbol, currentStatus, position, world, probabilityOfSpreading, currentExtraStatus):
        super().__init__(power, symbol, currentStatus, position, world, probabilityOfSpreading, currentExtraStatus)

    # PRINT SOSNOWSKY'S HOGWEED LOG
    def printLog(self):
        positionToPrint = self.getPosition()
        return "[SosnowskysHogweed (" + str(positionToPrint.getX()) + "," + str(positionToPrint.getY()) + ")]"

    # PRINT SOSNOWSKY'S HOGWEED SYMBOL
    def print(self):
        return SOSNOWSKYS_HOGWEED

    # SPECIFY SOSNOWSKY'S HOGWEED ACTION -> KILL ALL ANIMALS THAT ARE NEXT TO SOSNOWSKY'S HOGWEED,
    # ONLY CYBER SHEEP AND IMMORTAL HUMAN CAN SURVIVE
    def squareAction(self):
        self.findOrganismsAroundCoordinates(self.getPosition())
        if not self.spreading():
            print(self.printLog() + " spreading failed")
        else:
            self.setNewExtraStatus(ExtraStatusType.AFTER_SPREAD)
            print(self.printLog() + " spreading was successful")

    # THE SAME AS SQUARE
    def hexAction(self):
        self.squareAction()

    # FIND ALL NEIGHBOURS
    def findOrganismsAroundCoordinates(self, position):
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for offset in offsets:
            x = position.x + offset[0]
            y = position.y + offset[1]

            if 0 <= x < self.getWorld().getWidth() and 0 <= y < self.getWorld().getHeight() and \
                    self.getWorld().findOrganism(Point(x, y)) is not None:
                self.killOrganismInTheNeighbourhood(self.getWorld().findOrganism(Point(x, y)))

    # KILL ALL NEIGHBOURS
    def killOrganismInTheNeighbourhood(self, organism):
        if not organism.isImmuneToSosnowskysHogweed() and organism.getCurrentExtraStatusType() \
                != ExtraStatusType.IMMORTAL:
            world = self.getWorld()
            organism.setNewStatus(StatusType.TO_BE_KILLED)
            world.setToDelete(organism)
            print(organism.printLog() + " dies, due to being near " + self.printLog())

    # GENERATE SOSNOWSKY'S HOGWEED COPY
    def generateCopy(self):
        return SosnowskysHogweed(self.getPower(), SOSNOWSKYS_HOGWEED, self.getCurrentStatus(), self.getPosition(),
                                 self.getWorld(),
                                 SOSNOWSKYS_HOGWEED_SPREAD_PROBABILITY, self.getCurrentExtraStatusType())
