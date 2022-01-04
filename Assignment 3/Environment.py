import random
import matplotlib.pyplot as plt

class Environment:
	"The environment grid"
	gameWon = False
	stenchCount = 0
	breezeCount = 0
	pitLocations = []
	gameTerminated = False
	wumpusLocation = []
	wumpusAlive = True
	goldLocation = []
	actionCount = 0
	allowClimbWithoutGold = False
	
	def __init__(self, 
				width, 
				height, 
				pitProb,
				agent,
				printGrid=False):
		self.width = width
		self.height = height
		self.pitProb = pitProb
		self.agent = agent
		self.printGrid = printGrid
		self.initalizeAndGenerate()

		
		
	#used to create the 2D loop, set the wumpusLocation and goldLocation
	#and setting the pits with specified random value (0.20)
	#pass on the width and height to the agent
	def initalizeAndGenerate(self):
		#initializing grid
		self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
		
		#setting wumpus and gold locations
		self.my_custom_random(self.wumpusLocation, self.width, self.height)
		self.my_custom_random(self.goldLocation, self.width, self.height)
		
		#Setting probability
		for index, item in enumerate(self.grid):
			for index2, item2 in enumerate(item):
				#creating the nodes for the graph
				self.agent.graph.add_node((index,index2))
				prob = random.random()
				#print("prob: ", prob, " [", index, ",", index2, "]")
				if ((prob <= self.pitProb) and (index != 0 and index2 != 0)):
					self.pitLocations.append([index,index2])
		
		#sending information required for the agent
		self.agent.setWidthHeight(self.width, self.height)

		# ADDITION FOR A3
		#calling updateGrid and then calling agent perceive
		self.updateGrid()
		self.agent.perceive(self.grid[self.agent.coords[0]][self.agent.coords[1]])

		# ADDITION FOR A3
		for index, item in enumerate(self.grid):
			for index2, item2 in enumerate(item):
				if 's' in item2:
					self.stenchCount += 1
				if 'b' in item2:
					self.breezeCount += 1
		
		
	#needed to create a custom random function to exclude [0,0]
	#and exclude from an array value, appends the value to the
	#passed array as well
	def my_custom_random(self, excludeArray, width, height):
		x_rand = random.randint(0,width-1)
		y_rand = random.randint(0,height-1)
		#print(excludeArray) #delete
		#print("{", x_rand, ",", y_rand, "}")
		if (x_rand == 0 and y_rand == 0):
			return self.my_custom_random(excludeArray, width, height)
		elif ([x_rand,y_rand] in excludeArray):
			return self.my_custom_random(excludeArray, width, height)
		else:
			excludeArray.append([x_rand,y_rand])
			
			
	#update the grid, setting the pits, gold, wumpus locations on the grid
	#also updates the breeze and stench locations
	#this function is called everytime Vizualize is called, perhaps not
	#the most efficient way to use this function, but at the moment it works
	def updateGrid(self):
		for index, item in enumerate(self.grid):
			for index2, item2 in enumerate(item):
				text = ""
				if ([index, index2] in self.pitLocations):
					text = text + "P"
				if ([index, index2] in self.wumpusLocation):
					if (self.wumpusAlive):
						text = text + "W"
					else:
						text = text + "w"
				if ([index, index2] in self.goldLocation):
					text = text + "G"
					#text = text + "g" #glitter
				if ([index, index2] == self.agent.coords):
					text = text + "A"
				#print("text: ", text, " index: [", index, ",", index2, "]")
				self.grid[index][index2] = text
				if(([min(self.height-1,index + 1), index2] in self.pitLocations) or
					([max(0,index - 1), index2] in self.pitLocations) or
					([index, min(self.width-1, index2 + 1)] in self.pitLocations) or
					([index, max(0,index2 - 1)] in self.pitLocations)):
						if ("P" not in self.grid[index][index2]):
							self.grid[index][index2] = self.grid[index][index2] + "b"
				if(([min(self.height-1,index + 1), index2] in self.wumpusLocation) or
					([max(0,index - 1), index2] in self.wumpusLocation) or
					([index, min(self.width-1, index2 + 1)] in self.wumpusLocation) or
					([index, max(0,index2 - 1)] in self.wumpusLocation)):
						if (("W" not in self.grid[index][index2]) or ("w" not in self.grid[index][index2])):
							self.grid[index][index2] = self.grid[index][index2] + "s"
				
				
	#vizualize, prints out the grid, also calls the updateGrid() function everytime
	#also prints out the general information for each value state
	#also prints out game loop, its nice to look at
	def visualize(self):
		self.updateGrid()
		temp = self.grid.copy()
		temp.reverse()

		for index, item in enumerate(temp):
			print()
			for index2, item2 in enumerate(item):
				print("[",item2,"]", end="")
		print()
		print("Agent Location: ", self.agent.coords, " Direction: ", self.agent.direction)
		print("Agent has Gold: ", self.agent.hasGold)
		print("Agent hasArrow: ", self.agent.hasArrow)
		print("Agent isAlive: ", self.agent.isAlive)
		print("Wumpus Location: ", self.wumpusLocation)
		print("wumpusAlive: ", self.wumpusAlive)
		print("Gold Location: ", self.goldLocation)
		print("Pit Locations: ", self.pitLocations)
		print("Pit Prob: ", self.pitProb)
		print("AllowClimbWithoutGold: ", self.allowClimbWithoutGold)
		print("gameTerminated: ", self.gameTerminated)
		print("Agent Score: ", self.agent.score)
		print("Action Count (Game loop): ", self.actionCount)
		# ADDITION FOR A2
		print("Graph Info: ", self.agent.graph, self.agent.graph.edges())
		print("Path To Exit Map: {", self.agent.pathToExitLength, "edges }", self.agent.pathToExitCopy)
		print("Current Path To Exit: ", self.agent.pathToExit)
		# ADDITION FOR A3
		print("Stench History: ", self.agent.historyOfStench)
		print("Breeze History: ", self.agent.historyOfBreeze)
		print()
		print("-------------Visualize-------------")
		print()
		
		
	#all the actions are calculated here, for each action 1-6
	#all the required states are changed here, including printing
	#at the end of the function we are calling Vizualize to print
	#will need to consider how to combine with the Percepts for A2
	def action(self, action):
		# ADDITION FOR A2
		#checking if agent has gold, so we can follow map back to exit (1,1)
		if (self.agent.hasGold == True):
			action = self.agent.navigateToExit()
		#Theoretically "removing" the grab function from being randomized
		if (self.agent.coords in self.goldLocation):
			action = 4
			
		#GAME LOOP
		self.actionCount += 1
		# forward = 1
		if (action == 1):
			self.agent.forward()
			# ADDITION FOR A3
			self.agent.perceive(self.grid[self.agent.coords[0]][self.agent.coords[1]])
			if (self.printGrid == True):
				print("Action(1): Move Forward")
			if (self.agent.coords in self.wumpusLocation):
				if (self.wumpusAlive):
					self.agent.isAlive = False
					self.gameTerminated = True #game over
					print("You've been eaten by the Wumpus!!!")
					self.agent.score += -1000
			elif (self.agent.coords in self.pitLocations):
				self.agent.isAlive = False
				self.gameTerminated = True #game over
				print("You fell into a pit!!!")
				self.agent.score += -1000
			self.agent.score += -1
			
		# turnLeft = 2
		elif (action == 2):
			self.agent.turnLeft()
			self.agent.score += -1
			if (self.printGrid == True):
				print("Action(2): Turn Left")
			
		# turnRight = 3
		elif (action == 3):
			self.agent.turnRight()
			self.agent.score += -1
			if (self.printGrid == True):
				print("Action(3): Turn Right")
			
		# grab, if Gold in same room = 4
		elif (action == 4):
			if (self.printGrid == True):
				print("Action(4): Grab")
			#consider deleting first "if" statement below
			if (self.agent.hasGold == True):
				return
			if (self.agent.coords in self.goldLocation):
				self.agent.hasGold = True
				self.goldLocation.clear() #might need to delete later
				self.agent.agentGrabbedGold() # ADDITION FOR A2
			self.agent.score += -1
				
		# shoot = 5
		elif (action == 5):
			if (self.printGrid == True):
				print("Action(5): Shoot -> ", self.agent.direction)
			if (self.agent.hasArrow == False):
				return
			self.agent.hasArrow = False
			if (self.agent.direction == "EAST"):
				x = min(self.width - 1, self.agent.coords[1] + 1)
				if ([self.agent.coords[0], x] in self.wumpusLocation):
					self.wumpusAlive = False
					print("SCREEEEEEAAAAAAAAMMMMMMMM!!!!!!")
					print("Arrow shot and hit something!!!!")
			elif (self.agent.direction == "WEST"):
				x = max(0, self.agent.coords[1] - 1)
				if ([self.agent.coords[0], x] in self.wumpusLocation):
					self.wumpusAlive = False
					print("SCREEEEEEAAAAAAAAMMMMMMMM!!!!!!")
					print("Arrow shot and hit something!!!!")
			elif (self.agent.direction == "NORTH"):
				y = min(self.height - 1, self.agent.coords[0] + 1)
				if ([y, self.agent.coords[1]] in self.wumpusLocation):
					self.wumpusAlive = False
					print("SCREEEEEEAAAAAAAAMMMMMMMM!!!!!!")
					print("Arrow shot and hit something!!!!")
			elif (self.agent.direction == "SOUTH"):
				y = max(0, self.agent.coords[0] - 1)
				if ([y, self.agent.coords[1]] in self.wumpusLocation):
					self.wumpusAlive = False
					print("SCREEEEEEAAAAAAAAMMMMMMMM!!!!!!")
					print("Arrow shot and hit something!!!!")
			else:
				self.agent.score += -10
				if (self.printGrid == True):
					print("Arrow shot and missed.")
			
		# climb, with Gold, on [0,0] = 6
		elif (action == 6):
			if (self.printGrid == True):
				print("Action(6): Climb with Gold")
			if ((self.agent.coords == [0,0]) and (self.agent.hasGold == True)):
				self.gameTerminated = True #game over
				print("YOU WIN!!!!")
				self.agent.score += 1000
				self.gameWon = True
		#call vizualize
		if (self.printGrid == True):
			self.visualize()
		
