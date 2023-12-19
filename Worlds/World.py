from abc import ABC, abstractmethod
import random
from GUI.Point import Point
from EnumsAndConsts.StatusType import StatusType
from EnumsAndConsts.Parameters import *
from EnumsAndConsts.ExtraStatusType import ExtraStatusType
from EnumsAndConsts.ActionType import ActionType

from Organisms.Animals.Fox import Fox
from Organisms.Animals.Wolf import Wolf
from Organisms.Animals.CyberSheep import Cybersheep
from Organisms.Animals.Sheep import Sheep
from Organisms.Animals.Turtle import Turtle
from Organisms.Animals.Antelope import Antelope
from Organisms.Animals.Human import Human

from Organisms.Plants.Grass import Grass
from Organisms.Plants.Guarana import Guarana
from Organisms.Plants.Belladonna import Belladonna
from Organisms.Plants.Dandelion import Dandelion
from Organisms.Plants.SosnowskysHogweed import SosnowskysHogweed


class World(ABC):
    def __init__(self, newWidth, newHeight):
        self.immortalityControler = 0
        self.organisms = []
        self.toDelete = []
        self.sosnowskyHogweedInstances = []
        self.width = newWidth
        self.positionOfHuman = None
        self.height = newHeight
        self.tour = 0
        self.tmpPoint = Point(-1, -1)
        self.initializeStartupOrganisms()

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getTmpPoint(self):
        return self.tmpPoint

    def getImmortalityControler(self):
        return self.immortalityControler

    def setWidth(self, newWidth):
        self.width = newWidth

    def setHeight(self, newHeight):
        self.height = newHeight

    def setTmpPoint(self, newTmpPoint):
        self.tmpPoint = newTmpPoint

    def setImmortalityControler(self, newControler):
        self.immortalityControler = newControler

    @abstractmethod
    def makeTour(self):
        pass

    def addOrganism(self, newOrganism):
        if newOrganism is not None:
            self.organisms.append(newOrganism)

    def setToDelete(self, organismToBeDeleted):
        if organismToBeDeleted is not None:
            self.toDelete.append(organismToBeDeleted)

    def addSosnowskyHogweed(self, newSosnowskyHogweed):
        if newSosnowskyHogweed is not None:
            self.sosnowskyHogweedInstances.append(newSosnowskyHogweed)

    def deleteOrganism(self, organismToBeDeleted):
        if organismToBeDeleted in self.organisms:
            self.organisms.remove(organismToBeDeleted)

    def findOrganism(self, position):
        for organism in self.organisms:
            if organism.getPosition().getX() == position.getX() and organism.getPosition().getY() == position.getY():
                return organism
        return None

    @abstractmethod
    def findFreePosition(self, position):
        pass

    def getOrganismsOnPosition(self, position):
        organismsOnPosition = []
        for organism in self.organisms:
            if organism.getPosition().getX() == position.getX() and organism.getPosition().getY() == position.getY():
                organismsOnPosition.append(organism)
        return organismsOnPosition

    def collisionType(self, organismsOnPosition):
        symbol = organismsOnPosition[0].getSymbol()
        counter = 0
        Acounter = 0
        Pcounter = 0

        for organism in organismsOnPosition:
            if organism.getCurrentStatus() != StatusType.TO_BE_KILLED:
                tmp_symbol = symbol
                symbol = organism.getSymbol()

                if (tmp_symbol == symbol) and ((symbol == WOLF) or (symbol == SHEEP) or (symbol == FOX) or
                                               (symbol == TURTLE) or (symbol == ANTELOPE) or (symbol == CYBER_SHEEP)):
                    counter += 1
                    Acounter += 1
                    if organism.getCurrentExtraStatusType() != ExtraStatusType.AFTER_BREED:
                        if counter == 2:
                            return ActionType.MULTIPLICATION
                elif (symbol == WOLF) or (symbol == SHEEP) or (symbol == FOX) or (symbol == TURTLE) or \
                        (symbol == ANTELOPE) or (symbol == CYBER_SHEEP) or (symbol == HUMAN):
                    counter += 1
                    Acounter += 1
                    if counter == 2:
                        return ActionType.FIGHT

                if ((symbol == GRASS) or (symbol == DANDELION) or (symbol == GUARANA) or (symbol == BELLADONNA) or
                    (symbol == SOSNOWSKYS_HOGWEED)):
                    Pcounter += 1

        if Pcounter > 0 and Acounter > 0:
            return ActionType.EAT
        return ActionType.NONE

    @abstractmethod
    def findClosestSosnowskyHogweed(self, position):
        pass

    def createOrganism(self, lottery, position):
        organism = None
        if lottery == 0:
            organism = Wolf(WOLF_POWER, StatusType.DEFAULT, position, self, ExtraStatusType.DEFAULT)
        elif lottery == 1:
            organism = Sheep(SHEEP_POWER, StatusType.DEFAULT, position, self, ExtraStatusType.DEFAULT)
        elif lottery == 2:
            organism = Fox(FOX_POWER, StatusType.DEFAULT, position, self, ExtraStatusType.DEFAULT)
        elif lottery == 3:
            organism = Turtle(TURTLE_POWER, StatusType.DEFAULT, position, self, ExtraStatusType.DEFAULT)
        elif lottery == 4:
            organism = Antelope(ANTELOPE_POWER, StatusType.DEFAULT, position, self, ExtraStatusType.DEFAULT)
        elif lottery == 5:
            organism = Cybersheep(CYBER_SHEEP_POWER, StatusType.DEFAULT, position, self, ExtraStatusType.DEFAULT)
        elif lottery == 6:
            organism = Grass(GRASS_POWER, GRASS, StatusType.DEFAULT, position, self, GRASS_SPREAD_PROBABILITY,
                             ExtraStatusType.DEFAULT)
        elif lottery == 7:
            organism = Dandelion(DANDELION_POWER, DANDELION, StatusType.DEFAULT, position, self,
                                 DANDELION_SPREAD_PROBABILITY, ExtraStatusType.DEFAULT)
        elif lottery == 8:
            organism = Guarana(GUARANA_POWER, GUARANA, StatusType.DEFAULT, position, self,
                               GUARANA_SPREAD_PROBABILITY, ExtraStatusType.DEFAULT)
        elif lottery == 9:
            organism = Belladonna(BELLADONNA_POWER, BELLADONNA, StatusType.DEFAULT, position, self,
                                  BELLADONNA_SPREAD_PROBABILITY, ExtraStatusType.DEFAULT)
        elif lottery == 10:
            organism = SosnowskysHogweed(SOSNOWSKYS_HOGWEED_POWER, SOSNOWSKYS_HOGWEED, StatusType.DEFAULT,
                                         position, self, SOSNOWSKYS_HOGWEED_SPREAD_PROBABILITY,
                                         ExtraStatusType.DEFAULT)
        return organism

    def initializeStartupOrganisms(self):
        numberOfPositions = self.width * self.height
        numberOfOrganismsToInitialize = numberOfPositions * POPULATION_PERCENTAGE
        counter = 0
        while counter < int(numberOfOrganismsToInitialize):
            drawnPosition = self.drawPosition()
            lottery = random.randint(0, NUMBER_OF_IMPLEMENTED_ORGANISMS - 1)
            organism = self.createOrganism(lottery, drawnPosition)
            if organism:
                self.addOrganism(organism)
                if isinstance(organism, SosnowskysHogweed):
                    self.addSosnowskyHogweed(organism)
                counter += 1

        drawnPosition = self.drawPosition()
        organism = Human(HUMAN_POWER, StatusType.DEFAULT, drawnPosition, self, ExtraStatusType.DEFAULT)
        self.positionOfHuman = drawnPosition
        self.addOrganism(organism)

    def drawPosition(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.findOrganism(Point(x, y)) is None:
                return Point(x, y)

    def saveTheGame(self, path):
        try:
            with open(path, "w") as file:
                file.write(f"{self.width} {self.height} {self.tour} {self.immortalityControler}\n")
                for organism in self.organisms:
                    file.write(organism.saveToString())
            return True
        except IOError:
            return False

    def loadTheGame(self, path):
        try:
            with open(path, 'r') as reader:
                line = reader.readline()
                data = line.split(" ")
                self.width = int(data[0])
                self.height = int(data[1])
                self.tour = int(data[2])
                self.immortalityControler = int(data[3])
                self.organisms.clear()
                self.toDelete.clear()
                self.sosnowskyHogweedInstances.clear()

                for line in reader:
                    data = line.split(" ")
                    symbol = data[0][0]
                    x = int(data[1])
                    y = int(data[2])
                    power = int(data[3])
                    status = int(data[4])
                    extraStatus = int(data[5])

                    statusType = StatusType(status)
                    extraStatusType = ExtraStatusType(extraStatus)

                    if symbol == WOLF:
                        organism = Wolf(power, statusType, Point(x, y), self, extraStatusType)
                    elif symbol == SHEEP:
                        organism = Sheep(power, statusType, Point(x, y), self, extraStatusType)
                    elif symbol == FOX:
                        organism = Fox(power, statusType, Point(x, y), self, extraStatusType)
                    elif symbol == TURTLE:
                        organism = Turtle(power, statusType, Point(x, y), self, extraStatusType)
                    elif symbol == ANTELOPE:
                        organism = Antelope(power, statusType, Point(x, y), self, extraStatusType)
                    elif symbol == CYBER_SHEEP:
                        organism = Cybersheep(power, statusType, Point(x, y), self, extraStatusType)
                    elif symbol == GRASS:
                        organism = Grass(power, GRASS, statusType, Point(x, y), self, GRASS_SPREAD_PROBABILITY,
                                         extraStatusType)
                    elif symbol == DANDELION:
                        organism = Dandelion(power, DANDELION, statusType, Point(x, y), self,
                                             DANDELION_SPREAD_PROBABILITY, extraStatusType)
                    elif symbol == GUARANA:
                        organism = Guarana(power, GUARANA, statusType, Point(x, y), self,
                                           GUARANA_SPREAD_PROBABILITY, extraStatusType)
                    elif symbol == BELLADONNA:
                        organism = Belladonna(power, BELLADONNA, statusType, Point(x, y), self,
                                              BELLADONNA_SPREAD_PROBABILITY, extraStatusType)
                    elif symbol == SOSNOWSKYS_HOGWEED:
                        organism = SosnowskysHogweed(power, SOSNOWSKYS_HOGWEED, statusType, Point(x, y), self,
                                                     SOSNOWSKYS_HOGWEED_SPREAD_PROBABILITY, extraStatusType)
                    elif symbol == HUMAN:
                        organism = Human(power, statusType, Point(x, y), self, extraStatusType)
                    else:
                        return False

                    self.organisms.append(organism)
        except IOError:
            return False

        return True

    def getStatusTypeFromInt(self, value):
        if value == 0:
            return StatusType.TO_BE_KILLED
        elif value == 1:
            return StatusType.ALREADY_MOVED
        elif value == 2:
            return StatusType.RECENTLY_SPAWNED
        elif value == 3:
            return StatusType.DEFAULT

    def getExtraStatusTypeFromInt(self, value):
        if value == 0:
            return ExtraStatusType.AFTER_BREED
        elif value == 1:
            return ExtraStatusType.AFTER_SPREAD
        elif value == 2:
            return ExtraStatusType.IMMORTAL
        elif value == 3:
            return ExtraStatusType.DEFAULT

    def getPositionOfHuman(self):
        return self.positionOfHuman

    def setPositionOfHuman(self, newPositionOfHuman):
        self.positionOfHuman = newPositionOfHuman
