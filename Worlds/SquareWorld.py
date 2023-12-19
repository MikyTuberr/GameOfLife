from Worlds.World import World
from Organisms.Animals.Animal import Animal
from Organisms.Plants.Plant import Plant
from EnumsAndConsts.StatusType import StatusType
from EnumsAndConsts.ExtraStatusType import ExtraStatusType
from EnumsAndConsts.ActionType import ActionType
from GUI.Point import Point


class SquareWorld(World):
    def __init__(self, newWidth, newHeight):
        super().__init__(newWidth, newHeight)

    def makeTour(self):

        self.organisms.sort(key=lambda org: org.age, reverse=True)
        self.organisms.sort(key=lambda org: org.initiative, reverse=True)

        for organism in self.organisms:
            if organism is not None:
                i = 0
                if organism.getCurrentStatus() == StatusType.DEFAULT:
                    organism.squareAction()
                    organism.setAge(organism.getAge() + 1)
                    organism.setNewStatus(StatusType.ALREADY_MOVED)
                    if organism.getCurrentExtraStatusType() == ExtraStatusType.AFTER_SPREAD:
                        continue

                    position = organism.getPosition()
                    organisms_on_position = self.getOrganismsOnPosition(position)

                    action_type = self.collisionType(organisms_on_position)

                    if action_type == ActionType.EAT:
                        while True:
                            organism_tmp = organisms_on_position[i]
                            if isinstance(organism_tmp, Plant):
                                organism = organisms_on_position[i]
                                break
                            i += 1

                        if i > 0:
                            self.toDelete.append(organism.collision(organisms_on_position[i - 1]))
                        else:
                            self.toDelete.append(organism.collision(organisms_on_position[i + 1]))

                    elif action_type == ActionType.FIGHT:
                        while organism.getSymbol() == organisms_on_position[i].getSymbol() and i < len(
                                organisms_on_position):
                            organism = organisms_on_position[i]
                            i += 1

                        self.toDelete.append(organism.collision(organisms_on_position[i]))

                    elif action_type == ActionType.MULTIPLICATION:
                        animal = organism
                        if isinstance(animal, Animal):
                            animal.multiplication(organisms_on_position[0])
                            organisms_on_position[1].setNewExtraStatus(ExtraStatusType.AFTER_BREED)
                            break

                    organisms_on_position.clear()

        for deadOrganism in self.toDelete:
            for instance in self.sosnowskyHogweedInstances:
                if deadOrganism == instance:
                    self.sosnowskyHogweedInstances.remove(instance)
                    self.deleteOrganism(deadOrganism)
                    break
            if deadOrganism is not None:
                self.deleteOrganism(deadOrganism)

        self.toDelete.clear()

        for organism in self.organisms:
            organism.setNewStatus(StatusType.DEFAULT)
            if organism.getCurrentExtraStatusType() == ExtraStatusType.AFTER_SPREAD:
                organism.setNewExtraStatus(ExtraStatusType.DEFAULT)

        self.tour += 1

    def findFreePosition(self, position: Point) -> Point:
        newPosition = position
        offsets = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1), Point(-1, -1), Point(-1, 1), Point(1, -1),
                   Point(1, 1)]
        for offset in offsets:
            candidate = Point(position.getX() + offset.getX(), position.getY() + offset.getY())
            if 0 <= candidate.getX() < self.width and 0 <= candidate.getY() < self.height and \
                    self.findOrganism(candidate) is None:
                newPosition = candidate
                break
        if newPosition.getX() == position.getX() and newPosition.getY() == position.getY():
            newPosition = Point(-1, -1)
        return newPosition

    def findClosestSosnowskyHogweed(self, position: Point):
        closestHogweed = None
        closestDistance = float('inf')

        for organism in self.sosnowskyHogweedInstances:
            hogweedPosition = organism.getPosition()
            distance = abs(position.getX() - hogweedPosition.getX()) + abs(position.getY() - hogweedPosition.getY())

            if distance < closestDistance:
                closestDistance = distance
                closestHogweed = hogweedPosition

        if closestHogweed is not None:
            return closestHogweed

        return Point(-1, -1)

