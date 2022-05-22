from random import randint
from enum import Enum
from moveHeuristic import moveHeuristic, heuristic01

class ACTION(Enum):
	STAY = 0
	RIGHT = 1
	DIAG_DOWN_RIGHT = 2
	DOWN = 3
	DIAG_DOWN_LEFT = 4
	LEFT = 5
	DIAG_UP_LEFT = 6
	UP = 7
	DIAG_UP_RIGHT = 8 



class coordObject:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class POI:
	def __init__(self,coords:coordObject,expectedVisitTime:int):
		# coords is (x,y) pair of numbers in [0..1]
		self.coords = coords
		self.expectedVisitTime = expectedVisitTime
		self.lastVisit = 0

	def getSection(self,dim:coordObject):
		percentageOfSectionX = dim.x / self.coords.y
		percentageOfSectionY = dim.y / self.coords.y
		sectionX = int(self.coords.x / percentageOfSectionX)
		sectionY = int(self.coords.y / percentageOfSectionY)
		result = coordObject(sectionX,sectionY)
		return result

	def markVisited(self,time):
		self.lastVisit = time

class UAV:

	def __init__(self,dims:coordObject,base:coordObject):
		self.dims = dims
		self.position = base
		self.free = True
		self.moves = []
		self.target = 0
		self.moveHeuristic:moveHeuristic = heuristic01


	def possibleMoves(self):
		result = []
		moveRight = self.position.y + 1 <= self.dims.x
		moveDown = self.position.y -1 >= 0
		moveLeft = self.position.x -1 >= 0
		moveUp = self.position.y +1 <= self.dims.y
		result.append(ACTION.STAY)
		if(moveRight):
			result.append(ACTION.RIGHT)
			if(moveDown):
				result.append(ACTION.DIAG_DOWN_RIGHT)
		if(moveDown):
			result.append(ACTION.DOWN)
			if(moveLeft):
				result.append(ACTION.DIAG_DOWN_LEFT)
		if(moveLeft):
			result.append(ACTION.LEFT)
			if(moveUp):
				result.append(ACTION.DIAG_UP_LEFT)
		if(moveUp):
			result.append(ACTION.UP)
			if(moveRight):
				result.append(ACTION.DIAG_UP_RIGHT)
		return result

	def move(self,parameters:list[any]):
		parameters.append(self.position)
		parameters.append(self.possibleMoves())
		self.moveHeuristic.getMove(parameters)

	def shiftPosition(self,chosenMove):
		if chosenMove == ACTION.STAY:
			pass
		elif chosenMove == ACTION.RIGHT:
			self.position.x = self.position.x + 1
		elif chosenMove == ACTION.DIAG_DOWN_RIGHT:
			self.position.x = self.position.x + 1
			self.position.y = self.position.y - 1
		elif chosenMove == ACTION.DOWN:
			self.position.y = self.position.y - 1
		elif chosenMove == ACTION.DIAG_DOWN_LEFT:
			self.position.y = self.position.y - 1
			self.position.x = self.position.x - 1
		elif chosenMove == ACTION.LEFT:
			self.position.x = self.position.x - 1
		elif chosenMove == ACTION.DIAG_UP_LEFT:
			self.position.x = self.position.x - 1
			self.position.y = self.position.y + 1
		elif chosenMove == ACTION.UP:
			self.position.y = self.position.y + 1
		elif chosenMove == ACTION.DIAG_UP_RIGHT:
			self.position.y = self.position.y + 1
			self.position.x = self.position.x + 1
	
	def valuesArray(self):
		values = []
		for i in range(len(self.moves)):
			values.append(self.moves[i].value)
		return values