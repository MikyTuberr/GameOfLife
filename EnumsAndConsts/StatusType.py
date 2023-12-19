from enum import Enum


# STATUS TYPE TO SPECIFY STATUS AFTER COLLISION
class StatusType(Enum):
    TO_BE_KILLED = 1
    ALREADY_MOVED = 2
    RECENTLY_SPAWNED = 3
    DEFAULT = 4
