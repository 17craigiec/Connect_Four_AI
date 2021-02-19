from queue import PriorityQueue
import numpy as np
import math
import agent

###########################
# Alpha-Beta Search Agent #
###########################


class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        self.calc_heuristic(brd)

        return np.random.randint(0, brd.w-1)
    
    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ


# ========================== MINIMAX RELATED ===============================

    def minimax(self, brd):
        # Calculate the numeric best value
        best_val = self.get_max(brd)

        possible_moves = self.get_successors(brd)
        sorted_possible_moves = self.sort_moves_by_huer(possible_moves)

        best_move = None
        for move in sorted_possible_moves:
            if self.calc_heuristic(move[0]) == best_val:
                # The second value in the tuple is the column number to enter your disc
                best_move = move[1]
                break

        # Return the column number
        if best_move is None:
            print("ERROR no best move found...")
        return best_move

    def get_max(self, brd):
        # Check for a terminal state (list of free_cols is empty)
        if not brd.free_cols():
            return self.calc_heuristic(brd)

        # Set the max value beta to a value of negative inf
        beta = -1*float('inf')

        # Get a list of sorted possible moves
        possible_moves = self.get_successors(brd)
        sorted_possible_moves = self.sort_moves_by_huer(possible_moves)

        for move in sorted_possible_moves:
            beta = max(beta, self.get_min(move))
        return beta

    def get_min(self, brd):
        # Check for a terminal state (list of free_cols is empty)
        if not brd.free_cols():
            return self.calc_heuristic(brd)

        # Set the min value alpha to a value of inf
        alpha = float('inf')

        # Get a list of sorted possible moves
        possible_moves = self.get_successors(brd)
        # Reverse the sorted moves so that the worst board configuration is searched first
        sorted_possible_moves = self.sort_moves_by_huer(possible_moves)[::-1]

        for move in sorted_possible_moves:
            alpha = max(alpha, self.get_min(move))
        return alpha

    def sort_moves_by_huer(self, possible_moves):
        q = PriorityQueue()
        sorted_moves = []

        for move in possible_moves:
            q.put((self.calc_heuristic(move[0]), move[0]))

        while not q.empty():
            q_move = q.get()
            sorted_moves.append(q_move[1])

        return sorted_moves
        

    # ============================ END MINIMAX =================================
    # ==========================================================================
        
    # Calculate the heuristic for a given board space
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [int]: the heuristic for the given board, such that a higher score correlates to a preferable board 
    #
    # def calc_heuristic(self, brd):

    #     heuristic_total = 0

    #     freecols = brd.free_cols()  #the free cols, to go thru columns with only open moves

    #     for col in freecols: # go thru all cols that contain a free col - we are not super interested in filled spaces
    #         for row in range(0, brd.h):
    #             current_cell = brd.board[col][row]
                
    #             if(current_cell == 0):  # it is a free space and we need to rank its value
    #                 heuristic_total += 1

    #                 # heuristic_total += self.search_neighbors_linear(brd, row, col, dx, dy)

    #                 # heuristic_total += self.search_neighbors_break(brd)

    #                 # if the cell is an open space, I want to look around and see what the neighbors are
    #                 # if a neighbor is free, I'm not super interested - add 1 point, because there is space for future moves
    #                 # I will go nearby in each direction until I see a different cell other than mine
    #                 # if the next cell is my opponent's, ick - 0 points
    #                 # if the next cell is mine, +10 points
    #                 # will be a total of 100*(n-1) max points for how many are in a row there
    #                 heuristic_total += self.search_neighbors_linear(brd, row, col, 1, 0) #horizontal right
    #                 heuristic_total += self.search_neighbors_linear(brd, row, col, -1, 0) #horizontal left
    #                 heuristic_total += self.search_neighbors_linear(brd, row, col, 0, 1) #vertical (up)
    #                 heuristic_total += self.search_neighbors_linear(brd, row, col, 0, -1) #vertical (down)
    #                 heuristic_total += self.search_neighbors_linear(brd, row, col, 1, 1) #diagonal up, right
    #                 heuristic_total += self.search_neighbors_linear(brd, row, col, 1, -1) #diagonal down, right
    #                 heuristic_total += self.search_neighbors_linear(brd, row, col, -1, -1) #diagonal down, left
    #                 heuristic_total += self.search_neighbors_linear(brd, row, col, -1, 1) #diagonal up, right

    #                 # I will need a separate loop to check for if the space is between two of my own, because then I like it,
    #                 #   especially if both of the sides add to n-1 in total, or n if I move to that free spot!!
    #                 # this type of spot should also be worth 10*(n-1)
    #                 heuristic_total += self.search_neighbors_break(brd, row, col, 1)
    #                 heuristic_total += self.search_neighbors_break(brd, row, col, -1)
    #                 heuristic_total += self.search_neighbors_break(brd, row, col, 0)

    #     return heuristic_total

    # def search_neighbors_linear(self, brd, row, col, dx, dy):
    #     heuristic_total_linear = 0
    #     count_in_row = 0

    #     for i in range(0, brd.n):
    #         if (col + i*dy) < brd.w and (col + i*dy) > 0 and (row + i*dx) < brd.h and (row + i*dx) > 0:  # this checks that it is still in-bounds
    #             current = brd.board[col + i*dy][row + i*dx]
    #             if current == self.name:
    #                 count_in_row += 1
    #             else: #it is the other opponent or free - we're done investigating how many are in a row
    #                 break
        
    #     heuristic_total_linear = count_in_row * 1000 #1000 pts for each token

    #     if count_in_row < brd.n: #see how many free spaces surround the amt here
    #         current = brd.board[col][row]
    #         last_in_row_col = col+count_in_row*dy
    #         last_in_row_row = row+count_in_row*dx
    #         for i in range(0, brd.n - count_in_row + 1):
    #             if (last_in_row_col + i*dy) < brd.w and (last_in_row_col + i*dy) > 0 and (last_in_row_row + i*dx) < brd.h and (last_in_row_row + i*dx) > 0:
    #                 current = brd.board[last_in_row_col + i*dy][last_in_row_row + i*dx]
    #                 if current == 0 :
    #                     heuristic_total_linear += 500 #add 500 pts for each open space
    #                 elif current != self.name: #this is the other player!! we can't make a full row :( - null tthe points given to this
    #                     heuristic_total_linear = 0
    #                     break

    #     return heuristic_total_linear

    # def search_neighbors_break(self, brd, row, col, dy):
    #     heuristic_total_break = 0
    #     count_left = 0
    #     count_right = 0

    #     # curr_row = row
    #     # curr_col = col

    #     #loop "left"
    #     for i in range(0, brd.n):
    #         if (col + i*dy) < brd.w and (col + i*dy) > 0 and (row -i) < brd.h and (row -i) > 0:  # this checks that it is still in-bounds
    #             current_cell = brd.board[col + i*dy][row-i]
    #             if current_cell == self.name :
    #                 count_left += 1
    #                 heuristic_total_break += 50
    #             elif current_cell == 0:
    #                 heuristic_total_break += 25
    #                 break
    #             else:
    #                 heuristic_total_break = 0
    #                 break

    #     #loop "right"
    #     for i in range(0, brd.n):
    #         if (col + i*dy) < brd.w and (col + i*dy) > 0 and (row + i) < brd.h and (row + i) > 0:  # this checks that it is still in-bounds
    #             current_cell = brd.board[col + i*dy][row+i]
    #             if current_cell == self.name :
    #                 count_right += 1
    #                 heuristic_total_break += 50
    #             elif current_cell == 0:
    #                 heuristic_total_break += 25
    #                 break
    #             else:
    #                 heuristic_total_break = 0
    #                 break
                
    #     if count_right == brd.n-1:
    #         heuristic_total_break += 1000
    #     if count_left == brd.n-1:
    #         heuristic_total_break += 1000
    #     if count_right + count_left == brd.n-1:
    #         heuristic_total_break += 1000


    #     return heuristic_total_break


    