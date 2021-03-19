# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from sensed_world import SensedWorld

def getCharacterEntity(wrld):
    chars = next(iter(wrld.characters.values()))
    if len(chars):
        c = chars[0]
        return c
    return -1


def getCharacterLoc(wrld):
    chars = next(iter(wrld.characters.values()))
    if len(chars):
        c = chars[0]
        return (c.x, c.y)
    return -1

def getBomb(wrld):
    bombs = list(wrld.bombs.values())
    if len(bombs):
        b = bombs[0]
        return b
    return -1


class TestCharacter(CharacterEntity):

    char_x = 0
    char_y = 0
    
    bomb_timer = 0
    bomb_loc = (-1,-1)
    dangerous_locations = []

    # list of neighboring coordinates to walls, should be updated after bomb  -- NOT USED ANYMORE
    # cspace = []

    # Function run at the start of each move
    #
    # PARAM type wrld, type name: here
    # RETURN type: here
    def do(self, wrld):
        # Your code here

        print("\n\n")
        next_move = self.nextMoveHeuristic(wrld)

        ########### connor's bomb code 2 ##############
        # If no path to exit can be found aka next_move==(0,0), continue south untill a wall is encountered
        if next_move == (0,0) and self.bomb_timer == 0:
            self.place_bomb()
            self.bomb_loc = getCharacterLoc(wrld)
            self.dangerous_locations = self.calcPotentiallyExplosiveLocations(self.bomb_loc)
            # Start the timer
            self.bomb_timer += 1

        elif self.bomb_timer > 0:
            # This esle statement contains the instructions for bomberman when a bomb is placed
            self.bomb_timer += 1
            if self.bomb_timer > 14:
                print("RESETTING BOMB TIMER")
                self.bomb_timer = 0
                self.bomb_loc = (-1,-1)
                self.dangerous_locations = []

        self.moveChar(wrld, next_move[0], next_move[1])


    def nextMoveHeuristic(self, wrld):
        #if i'm too close to a monster, run minimax
        distances_to_mon = self.distanceToMonsters(wrld, getCharacterLoc(wrld))
        closest_monster = 999

        best_option = ((0, 0), float('-inf'))
        for neigh in self.getNeighbors(wrld, self.char_x, self.char_y):
            h = self.calcHeuristic(wrld, neigh[0], neigh[1])
            print(neigh, h)
            if h > best_option[1]:
                best_option = (neigh, h)

        for m in distances_to_mon:
            monTypes = self.getMonsterName(wrld, m[0][0], m[0][1])
            if m[1] < closest_monster:
                closest_monster = m[1]

            # for mtype in monTypes:
            #     if mtype == "stupid" and m[1] <= 3:
            #         print("Too close to stupid monster!!")
            #         best = self.ab_minimax(wrld, self.char_x, self.char_y, 2, True, float('-inf'), float('inf'))
            #         print("THE BEST OF THE BEST: "+str(best))
            #         best_option = (best, float('inf'))

            #     elif mtype != "stupid" and m[1] <= 5:
            #         print("Too close to smart monster!!!!")
            #         print("Monster info:" + str(m[0]))
            #         best = self.ab_minimax(wrld, self.char_x, self.char_y, 2, True, float('-inf'), float('inf'))
            #         print("THE BEST OF THE BEST: "+str(best))
            #         best_option = (best, float('inf'))


        # Check to see if there is no path to exit
        if self.isSouthMost(wrld) and self.bomb_timer == 0 and closest_monster > 2:
            print("I AM SOUTHMOST")
            return (0,0)

        next_move = (best_option[0][0]-self.char_x, best_option[0][1]-self.char_y)
        print(next_move)

        return next_move


    def calcPotentiallyExplosiveLocations(self, bomb_loc):
        bomb_r = 4
        danger_zones = [bomb_loc]

        for d in [(0,1), (1,0), (0,-1), (-1,0)]:
            for r in range(1, bomb_r+1):
                danger_zones.append( (bomb_loc[0]+r*d[0], bomb_loc[1]+r*d[1]) )

        return danger_zones


    def calcHeuristic(self, wrld, x, y):
        monsters = self.distanceToMonsters(wrld, (x, y))
        # This if statement is here to avoid div by 0
        if monsters:
            closest_monster = 0
        else:
            closest_monster = 1

        # Heuristic driven from closeness to monster and by type of monster
        monst_hur = 0
        closest_monster = (None, 999)
        for m in monsters:
            if m[1] < closest_monster[1]:
                closest_monster = m
                monTypes = self.getMonsterName(wrld, m[0][0], m[0][1])
                for mtype in monTypes:
                    if mtype == "stupid":
                        monst_hur += -600/pow(closest_monster[1],4)
                    elif mtype != "stupid":
                        monst_hur += -1000/pow(closest_monster[1],4)

        # Heuristic driven from closeness to monster
        # monst_hur = -1000/pow(closest_monster,4)


        # Heuristic driven from distance to exit
        # If there is a close monster between you and the exit, just evade
        d = self.distanceToExit(wrld, x, y)
        exit_hur = 0
        if d != -1 and d < wrld.width():
            exit_hur = 5*y + (wrld.width() -2*d + pow(3, -1*(d-5.5)))
        else:
            # If there is no path to exit, make it drift south
            exit_hur = 5*y

        # Make bomberman afriad of walls
        w = wrld.width()
        wall_hur = -1*pow(x-w/2, 2) + 2*w

        # Make Bomberman especially afraid of the walls the monster is near
        if closest_monster[0] != None:
            monster_x = closest_monster[0][0]
            monster_y = closest_monster[0][1]
            if monster_y > self.char_y & closest_monster[1] > 3:
                wall_hur += -1*pow((x-w/2)+(monster_x-w/2), 2) + 2*w

        bomb_hur = 0
        if y > self.bomb_loc[1]:
            bomb_hur = -10

        # Sum all huristic values
        total = monst_hur + exit_hur + wall_hur + bomb_hur

        # print("total: "+str(total)+"  monst: "+str(monst_hur)+"  exit: "+str(exit_hur)+"  wall: "+str(wall_hur)+"  bomb: "+str(bomb_hur))

        return total


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

        # print("!!! No path to EXIT detected !!!")
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


    def distanceToMonsters(self, wrld, loc):
        # Simple BFS to poll the monsters
        monsters = []
        q = [loc]
        visited = []
        path = {}

        while q:
            cur = q.pop(0)
            visited.append(cur)
            # If cur holds a monster log its location
            if wrld.monsters_at(cur[0], cur[1]) != None:
                dist = 1
                tmp = cur
                while tmp != loc:
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
        # Bounds check
        if x >= wrld.width() or x < 0:
            return False
        if y >= wrld.height() or y < 0:
            return False
        if wrld.wall_at(x, y):
            return False
        if self.bomb_timer >= 10:
            if (x, y) in self.dangerous_locations:
                return False
        if wrld.explosion_at(x, y):
            return False

        return True


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


    def ab_minimax(self, wrld, char_x, char_y, depth, is_maximizing, alpha, beta):
        # best is defined as [x, y, score/heuristic of state]
        if is_maximizing:
            best = [-1, -1, float('-inf')]  #might need to change this because this according to ref code is x, y --> we might need move in x, y not to a specific cell
        else:
            best = [-1, -1, float('inf')]

        # if (depth == 0) or (wrld.monsters_at(char_x, char_y) != None) or (wrld.exit_at(char_x, char_y)):
        if (depth == 0):
            score = self.calcHeuristic(wrld, char_x, char_y)  #get the heuristic of the board
            return [-1, -1, score]
        if wrld.monsters_at(char_x, char_y) != None:
            score = float('-inf')
            return [-1, -1, score]
        if wrld.exit_at(char_x, char_y):
            score = float('inf')
            return [-1, -1, score]

        for move in self.getNeighbors(wrld, char_x, char_y):
            char_x_temp = move[0]
            char_y_temp = move[1]

            temp_world = SensedWorld.from_world(wrld)
            # THIS BREAKS
            # temp_char = getCharacterEntity(temp_world)
            # print("TEMP_CHAR: "+str(temp_char))
            # if temp_char != -1:
            #     temp_char.move(char_x_temp, char_y_temp)

            # print("hello")
            (next_temp_wrld, temp_events) = temp_world.next()

            # #recursively call minimax on the next move as:
            score = self.ab_minimax(next_temp_wrld, char_x_temp, char_y_temp, depth-1, not is_maximizing, alpha, beta)

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

        print(best)
        return best


    def isSouthMost(self, wrld):
        neighbors = self.getNeighbors(wrld, self.char_x, self.char_y)
        for n in neighbors:
            # If a neighbor is seen and is more south, return false
            if n[1] > self.char_y:
                return False

            if self.char_x+1 < wrld.width() and self.char_x-1 > 0:
                if wrld.wall_at(self.char_x+1, self.char_y) and wrld.wall_at(self.char_x-1, self.char_y):
                    return True

        return True
   
