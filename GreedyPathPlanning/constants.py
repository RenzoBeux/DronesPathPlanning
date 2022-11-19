from enum import Enum
from coordObject import coordObject
from Obstacle import Obstacle


#################################
##########CONTEXT################
#################################
DIM = coordObject(8, 3)
BIGDIM = coordObject(32, 12)
ORIGIN = coordObject(0, 0)
UAVAMOUNT = 6
TIMELENGTH = 100
POIS = [coordObject(0.031, 0.909), coordObject(0.56, 0.09),
        coordObject(0.937, 0.09), coordObject(0.937, 0.909)]
POIS_TIMES = [10, 18, 18, 18]
OBSTACLES = [
    Obstacle(coordObject(0.32, 0.45), coordObject(0.7, 0.54), 0),
    Obstacle(coordObject(0.94, 0.4), coordObject(0.95, 0.5), 1),
]


OBS_PUNISH = 0.8

# Time to charge must be aprox 2.5 times the BATTERY_CAPACITY
BATTERY_CAPACITY = 20
TIME_TO_CHARGE = 50

PAUSE_TIME = 0.05


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
