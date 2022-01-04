
from Agent import Agent
from Environment import Environment
import random

#play game function
def playGame(env):
    while (env.gameTerminated == False):
        env.action(random.randint(1,6))
        
    
def main(args):
	#create the Agent and pass into the Environment
	print("Hello World")
	agent = Agent(False, True, True)
	env = Environment(4, 4, 0.2, False, agent, False, True)
	
	#playing the game, pass environment
	playGame(env)
	
	return 0
    

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))




