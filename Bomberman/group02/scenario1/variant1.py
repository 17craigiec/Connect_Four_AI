# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../groupNN')

def heuristic(locA, locB) -> float:
    (x1, y1) = locA
    (x2, y2) = locB
    return abs(x1-x2) + abs(y1-y2)


def Astar(graph, start, exit):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    lastLocation: Dict[exit] = {}
    costSoFar: Dict[exit, float] = {}
    lastLocation[start] = None
    costSoFar[start] = 0

    while not frontier.empty():
        current: Location = frontier.get()

        if current == exit:
            break

        for next in graph.neighbors(current):
            newCost = costSoFar[current] + graph.cost(current, next)
            if next not in costSoFar or newCost < costSoFar[next]:
                costSoFar[next] = newCost
                priority = newCost + heuristic(next, exit)
                frontier.put(next, priority)
                lastLocation[next] = current

    return lastLocation, costSoFar



# Uncomment this if you want the empty test character
#from testcharacter import TestCharacter

# Uncomment this if you want the interactive character
from interactivecharacter import InteractiveCharacter

# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character

# Uncomment this if you want the test character
# g.add_character(TestCharacter("me", # name
#                               "C",  # avatar
#                               0, 0  # position
# ))

# Uncomment this if you want the interactive character
g.add_character(InteractiveCharacter("me", # name
                                     "C",  # avatar
                                     0, 0  # position
))

# Run!

# Use this if you want to press ENTER to continue at each step
# g.go(0)

# Use this if you want to proceed automatically
g.go(1)
