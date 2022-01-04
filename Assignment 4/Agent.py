class Agent:
	"Agent in the cave"	
	def __init__(self):
		self.direction = "EAST"
		self.coords = [0,0]
		self.hasGold = False
		self.perceivesGlitter = False
		self.hasArrow = True
		self.heardScream = False
		self.isAlive = True
		self.score = 0

	# ADDITION FOR A4
	def initArrays(self):
		self.agentLocationArray = [[0 for x in range(self.width)] for y in range(self.height)]
		self.agentVisitedArray = [[0 for x in range(self.width)] for y in range(self.height)]
		self.agentStenchArray = [[0 for x in range(self.width)] for y in range(self.height)]
		self.agentBreezeArray = [[0 for x in range(self.width)] for y in range(self.height)]
		self.directionEastBool = True
		self.directionWestBool = False
		self.directionNorthBool = False
		self.directionSouthBool = False
		#setting the current location
		self.agentLocationArray[self.coords[0]][self.coords[1]] = 1

	# ADDITION FOR A4
	# For Stench and Breeze array
	def setStenchBreezeArrays(self, grid):
		for index, item in enumerate(grid):
			for index2, item2 in enumerate(item):
				if 's' in item2:
					self.agentStenchArray[index][index2] = 1
				if 'b' in item2:
					self.agentBreezeArray[index][index2] = 1

	# ADDITION FOR A4
	def updateAgentArrays(self, previousCoords):
		self.agentVisitedArray[previousCoords[0]][previousCoords[1]] = 1
		self.agentLocationArray[previousCoords[0]][previousCoords[1]] = 0
		self.agentLocationArray[self.coords[0]][self.coords[1]] = 1

	# ADDITION FOR A4
	def updateAgentDirectionBools(self, east=False, west=False, north=False, south=False):
		self.directionEastBool = east
		self.directionWestBool = west
		self.directionNorthBool = north
		self.directionSouthBool = south

	# ADDITION FOR A4
	#printing all the grids
	def printGrids(self):
		#Location Array
		print('Agent Location Array')
		temp = self.agentLocationArray.copy()
		temp.reverse()
		for index, item in enumerate(temp):
			for index2, item2 in enumerate(item):
				print('[', item2, ']', end='')
			print()
		print()
		#Visited Array
		print('Agent Visited Array')
		temp = self.agentVisitedArray.copy()
		temp.reverse()
		for index, item in enumerate(temp):
			for index2, item2 in enumerate(item):
				print('[', item2, ']', end='')
			print()
		print()
		#Stench Array
		print('Stench Location Array')
		temp = self.agentStenchArray.copy()
		temp.reverse()
		for index, item in enumerate(temp):
			for index2, item2 in enumerate(item):
				print('[', item2, ']', end='')
			print()
		print()
		#Breeze Array
		print('Breeze Location Array')
		temp = self.agentBreezeArray.copy()
		temp.reverse()
		for index, item in enumerate(temp):
			for index2, item2 in enumerate(item):
				print('[', item2, ']', end='')
			print()
		print()
		#Direction Bools
		print('directionEastBool: ', self.directionEastBool)
		print('directionWestBool: ', self.directionWestBool)
		print('directionNorthBool: ', self.directionNorthBool)
		print('directionSouthBool: ', self.directionSouthBool)

	#used by the Environment object to pass on the
	#width and height to be used when moving
	def setWidthHeight(self, width, height):
		self.width = width
		self.height = height
		self.initArrays()
		
	# y = [0]  x = [1]
	# [y][x]
	# [3][0] = 9
	#[1, 0, 0, 0]
	#[0, 2, 0, 0]
	#[0, 0, 3, 0]
	#[9, 0, 0, 4]

	# MODIFIED FOR A4 - last line
	#Forward action function
	def forward(self):
		previousCoords = self.coords
		if (self.direction == "EAST"):
			x = min(self.width - 1, self.coords[1] + 1)
			self.coords = [self.coords[0], x]
		elif (self.direction == "WEST"):
			x = max(0, self.coords[1] - 1)
			self.coords = [self.coords[0], x]
		elif (self.direction == "NORTH"):
			y = min(self.height - 1, self.coords[0] + 1)
			self.coords = [y, self.coords[1]]
		elif (self.direction == "SOUTH"):
			y = max(0, self.coords[0] - 1)
			self.coords = [y, self.coords[1]]
		self.updateAgentArrays(previousCoords)

	# ADDITION FOR A4
	def updatePerceivesGlitter(self, goldLocation):
		if self.hasGold:
			self.perceivesGlitter = False
			return
		if self.coords in goldLocation:
			self.perceivesGlitter = True
		else:
			self.perceivesGlitter = False

	# MODIFIED FOR A4
	#turn left function
	def turnLeft(self):
		if (self.direction == "EAST"):
			self.direction = "NORTH"
			self.updateAgentDirectionBools(north=True)
		elif (self.direction == "NORTH"):
			self.direction = "WEST"
			self.updateAgentDirectionBools(west=True)
		elif (self.direction == "WEST"):
			self.direction = "SOUTH"
			self.updateAgentDirectionBools(south=True)
		elif (self.direction == "SOUTH"):
			self.direction = "EAST"
			self.updateAgentDirectionBools(east=True)
	#turn right function
	def turnRight(self):
		if (self.direction == "EAST"):
			self.direction = "SOUTH"
			self.updateAgentDirectionBools(south=True)
		elif (self.direction == "SOUTH"):
			self.direction = "WEST"
			self.updateAgentDirectionBools(west=True)
		elif (self.direction == "WEST"):
			self.direction = "NORTH"
			self.updateAgentDirectionBools(north=True)
		elif (self.direction == "NORTH"):
			self.direction = "EAST"
			self.updateAgentDirectionBools(east=True)
	

	
