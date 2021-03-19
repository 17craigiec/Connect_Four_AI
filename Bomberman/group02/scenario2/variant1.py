# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# This is your code!
sys.path.insert(1, '../group02')
from testcharacter import TestCharacter


# Create the game
g = Game.fromfile('map.txt')

# Add your character
g.add_character(TestCharacter("Group02", # name
                              "C",  # avatar
                              0, 0  # position
))

# Run!
# g.go()
g.go(1)