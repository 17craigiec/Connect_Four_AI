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
            succ.append((nb, col))
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



    # ========================= HEURISTIC RELATED ==============================

    def calc_heuristic(self, brd):
        # Heuristic will be = your board score - opponent board score
        self_score = self.get_player_score(brd, 2)
        print("Self score calculated: " + str(self_score))
        opponent_score = self.get_player_score(brd, 1)
        print("Opponent score calculated: " + str(opponent_score))

        heur = self_score - opponent_score
        print("Heuristic Value (-opponent_leaning +self_leaning): " + str(heur))
        return heur

    def get_player_score(self, brd, player):
        valid_rows = self.get_valid_rows(brd)
        player_score = 0

        for row in valid_rows:
            row_cnt = 0
            for row_dir in [row, row[::-1]]:
                for r in row_dir:
                    if r[0] == player:
                        row_cnt = row_cnt + 1
                    if r[0] == 0 and row_cnt != 0:
                        player_score = player_score + row_cnt*(brd.h-self.get_pos_height(brd, r[1]))
                        row_cnt = 0

        return player_score

    def get_pos_height(self, brd, pos):
        np_board = np.array(brd.board)
        height = 0
        while pos[0] >= 0 and np_board[pos[0], pos[1]] == 0:
            pos = (pos[0]-1, pos[1])
            height = height + 1
        return height-1

    def get_valid_rows(self, brd):
        # check vertical rows
        # check horizontal rows
        # check diagonal right
        # check diagonal left

        np_board = np.array(brd.board)
        # A collection of all rows (and their states) in which a connect-n is possible
        valid_rows = []

        # vertical rows
        for w in range(brd.w):
            tmp_row = []
            for h in range(brd.h):
                tmp_row.append((np_board[h, w], (h, w)))
            valid_rows.append(tmp_row)

        # horizontal rows
        for h in range(brd.h):
            tmp_row = []
            for w in range(brd.w):
                tmp_row.append((np_board[h, w], (h, w)))
            valid_rows.append(tmp_row)

        # diagonal right
        for h in range(brd.h - (brd.n - 1)):
            tmp_row = []
            curr = (h, 0)  # starts from w = 0
            # Check to see the diagonal can ascend unbounded else bound to size of min axis
            if brd.w > brd.h - h:
                diagonal_width = brd.h - h
            else:
                diagonal_width = brd.w
# ??? loop not used
            for w in range(diagonal_width):
                tmp_row.append((np_board[curr[0], curr[1]], curr))
                curr = (curr[0]+1, curr[1]+1)
            valid_rows.append(tmp_row)
        for w in range(brd.w - (brd.n - 1))[1:]:  # The diagonal at 0,0 if covered by the loop above
            tmp_row = []
            curr = (0, w)  # current always starts at h = 0
            # Check to see the diagonal can ascend unbounded else bound to size of min axis
            if brd.h > brd.w - w:
                diagonal_width = brd.w - w
            else:
                diagonal_width = brd.h
                # loop not used????
            for h in range(diagonal_width):
                tmp_row.append((np_board[curr[0], curr[1]], curr))
                curr = (curr[0]+1, curr[1]+1)
            valid_rows.append(tmp_row)

        # diagonal left
        for h in range(brd.h - (brd.n - 1)):
            tmp_row = []
            curr = (h, brd.w-1)  # starts from w = brd.w
            # Check to see the diagonal can ascend unbounded else bound to size of min axis
            if brd.w > brd.h - h:
                diagonal_width = brd.h - h
            else:
                diagonal_width = brd.w
# loop not used?
            for w in range(diagonal_width):
                tmp_row.append((np_board[curr[0], curr[1]], curr))
                curr = (curr[0]+1, curr[1]-1)
            valid_rows.append(tmp_row)
        for w in [brd.w - x for x in range(brd.w - (brd.n - 1))[1:]]:  # diagonal at 0,0 if covered by the loop above
            tmp_row = []
            curr = (0, w-1)  # current always starts at h = 0
            # Check to see the diagonal can ascend unbounded else bound to size of min axis
            if brd.h > w:
                diagonal_width = w
            else:
                diagonal_width = brd.h
            for h in range(diagonal_width):
                tmp_row.append((np_board[curr[0], curr[1]], curr))
                curr = (curr[0]+1, curr[1]-1)
            valid_rows.append(tmp_row)
            
        return valid_rows

        # =========================== END HEURISTIC ================================
        # ==========================================================================
