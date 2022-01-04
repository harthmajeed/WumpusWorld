Harth Majeed
Intelligent Agents and Reinforcement Learning - Assignment 2

There are 3 files:
Agent.py
Environment.py
main.py

To run the application please run the main.py via pycharm ,or visual studio, or any other
IDE.

You can also execute a CMD/PowerShell from this folder (Hold SHIFT + Right Click) and 
run the command "python main.py" and the application should run no problems.

Everytime you run the application it will run a loop and stop when eaten or exited the cave with the Gold. The game loop counter, the state information, environment and agent information, and the grid will be displayed for each run. Each action taken will also be displayed, each action increments the game loop.

The grid will be split using [], [] represents each room, and will contain the appropiate letters to indicate what's contained in them. 
A = Agent
G = Gold/glitter
P = pit
W = wumpus
b = breeze
s = stench

# ADDITION FOR A2
I've added a jupyter notebooke file, called "VisualTesting". This has the same code as main.py, but slightly modified, when this is run it will execute the application and then draw the graph with nodes and edges. It's there for visualization purposes and can be used if you like.