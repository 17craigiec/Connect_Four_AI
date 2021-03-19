# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# This is your code!
sys.path.insert(1, '../group02')
from testcharacter import TestCharacter

# Create the game
random.seed(10)
# random.seed(20)
# random.seed(30)
# random.seed(40)
# random.seed(50)
# random.seed(60)
# random.seed(70)
# random.seed(80)
# random.seed(90)
# random.seed(100)

g = Game.fromfile('map.txt')
g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    3, 13,        # position
                                    2             # detection range
))

# Add your character
g.add_character(TestCharacter("Group02", # name
                              "C",  # avatar
                              0, 0  # position
))

# Run!
#g.go()
g.go(1)
