from coordObject import coordObject


class POI:
    def __init__(self, coords: coordObject, expectedVisitTime: int, id: int):
        # coords is (x,y) pair of numbers in [0..1]
        self.coords = coords
        if (self.coords.x == 1):
            self.coords.x = 0.99
        if (self.coords.y == 1):
            self.coords.y = 0.99
        self.expectedVisitTime = expectedVisitTime
        self.lastVisit = 0
        self.id = id

    def getSection(self, dim: coordObject) -> coordObject:
        percentageOfSectionX = dim.x * self.coords.x
        percentageOfSectionY = dim.y * self.coords.y
        sectionX = int(percentageOfSectionX)
        sectionY = int(percentageOfSectionY)
        result = coordObject(sectionX, sectionY)
        return result

    def markVisited(self, time):
        self.lastVisit = time
