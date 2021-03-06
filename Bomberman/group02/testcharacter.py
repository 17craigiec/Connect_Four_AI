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

    def moveSouth2(self, wrld):
        # Simple BFS move to a south most point
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
        south_most = (0, 0)
        for v in visited:
            if v[1] > south_most[1]:
                south_most = v
        print("SOUTH MOST: " + str(south_most))
        if south_most[1] > self.char_y:
            tmp = south_most
            while path[tmp] != (self.char_x, self.char_y):
                tmp = path[tmp]
            return (tmp[0] - self.char_x, tmp[1] - self.char_y)
        else:
            return (0, 0)

    # def __ge__(self, other):
    #     if other > self:

    def findWalls(self, wrld):
        # Simple BFS to poll the walls
        walls = []
        q = [(self.char_x, self.char_y)]
        visited = []
        path = {}

        while q:
            current = q.pop(0)
            visited.append(current)
            # If cur holds a wall log its location
            if wrld.walls_at(current[0], current[1]) != None:
                dist = 1
                tmp = current
                while tmp != (self.char_x, self.char_y):
                    dist = dist + 1
                    tmp = path[tmp]
                walls.append(((current[0], current[1]), dist))

            # break early if both walls are found
            if len(walls) >= 4:
                return walls

            for neigh in self.getNeighbors(wrld, current[0], current[1]):
                if neigh not in visited and neigh not in q:
                    q.append(neigh)
                    path[neigh] = current

        return monsters

    def moveThruWall(self, wrld):
        # find all the walls based on current location
        walls = self.findWalls(wrld)
        # identify wall closest to exit - valid moveable point, lowest y val (south)
        wallToBomb = []
        for wall in walls:
            if walls[wall].y > wallToBomb[1]:
                wallToBomb = [wall.x, wall.y]
        # move to said wall
        self.move(wallToBomb[0], wallToBomb[1])
        # drop bomb against wall
        self.char.drop_bomb()
        # move diagonally while bomb explodes
        self.move(x - 1, y + 1)
        # wait for explosion - change to bomb time
        while wrld.explosion_at(self.char_x, self.char_y):
            # don't move
            wait
        # move back to bomb space
        self.move(x + 1, y - 1)
        nextMove = self.moveSouth2(wrld)
        self.move(nextMove[0], nextMove[1])
        return

    def moveThruWall2(self, wrld):
        # identify wall closest to exit - valid moveable point, lowest y val (south)
        moveToWall = self.moveSouth2(wrld)
        # move to said wall
        self.move(moveToWall[0], wallToWall[1])
        # drop bomb against wall
        self.char.drop_bomb()
        # move diagonally while bomb explodes
        self.move(x - 1, y + 1)
        # wait for explosion - change to bomb time
        while wrld.explosion_at(moveToWall[0], moveToWall[1]):
            # don't move
            wait
        # move back to bomb space
        self.move(x + 1, y - 1)
        return
