import math, random, pygame, time
import multiprocessing as mp
from Ghost import Ghost

class App:
    #keep odd numbers for viewSize dims
    def __init__(self,title="Default Title",winSize=(500,500),worldSize=(32,32)):
        self.title = title
        self.winSize = winSize
        self.worldSize = worldSize
        self.leftDrag = False
        self.rightDrag = False

        self.processes = []

        self.ghostQueue = mp.Queue(1)
        self.ghostProcess = mp.Process(target=Ghost,kwargs={"queue":self.ghostQueue})
        self.processes.append(self.ghostProcess)

        mapping = input("Mapping mode? (t/f)").lower()
        if (mapping == "t") or (mapping == "true"):
            self.mapping = True
        else:
            self.mapping = False

        self.startPygame()



    def startPygame(self):
        if (self.mapping):
            self.initMap(self.mapping)
            self.initFunctions()
            self.mappingLoop()
        else:
            number = input("Map number? ")
            self.mapName = "Map" + number + ".txt"
            self.initMap(self.mapping)
            self.initFunctions()
            self.mainloop()



    def initFunctions(self):
        if __name__=="__main__":
            self.ghostProcess.start()

        pygame.init()

        pygame.display.set_caption(self.title)
        self.window = pygame.display.set_mode(self.winSize, pygame.RESIZABLE)
        self.running = True
        self.clock = pygame.time.Clock()



    def initMap(self,mode):
        if mode:
            self.worldCols = [[(255,255,255) for y in range(self.worldSize[1])] for x in range(self.worldSize[0])]
        else:
            self.loadMap(self.mapName)



    def createTiles(self,mapping):
        if mapping:
            pad = 1
        else:
            pad = 0
        self.tileSize = min(self.winSize[0]//self.worldSize[0], self.winSize[1]//self.worldSize[1])
        rectDims = (self.tileSize - (pad * 2),self.tileSize - (pad * 2))

        self.worldXHalf = self.worldSize[0] // 2
        self.worldYHalf = self.worldSize[1] // 2

        self.playerPos = [self.worldXHalf,self.worldYHalf]
        self.playerPadX = 4      #keep even numbers for playerPads
        self.playerPadY = 4
        self.playerCol = (255,255,255)
        self.playerDims = (self.tileSize-self.playerPadX,self.tileSize-self.playerPadY)

        self.winPadX = (self.winSize[0] - (self.tileSize * self.worldSize[0])) // 2
        self.winPadY = (self.winSize[1] - (self.tileSize * self.worldSize[1])) // 2

        self.tiles = []
        for x in range(self.worldSize[0]):
            row = []
            for y in range(self.worldSize[1]):
                rectX = (self.tileSize * x) + self.winPadX + pad
                rectY = (self.tileSize * y) + self.winPadY + pad
                row.append(pygame.Rect((rectX,rectY),rectDims))
            self.tiles.append(row)



    def updatePlayer(self):
        if self.playerPos[0] < self.worldXHalf:
            playerX = self.playerPos[0]
        elif (self.worldSize[0] - self.playerPos[0]) <= self.worldXHalf:
            playerX = self.worldSize[0] - (self.worldSize[0] - self.playerPos[0])
        else:
            playerX = self.worldXHalf

        if self.playerPos[1] < self.worldYHalf:
            playerY = self.playerPos[1]
        elif (self.worldSize[1] - self.playerPos[1]) <= self.worldYHalf:
            playerY = self.worldSize[1] - (self.worldSize[1] - self.playerPos[1])
        else:
            playerY = self.worldYHalf

        squareX = (self.tileSize * playerX) + (self.playerPadX // 2) + self.winPadX
        squareY = (self.tileSize * playerY) + (self.playerPadY // 2) + self.winPadY
        self.playerRect = pygame.Rect((squareX,squareY),self.playerDims)



    def resizeWindow(self,newSize):
        self.winSize = newSize
        self.createTiles(self.mapping)
        self.updatePlayer()



    def mainloop(self):
        while self.running:
            #keyboard processing
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            #event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    for p in self.processes:
                        p.kill()
                    pygame.quit()
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.playerPos[1] = UF.clamp(self.playerPos[1]-1,0,self.worldSize[1]-1)
                        self.updatePlayer()
                    elif event.key == pygame.K_DOWN:
                        self.playerPos[1] = UF.clamp(self.playerPos[1]+1,0,self.worldSize[1]-1)
                        self.updatePlayer()
                    elif event.key == pygame.K_LEFT:
                        self.playerPos[0] = UF.clamp(self.playerPos[0]-1,0,self.worldSize[0]-1)
                        self.updatePlayer()
                    elif event.key == pygame.K_RIGHT:
                        self.playerPos[0] = UF.clamp(self.playerPos[0]+1,0,self.worldSize[0]-1)
                        self.updatePlayer()

                elif event.type == pygame.VIDEORESIZE:
                    self.resizeWindow([event.w,event.h])

            if not self.running:
                break

            if self.ghostQueue.full():
                try:
                    self.ghostCols = self.ghostQueue.get_nowait()
                except:
                    pass

            self.window.fill((63,63,63))

            for x in range(self.worldSize[0]):
                for y in range(self.worldSize[1]):
                    wx = UF.clamp(x + self.playerPos[0] - self.worldXHalf, 0 + x, self.worldSize[0] - (self.worldSize[0] - x))
                    wy = UF.clamp(y + self.playerPos[1] - self.worldYHalf, 0 + y, self.worldSize[1] - (self.worldSize[1] - y))
                    pygame.draw.rect(self.window,self.worldCols[x][y],self.tiles[x][y])

            pygame.draw.rect(self.window,self.playerCol,self.playerRect)

            pygame.display.flip()
            self.clock.tick(60)



    #When printing worldCols, the map appears sideways because of how the coordinate system
    #in pygame translates to a 2D array; because of this, saving the map will "technically"
    #save it sideways, to allow for intuitive viewing/editing of the actual map file
    def saveMap(self):
        sig = True
        num = 1
        while sig:
            try:
                fstr = "Map" + str(num) + ".txt"
                file = open(fstr,"x")
                sig = False
            except:
                num += 1

        #logic for saving sideways: parent loop is y and nested is x, instead of the
        #normally used setup
        for y in range(self.worldSize[1]):
            lstr = ""
            for x in range(self.worldSize[0]):
                if self.worldCols[x][y] == ((255,255,255)):
                    lstr += "s"
                elif self.worldCols[x][y] == ((0,0,255)):
                    lstr += "w"
                elif self.worldCols[x][y] == ((0,127,0)):
                    lstr += "p"
                elif self.worldCols[x][y] == ((255,0,0)):
                    lstr += "g"
            file.write(lstr+"\n")

        file.close()



    #As mentioned in the saveMap function, the map is actually saved sideways, but
    #looks to be the correct orientation; because it's saved sideways, loadMap has
    #to flip the map back to it's original orientation
    def loadMap(self,map):
        try:
            file = open(map,"r")
        except:
            print("Error - cannot open file!!")
            quit()

        lines = []
        while True:
            line = file.readline()[:-1]
            if line == "":
                break
            lines.append(line)
        self.map = []
        self.worldCols = []

        #logic for loading is the same as for saving, just loop through y first
        for y in range(self.worldSize[1]):
            row = []
            colRow = []
            for x in range(self.worldSize[0]):
                val = lines[x][y]
                row.append(val)
                if val == "s":
                    colRow.append((255,255,255))
                elif val == "w":
                    colRow.append((0,0,255))
                elif val == "p":
                    colRow.append((0,127,0))
                elif val == "g":
                    colRow.append((255,0,0))

            self.map.append(row)
            self.worldCols.append(colRow)

        file.close()



    def setColorAtTile(self,color):
        x,y = pygame.mouse.get_pos()
        x = UF.clamp((x - self.winPadX) // self.tileSize, 0, self.worldSize[0] - 1)
        y = UF.clamp((y - self.winPadY) // self.tileSize, 0, self.worldSize[1] - 1)
        self.worldCols[x][y] = color



    def checkColorAtTile(self):
        x,y = pygame.mouse.get_pos()
        x = UF.clamp((x - self.winPadX) // self.tileSize, 0, self.worldSize[0] - 1)
        y = UF.clamp((y - self.winPadY) // self.tileSize, 0, self.worldSize[1] - 1)
        return self.worldCols[x][y]



    def mappingLoop(self):
        while self.running:
            #keyboard processing
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            #event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    for p in self.processes:
                        p.kill()
                    pygame.quit()
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.saveMap()
                    elif event.key == pygame.K_p:
                        if self.checkColorAtTile() == (0,127,0):
                            self.setColorAtTile((255,255,255))
                        else:
                            self.setColorAtTile((0,127,0))
                    elif event.key == pygame.K_g:
                        if self.checkColorAtTile() == (255,0,0):
                            self.setColorAtTile((255,255,255))
                        else:
                            self.setColorAtTile((255,0,0))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.leftDrag = True
                    elif event.button == 3:
                        self.rightDrag = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.leftDrag = False
                    elif event.button == 3:
                        self.rightDrag = False

                if self.leftDrag:
                    self.setColorAtTile((0,0,255))

                if self.rightDrag:
                    self.setColorAtTile((255,255,255))

                elif event.type == pygame.VIDEORESIZE:
                    self.resizeWindow([event.w,event.h])

            if not self.running:
                break

            self.window.fill((63,63,63))

            for x in range(self.worldSize[0]):
                for y in range(self.worldSize[1]):
                    pygame.draw.rect(self.window,self.worldCols[x][y],self.tiles[x][y])

            pygame.display.flip()
            self.clock.tick(60)





class UF:
    def clamp(val,minv,maxv):
        return min(max(val,minv),maxv)




if __name__ == "__main__":
    appOps = {"title":"PacMan","winSize":(1000,800),"worldSize":(20,20)}
    a = App(**appOps)
