from keras import models, layers, Input
from coordObject import coordObject

class discriminator():
    def __init__(self,time:int,dimension:coordObject,UAVAmount:int):
        self.layers = models.Sequential([
            Input(shape=(UAVAmount,time)),
            layers.Dense(1),
        ])