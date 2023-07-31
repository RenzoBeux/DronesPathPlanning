import argparse
import traceback

parser = argparse.ArgumentParser()

from collections import Counter
from classes import coordObject, POI, ACTION
from constants import constants
from enum import Enum


def parseFile(fileName) -> list[list[int]]:
    file = open(fileName, "r")
    res = []
    for line in file:
        res.append(list(map(lambda x: int(x), line.split())))
    return res


def parseMoves(listOfLists: list[list[int]]) -> list[list[ACTION]]:
    res = []
    for line in listOfLists:
        res.append(list(map(lambda x: ACTION(x), line)))
    return res


def populateArea(
    actions: list[list[ACTION]], areaDims: coordObject
) -> tuple[list[list[list[int]]], float, float, float]:
    res: list[list[list[int]]] = []
    currentPos: list[coordObject] = []
    oob_pen: list[float] = []
    total_time = len(actions[0])
    time_oob = 0
    num_uavs = len(actions)
    ooBattery = [1.0 for _ in range(num_uavs)]
    # UAVs start with constants.BATTERY_CAPACITY battery
    uav_battery = [float(constants.BATTERY_CAPACITY) for _ in range(num_uavs)]
    # This builds the 2d array representing the area
    for i in range(int(areaDims.x)):
        res.append([])
        for j in range(int(areaDims.y)):
            res[i].append([])
    # Initializes all drones in currentPos, oob_pen and res
    # currentPos is a list of coordObjects, each one representing the current position of a drone
    # oob_pen is a list of floats, each one representing the penalty of a drone
    # res is a 2d array of lists of ints, each one representing the time in which a drone is in that position
    for i in range(num_uavs):
        currentPos.append(coordObject(0, 0))
        oob_pen.append(0)
        res[int(currentPos[i].x)][int(currentPos[i].y)].append(0)
    for uav in range(num_uavs):
        for time in range(len(actions[uav])):
            oob_penalize = 0
            chosenMove = actions[uav][time]
            if chosenMove == ACTION.RIGHT:
                currentPos[uav].x = currentPos[uav].x + 1
            elif chosenMove == ACTION.DIAG_DOWN_RIGHT:
                currentPos[uav].x = currentPos[uav].x + 1
                currentPos[uav].y = currentPos[uav].y - 1
            elif chosenMove == ACTION.DOWN:
                currentPos[uav].y = currentPos[uav].y - 1
            elif chosenMove == ACTION.DIAG_DOWN_LEFT:
                currentPos[uav].y = currentPos[uav].y - 1
                currentPos[uav].x = currentPos[uav].x - 1
            elif chosenMove == ACTION.LEFT:
                currentPos[uav].x = currentPos[uav].x - 1
            elif chosenMove == ACTION.DIAG_UP_LEFT:
                currentPos[uav].x = currentPos[uav].x - 1
                currentPos[uav].y = currentPos[uav].y + 1
            elif chosenMove == ACTION.UP:
                currentPos[uav].y = currentPos[uav].y + 1
            elif chosenMove == ACTION.DIAG_UP_RIGHT:
                currentPos[uav].y = currentPos[uav].y + 1
                currentPos[uav].x = currentPos[uav].x + 1
            # If it is in the origin and the action is STAY, it charges the battery
            # We have to take into account that the battery charges from 0 to constants.BATTERY_CAPACITY in constants.TIME_TO_CHARGE
            if (
                currentPos[uav].x == constants.ORIGIN.x
                and currentPos[uav].y == constants.ORIGIN.y
                and chosenMove == ACTION.STAY
                and uav_battery[uav] < constants.BATTERY_CAPACITY
            ):
                uav_battery[uav] += (
                    constants.BATTERY_CAPACITY / constants.TIME_TO_CHARGE
                )
            # If it is not in the origin it uses battery
            elif (
                currentPos[uav].x != constants.ORIGIN.x
                or currentPos[uav].y != constants.ORIGIN.y
            ):
                uav_battery[uav] -= 1
            # If the battery is 0 or less, it is out of battery
            # we need to penalize it, we want to make it 0 if the battery became more negative than -constants.BATTERY_CAPACITY/3
            ooBatteryPenalization = 3 / constants.BATTERY_CAPACITY
            if uav_battery[uav] <= 0:
                if ooBattery[uav] > 0:
                    ooBattery[uav] -= ooBatteryPenalization
                    if ooBattery[uav] < 0:
                        ooBattery[uav] = 0
            how_far_x = min(currentPos[uav].x, areaDims.x - currentPos[uav].x - 1)
            how_far_y = min(currentPos[uav].y, areaDims.y - currentPos[uav].y - 1)
            if how_far_x < 0 or how_far_y < 0:
                time_oob += 1
                oob_penalize += min(how_far_x, 0)
                oob_penalize += min(how_far_y, 0)
                oob_pen[uav] += oob_penalize
            else:
                # in the 2d array (aka the area) we append the time in which the drone is in that position
                res[int(currentPos[uav].x)][int(currentPos[uav].y)].append(time)
    max_pen = 0
    for pen in oob_pen:
        if pen < max_pen:
            max_pen = pen
    max_pen = -max_pen / ((total_time + 1) * total_time)
    return (
        res,
        1 - max_pen,
        1 - time_oob / (num_uavs * total_time),
        sum(ooBattery) / (num_uavs),
    )


def get_duplicates(array):
    c = Counter(array)
    return {k: v for k, v in c.items() if v > 1}


################################################################################################################################################
########################################################## QUALITY EVALUATOR FUNCTIONS #########################################################
################################################################################################################################################


def evaluateCoverageArea(
    area: list[list[list[int]]], _, areaDims: coordObject
) -> float:
    numberOfSquares = areaDims.x * areaDims.y
    res = numberOfSquares
    for i in range(int(areaDims.x)):
        for j in range(int(areaDims.y)):
            if len(area[i][j]) == 0:
                res = res - 1
    return res / numberOfSquares


def evaluateDronesCollision(
    area: list[list[list[int]]], actions: list[list[ACTION]], areaDims: coordObject
) -> float:
    numberOfDrones = len(actions)
    numberOfTimes = len(actions[0])
    worstCase = numberOfDrones * numberOfTimes
    res = 0
    for i in range(int(areaDims.x)):
        for j in range(int(areaDims.y)):
            if i == constants.ORIGIN.x and j == constants.ORIGIN.y:
                continue
            duplicates = get_duplicates(area[i][j])
            for k in duplicates:
                res = res + duplicates[k]
    return 1 - (res / worstCase)


def evaluateObstacles(
    area: list[list[list[int]]], actions: list[list[ACTION]], _
) -> float:
    numberOfDrones = len(actions)
    numberOfTimes = len(actions[0])
    worstCase = numberOfDrones * numberOfTimes
    flat_obs = constants.FLAT_OBSTACLES
    timeOnObs = 0
    for obs in flat_obs:
        x = obs.x
        y = obs.y
        timeOnObs += len(area[x][y])  # type: ignore
    return 1 - timeOnObs / worstCase


def evaluatePOICoverage(
    area: list[list[list[int]]], actions: list[list[ACTION]], areaDims: coordObject
) -> float:
    timeSpentNeedy = [0 for _ in constants.POIS]
    lastVisit = [0 for _ in constants.POIS]
    time = len(actions[0])
    pois = [POI(coords, 0, 0) for coords in constants.POIS]
    for t in range(time):
        for i, poi in enumerate(pois):
            coords = poi.getSection(areaDims)
            x = coords.x
            y = coords.y
            if t in area[x][y]:  # type: ignore
                lastVisit[i] = t
            elif t - lastVisit[i] > constants.POIS_TIMES[i]:
                timeSpentNeedy[i] += 1
    totalTimeSpentNeedy = 0
    for needy in timeSpentNeedy:
        totalTimeSpentNeedy += needy
    maxNeedyTimes = [time - poiTime for poiTime in constants.POIS_TIMES]
    maximumNeediness = 0
    for needy in maxNeedyTimes:
        maximumNeediness += needy
    return 1 - totalTimeSpentNeedy / maximumNeediness


def evaluateDroneUpTime(
    area: list[list[list[int]]], actions: list[list[ACTION]], areaDims: coordObject
) -> float:
    time = len(actions[0])
    dronesUp = 0
    breaked = False
    for t in range(time):
        for i in range(int(areaDims.x)):
            if breaked:
                breaked = False
                break
            for j in range(int(areaDims.y)):
                if i == constants.ORIGIN.x and j == constants.ORIGIN.y:
                    continue
                if t in area[i][j]:
                    dronesUp += 1
                    breaked = True
                    break
    return dronesUp / time


class EvaluatorModules(Enum):
    COVERAGE = "Coverage"
    COLLISION = "Collision"
    OBSTACLES = "Obstacles"
    POIS = "POIS"
    UPTIME = "Uptime"
    OUTOFBOUND = "OutOfBound"
    BATTERY = "Battery"


def evaluate(
    grid: list[list[ACTION]], activeModules: list[EvaluatorModules] | None = None
):
    gridDimensions = constants.DIM
    area, oob_dist, oob_time, batteryEvaluation = populateArea(grid, gridDimensions)
    if activeModules is None:
        evaluators = {
            "Coverage": evaluateCoverageArea,
            "Collision": evaluateDronesCollision,
            "Obstacles": evaluateObstacles,
            "POIS": evaluatePOICoverage,
            "Uptime": evaluateDroneUpTime,
            "OutOfBound": lambda _, __, ___: ((oob_dist + oob_time) / 2) ** 2,
        }
    else:
        evaluators = {}
        if EvaluatorModules.COVERAGE in activeModules:
            evaluators["Coverage"] = evaluateCoverageArea
        if EvaluatorModules.COLLISION in activeModules:
            evaluators["Collision"] = evaluateDronesCollision
        if EvaluatorModules.OBSTACLES in activeModules:
            evaluators["Obstacles"] = evaluateObstacles
        if EvaluatorModules.POIS in activeModules:
            evaluators["POIS"] = evaluatePOICoverage
        if EvaluatorModules.UPTIME in activeModules:
            evaluators["Uptime"] = evaluateDroneUpTime
        if EvaluatorModules.OUTOFBOUND in activeModules:
            evaluators["OutOfBound"] = (
                lambda _, __, ___: ((oob_dist + oob_time) / 2) ** 2
            )
        if EvaluatorModules.BATTERY in activeModules:
            evaluators["Battery"] = lambda _, __, ___: batteryEvaluation
    evaluateMetric = lambda eval: eval(area, grid, gridDimensions)
    results = {metric: evaluateMetric(eval) for metric, eval in evaluators.items()}
    accumulator = 0
    for v in results.values():
        accumulator += v
    return accumulator / len(results)


def evaluateGAN(
    generatedList: list[list[int]], activeModules: list[EvaluatorModules] | None = None
):
    """
    activeModules: List of the modules to be used in the evaluation, if None all will be used
    Returns:
        Dict[str, float]: Dictionary with the results of the evaluation
        None: If the generated list is invalid
    """
    parsedList = parseMoves(generatedList)
    return evaluate(parsedList, activeModules)


def evaluate_file(file: str, activeModules: list[EvaluatorModules] | None = None):
    with open(file, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [line.split(" ") for line in lines]
    lines = [[int(x) for x in line] for line in lines]
    return evaluateGAN(lines, activeModules)


if __name__ == "__main__":
    try:
        parser.add_argument(
            "-f", "--file", help="File to interpret", dest="file", type=str
        )
        args = parser.parse_args()

        print(evaluate_file(args.file, [EvaluatorModules.BATTERY]))
    except:
        traceback.print_exc()
