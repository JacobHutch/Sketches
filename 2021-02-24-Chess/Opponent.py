import random as rand
class Opponent:
    def __init__(self,grid,color):
        self.grid = grid
        if color == "w":
            self.color = "b"
        else:
            self.color = "w"

    def move(self):
        piece = None
        for x in range(8):
            for y in range(8):
                p = self.grid[x][y]
                if piece == None:
                    piece = p
                elif p and (p.color == self.color):
                    if p.score > piece.score:
                        piece = p
                    elif p.score == piece.score:
                        piece = rand.choice([piece, p])
        piece.moveHighestScore()
