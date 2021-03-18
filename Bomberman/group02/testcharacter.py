# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    char = CharacterEntity
    char_x = 0
    char_y = 0

    bomb_timer = 0

    # list of neighboring coordinates to walls, should be updated after bomb  -- NOT USED ANYMORE
    # cspace = []

    # Function run at the start of each move
    #
    # PARAM type wrld, type name: here
    # RETURN type: here
    def do(self, wrld):
        # Your code here
        # print("I am Located at ("+str(self.char_x)+", "+str(self.char_y)+")")

        print("\n\n")
        # self.updateCspaceCoords(wrld)
        # next_move = self.nextMoveHeuristic(wrld)
        monsters = self.locateMonsters(wrld)
        next_move = self.nextMoveToExit(wrld) # connor's code

        

        # self.moveChar(wrld, next_move[0], next_move[1])
        # print("Monsters Located at: "+str(self.locateMonsters(wrld)))
        # print("distance to EXIT is: "+str(self.distanceToExit(wrld, self.char_x, self.char_y)))

        ########### connor's bomb code ##############
        if next_move == (0,0) and self.bomb_timer == 0:
            next_move = self.moveSouth2(wrld)
            if next_move == (0,0):
                self.place_bomb()
                self.bomb_timer += 1
            else:
                self.moveChar(wrld, next_move[0], next_move[1])
            return
        elif self.bomb_timer > 0:
            self.placeBombSittingDuck(wrld)
            self.bomb_timer += 1
            if self.bomb_timer > 14:
                print("RESETTING BOMB TIMER")
                self.bomb_timer = 0
            return

        if self.bomb_timer == 0:
            next_move = self.nextMoveHeuristic(wrld)
            self.moveChar(wrld, next_move[0], next_move[1])


    def nextMoveHeuristic(self, wrld):
        #if i'm too close to a monster, run minimax
        distances_to_mon = self.distanceToMonsters(wrld, self.char_x, self.char_y)
        for m in distances_to_mon:
            monTypes = self.getMonsterName(wrld, m[0][0], m[0][1])
            # print("Montype:" + monType)
            for mtype in monTypes:
                if mtype == "stupid" and m[1] <= 2:
                    print("Too close to stupid monster!!")
                    # best = self.minimax(wrld, self.char_x, self.char_y, 3, True)
                    best = self.ab_minimax(wrld, self.char_x, self.char_y, 3, True, float('-inf'), float('inf'))
                    return (best[0]-self.char_x,best[1]-self.char_y)
                elif mtype != "stupid" and m[1] <= 4:
                    print("Too close to smart monster!!!!")
                    print("Monster info:" + str(m[0]))
                    # best = self.minimax(wrld, self.char_x, self.char_y, 4, True)
                    best = self.ab_minimax(wrld, self.char_x, self.char_y, 5, True, float('-inf'), float('inf'))
                    return (best[0]-self.char_x,best[1]-self.char_y)
        #else, run bfs
            # else:
                # best_option = ((0,0), -1)
        best_option = ((0,0), float('-inf'))
        for neigh in self.getNeighbors(wrld, self.char_x, self.char_y):
            h = self.calcHeuristic(wrld, neigh[0], neigh[1])
            if h > best_option[1]:
                best_option = (neigh, h)

        return (best_option[0][0]-self.char_x, best_option[0][1]-self.char_y)


    def updateCspaceCoords(self, wrld):
        # Init empty if need to rebuild after bomb explosion
        self.cspace = []

        for x in range(wrld.width()):
            for y in range(wrld.height()):
                if wrld.wall_at(x, y):
                    neighbors = self.getNeighbors(wrld, x, y)
                    for neigh in neighbors:
                        if neigh not in self.cspace:
                            self.cspace.append(neigh)


    def calcHeuristic(self, wrld, x, y):
        monsters = self.distanceToMonsters(wrld, x, y)
        # This if statement is here to avoid div by 0
        if monsters:
            closest_monster = 0
        else:
            closest_monster = 1

        closest_monster = 999
        for m in monsters:
            if m[1] < closest_monster:
                closest_monster = m[1]
                # print("Monster Name: "+self.getMonsterName(wrld, m[0][0], m[0][1])[0])

        # total = (-1000/pow(closest_monster,4))-2*pow(self.distanceToExit(wrld, x, y),1.2)
        # Heuristic driven from closeness to monster
        monst_hur = -1000/pow(closest_monster,4)

        # Heuristic driven from distance to exit
        d = self.distanceToExit(wrld, x, y)
        exit_hur = -2*d + pow(3,-(d-5.5))

        # Make bomberman afriad of walls
        w = wrld.width()
        wall_hur = -1*pow(x-w/2, 2) + 2*w

        # Check

        # Sum all huristic values
        total = monst_hur + exit_hur + wall_hur

        # Nonlinear threshold getting close to monster
        if closest_monster <= 2:
            total += -2000

        # if (x, y) in self.cspace:
        #     total -= 10

        return total


    def nextMoveToExit(self, wrld):
        # Simple BFS to poll the exit
        q = [(self.char_x, self.char_y)]
        visited = []
        path = {}

        while q:
            cur = q.pop(0)
            visited.append(cur)

            if wrld.exit_at(cur[0],cur[1]):
                print("EXIT FOUND: (" + str(cur[0])+", "+str(cur[1])+")")
                # Find next movement
                tmp = cur
                while path[tmp] != (self.char_x, self.char_y):
                    tmp = path[tmp]
                return (tmp[0]-self.char_x, tmp[1]-self.char_y)
                
            for neigh in self.getNeighbors(wrld, cur[0], cur[1]):
                if neigh not in visited and neigh not in q:
                    q.append(neigh)
                    path[neigh] = cur

        print("!!! No path to EXIT detected !!!")
        return (0,0)


    def distanceToExit(self, wrld, x, y):
        # Simple BFS to poll the exit
        q = [(x, y)]
        visited = []
        path = {}

        while q:
            cur = q.pop(0)
            visited.append(cur)

            if wrld.exit_at(cur[0],cur[1]):
                # Find next movement
                dist = 1
                tmp = cur
                while tmp != (x, y):
                    dist = dist + 1
                    tmp = path[tmp]
                return dist
                
            for neigh in self.getNeighbors(wrld, cur[0], cur[1]):
                if neigh not in visited and neigh not in q:
                    q.append(neigh)
                    path[neigh] = cur

        print("!!! No path to EXIT detected !!!")
        return -1


    def getMonsterName(self, wrld, x, y):
        if wrld.monsters_at(x, y) != None:
            names = []
            monsters = wrld.monsters_at(x, y)
            for m in monsters:
                names.append(m.name)
        else:
            print("ERROR: not a monster coordinate in getMonsterName()")
        return names


    def locateMonsters(self, wrld):
        # Simple BFS to poll the monsters
        monsters = []
        q = [(self.char_x, self.char_y)]
        visited = []
        path = {}

        while q:
            cur = q.pop(0)
            visited.append(cur)
            # If cur holds a monster log its location
            if wrld.monsters_at(cur[0], cur[1]) != None:
                dist = 1
                tmp = cur
                while tmp != (self.char_x, self.char_y):
                    dist = dist + 1
                    tmp = path[tmp]
                monsters.append( ((cur[0], cur[1]), dist) )

            # break early if both monsters are found
            if len(monsters) >= 2:
                return monsters

            for neigh in self.getNeighbors(wrld, cur[0], cur[1]):
                if neigh not in visited and neigh not in q:
                    q.append(neigh)
                    path[neigh] = cur

        return monsters


    def distanceToMonsters(self, wrld, x, y):
        # Simple BFS to poll the monsters
        monsters = []
        q = [(x, y)]
        visited = []
        path = {}

        while q:
            cur = q.pop(0)
            visited.append(cur)
            # If cur holds a monster log its location
            if wrld.monsters_at(cur[0], cur[1]) != None:
                dist = 1
                tmp = cur
                while tmp != (x, y):
                    dist = dist + 1
                    tmp = path[tmp]
                monsters.append( ((cur[0], cur[1]), dist) )

            # break early if both monsters are found
            if len(monsters) >= 2:
                return monsters

            for neigh in self.getNeighbors(wrld, cur[0], cur[1]):
                if neigh not in visited and neigh not in q:
                    q.append(neigh)
                    path[neigh] = cur

        return monsters


    def isCoordinateValid(self, wrld, x, y):
        is_valid = True

        # Bounds check
        if x >= wrld.width() or x < 0:
            return False
        if y >= wrld.height() or y < 0:
            return False
        if wrld.wall_at(x, y):
            is_valid = False

        return is_valid


    def getNeighbors(self, wrld, x, y):
        offsets = [-1, 0, 1]
        neighbors = []

        for dx in offsets:
            for dy in offsets:
                # dx,dy == 0,0 is the searchng node
                if not (dx == 0 and dy == 0):
                    if self.isCoordinateValid(wrld, x+dx, y+dy):
                        neighbors.append((x+dx, y+dy))

        return neighbors


    def moveChar(self, wrld, dx, dy):
        # X check
        if dx > 1:
            dx = 1
        elif dx < -1:
            dx = -1
        # Y check
        if dy > 1:
            dy = 1
        elif dy < -1:
            dy = -1

        # Bounds check
        if not self.isCoordinateValid(wrld, self.char_x+dx, self.char_y+dy):
            print("Invalid Move Detected")
            dx = 0
            dy = 0

        self.char_x = self.char_x + dx
        self.char_y = self.char_y + dy
        print("I am now at ("+str(self.char_x)+", "+str(self.char_y)+")")
        self.move(dx, dy)


    def minimax(self, wrld, char_x, char_y, depth, is_maximizing):

        # print("I called minimax.  Am I maximizing?" + str(is_maximizing))

        # best is defined as [x, y, score/heuristic of state]

        if is_maximizing:
            best = [-1, -1, float('-inf')]  #might need to change this because this according to ref code is x, y --> we might need move in x, y not to a specific cell
        else:
            best = [-1, -1, float('inf')]

        if depth == 0:
            score = self.calcHeuristic(wrld, char_x, char_y)  #get the heuristic of the board
            return [-1, -1, score]
        if wrld.monsters_at(char_x, char_y) != None:
            score = -1000
            return [-1, -1, score]
        if wrld.exit_at(char_x, char_y):
            score = 2000
            return [-1, -1, score]

        for move in self.getNeighbors(wrld, char_x, char_y):
            char_x_temp = move[0]
            char_y_temp = move[1]

            # temp_state = ?
            #recursively call minimax on the next move as:
            score = self.minimax(wrld, char_x_temp, char_y_temp, depth-1, not is_maximizing)
            score[0], score[1] = char_x_temp, char_y_temp

            # print("Current score is: "+str(score[2])+", best score is " + str(best[2]))

            if is_maximizing:
                if score[2] > best[2]:
                    best = score
                    # print("Best score is: "+str(score[2])+" for turn " + str(is_maximizing))
                # else:
                    # print("Best score is (but didn't maximize): "+str(score[2])+" for turn " + str(is_maximizing))
            else:
                if score[2] < best[2]:
                    best = score
                    # print("Best score is: "+str(score[2])+" for turn " + str(is_maximizing))
                # else:
                    # print("Best score is (but didn't minimize): "+str(score[2])+" for turn " + str(is_maximizing))

            # print("AFTER max or min, Current score is: "+str(score[2])+", best score is " + str(best[2]))

        return best

    def ab_minimax(self, wrld, char_x, char_y, depth, is_maximizing, alpha, beta):
        # best is defined as [x, y, score/heuristic of state]
        if is_maximizing:
            best = [-1, -1, float('-inf')]  #might need to change this because this according to ref code is x, y --> we might need move in x, y not to a specific cell
        else:
            best = [-1, -1, float('inf')]

        if depth == 0:
            score = self.calcHeuristic(wrld, char_x, char_y)  #get the heuristic of the board
            return [-1, -1, score]
        if wrld.monsters_at(char_x, char_y) != None:
            score = -1000
            return [-1, -1, score]
        if wrld.exit_at(char_x, char_y):
            score = 2000
            return [-1, -1, score]

        for move in self.getNeighbors(wrld, char_x, char_y):
            char_x_temp = move[0]
            char_y_temp = move[1]

            #recursively call minimax on the next move as:
            score = self.ab_minimax(wrld, char_x_temp, char_y_temp, depth-1, not is_maximizing, alpha, beta)
            score[0], score[1] = char_x_temp, char_y_temp

            if is_maximizing and (score[2] > best[2]):
                    best = score
                    alpha = max(alpha, score[2])
                    if score[2] >= beta:
                        break
            elif not is_maximizing and (score[2] < best[2]):
                    best = score
                    beta = min(beta, best[2])
                    if score[2] <= alpha:
                        break

        return best

    def placeBombSittingDuck(self, wrld):
        if self.bomb_timer == 1:
            print("MOVING TO SITTING DUCK LOCATION")
            neigh = self.getNeighbors(wrld, self.char_x, self.char_y)
            if (self.char_x-1, self.char_y-1) in neigh:
                self.moveChar(wrld, -1, -1)
            else:
                self.moveChar(wrld, 1, -1)
        else:
            print("WAITING AT SITTING DUCK LOCATION : timer " + str(self.bomb_timer))
            self.moveChar(wrld, 0, 0)


    def moveSouth(self, wrld):
        neigh = self.getNeighbors(wrld, self.char_x, self.char_y)
        if (self.char_x, self.char_y+1) in neigh:
            self.moveChar(wrld, 0, 1)
            return False
        else:
            print("Wall Detected")
            return True


    def moveSouth2(self, wrld):
        # Simple BFS move to a southmost point
        q = [(self.char_x, self.char_y)]
        visited = []
        path = {}

        while q:
            cur = q.pop(0)
            visited.append(cur)
                
            for neigh in self.getNeighbors(wrld, cur[0], cur[1]):
                if neigh not in visited and neigh not in q:
                    q.append(neigh)
                    path[neigh] = cur

        # Find next movement
        south_most = (0,0)
        for v in visited:
            if v[1] > south_most[1]:
                south_most = v

        print("SOUTH MOST: "+str(south_most))
        if south_most[1] > self.char_y:
            tmp = south_most
            while path[tmp] != (self.char_x, self.char_y):
                tmp = path[tmp]
            return (tmp[0]-self.char_x, tmp[1]-self.char_y)
        else:
            return (0,0)