from enum import Enum
from coordObject import coordObject

DIM = coordObject(5,5)
UAVAMOUNT = 2
TIMELENGTH = 10

class ACTION(Enum):
    STAY = 0
    RIGHT = 1
    DIAG_DOWN_RIGHT = 2
    DOWN = 3
    DIAG_DOWN_LEFT = 4
    LEFT = 5
    DIAG_UP_LEFT = 6
    UP = 7
    DIAG_UP_RIGHT = 8 


P_SUCC = 0.8
P_FAIL = 0.2 