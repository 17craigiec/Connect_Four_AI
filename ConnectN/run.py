import random
import game
import agent
# import alpha_beta_agent as aba
# import alpha_beta_agent_connor as abac

from Group02.alpha_beta_agent import THE_AGENT as TestGroup02

# Set random seed for reproducibility
random.seed(1)

#
# Random vs. Random
# #
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.RandomAgent("random1"),       # player 1
#               agent.RandomAgent("random2"))       # player 2

#
# Human vs. Random

# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               agent.RandomAgent("random"))        # player 2

#
# Random vs. AlphaBeta

# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.RandomAgent("random"),        # player 1
#               aba.AlphaBetaAgent("alphabeta", 4)) # player 2

#
# Human vs. AlphaBeta
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               aba.AlphaBetaAgent("alphabeta", 4)) # player 2

#
# Human vs. Human
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human1"),   # player 1
#               agent.InteractiveAgent("human2"))   # player 2

# Connor vs Ilona

# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               aba.AlphaBetaAgent("IlonaAlphaBeta", 3),   # player 1
#               abac.AlphaBetaAgent("ConnorAlphaBeta", 4))   # player 2

# Execute the game
# outcome = g.go()


# all the things I need to play

# ilona ab vs random - ilona 2nd
# g = game.Game(10, # width
#               8, # height
#               5, # tokens in a row to win
#               agent.RandomAgent("random"),        # player 1
#               aba.AlphaBetaAgent("IlonaAlphaBeta", 3)) # player 2

# ilona ab vs random - ilona 1st
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               aba.AlphaBetaAgent("IlonaAlphaBeta", 4),        # player 1
#               agent.RandomAgent("random")) # player 2

# connor ab vs random - connor 2nd
# g = game.Game(10, # width
#               8, # height
#               5, # tokens in a row to win
#               agent.RandomAgent("random"),        # player 1
#               abac.AlphaBetaAgent("ConnorAlphaBeta", 7)) # player 2

# connor ab vs random - connor 1st
g = game.Game(7, # width
              6, # height
              4, # tokens in a row to win
              TestGroup02,        # player 1
              agent.RandomAgent("random")) # player 2

# g = game.Game(10, # width
#               8, # height
#               5, # tokens in a row to win
#               agent.RandomAgent("random"),        # player 1
#               TestGroup02) # player 2


outcome = g.timed_go(15)