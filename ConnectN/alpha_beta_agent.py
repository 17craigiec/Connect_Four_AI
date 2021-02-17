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

        #this is going to be where the minimax / pruning algorithm goes
    
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
        
    # Calculate the heuristic for a given board space
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [int]: the heuristic for the given board, such that a higher score correlates to a preferable board 
    #
    def get_heuristic(self, brd):

        heuristic_total = 0

        freecols = brd.free_cols()  #the free cols, to go thru columns with only open moves

        for col in freecols: # go thru all cols that contain a free col - we are not super interested in filled spaces
            for row in range(0, brd.h):
                current_cell = brd[col][row]
                
                if(current_cell == 0):  # it is a free space and we need to rank its value
                    heuristic_total += 1

                    # heuristic_total += self.search_neighbors_linear(brd, row, col, dx, dy)

                    # heuristic_total += self.search_neighbors_break(brd)

                    # if the cell is an open space, I want to look around and see what the neighbors are
                    # if a neighbor is free, I'm not super interested - add 1 point, because there is space for future moves
                    # I will go nearby in each direction until I see a different cell other than mine
                    # if the next cell is my opponent's, ick - 0 points
                    # if the next cell is mine, +10 points
                    # will be a total of 100*(n-1) max points for how many are in a row there
                    heuristic_total += self.search_neighbors_linear(brd, row, col, 1, 0) #horizontal right
                    heuristic_total += self.search_neighbors_linear(brd, row, col, -1, 0) #horizontal left
                    heuristic_total += self.search_neighbors_linear(brd, row, col, 0, 1) #vertical (up)
                    heuristic_total += self.search_neighbors_linear(brd, row, col, 0, -1) #vertical (down)
                    heuristic_total += self.search_neighbors_linear(brd, row, col, 1, 1) #diagonal up, right
                    heuristic_total += self.search_neighbors_linear(brd, row, col, 1, -1) #diagonal down, right
                    heuristic_total += self.search_neighbors_linear(brd, row, col, -1, -1) #diagonal down, left
                    heuristic_total += self.search_neighbors_linear(brd, row, col, -1, 1) #diagonal up, right

                    # I will need a separate loop to check for if the space is between two of my own, because then I like it,
                    #   especially if both of the sides add to n-1 in total, or n if I move to that free spot!!
                    # this type of spot should also be worth 10*(n-1)

        return heuristic_total

    def search_neighbors_linear(self, brd, row, col, dx, dy):
        heuristic_total_linear = 0
        count_in_row = 0

        for i in range(0, brd.n):
            if (col + i*dy) < brd.w and (col + i*dy) > 0 and (row + i*dx) < brd.h and (row + i*dx) > 0:  # this checks that it is still in-bounds
                current = brd[col + i*dy][row + i*dx]
                if current == self.name:
                    count_in_row += 1
                else: #it is the other opponent or free - we're done investigating how many are in a row
                    break
        
        heuristic_total_linear = count_in_row * 1000 #1000 pts for each token

        if count_in_row < brd.n: #see how many free spaces surround the amt here
            current = brd[col][row]
            last_in_row_col = col+count_in_row*dy
            last_in_row_row = row+count_in_row*dx
            for i in range(0, brd.n - count_in_row + 1):
                if (last_in_row_col + i*dy) < brd.w and (last_in_row_col + i*dy) > 0 and (last_in_row_row + i*dx) < brd.h and (last_in_row_row + i*dx) > 0:
                    current = brd[last_in_row_col + i*dy][last_in_row_row + i*dx]
                    if current == 0 :
                        heuristic_total_linear += 500 #add 500 pts for each open space
                    elif current != self.name: #this is the other player!! we can't make a full row :( - null tthe points given to this
                        heuristic_total_linear = 0
                        break

        return heuristic_total_linear

    def search_neighbors_break(self, brd):
        heuristic_total_break = 0
        count_left = 0
        count_right = 0

        #loop "left"


        #loop "right"


        return heuristic_total_break