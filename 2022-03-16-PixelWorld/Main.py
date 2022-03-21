import math, random, pygame, time
import multiprocessing as mp
from Creature import Creature
from World import World

class App:
    #keep odd numbers for viewSize dims
    def __init__(self,title="Default Title",winSize=(500,500),viewSize=(51,51),worldSize=(100,100)):
        self.title = title
        self.winSize = winSize
        self.viewSize = viewSize
        self.worldSize = worldSize

        self.processes = []

        self.worldQueue = mp.Queue(1)
        self.worldProcess = mp.Process(target=World,kwargs={"queue":self.worldQueue,"worldSize":worldSize})
        self.processes.append(self.worldProcess)

        self.world = World
        self.worldCols = [[(0,0,0) for y in range(worldSize[1])] for x in range(worldSize[0])]

        self.createTiles()
        self.updatePlayer()

        if __name__=="__main__":
            self.worldProcess.start()

            self.startPygame()



    def startPygame(self):
        pygame.init()

        pygame.display.set_caption(self.title)
        self.window = pygame.display.set_mode(self.winSize)
        self.running = True
        self.clock = pygame.time.Clock()

        self.mainloop()



    def createTiles(self):
        self.worldXHalf = self.worldSize[0] // 2
        self.worldYHalf = self.worldSize[1] // 2

        self.tileSize = min(self.winSize[0]//max(self.viewSize[0],self.worldSize[0]), self.winSize[1]//max(self.viewSize[1],self.worldSize[1]))
        rectDims = (self.tileSize,self.tileSize)

        self.viewXHalf = self.viewSize[0] // 2
        self.viewYHalf = self.viewSize[1] // 2

        self.playerPos = [min(self.viewXHalf,self.worldXHalf),min(self.viewYHalf,self.worldYHalf)]
        self.playerPadX = 4      #keep even numbers for playerPads
        self.playerPadY = 4
        self.playerCol = (255,255,255)
        self.playerDims = (self.tileSize-self.playerPadX,self.tileSize-self.playerPadY)

        self.winPadX = (self.winSize[0] - (self.tileSize * self.viewSize[0])) // 2
        self.winPadY = (self.winSize[1] - (self.tileSize * self.viewSize[1])) // 2

        self.tiles = []
        for x in range(self.viewSize[0]):
            row = []
            for y in range(self.viewSize[1]):
                rectX = (self.tileSize * x) + self.winPadX
                rectY = (self.tileSize * y) + self.winPadY
                row.append(pygame.Rect((rectX,rectY),rectDims))
            self.tiles.append(row)



    def updatePlayer(self):
        playerX = (self.tileSize * self.playerPos[0]) + (self.playerPadX // 2) + self.winPadX
        playerY = (self.tileSize * self.playerPos[1]) + (self.playerPadY // 2) + self.winPadY
        self.playerRect = pygame.Rect((playerX,playerY),self.playerDims)



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
                    elif event.key == pygame.K_DOWN:
                        self.playerPos[1] = UF.clamp(self.playerPos[1]+1,0,self.worldSize[1]-1)
                    elif event.key == pygame.K_LEFT:
                        self.playerPos[0] = UF.clamp(self.playerPos[0]-1,0,self.worldSize[0]-1)
                    elif event.key == pygame.K_RIGHT:
                        self.playerPos[0] = UF.clamp(self.playerPos[0]+1,0,self.worldSize[0]-1)
                    print(self.playerPos)

            if not self.running:
                break

            if self.worldQueue.full():
                try:
                    self.worldCols = self.worldQueue.get_nowait()
                except:
                    pass

            self.window.fill((63,63,63))

            for x in range(self.viewSize[0]):
                for y in range(self.viewSize[1]):
                    wx = UF.clamp(x + self.playerPos[0] - self.viewXHalf, 0, self.worldSize[0] - 1)
                    wy = UF.clamp(y + self.playerPos[1] - self.viewYHalf, 0, self.worldSize[1] - 1)
                    pygame.draw.rect(self.window,self.worldCols[wx][wy],self.tiles[x][y])

            pygame.draw.rect(self.window,self.playerCol,self.playerRect)

            pygame.display.flip()
            self.clock.tick(60)





class UF:
    def clamp(val,minv,maxv):
        return min(max(val,minv),maxv)





appOps = {"title":"Pixel World 2","winSize":(1000,800),"worldSize":(40,40),"viewSize":(75,75)}
a = App(**appOps)
