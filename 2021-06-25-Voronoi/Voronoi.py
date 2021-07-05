import math
import random
import pygame

class App:
    def __init__(self,winSize=(500,500),pointCount=20):
        self.winSize = winSize
        self.pointCount = pointCount
        self.running = True
        self.clock = pygame.time.Clock()
        self.drag = None
        self.radii = 100
        self.closestPoint = [[None for y in range(self.winSize[1])] for x in range(self.winSize[0])]
        self.recentDrag = None
        self.selectedDistance = "true"

        self.distances = {"true":self.trueDistance,"manhattan":self.manhattanDistance,"test":self.testDistance}

        self.initPoints(self.pointCount)
        pygame.init()
        self.window = pygame.display.set_mode(self.winSize)
        self.pixels = pygame.PixelArray(self.window)
        self.mainloop()



    def initPoints(self,count):
        self.points = []
        self.colors = []
        for c in range(count):
            self.points.append([random.randint(0,self.winSize[0]),random.randint(0,self.winSize[1])])
            color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
            self.colors.append(color)



    def trueDistance(self,p1,p2):
        return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))



    def manhattanDistance(self,p1,p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])



    def testDistance(self,p1,p2):
        return (p1[0] % p2[0]) + (p1[1] % p2[1])



    def distance(self,p1,p2):
        return self.distances[self.selectedDistance](p1,p2)



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
                    for p in range(self.pointCount):
                        if (self.trueDistance(event.pos,self.points[p]) < 15):
                            self.drag = p
                            self.recentDrag = self.drag

                if self.drag != None:
                    self.points[self.drag] = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONUP:
                    self.drag = None

            if not self.running:
                break

            self.window.fill((255,255,255))

            '''for p in range(self.pointCount):
                pygame.draw.circle(self.window,self.colors[p],self.points[p],self.radii)'''

            for x in range(0,self.winSize[0],1):
                for y in range(0,self.winSize[1],2):
                    closest = 0
                    if self.closestPoint[x][y] == None:
                        for p in range(0,self.pointCount):
                            if self.distance((x,y),self.points[p]) < self.distance((x,y),self.points[closest]):
                                closest = p
                        self.closestPoint[x][y] = closest

                    elif self.closestPoint[x][y] == self.drag:
                        for p in range(1,self.pointCount):
                            if self.distance((x,y),self.points[p]) < self.distance((x,y),self.points[closest]):
                                closest = p
                        self.closestPoint[x][y] = closest

                    elif self.recentDrag:
                        if self.distance((x,y),self.points[self.recentDrag]) < self.distance((x,y),self.points[self.closestPoint[x][y]]):
                            closest = self.drag
                            self.closestPoint[x][y] = closest

                    self.pixels[x,y] = tuple(self.colors[self.closestPoint[x][y]])

            for p in self.points:
                pygame.draw.circle(self.window,"black",p,2)

            pygame.display.flip()
            self.clock.tick(60)

appOps = {"winSize":(250,250),"pointCount":20}

a = App(**appOps)
