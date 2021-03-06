from enum import Enum
from coordObject import coordObject
from Obstacle import Obstacle


#################################
##########CONTEXT################
#################################
DIM = coordObject(6, 6)
BIGDIM = coordObject(18,18)
UAVAMOUNT = 2
TIMELENGTH = 100
OBSTACLES = [
    Obstacle(coordObject(0.3, 0.2), coordObject(0.3,0.2 ), 0),
    Obstacle(coordObject(0.5, 0.5), coordObject(0.5, 0.5), 1),
    Obstacle(coordObject(0, 0.99), coordObject(0, 0.99), 2),
]

PAUSE_TIME = 0.2

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

class OPERATION(Enum):
    Generate = 0
    Draw = 1
    Resize = 2
