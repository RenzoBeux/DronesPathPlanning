from keras import models, layers, Input
from coordObject import coordObject

noise_dimension = 256

class Generator:
    def __init__(self,time:int,dimension:coordObject,UAVAmount:int):
        self.layers = models.Sequential([
            Input(shape=(noise_dimension)),
            layers.Dense(1),
        ])