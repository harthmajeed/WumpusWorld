import networkx as nx
import matplotlib.pyplot as plt


'''
3547 Assignment 3
This assignment builds on your Beeline Agent. The new agent will keep the same strategy for planning 
the route home after grabbing the gold but will have a new added superpower: a strategy for searching 
the grid for the gold as safely as it can. This will require it to make inferences about which squares 
definitely don’t have a pit or Wumpus, or for those that might, what the probability is so it can take 
calculated risks.

Instructions
1. Create a copy of the BeelineAgent called ProbAgent (because it will use probabilistic reasoning)
or make ProbAgent a subclass of Beeline Agent if you prefer. You’ll need to add additional belief 
state variables to track the history of locations of Stench and Breeze percepts. You’ll need these 
to make inferences about the probability of there being a Wumpus or pit at locations the agent 
hasn’t visited yet, which will enable it to perform much better than even a Logical Agent. You’ll 
also want to keep track of whether you heard a Scream or not.

2. Use the Python Pomegranate library to build two causal graphs, one for the relationship 
between pit locations and breeze locations, and one for the relationship between Wumpus
locations and stench locations. The first graph should encode how the locations of the pits 
cause breezes at other grid locations. Initialize the graphs with the prior probabilities of there 
being a pit or Wumpus at each location.

3. The agent should use the percepts it receives at each step to update the state variables 
mentioned above, which will change the probabilities of there being pits and a Wumpus at other 
locations.

4. Use the probabilities which can be queried from the two models to decide how best to search 
the grid for the gold. You don’t want your agent to (a) unnecessarily visit locations it’s already 
been (b) take unnecessary risks (c) give up without attempting to kill the Wumpus if it is likely to
be beneficial, (d) waste its arrow unnecessarily, or (e) to give up unless the next move is more 
than 50% (1) likely to result in its death (in which case it should proceed as quickly as it can to (1,1) 
and Climb). You may find that a modified version of your route planner from the BeelineAgent 
can help speed up the search part of the game as well. Your agent will need to take risks and 
occasionally die to play its long-run best, but they should be calculated risks and only when 
there are no risk-free paths known to be available. Note also that the arrow isn’t just a weapon; 
it can also be used as a probe for information about the Wumpus’ location.

5. What is your agent’s total score after exactly 1,000 games?

(1) You won’t know what the real probability of success is, jus the probability of dying on the next move. If the 
chance of dying on the next move is 50-50, the probability of successfully completing the maze will a be a bit lower 
than that, so under the rules of the game the best strategy in that situation would be to abort the mission. If we 
increase the payoff for success from +1,000 to something larger or add a penalty for quitting empty-handed, the 
probabilistic agent will clearly outperform a logical agent by accepting the occasional low-probability death in 
return for a greater long-run reward. A logical agent can’t distinguish low and high risk moves, just safe and unsafe 
ones

1. 	track history of locations of stench
	track history of locations of breeze
	screamHeard = False

2. 	build casual pomegranate graph for breeze and pit locations
	build casual pomegranate graph for stench and wumpus location
	--first graph should encode how the locations of the pits cause breezes at other grid locations
	--Initialize the graphs with the prior probabilities of there being a pit or Wumpus at each location
	
3.	agent should update state variables when coming into contact with breeze or stench

4.	query the probabilities from the 2 models to decide how to search for gold
	a) don't visit locations already visited
	b) don't take unnecessary risks
	c) dont give up attempting to kill Wumpus
	d) don't waste arrow unnecessary
	e) don't give up unless next move is more than 50% chance of death
	--Arrow can be used as probe information about Wumpus location
'''


class Agent:
	"Agent in the cave"	
	def __init__(self):
		self.direction = "EAST"
		self.coords = [0,0]
		self.hasGold = False
		self.hasArrow = True
		self.isAlive = True
		self.score = 0
		self.pathToExitLength = 0
		self.pathToExit = []
		self.pathToExitCopy = []
		self.historyOfStench = []
		self.historyOfBreeze = []
		self.historyOfGold = []
		self.graph = nx.DiGraph()
		
		
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


	# ADDITION FOR A3
	def perceive(self, locationContent):
		#stench
		if ('s' in locationContent):
			if (self.coords not in self.historyOfStench):
				self.historyOfStench.append(self.coords)
		#breeze
		if ('b' in locationContent):
			if (self.coords not in self.historyOfBreeze):
				self.historyOfBreeze.append(self.coords)

	
	
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
		
		#print("Directional Coordinates Adjacent to Agent")
		#print("East",eastCoords,"West",westCoords,"North",northCoords,"South",southCoords)
		#print()
		
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
	

	
