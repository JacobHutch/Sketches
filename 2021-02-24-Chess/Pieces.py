class Piece:
    def __init__(self,grid,id):
        self.grid = grid
        self.id = id
        self.type = id[:-1]

    def __str__(self):
        return self.id

class Board:
    def __init__(self):
        self.colors = [[("white" if (x + y) % 2 == 0 else "black") for y in range(8)] for x in range(8)]
        self.grid = [[None for y in range(8)] for x in range(8)]

        for i in range(8):
            self.grid[i][1] = Piece(self.grid, "wp" + str(i+1))
            self.grid[i][6] = Piece(self.grid, "bp" + str(i+1))

        for i in range(2):
            self.grid[i * 7][0] = Piece(self.grid, "wr" + str(i+1))
            self.grid[(i * 5) + 1][0] = Piece(self.grid, "wh" + str(i+1))
            self.grid[(i * 3) + 2][0] = Piece(self.grid, "wb" + str(i+1))
            self.grid[i * 7][7] = Piece(self.grid, "br" + str(i+1))
            self.grid[(i * 5) + 1][7] = Piece(self.grid, "bh" + str(i+1))
            self.grid[(i * 3) + 2][7] = Piece(self.grid, "bb" + str(i+1))

        self.grid[4][0] = Piece(self.grid, "wq1")
        self.grid[3][0] = Piece(self.grid, "wk1")
        self.grid[4][7] = Piece(self.grid, "bq1")
        self.grid[3][7] = Piece(self.grid, "bk1")

        #Captured pieces, white then black
        self.grid.append([[],[]])



    def movePiece(self):
        pass



    def blit(self):
        ret = []
        for x in range(8):
            for y in range(8):
                if self.grid[x][y]:
                    ret.append([self.grid[x][y].type,x,y])
        return ret
