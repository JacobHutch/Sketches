import random as rand
class Piece:
    def __init__(self,grid,id):
        self.grid = grid
        self.id = id
        self.color = id[0]
        if self.color == "w":
            self.forward = 1
        else:
            self.forward = -1
        self.type = id[1]
        self.number = int(id[2])
        self.numMoves = 0
        self.moves = []
        self.attacks = []
        self.special = []
        self.dangers = []

        self.score = 0
        self.highestScoreMove = [0,0]
        self.values = {"p":1, "r":2, "h":3, "b":4, "q":5, "k":6}



    def __str__(self):
        return "Piece " + self.id



    def initPos(self):
        for i,a in enumerate(self.grid):
            for j,b in enumerate(a):
                if self.grid[i][j] == self:
                    self.pos = [i,j]
                    break
        self.findMoves()
        self.communicateDangers()



    # Left to implement:
    # Pawn: en passant
    # Rook: castle
    # Knight: Done
    # Bishop: Done
    # Queen: Done
    # King: check, castle
    #
    # As a side note, this feels like a terribly inefficient way to implement
    # some of these movements, so it might change later (especially if the
    # AI is slow because of it)
    def findMoves(self):
        self.moves = []
        self.attacks = []
        self.special = []
        self.dangers = []
        x,y = self.pos
        if self.type == "p":
            if (y + self.forward >= 0) and (y + self.forward < 8):
                #movement
                if (self.grid[x][y + self.forward] == None):
                    self.moves.append([x, y + self.forward])
                    if (self.numMoves == 0) and (self.grid[x][y + (2 * self.forward)] == None):
                        self.moves.append([x, y + (2 * self.forward)])

                #attack
                if (x+1 < 8) and (self.grid[x+1][y+self.forward]):
                    self.findAttack([x + 1, y + self.forward])
                if (x-1 >= 0) and (self.grid[x-1][y+self.forward]):
                    self.findAttack([x - 1, y + self.forward])

                #promotion
                if ((y == 1) and (self.forward == -1)):
                    self.special.append([x,0])
                    if (x+1 < 8):
                        self.special.append([x+1,0])
                    if (x-1 >= 0):
                        self.special.append([x-1,0])
                if ((y == 6) and (self.forward == 1)):
                    self.special.append([x,7])
                    if (x+1 < 8):
                        self.special.append([x+1,7])
                    if (x-1 >= 0):
                        self.special.append([x-1,7])

        elif (self.type == "r"):
            for i in range(x+1,8):
                if self.grid[i][y] == None:
                    self.moves.append([i,y])
                else:
                    self.findAttack([i,y])
                    break

            for i in range(x-1,-1,-1):
                if self.grid[i][y] == None:
                    self.moves.append([i,y])
                else:
                    self.findAttack([i,y])
                    break

            for i in range(y+1,8):
                if self.grid[x][i] == None:
                    self.moves.append([x,i])
                else:
                    self.findAttack([x,i])
                    break

            for i in range(y-1,-1,-1):
                if self.grid[x][i] == None:
                    self.moves.append([x,i])
                else:
                    self.findAttack([x,i])
                    break

        elif self.type == "h":
            moves = [(x+1,y+2),(x+1,y-2),(x-1,y+2),(x-1,y-2),(x+2,y+1),(x+2,y-1),(x-2,y+1),(x-2,y-1)]
            for m in moves:
                if (m[0] >= 0) and (m[0] < 8) and (m[1] >= 0) and (m[1] < 8):
                    if self.grid[m[0]][m[1]] == None:
                        self.moves.append([m[0],m[1]])
                    else:
                        self.findAttack([m[0],m[1]])

        elif self.type == "b":
            for i in range(x+1,8):
                if (y+i-x) < 8:
                    if self.grid[i][y+i-x] == None:
                        self.moves.append([i,y+i-x]);
                    else:
                        self.findAttack([i,y+i-x])
                        break

            for i in range(x-1,-1,-1):
                if (y+i-x) >= 0:
                    if self.grid[i][y+i-x] == None:
                        self.moves.append([i,y+i-x]);
                    else:
                        self.findAttack([i,y+i-x])
                        break

            for i in range(x+1,8):
                if (y-i+x) >= 0:
                    if self.grid[i][y-i+x] == None:
                        self.moves.append([i,y-i+x]);
                    else:
                        self.findAttack([i,y-i+x])
                        break

            for i in range(x-1,-1,-1):
                if (y-i+x) < 8:
                    if self.grid[i][y-i+x] == None:
                        self.moves.append([i,y-i+x]);
                    else:
                        self.findAttack([i,y-i+x])
                        break

        elif self.type == "q":
            for i in range(x+1,8):
                if self.grid[i][y] == None:
                    self.moves.append([i,y])
                else:
                    self.findAttack([i,y])
                    break

            for i in range(x-1,-1,-1):
                if self.grid[i][y] == None:
                    self.moves.append([i,y])
                else:
                    self.findAttack([i,y])
                    break

            for i in range(y+1,8):
                if self.grid[x][i] == None:
                    self.moves.append([x,i])
                else:
                    self.findAttack([x,i])
                    break

            for i in range(y-1,-1,-1):
                if self.grid[x][i] == None:
                    self.moves.append([x,i])
                else:
                    self.findAttack([x,i])
                    break

            for i in range(x+1,8):
                if (y+i-x) < 8:
                    if self.grid[i][y+i-x] == None:
                        self.moves.append([i,y+i-x]);
                    else:
                        self.findAttack([i,y+i-x])
                        break

            for i in range(x-1,-1,-1):
                if (y+i-x) >= 0:
                    if self.grid[i][y+i-x] == None:
                        self.moves.append([i,y+i-x]);
                    else:
                        self.findAttack([i,y+i-x])
                        break

            for i in range(x+1,8):
                if (y-i+x) >= 0:
                    if self.grid[i][y-i+x] == None:
                        self.moves.append([i,y-i+x]);
                    else:
                        self.findAttack([i,y-i+x])
                        break

            for i in range(x-1,-1,-1):
                if (y-i+x) < 8:
                    if self.grid[i][y-i+x] == None:
                        self.moves.append([i,y-i+x]);
                    else:
                        self.findAttack([i,y-i+x])
                        break

        elif self.type == "k":
            moves = [(x+1,y+1),(x+1,y),(x+1,y-1),(x,y-1),(x-1,y-1),(x-1,y),(x-1,y+1),(x,y+1)]
            for m in moves:
                if (m[0] >= 0) and (m[0] < 8) and (m[1] >= 0) and (m[1] < 8):
                    if self.grid[m[0]][m[1]] == None:
                        self.moves.append([m[0],m[1]])
                    else:
                        self.findAttack([m[0],m[1]])


        self.communicateDangers()


    def findAttack(self,pos):
        x,y = pos
        if self.grid[x][y].color != self.color:
            self.attacks.append(pos)
            self.moves.append(pos)



    # It's much faster (and more chivalrous) for each piece to tell others that
    # it's attacking them, rather than have every piece look for attackers.
    def communicateDangers(self):
        for a in self.attacks:
            x,y = a
            self.grid[x][y].dangers.append(self.pos)



    def move(self,newpos):
        x,y = newpos
        self.grid[self.pos[0]][self.pos[1]] = None
        if self.grid[x][y]:
            self.attack(newpos)
        if newpos in self.special:
            if self.type == "p":
                self.type = "q"
                self.id = self.color + self.type + str(self.number)
        self.grid[x][y] = self
        self.pos = newpos
        self.numMoves += 1



    def attack(self,pos):
        x,y = pos
        if self.grid[x][y].color == "w":
            self.grid[8][0].append(self.grid[x][y])
        else:
            self.grid[8][1].append(self.grid[x][y])



    def findHighestScore(self):
        self.score = 0
        tempScore = 0

        for a in self.attacks:
            x,y = a
            tempScore = self.values[self.grid[x][y].type] + 1
            if tempScore > self.score:
                self.score = tempScore
                self.highestScoreMove = a

        if (self.score == 0) and (len(self.moves) > 0):
            self.score = 1
            self.highestScoreMove = rand.choice(self.moves)



    def moveHighestScore(self):
        self.move(self.highestScoreMove)
