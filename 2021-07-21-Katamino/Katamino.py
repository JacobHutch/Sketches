import math, random, pygame
import numpy as np

class App:
    def __init__(self,winSize=(500,500),puzzleName="c5"):
        self.winSize = winSize
        self.puzzleInfo = list(puzzleName)
        self.puzzleInfo[1] = int("".join(self.puzzleInfo[1:]))

        self.board = np.ones(shape=(5,self.puzzleInfo[1]),dtype=int)
        self.pieceConfigs = np.zeros(shape=(8),dtype=int)

        self.operationsCounter = 0
        self.boardWidth = self.puzzleInfo[1]
        self.boardHeight = 5

        self.parseShapes()
        self.parsePuzzles()
        self.createLines()
        self.solveBrute()

        #self.startPygame()



    def parseShapes(self):
        self.shapes = {}
        shapeFile = open("shapes.txt","rt")
        shapeLine = shapeFile.readline()
        while shapeLine:
            shapeList = shapeLine.split(",")
            shapeName = shapeList.pop(0)
            shapeList[-1] = shapeList[-1][:-1]
            shape = []
            for i in range(0,len(shapeList)):
                sliced = list(shapeList[i])
                for j in range(0,len(sliced)):
                    sliced[j] = int(sliced[j])
                shape.append(sliced)
            self.shapes[shapeName] = np.array(shape)
            shapeLine = shapeFile.readline()
        shapeFile.close()



    def parsePuzzles(self):
        self.puzzles = []
        puzzleFile = open("puzzles.txt","rt")
        puzzleLine = puzzleFile.readline()
        while puzzleLine:
            puzzleRow = puzzleLine.split(" ")
            puzzleRow[-1] = puzzleRow[-1][:-1]
            self.puzzles.append(puzzleRow)
            puzzleLine = puzzleFile.readline()
        puzzleFile.close()
        row = min(max(ord(self.puzzleInfo[0])-97, 0), 6)
        col = min(max(self.boardWidth, 3), 8)
        self.puzzle = self.puzzles[row][:col]
        print("\n----------------\n\n--Puzzle--")
        print(self.puzzle)
        print("\n--Pieces--")
        for s in self.puzzle:
            print(s)
            print(self.shapes[s])
            print()
        print("----------------\n")



    def createLines(self):
        self.lines = []
        xPad = 10
        yPadTop = 10
        yPadBottom = 200
        xSquareSize = (self.winSize[0] - (2 * xPad)) // self.boardWidth
        ySquareSize = (self.winSize[1] - (yPadTop + yPadBottom)) // 5
        #squareSize = min(xSquareSize,ySquareSize) (relative size)
        squareSize = 80
        xPad = (self.winSize[0] - (squareSize * self.boardWidth)) // 2
        for x in range(self.boardWidth+1):
            self.lines.append((
                (xPad + (x * squareSize), yPadTop),
                (xPad + (x * squareSize), yPadTop + (5 * squareSize))
            ))

        for y in range(6):
            self.lines.append((
                (xPad, yPadTop + (y * squareSize)),
                (xPad + (self.boardWidth * squareSize), yPadTop + (y * squareSize))
            ))



    def solveBrute(self):
        self.solveBruteRots(0)
        print(self.operationsCounter)



    def solveBruteRots(self,index):
        if index < len(self.puzzle):
            for i in range(8):
                self.pieceConfigs[index] = i
                self.solveBruteRots(index+1)
        else:
            self.operationsCounter += 1
            self.solveBruteBoard(0)



    def solveBruteBoard(self,index):
        if index < len(self.puzzle):
            self.solveBruteBoard(index+1)
        else:
            for p in self.puzzle:
                shape = self.shapes[p]
                shapeWidth,shapeHeight = shape.shape
                maxX = self.boardWidth - shapeWidth + 1
                maxY = self.boardHeight - shapeHeight + 1
                for x in range(maxX):
                    for y in range(maxY):
                        for w in range(shapeWidth):
                            for h in range(shapeHeight):
                                if self.board[w+x,h+y] == 1:
                                    return




    def startPygame(self):
        self.window = pygame.display.set_mode(self.winSize)
        self.running = True
        self.clock = pygame.time.Clock()

        pygame.init()
        self.mainloop()



    def mainloop(self):
        while self.running:
            #keyboard processing
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            #event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False

            if not self.running:
                break

            self.window.fill((255,255,255))

            for l in self.lines:
                pygame.draw.line(self.window,(0,0,0),l[0],l[1])

            pygame.display.flip()
            self.clock.tick(60)

appOps = {"winSize":(1000,800),"puzzleName":"c3"}

a = App(**appOps)
