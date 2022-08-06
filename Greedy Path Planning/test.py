from POI import POI
from routeDrawer import drawRouteAlt, readFileAction
from coordObject import coordObject
from constants import BIGDIM, DIM, POIS, ORIGIN, OBSTACLES
from evaluator import evaluateDronesCollision


originalDims = BIGDIM
targetDims = DIM

routes = readFileAction('./output/75/1.txt')
pois:list[POI] = list(map(lambda coords: POI(coords,0,0),POIS))
# print(evaluateDronesCollision(routes,DIM))


# drawRouteAlt(DIM,pois,ORIGIN,OBSTACLES, routes)


