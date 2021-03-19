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

    # Run each time TestCharacter is run - ultimately makes bomberman move according to best heuristic
    #
    # PARAM [World] wrld: current world
    # RETURN [NONE]
    def do(self, wrld):
        print("\n\n")
        next_move = self.nextMoveHeuristic(wrld)

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

    # Calculate heuristic of current bomberman location, and all immediate neighbors, choosing the best 
    #
    # PARAM [World[]] wrld: current world
    # RETURN [tuple(int,int)]: (0,0) if the current bomberman location is somewhere a bomb should be placed.  Else returns a valid (x,y) movement direction for next best move.
    def nextMoveHeuristic(self, wrld):
        distance_to_exit = self.distanceToExit(wrld, self.char_x, self.char_y)
        distances_to_mon = self.distanceToMonsters(wrld, getCharacterLoc(wrld))
        closest_monster = 999

        best_option = ((0, 0), float('-inf'))
        for neigh in self.getNeighbors(wrld, self.char_x, self.char_y):
            h = self.calcHeuristic(wrld, neigh[0], neigh[1])
            print(neigh, h)
            if h > best_option[1]:
                best_option = (neigh, h)

        monster_info = (None, 999)
        for m in distances_to_mon:
            if m[1] < closest_monster:
                closest_monster = m[1]
                monster_info = m

        # Check to see if there is no path to exit
        if self.isSouthMost(wrld) and self.isObstructed(monster_info, distance_to_exit) and self.bomb_timer == 0 and closest_monster > 2:
            print("I AM SOUTHMOST")
            return (0,0)

        next_move = (best_option[0][0]-self.char_x, best_option[0][1]-self.char_y)

        return next_move

    # Find dangeous spots where bomb is blowing up
    #
    # PARAM [tuple(int, int)] bomb_loc: holds the (x,y) coordinate of the bomb that bomberman placed
    # RETURN [list(tuple(int, iny))]: list of (x,y) coordinates where the bomb is currently exploding and we should not move into to avoid certain death
    def calcPotentiallyExplosiveLocations(self, bomb_loc):
        bomb_r = 4
        danger_zones = [bomb_loc]

        for d in [(0,1), (1,0), (0,-1), (-1,0)]:
            for r in range(1, bomb_r+1):
                danger_zones.append( (bomb_loc[0]+r*d[0], bomb_loc[1]+r*d[1]) )

        return danger_zones

    # Calculate the heuristic  of the given (x, y) position
    #
    # PARAM [World] wrld: current world
    # PARAM [int] x: given x location on board
    # PARAM [int] y: given y location on board
    # RETURN [int]: heuristic of given (x,y) position by weighting and combining distance to monsters, distance to exit, and distance to walls
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
                    # print("Monster type: " + str(mtype))
                    if mtype == "stupid":
                        monst_hur += -1000/pow(closest_monster[1],3)
                    elif mtype != "stupid":
                        monst_hur += -1000/pow(closest_monster[1],2)

        # Make bomberman afriad of walls
        w = wrld.width()
        wall_hur = -1*pow(x-w/2, 2) + 2*w

        # Make Bomberman especially afraid of the walls the monster is near
        if closest_monster[0] != None:
            monster_x = closest_monster[0][0]
            monster_y = closest_monster[0][1]
            if monster_y > self.char_y & closest_monster[1] > 3:
                wall_hur += -1*pow((x-w/2)+(monster_x-w/2), 2) + 2*w


        # Heuristic driven from distance to exit
        # If there is a close monster between you and the exit, just evade
        d = self.distanceToExit(wrld, x, y)
        exit_hur = 0
        if d != -1 and d < wrld.width():
            if not self.isObstructed(closest_monster, d):
                exit_hur = 1000*(100-d)
            else:
                exit_hur = 5*y + (wrld.width() -2*d + pow(3, -1*(d-5.5)))
        else:
            # If there is no path to exit, make it drift south
            exit_hur = 5*y

        bomb_hur = 0
        if y > self.bomb_loc[1]:
            bomb_hur = -10

        # Sum all huristic values
        total = monst_hur + exit_hur + wall_hur + bomb_hur

        return total

    # Calculate a distance to the exit from given location
    #
    # PARAM [World] wrld: current world
    # PARAM [int] x: given x location on board
    # PARAM [int] y: given y location on board
    # RETURN [int]: distance to exit by BFS if exit found, else return -1 because no path to exit detected 
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

        return -1

    # Make a list of monster types / names at a given (x, y) location
    #
    # PARAM [World] wrld: current world
    # PARAM [int] x: given x location on board
    # PARAM [int] y: given y location on board
    # RETURN [list(str)]: list of monster names, ie "stupid", "aggressive", "selfpreserving" for each monster detected by bomberman
    def getMonsterName(self, wrld, x, y):
        if wrld.monsters_at(x, y) != None:
            names = []
            monsters = wrld.monsters_at(x, y)
            for m in monsters:
                names.append(m.name)
        else:
            print("ERROR: not a monster coordinate in getMonsterName()")
        return names

    # Calculate distance from character to monsters
    #
    # PARAM [World] wrld: current world
    # PARAM [tuple(int, int)]: location of bomberman as 
    # RETURN [list(tuples(monsterEntity, int))]: tuple of ((monster info), distance to monster) such that monster info is the found monster entity
    #                          and distance to monster is the calculated distance to monster by BFS
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

    # Determine if givne (x,y) coordinate is within world bounds
    #
    # PARAM [World] wrld: current world
    # PARAM [int] x: given x position
    # PARAM [int] y: given y position
    # RETURN [Boolean]: True if (x, y) coordinate is within world bounds, False otherwise
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

    # Function purpose
    #
    # PARAM type wrld, type name: here
    # RETURN type: here
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

    # Make bomberman move
    #
    # PARAM [World] wrld: current world
    # PARAM [int] dx: how to move bomberman in x direction/
    # PARAM [int] dy: how to move bomberman in y direction
    # RETURN [None]
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
        self.move(dx, dy)

    # Determine whether bomberman is at a "southern" point / a good position to place a bomb
    #
    # PARAM [World] wrld: current world
    # RETURN [bool]: True if bomberman is "southmost", ie, in a location where a bomb should be placed, else false
    def isSouthMost(self, wrld):
        neighbors = self.getNeighbors(wrld, self.char_x, self.char_y)
        for n in neighbors:
            # If a neighbor is seen and is more south, return false
            if n[1] > self.char_y:
                return False

            if self.char_x+1 < wrld.width() and self.char_x-1 > 0:
                if wrld.wall_at(self.char_x+1, self.char_y) and wrld.wall_at(self.char_x-1, self.char_y):
                    return True
            elif (not self.char_x+1 < wrld.width()) and wrld.wall_at(self.char_x-1, self.char_y):
                return True
            elif (not self.char_x-1 > 0) and wrld.wall_at(self.char_x+1, self.char_y):
                return True

        return True

    # Check to see if path to exit is obstructed by a wall or by a monster between bomberman and exit
    #
    # PARAM [tuple] monster_info: list of monsters present on map, None if no monsters detected
    # PARAM [int] distance_to_exit: distance to exit according to heuristic and BFS
    # RETURN [bool]: True if path is obstructed by monster or wall, else false
    def isObstructed(self, monster_info, distance_to_exit):
        if monster_info[0] is not None:
            monster_y = monster_info[0][1]
            # is the monster in our way?
            if self.char_y < monster_y or monster_info[1] < 2:
                return True
        if distance_to_exit == -1:
            return True
        
        return False
   
