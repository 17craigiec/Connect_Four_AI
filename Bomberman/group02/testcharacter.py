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

    def do(self, wrld):
        # Your code here
        # print("I am Located at ("+str(self.char_x)+", "+str(self.char_y)+")")

        print("\n\n")
        # next_move = self.nextMoveToExit(wrld)
        next_move = self.nextMoveHeuristic(wrld)

        self.moveChar(wrld, next_move[0], next_move[1])
        print("Monsters Located at: "+str(self.locateMonsters(wrld)))
        print("distance to EXIT is: "+str(self.distanceToExit(wrld, self.char_x, self.char_y)))


    def nextMoveHeuristic(self, wlrd):
        best_option = ((0,0), -1)
        for neigh in self.getNeighbors(wlrd, self.char_x, self.char_y):
            h = self.calcHeuristic(wlrd, neigh[0], neigh[1])
            if h > best_option[1]:
                best_option = (neigh, h)

        return (best_option[0][0]-self.char_x, best_option[0][1]-self.char_y)


    def calcHeuristic(self, wrld, x, y):
        monsters = self.distanceToMonsters(wrld, x, y)
        if monsters:
            dist_from_monsters = 0
        else:
            dist_from_monsters = 1

        for m in monsters:
            dist_from_monsters += m[1]

        print(-20/dist_from_monsters)
        return (-10/dist_from_monsters)+(100-self.distanceToExit(wrld, x, y))


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
