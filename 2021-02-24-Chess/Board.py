from Pieces import Piece
from Opponent import Opponent

# Piece ids: string of 3 chars, "ct#"
# c is color, either 'w' or 'b'
# t is type, 'p' = pawn, 'r' = rook, 'h' = knight (horse), 'b' = bishop,
#   'q' = queen, 'k' = king
# # is the unique number for each piece, so while there will only be one king
#   per side, "wk1" and "bk1", there will be 8 pawns, "wp1"-"wp8"
class Board:
    def __init__(self):
        self.playerCol = "w"
        self.turn = "w"
        self.selected = None
        self.colors = [[([0,0,0] if (x + y) % 2 == 0 else [0,1,0]) for y in range(8)] for x in range(8)]
        self.grid = [[None for y in range(8)] for x in range(8)]

        self.opponent = Opponent(self.grid,self.playerCol)

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
        for x in self.grid:
            for y in x:
                if y:
                    y.initPos()



    def selectSquare(self,pos):
        ret = -1
        x,y = pos

        #if a piece is not currently selected
        if self.selected == None:
            #making sure a piece was clicked, and of the right color
            if self.grid[x][y] and (self.grid[x][y].color == self.turn):

                #select piece and highlight it, then
                #color the board with selected piece's movement options
                self.selected = self.grid[x][y]
                self.colors[x][y][2] = 1

                for m in self.selected.moves:
                    x,y = m
                    if m in self.selected.attacks:
                        self.colors[x][y][2] = 2
                    elif m in self.selected.special:
                        self.colors[x][y][2] = 3
                    else:
                        self.colors[x][y][2] = 1
                print("ding")

        #if a piece is currently selected
        else:
            #if piece clicked is the selected piece (deselection)
            if self.selected == self.grid[x][y]:
                self.colors[x][y][2] = 0
                for m in self.selected.moves:
                    x,y = m
                    self.colors[x][y][2] = 0
                self.selected = None
                print("dong")

            #if piece clicked is a valid move
            elif pos in self.selected.moves:
                x,y = self.selected.pos
                self.colors[x][y][2] = 0
                for m in self.selected.moves:
                    x,y = m
                    self.colors[x][y][2] = 0
                self.selected.move(pos)
                self.updateMoves()
                '''if self.turn == "w":
                    self.turn = "b"
                else:
                    self.turn = "w"'''
                self.selected = None
                print("bong")
                ret = 1

            else:
                print("invalid")

        return ret



    def updateMoves(self):
        for x in range(8):
            for y in range(8):
                if self.grid[x][y]:
                    self.grid[x][y].findMoves()

        for x in range(8):
            for y in range(8):
                if self.grid[x][y]:
                    self.grid[x][y].findHighestScore()



    def blit(self):
        ret = []
        for x in range(8):
            for y in range(8):
                if self.grid[x][y]:
                    ret.append([self.grid[x][y].id[:-1],x,y])
        return ret
