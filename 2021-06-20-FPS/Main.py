import pygame, math, time
import numpy as np

class App:
    def __init__(self,name="Pygame App",winSize=(500,500),tick=60):
        self.running = True
        self.clock = pygame.time.Clock()
        self.tick = tick

        self.lastX = 0
        self.lastY = 0

        #player scale is 1 (height), width is .5
        #mapScale is how large each cube of the map is compared to the player height
        #wallScale is how tall the walls are
        self.playerWidth = 0.5
        self.mapScale = 5
        self.wallScale = 2
        self.turnInc = math.pi / 12

        self.fov = 70
        self.displayPolys = []

        self.parseMap("Map1.txt")

        self.winSize = winSize
        pygame.init()
        self.window = pygame.display.set_mode(self.winSize, pygame.RESIZABLE)
        pygame.display.set_caption(name)
        self.resize(self.winSize)
        self.mainloop()



    def parseMap(self,filename):
        file = open(filename, "rt")
        self.map = []
        while True:
            line = file.readline()
            if not line:
                break
            line = list(line)
            line.pop()
            self.map.append(line)
        file.close()
        self.loadMap()



    def loadMap(self):
        #bottom positions, then top
        self.walls = []
        for x in range(8):
            for y in range(8):
                if self.map[x][y] == "w":
                    if (x < 7) and (self.map[x+1][y] == "w"):
                        self.walls.append(((x,y,0),(x+1,y,0),(x,y,self.wallScale),(x+1,y,self.wallScale)))
                    elif (y < 7) and (self.map[x][y+1] == "w"):
                        self.walls.append(((x,y,0),(x,y+1,0),(x,y,self.wallScale),(x,y+1,self.wallScale)))

                elif self.map[x][y] == "x":
                    self.cameraPos = [x,y,1]
                    self.cameraDir = [1,0,0]



    def distance(self,p1,p2):
        return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2) + ((p1[2] - p2[2]) ** 2))



    def magnitude(self,v1):
        sum = 0
        for i in v1:
            sum += (i ** 2)
        return math.sqrt(sum)



    def dot(self,v1,v2):
        sum = 0
        assert(len(v1) == len(v2))
        for i in range(len(v1)):
            sum += (v1[i] * v2[i])
        return sum



    def normalize(self,v1):
        normalVec = []
        mag = self.magnitude(v1)
        for v in v1:
            normalVec.append(v / mag)
        return normalVec



    def calcDisplay(self):
        for w in self.walls:
            drawWall = False
            for p in w:
                xdist = p[0] - self.cameraPos[0]
                ydist = p[1] - self.cameraPos[1]

                if (xdist > 0) and (ydist > 0):
                    quad = 0
                elif (xdist < 0) and (ydist > 0):
                    quad = 1
                elif (xdist < 0) and (ydist < 0):
                    quad = 2
                elif (xdist > 0) and (ydist < 0):
                    quad = 3

                angle = (abs(math.degrees(math.atan2(xdist,ydist))) + (90 * quad)) % 360

                if (angle > ((self.cameraDir[2] - (self.fov / 2)) % 360)) and (angle < ((self.cameraDir[2] + (self.fov / 2)) % 360)):
                    drawWall = True
                    break

            if drawWall:
                polys = []
                for p in w:
                    adj = self.distance(p,self.cameraPos)
                    opp = math.tan(self.fov / 2) * adj
                    polys.append(((opp*self.winSize[0]*.5)+self.xOffset,4+p[1]+self.yOffset))
                self.displayPolys.append(polys)




    def resize(self,winSize):
        print(winSize)
        self.padding = int(math.log(min(winSize),2))
        self.squareSize = (min(winSize) - self.padding) // 9
        self.xOffset = winSize[0] // 2
        self.yOffset = winSize[1] // 2



    def display(self):
        self.window.fill("black")
        #for d in self.displayPolys:
            #pygame.draw.polygon(self.window,"white",d)
        pygame.display.flip()



    def mainloop(self):
        while self.running:
            #keyboard processing
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if keys[pygame.K_r]:
                self.resize(self.window.get_size())

            if keys[pygame.K_a]:
                old = self.cameraDir[:2]
                self.cameraDir[0] = (old[0] * math.cos(self.turnInc)) - (old[1] * math.sin(self.turnInc))
                self.cameraDir[1] = (old[0] * math.sin(self.turnInc)) + (old[1] * math.cos(self.turnInc))
                print(self.cameraDir)
            if keys[pygame.K_d]:
                old = self.cameraDir[:2]
                self.cameraDir[0] = (old[0] * math.cos(-self.turnInc)) - (old[1] * math.sin(-self.turnInc))
                self.cameraDir[1] = (old[0] * math.sin(-self.turnInc)) + (old[1] * math.cos(-self.turnInc))
                print(self.cameraDir)

            #event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = event.pos

                if event.type == pygame.VIDEORESIZE:
                    self.winSize = [event.w,event.h]
                    self.resize(self.winSize)

            if not self.running:
                break

            x,y = pygame.mouse.get_pos()
            x = (x - self.xOffset) // self.squareSize
            y = (y - self.yOffset) // self.squareSize

            #self.calcDisplay()

            self.display()
            pygame.event.pump()
            self.clock.tick(self.tick)





kwargs = {"name":"FPS","winSize":(1000,800),"tick":60}

p = App(**kwargs)
