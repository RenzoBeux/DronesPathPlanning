class coordObject:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def copy(self):
        return coordObject(self.x,self.y)