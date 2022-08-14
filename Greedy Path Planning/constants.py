from enum import Enum
from coordObject import coordObject
from Obstacle import Obstacle


#################################
##########CONTEXT################
#################################
DIM = coordObject(6, 6)
BIGDIM = coordObject(18, 18)
ORIGIN = coordObject(0, 0)
UAVAMOUNT = 2
TIMELENGTH = 50
POIS = [coordObject(0.8, 0.8)]
POIS_TIMES = [5]
OBSTACLES = [
    Obstacle(coordObject(0.3, 0.2), coordObject(0.3, 0.2), 0),
    Obstacle(coordObject(0.5, 0.5), coordObject(0.5, 0.5), 1),
    Obstacle(coordObject(0, 0.99), coordObject(0, 0.99), 2),
]
OBS_PUNISH=0.2

ORIGIN = coordObject(0,0)
BATTERY_CAPACITY = 20
TIME_TO_CHARGE = 20

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

colors = ['b', 'g', 'r', 'c', 'm', 'k']
markers = ['o', '^', 'v']

metrics = ['Coverage','Collision','Obstacles','POIS']


class OPERATION(Enum):
    Generate = 0
    Draw = 1
    Resize = 2
