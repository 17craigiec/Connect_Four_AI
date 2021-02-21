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
        self.m_max_depth = max_depth

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

        return self.minimax(brd)

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
        print("Running minimax")
        # Calculate the numeric best value
        # best_val = self.get_max(brd)

        depth = self.m_max_depth
        possible_moves = self.get_successors(brd)

        sorted_possible_moves = self.sort_moves_by_huer(possible_moves)

        best_move = sorted_possible_moves[0]
        best_val = -float("Infinity")
        for move in sorted_possible_moves:
            val = self.get_min(move[0], float('inf'), -float('inf'), depth)
            if val > best_val:
                best_move = move[1]
                best_val = val

        return best_move

        # sorted_possible_moves = self.sort_moves_by_huer(possible_moves)

        # best_move = None
        # for move in sorted_possible_moves:
        #     if self.calc_heuristic(move[0]) == best_val:
        #         # The second value in the tuple is the column number to enter your disc
        #         best_move = move[1]
        #         break

        # Return the column number

    def get_max(self, brd, alpha, beta, depth):
        outcome = brd.get_outcome()
        if outcome != 0:
            return -float('inf')

        # Check for a terminal state (list of free_cols is empty)
        if not brd.free_cols():
            return 0

        if depth == 0:
            return self.calc_heuristic(brd)

        # Get a list of sorted possible moves
        possible_moves = self.get_successors(brd)
        # sorted_possible_moves = self.sort_moves_by_huer(possible_moves)
        val = -float('inf')
        for move in possible_moves:
            val = max(val, self.get_min(move[0], alpha, beta, depth -1))
            beta = max(val, beta)
            if beta > alpha:
                return val
        return val

    def get_min(self, brd, alpha, beta, depth):
        if brd.get_outcome() != 0:
            return float('inf')
        # Check for a terminal state (list of free_cols is empty)
        if not brd.free_cols():
            return 0

        if depth == 0:
            return self.calc_heuristic(brd)

        # Get a list of sorted possible moves
        possible_moves = self.get_successors(brd)
        # Reverse the sorted moves so that the worst board configuration is searched first
        # sorted_possible_moves = self.sort_moves_by_huer(possible_moves)[::-1]
        val = float('inf')
        for move in possible_moves:
            val = min(val, self.get_max(move[0], alpha, beta, depth - 1))
            alpha = min(val, beta)
            if alpha < beta:
                return val
        return val

    def sort_moves_by_huer(self, possible_moves):
        print("Sorting the heuristics")
        # q = PriorityQueue()
        # sorted_moves = []

        # for move in possible_moves:
        #     # print(int(self.calc_heuristic(move[0])))
        #     # q.put((self.calc_heuristic(move[0]), move[0]))
        #     q.put((self.calc_heuristic(move[0]), 'Hello'))

        # while not q.empty():
        #     q_move = q.get()
        #     sorted_moves.append(q_move[1])
        #     print(q_move[0])

        sorted_moves = []

        for move in possible_moves:
            sorted_moves.append((self.calc_heuristic(move[0]), move))

        sorted_moves.sort(key=self.sortByHeur)

        final_sorted_moves = []

        for move in sorted_moves:
            print("Heuristic:" + str(move[0]))
            final_sorted_moves.append(move[1])

        return final_sorted_moves

    def sortByHeur(self, val):
        return val[0]
        

    # ============================ END MINIMAX =================================
    # ==========================================================================



    # ========================= HEURISTIC RELATED ==============================

    def calc_heuristic(self, brd):
        # Heuristic will be = your board score - opponent board score
        self_score = self.get_player_score(brd, 2)
        # print("Self score calculated: " + str(self_score))
        opponent_score = self.get_player_score(brd, 1)
        # print("Opponent score calculated: " + str(opponent_score))

        heur = self_score - opponent_score
        # print("Heuristic Value (-opponent_leaning +self_leaning): " + str(heur))
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
                        if row_cnt == brd.n:
                            player_score = player_score + 9000
                            return player_score
                    # added by ilona to try to catch the case that it is a free spot AND row count is n-1 to get the immediate win
                    # if r[0] == 0 and row_cnt == (brd.n-1):
                    #     return 
                    ###
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
