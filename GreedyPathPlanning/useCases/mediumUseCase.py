from enum import Enum
from coordObject import coordObject
from Obstacle import Obstacle


#################################
##########CONTEXT################
#################################
DIM = coordObject(5, 5)
BIGDIM = coordObject(10, 10)
ORIGIN = coordObject(0, 0)
UAVAMOUNT = 3
TIMELENGTH = 60
POIS = [coordObject(0.3, 0.79), coordObject(1, 1)]
POIS_TIMES = [5, 10]
OBSTACLES = [
    Obstacle(coordObject(0.5, 0.3), coordObject(0.6, 0.6), 0),
]


OBS_PUNISH = 0.8

# Time to charge must be aprox 2.5 times the BATTERY_CAPACITY
BATTERY_CAPACITY = 12
TIME_TO_CHARGE = 30

PAUSE_TIME = 0.5


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


colors = ['b', 'g', 'r', 'c', 'm', 'k']
markers = ['o', '^', 'v', '<', '>', 's',
           'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']

metrics = ['Coverage', 'Collision', 'Obstacles', 'POIS', 'Uptime']
