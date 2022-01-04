class Agent:
	"Agent in the cave"	
	def __init__(self,
				hasGold, 
				hasArrow, 
				isAlive):
		self.direction = "EAST"
		self.coords = [0,0]
		self.hasGold = hasGold
		self.hasArrow = hasArrow
		self.isAlive = isAlive
		
	#used by the Environment object to pass on the
	#width and height to be used when moving
	def setWidthHeight(self, width, height):
		self.width = width
		self.height = height
		
	# y = [0]  x = [1]
	# [y][x]
	# [3][0] = 9
	#[1, 0, 0, 0]
	#[0, 2, 0, 0]
	#[0, 0, 3, 0]
	#[9, 0, 0, 4]
		
	#Forward action function
	def forward(self):
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
			
	#turn left function
	def turnLeft(self):
		if (self.direction == "EAST"):
			self.direction = "NORTH"
		elif (self.direction == "NORTH"):
			self.direction = "WEST"
		elif (self.direction == "WEST"):
			self.direction = "SOUTH"
		elif (self.direction == "SOUTH"):
			self.direction = "EAST"
	#turn right function
	def turnRight(self):
		if (self.direction == "EAST"):
			self.direction = "SOUTH"
		elif (self.direction == "SOUTH"):
			self.direction = "WEST"
		elif (self.direction == "WEST"):
			self.direction = "NORTH"
		elif (self.direction == "NORTH"):
			self.direction = "EAST"
	

	
