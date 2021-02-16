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
        # check for triples, doubles
        player1Threes = self.getThrees(brd, 1)
        player2Threes = self.getThrees(brd, 2)
        player1Twos = self.getTwos(brd, 1)
        player2Twos = self.getTwos(brd, 2)
        return 25 * player1Threes + 5 * player1Twos - (player2Threes * 25 + player2Twos)

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

    def getThrees(self, brd, player):
        """returns the number of three in a rows for a given player (counts threes that are not touching)"""
        numThrees = 0
        for x in range(brd.w):
            for y in range(brd.h):
                if brd.board[y][x] == 0:
                    break
                if brd.board[y][x] != player:
                    continue
                # boundry checking
                if x + 2 < brd.w:
                    # can go to the right
                    if brd.board[y][x + 1] == player and brd.board[y][x + 2] == player:
                        numThrees += 1
                if y + 2 < brd.h:
                    # can go down
                    if brd.board[y + 1][x] == player and brd.board[y + 2][x] == player:
                        numThrees += 1
                if x + 2 < brd.w and y + 2 < brd.h:
                    # down right
                    if brd.board[y + 1][x + 1] == player and brd.board[y + 2][x + 2] == player:
                        numThrees += 1
                if x - 2 >= 0 and y + 2 < brd.h:
                    # down left
                    if brd.board[y + 1][x - 1] == player and brd.board[y + 2][x - 2] == player:
                        numThrees += 1
        return numThrees

    def getTwos(self, brd,player):
        numTwos = 0
        for x in range(brd.w):
            for y in range(brd.h):
                if brd.board[y][x] == 0:
                    break
                if brd.board[y][x] != player:
                    continue
                # boundry checking
                if x + 1 < brd.w:
                    # can go to the right
                    if brd.board[y][x + 1] == player:
                        numTwos += 1
                if y + 1 < brd.h:
                    # can go down
                    if brd.board[y + 1][x] == player:
                        numTwos += 1
                if x + 1 < brd.w and y + 1 < brd.h:
                    # down right
                    if brd.board[y + 1][x + 1] == player:
                        numTwos += 1
                if x - 1 >= 0 and y + 1 < brd.h:
                    # down left
                    if brd.board[y + 1][x - 1] == player:
                        numTwos += 1
        return numTwos