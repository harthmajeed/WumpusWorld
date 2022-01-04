import networkx as nx
import matplotlib.pyplot as plt

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
		self.score = 0
		self.graph = nx.DiGraph()
		self.pathToExitLength = 0
		self.pathToExit = []
		self.pathToExitCopy = []
		
		
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
	
	
	# ADDITION FOR A2
	#return either of the following actions
	# forward = 1
	# turnLeft = 2
	# turnRight = 3
	def navigateToExit(self):
		# climb, with Gold, on [0,0] = 6
		if (self.coords == [0,0]):
			return 6
			
		x = min(self.width - 1, self.coords[1] + 1)
		eastCoords = (self.coords[0], x)
		
		x = max(0, self.coords[1] - 1)
		westCoords = (self.coords[0], x)
		
		y = min(self.height - 1, self.coords[0] + 1)
		northCoords = (y, self.coords[1])
		
		y = max(0, self.coords[0] - 1)
		southCoords = (y, self.coords[1])
		
		print("Directional Coordinates Adjacent to Agent")
		print("East",eastCoords,"West",westCoords,"North",northCoords,"South",southCoords)
		print()
		
		if (self.direction == "EAST" and eastCoords == self.pathToExit[0]):
			self.pathToExit.pop(0)
			return 1
		elif(self.direction == "WEST" and westCoords == self.pathToExit[0]):
			self.pathToExit.pop(0)
			return 1
		elif(self.direction == "NORTH" and northCoords == self.pathToExit[0]):
			self.pathToExit.pop(0)
			return 1
		elif(self.direction == "SOUTH" and southCoords == self.pathToExit[0]):
			self.pathToExit.pop(0)
			return 1
		else:
			return 2 #turnLeft
		
		
	# ADDITION FOR A2
	def agentGrabbedGold(self):
		self.pathToExitLength, self.pathToExit = nx.single_source_dijkstra(self.graph, (0,0), (self.coords[0],self.coords[1]))
		self.pathToExit.reverse()
		self.pathToExit.pop(0) #need to pop the first one, always
		self.pathToExitCopy = self.pathToExit.copy()
	
	
	# ADDITION FOR A2
	def mapPath(self, current, new):
		if (current == new):
			return
		elif (self.graph.has_edge(current, new)):
			return
		else:
			self.graph.add_edge(current, new)
		
		
	#Forward action function
	def forward(self):
		if (self.direction == "EAST"):
			x = min(self.width - 1, self.coords[1] + 1)
			self.mapPath((self.coords[0],self.coords[1]), (self.coords[0], x))
			self.coords = [self.coords[0], x]
		elif (self.direction == "WEST"):
			x = max(0, self.coords[1] - 1)
			self.mapPath((self.coords[0],self.coords[1]), (self.coords[0], x))
			self.coords = [self.coords[0], x]
		elif (self.direction == "NORTH"):
			y = min(self.height - 1, self.coords[0] + 1)
			self.mapPath((self.coords[0],self.coords[1]), (y, self.coords[1]))
			self.coords = [y, self.coords[1]]
		elif (self.direction == "SOUTH"):
			y = max(0, self.coords[0] - 1)
			self.mapPath((self.coords[0],self.coords[1]), (y, self.coords[1]))
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
	

	
