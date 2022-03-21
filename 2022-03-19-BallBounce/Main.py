import pygame

class App:
    def __init__(self,title,winSize):
        self.title = title
        self.winSize = winSize

        self.initPhys()
        self.startPygame()



    def initPhys(self):
        self.ballPos = [50,49]
        x,y = self.ballPos
        self.ballDis = [round(x),round(y)]
        self.ballVec = [5.3,7.4]
        self.ballRad = 10
        self.trail = []



    def tickPhys(self):
        cx,cy = self.ballPos
        vx,vy = self.ballVec
        fx = cx + vx
        fy = cy + vy
        nx = fx
        ny = fy

        if (fx - self.ballRad) < 0:
            nx = ((fx - self.ballRad) * -1) + self.ballRad
            self.ballVec = [vx * -1, vy]

        elif (fx + self.ballRad) > self.winSize[0]:
            nx = (2 * self.winSize[0]) - fx + (2 * self.ballRad)
            self.ballVec = [vx * -1, vy]

        if (fy - self.ballRad) < 0:
            ny = ((fy - self.ballRad) * -1) + self.ballRad
            self.ballVec = [vx, vy * -1]

        elif (fy + self.ballRad) > self.winSize[1]:
            ny = (2 * self.winSize[1]) - fy + (2 * self.ballRad)
            self.ballVec = [vx, vy * -1]

        self.trail.append(self.ballDis)
        self.ballLineD = [round(nx+(vx*3)), round(ny+(vy*3))]
        self.ballPos = [nx, ny]
        self.ballDis = [round(nx), round(ny)]



    def startPygame(self):
        self.window = pygame.display.set_mode(self.winSize)
        pygame.display.set_caption(self.title)
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

            self.tickPhys()

            self.window.fill((255,255,255))

            for t in self.trail:
                pygame.draw.circle(self.window,(0,0,0),t,0)
            pygame.draw.line(self.window,(0,0,0),self.ballDis,self.ballLineD,1)
            pygame.draw.circle(self.window,(0,127,127),self.ballDis,self.ballRad)

            pygame.display.flip()
            self.clock.tick(60)





kopts = {"title":"","winSize":(1000,800)}
app = App(**kopts)
