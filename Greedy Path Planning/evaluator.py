# this function parses the txt file and returns a list of lists
from constants import *


def parseFile(fileName):
    file = open(fileName, 'r')
    res = []
    for line in file:
        res.append(list(map(lambda x: int(x), line.split())))
    return res

# given a list of lists of strings, returns a list of ACTIONS
def parseMoves(listOfLists: list[list[str]]) -> list[ACTION]:
    res = []
    for line in listOfLists:
        res.append(list(map(lambda x: ACTION(x), line)))
    return res

#this will return a matrix of lists of ints where each int is the time a drone passed by that square
def populateArea(actions:list[list[ACTION]], areaDims:coordObject) -> list[list[list[int]]]:
    #res will have areadims.x * areadims.y elements
    res: list[list[list[int]]] = []
    #initialize res with 0s
    for i in range(areaDims.x):
        res.append([])
        for j in range(areaDims.y):
            res[i].append([])
    #here we will store current pos for each drone
    currentPos: list[coordObject] = []
    #for each drone we will initialize his current point in 0,0
    for i in range(len(actions)):
        currentPos.append(coordObject(0,0))
    #for each drone
    for i in range(len(actions)):
        # we will iterate through the actions
        for j in range(len(actions[i])):
            chosenMove = actions[i][j]
            if chosenMove == ACTION.RIGHT:
                currentPos[i].x = currentPos[i].x + 1
            elif chosenMove == ACTION.DIAG_DOWN_RIGHT:
                currentPos[i].x = currentPos[i].x + 1
                currentPos[i].y = currentPos[i].y - 1
            elif chosenMove == ACTION.DOWN:
                currentPos[i].y = currentPos[i].y - 1
            elif chosenMove == ACTION.DIAG_DOWN_LEFT:
                currentPos[i].y = currentPos[i].y - 1
                currentPos[i].x = currentPos[i].x - 1
            elif chosenMove == ACTION.LEFT:
                currentPos[i].x = currentPos[i].x - 1
            elif chosenMove == ACTION.DIAG_UP_LEFT:
                currentPos[i].x = currentPos[i].x - 1
                currentPos[i].y = currentPos[i].y + 1
            elif chosenMove == ACTION.UP:
                currentPos[i].y = currentPos[i].y + 1
            elif chosenMove == ACTION.DIAG_UP_RIGHT:
                currentPos[i].y = currentPos[i].y + 1
                currentPos[i].x = currentPos[i].x + 1
            res[currentPos[i].x ][currentPos[i].y ].append(j)
    return res

#This function evaluates the coverage of the area
def evaluateCoverageArea(actions:list[list[ACTION]], areaDims:coordObject) -> float:
    area = populateArea(actions, areaDims)
    res = 100
    for i in range(areaDims.x):
        for j in range(areaDims.y):
            if len(area[i][j]) == 0:
                res = res - 1
    numberOfSquares = areaDims.x * areaDims.y
    return res / numberOfSquares

def evaluate(grid:list[list[ACTION]]):
    print(evaluateCoverageArea(grid,coordObject(5, 5)))


lista = parseFile("output/90/1.txt")
renderedList = parseMoves(lista)
evaluate(renderedList)
