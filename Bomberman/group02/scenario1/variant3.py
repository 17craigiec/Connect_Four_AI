# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
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
g.add_monster(SelfPreservingMonster("selfpreserving", # name
                                    "S",              # avatar
                                    3, 9,             # position
                                    1                 # detection range
))

# Add your character as TestCharacter
g.add_character(TestCharacter("Group02", # name
                              "C",  # avatar
                              0, 0  # position
))

# Run!
# g.go()
g.go(1)
