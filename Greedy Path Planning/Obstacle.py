from coordObject import coordObject


class Obstacle:

    def __init__(self, dimsInit: coordObject, dimsEnd: coordObject, id: int):
        self.dimsInit = dimsInit
        self.dimsEnd = dimsEnd
        self.id = id

    def toSections(self, gridDimensions: coordObject) -> list[coordObject]:
        sections = []
        percentageOfSectionInitX = gridDimensions.x * self.dimsInit.x
        percentageOfSectionEndX = gridDimensions.x * self.dimsEnd.x
        percentageOfSectionInitY = gridDimensions.y * self.dimsInit.y
        percentageOfSectionEndY = gridDimensions.y * self.dimsEnd.y
        sectionInitX = int(percentageOfSectionInitX)
        sectionEndX = int(percentageOfSectionEndX)
        sectionInitY = int(percentageOfSectionInitY)
        sectionEndY = int(percentageOfSectionEndY)
        for i in range(sectionInitX, sectionEndX):
            for j in range(sectionInitY, sectionEndY):
                sections.append(coordObject(i, j))
        return sections
