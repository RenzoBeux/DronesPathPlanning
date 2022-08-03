from dimConverter import converter
from routeDrawer import drawRoute, readFileAction
from coordObject import coordObject

originalDims = coordObject(8,8)
targetDims = coordObject(4,4)

routes = readFileAction('1.txt')

drawRoute(originalDims,[],coordObject(0,0),routes)

newRoutes = map(lambda route:converter(originalDims,targetDims,route),routes)

drawRoute(targetDims,[],coordObject(0,0),newRoutes)
