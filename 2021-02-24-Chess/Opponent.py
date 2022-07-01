import random as rand

class Opponent:
    def __init__(self,grid,playerCol):
        self.grid = grid
        if playerCol == "w":
            self.color = "b"
        else:
            self.color = "w"



    def move(self):
        piece = None
        plist = []
        for x in range(8):
            for y in range(8):
                p = self.grid[x][y]
                if (piece == None) and p:
                    if p.color == self.color:
                        piece = p
                elif p and (p.color == self.color):
                    if p.score > piece.score:
                        piece = p
                        plist = []
                    elif p.score == piece.score:
                        plist.append(p)
        if len(plist) > 0:
            plist.append(piece)
            piece = rand.choice(plist)
        piece.moveHighestScore()
