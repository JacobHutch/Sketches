import pygame

class App:
    def __init__(self,title,winSize):
        self.title = title
        self.winSize = winSize
        self.winX = winSize[0]
        self.winY = winSize[1]

        colors = [(255,63,63),(15,127,15),(15,63,127),(127,15,255),(255,127,15)]

        self.xHalf = self.winSize[0] // 2
        self.yHalf = self.winSize[1] // 2

        self.genSquare(colors)
        self.startPygame()



    def genSquare(self,colors):
        minWin = min(self.winSize[0],self.winSize[1])
        maxWin = max(self.winSize[0],self.winSize[1])
        padding = 2
        count = len(colors)
        squareSize = ((minWin // count) * count) - (padding * 2)
        realPad = (maxWin - squareSize + padding) // 2
        offset = squareSize // count
        angleOffset = 700

        tickSize = 10
        self.tickLines = []
        for i in range(0,count+1):
            x = int(offset * i) + realPad
            y1 = self.yHalf - tickSize
            y2 = self.yHalf + tickSize
            self.tickLines.append([(x,y1),(x,y2)])

        self.polygons = []
        #    x2--x3
        #   /    /
        #  x1--x4
        for i in range(count):
            x1 = (offset * i) - angleOffset + realPad
            x2 = (offset * i) + angleOffset + realPad
            x3 = (offset * (i + 1)) + angleOffset + realPad
            x4 = (offset * (i + 1)) - angleOffset + realPad

            y1 = padding
            y2 = squareSize - padding

            if (i == 0):
                x2 = x1#self.clamp(x1,realPad,self.winX-realPad)
            elif (i == (count - 1)):
                x4 = x3#self.clamp(x3,realPad,self.winX-realPad)

            points = [(x2,y1),(x3,y1),(x4,y2),(x1,y2)]
            for p in range(len(points)):
                x,y = points[p]
                xc = self.clamp(x,realPad,self.winX-realPad)
                if x > (self.winX-realPad):
                    if y == padding:
                        y += (x - xc)
                elif x < realPad:
                    if y == squareSize - padding:
                        y -= (xc - x)
                points[p] = (xc,y)

            polygon = [points,colors[i]]
            print(polygon)
            self.polygons.append(polygon)



    def clamp(self,num,mn,mx):
        test = min(mx,max(mn,num))
        return test



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

            self.window.fill((192,192,192))

            for p in self.polygons:
                pygame.draw.polygon(self.window,p[1],p[0])
                pygame.draw.line(self.window,(0,0,0),(0,self.yHalf),(self.winX,self.yHalf))
                pygame.draw.line(self.window,(0,0,0),(self.xHalf,0),(self.xHalf,self.winY))
                for l in self.tickLines:
                    pygame.draw.line(self.window,(0,0,0),l[0],l[1])
                pygame.draw.circle(self.window,(0,0,0),(self.xHalf,self.yHalf),3)

            pygame.display.flip()
            self.clock.tick(60)





kopts = {"title":"Paint","winSize":(1500,800)}
app = App(**kopts)
