from enum import Enum


# EXTRA STATUS TYPE TO SPECIFY STATUS AFTER COLLISION
class ExtraStatusType(Enum):
    AFTER_BREED = 1
    AFTER_SPREAD = 2
    IMMORTAL = 3
    DEFAULT = 4
