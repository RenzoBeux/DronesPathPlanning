from random import randint
from classes import coordObject, POI, ACTION


class moveHeuristic:
  def getMove(parameters:list)->ACTION:
  	pass

class heuristic01(moveHeuristic):
	target = 0
	free = True

	def getMove(self,parameters)->ACTION:
		# Parse parameters
		time = parameters[0]
		dim = parameters[1]
		needyPOI:list[POI] = parameters[2]
		position = parameters[3]
		possibleMoves:list[ACTION] = parameters[4]
		# Deal with target accordingly
		if(self.isOnTarget(position,dim)):
			self.removeTarget(time)
		if(self.isFree() and len(needyPOI) > 0):
			self.setTarget(needyPOI.pop())
		# Chose move accordingly
		if self.target != 0:
			movesTowardsTarget:list[ACTION] = self.getMoveTowardsTarget(self.target)
			probMoves = [*possibleMoves,*movesTowardsTarget]
			randomNumber = randint(0,len(probMoves)-1)
			chosenMove = probMoves[randomNumber]
		else:
			randomNumber = randint(0,len(possibleMoves)-1)
			chosenMove = possibleMoves[randomNumber]
		return chosenMove
  
	def setTarget(self,target:POI):
		self.free = False
		self.target = target
	
	def removeTarget(self,time):
		self.target.lastVisit = time
		self.target = 0
		self.free = True

	def isOnTarget(self,position:coordObject,dim:coordObject):
		if self.target == 0:
			return False
		targetCoords = self.target.getSection(dim)
		result:bool = (targetCoords.x == position.x) and (targetCoords.y == position.y)
		return result

	def isFree(self)->bool:
		return self.free

	def getMoveTowardsTarget(self,position:coordObject,dims:coordObject)->list[ACTION]:
		targetCoords = self.target.getSection(dims)
		results:list[ACTION] = []
		if self.position.x < targetCoords.x:
			results.append(ACTION.RIGHT)
			if self.position.y < targetCoords.y:
				results.append(ACTION.DIAG_DOWN_RIGHT)
		if self.position.y > targetCoords.y:
			results.append(ACTION.DOWN)
			if self.position.x > targetCoords.x:
				results.append(ACTION.DIAG_DOWN_LEFT)
		if self.position.x > targetCoords.x:
			results.append(ACTION.LEFT)
			if self.position.y < targetCoords.y:
				results.append(ACTION.DIAG_UP_LEFT)
		if self.position.y < targetCoords.y:
			results.append(ACTION.UP)
			if self.position.x < targetCoords.x:
				results.append(ACTION.DIAG_UP_RIGHT)
		return results