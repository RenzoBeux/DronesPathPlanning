# this function parses the txt file and returns a list of lists
from collections import Counter
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
    #we mark the initial point of each drone as visited
    for i in range(len(actions)):
        res[currentPos[i].x][currentPos[i].y].append(0)
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

def get_duplicates(array):
    c = Counter(array)
    #return a dictonary
    return {k: v for k, v in c.items() if v > 1}

################################################################################################################################################
########################################################## QUALITY EVALUATOR FUNCTIONS #########################################################
################################################################################################################################################

#This function evaluates the coverage of the area
def evaluateCoverageArea(actions:list[list[ACTION]], areaDims:coordObject) -> float:
    area = populateArea(actions, areaDims)
    numberOfSquares = areaDims.x * areaDims.y
    res = numberOfSquares
    for i in range(areaDims.x):
        for j in range(areaDims.y):
            if len(area[i][j]) == 0:
                res = res - 1
    return res / numberOfSquares *100

#This function will punish if drones share the same square at the same time
def evaluateDronesCollision(actions:list[list[ACTION]], areaDims:coordObject) -> float:
    area = populateArea(actions, areaDims)
    numberOfDrones = len(actions)
    numberOfTimes = len(actions[0])
    worstCase = numberOfDrones * numberOfTimes #all time moves together
    res = 0
    for i in range(areaDims.x):
        for j in range(areaDims.y):
            #find the repeted times in the list
            duplicates = get_duplicates(area[i][j])
            for k in duplicates:
                res = res + duplicates[k]

            
    return 100 - (res / worstCase * 100)


def evaluate(grid:list[list[ACTION]]):
    print(evaluateCoverageArea(grid,coordObject(5, 5)))
    print(evaluateDronesCollision(grid,coordObject(5, 5)))


lista = parseFile('output/90/1.txt')
renderedList = parseMoves(lista)
evaluate(renderedList)