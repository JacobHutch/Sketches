import math
import random
import pygame

class Triangle:
    def __init__(self,winSize):
        x,y = winSize
        self.points = [[400,150],[250,700],[800,800]]
        self.angles = [0,0,0]
        self.bisectorPoints = [None,None,None]
        self.sideSlopes = [0,0,0]
        self.perpBisectorPoints = [None,None,None]
        self.altitudes = [None,None,None]
        self.update()

    def distance(self,p1,p2):
        return (((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)) ** 0.5

    def magnitude(self, vec):
        return ((vec[0] ** 2) + (vec[1] ** 2)) ** 0.5

    def getInfo(self):
        return [self.points,self.bisectorPoints,self.centroid,self.perpBisectorPoints,self.circumcenter,self.altitudes,self.orthocenter]

    def update(self):
        self.findAngles()
        self.findLineBisectorPoints()
        self.findSideSlopes()
        self.findPerpBisectorPoints()
        self.findAltitudes()

    def findAngles(self):
        for i in range(3):
            self.angles[i] = math.degrees(math.acos(((self.distance(self.points[i],self.points[i-1]) ** 2) + (self.distance(self.points[i],self.points[i-2]) ** 2) - (self.distance(self.points[i-1],self.points[i-2]) ** 2)) /
                (2 * self.distance(self.points[i],self.points[i-1]) * self.distance(self.points[i],self.points[i-2]))))

    def findLineBisectorPoints(self):
        for i in range(3):
            self.bisectorPoints[i] = ((self.points[i][0] + self.points[i-1][0]) / 2, (self.points[i][1] + self.points[i-1][1]) / 2)
        self.centroid = (self.bisectorPoints[2][0] + ((self.points[0][0] - self.bisectorPoints[2][0]) / 3),
                        self.bisectorPoints[2][1] + ((self.points[0][1] - self.bisectorPoints[2][1]) / 3))

    def findSideSlopes(self):
        for i in range(3):
            if self.points[i][0] != self.points[i-1][0]:
                self.sideSlopes[i] = (self.points[i][1] - self.points[i-1][1]) / (self.points[i][0] - self.points[i-1][0])
            else:
                if self.points[i][1] > self.points[i-1][1]:
                    self.sideSlopes[i] = math.inf
                else:
                    self.sideSlopes[i] = -math.inf

    def findPerpBisectorPoints(self):
        for i in range(3):
            if (self.sideSlopes[i] == math.inf) or (self.sideSlopes[i] == -math.inf):
                m = 0
                self.perpBisectorPoints[i] = None
            elif self.sideSlopes[i] == 0:
                m = math.inf
                self.perpBisectorPoints[i] = None
            else:
                self.perpBisectorPoints[i] = None
        self.circumcenter = (0,0)

    def findAltitudes(self):
        for i in range(3):
            if (self.sideSlopes[i] == math.inf) or (self.sideSlopes[i] == -math.inf):
                m = 0
                self.perpBisectorPoints[i] = None
            elif self.sideSlopes[i] == 0:
                m = math.inf
                self.perpBisectorPoints[i] = None
            else:
                self.perpBisectorPoints[i] = None
        self.orthocenter = (0,0)

class App:
    def __init__(self,winSize=(500,500)):
        self.running = True
        self.clock = pygame.time.Clock()
        self.triangle = Triangle(winSize)
        self.drag = None
        pygame.init()
        self.window = pygame.display.set_mode(winSize)
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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (self.distance(event.pos,self.triangle.points[0]) < 15):
                        self.drag = "A"
                    elif (self.distance(event.pos,self.triangle.points[1]) < 15):
                        self.drag = "B"
                    elif (self.distance(event.pos,self.triangle.points[2]) < 15):
                        self.drag = "C"

                if self.drag != None:
                    if self.drag == "A":
                        self.triangle.points[0] = pygame.mouse.get_pos()
                    elif self.drag == "B":
                        self.triangle.points[1] = pygame.mouse.get_pos()
                    elif self.drag == "C":
                        self.triangle.points[2] = pygame.mouse.get_pos()
                    self.triangle.update()

                if event.type == pygame.MOUSEBUTTONUP:
                    self.drag = None

            if not self.running:
                break

            self.window.fill((255,255,255))

            info = self.triangle.getInfo()
            main = info[0]
            bisectorPoints = info[1]
            centroid = info[2]
            perpBisectorPoints = info[3]
            circumcenter = info[4]
            altitudes = info[5]
            orthocenter = info[6]

            for i in range(3):
                pygame.draw.line(self.window,(255,127,0),bisectorPoints[i],main[i-2],1)

            for i in range(3):
                pygame.draw.line(self.window,(0,0,0),main[i],main[i-1],3)

            for i in range(3):
                pygame.draw.circle(self.window,(255,127,0),bisectorPoints[i],5,2)

            pygame.draw.circle(self.window,(255,127,0),centroid,5)
            pygame.draw.circle(self.window,(0,127,0),circumcenter,5)
            pygame.draw.circle(self.window,(0,0,255),orthocenter,5)

            for i in range(3):
                pygame.draw.circle(self.window,(0,0,0),main[i],10,3)

            pygame.display.flip()
            self.clock.tick(60)

    def distance(self,p1,p2):
        return (((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)) ** 0.5

appOps = {"winSize":(1000,1000)}

a = App(**appOps)
