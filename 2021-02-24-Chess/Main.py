import pygame, math
from Images import Images
from Pieces import Piece, Board

class App:
    def __init__(self,name="Pygame App",winSize=(500,500),tick=60):
        self.running = True
        self.clock = pygame.time.Clock()
        self.tick = tick

        self.colorModifier = ""
        self.colors = {}
        self.colors["bgColor"] = (64,64,128)
        self.colors["white"] = (255,230,180)
        self.colors["black"] = (32,32,32)
        self.colors["h-mouse"] = (255,255,255,0.4)
        self.colors["h-move"] = (255,255,0,0.5)
        self.colors["h-attack"] = (255,0,0,0.75)
        self.compositeColors()

        self.lastX = 0
        self.lastY = 0

        self.board = Board()

        pygame.init()
        self.window = pygame.display.set_mode(winSize, pygame.RESIZABLE)
        pygame.display.set_caption(name)
        self.images = Images(self.window)
        self.resize(winSize)
        self.mainloop()



    def compositeColors(self):
        wr,wg,wb = self.colors["white"]
        br,bg,bb = self.colors["black"]
        newColors = []
        for c in self.colors:
            if c[0:2] == "h-":
                r,g,b,a = self.colors[c]
                r = round((wr * (1 - a)) + (r * a))
                g = round((wg * (1 - a)) + (g * a))
                b = round((wb * (1 - a)) + (b * a))
                newColors.append(["white"+c[2:], (r,g,b)])

                r,g,b,a = self.colors[c]
                r = round((br * (1 - a)) + (r * a))
                g = round((bg * (1 - a)) + (g * a))
                b = round((bb * (1 - a)) + (b * a))
                newColors.append(["black"+c[2:], (r,g,b)])
        for c in newColors:
            self.colors[c[0]] = c[1]



    def resize(self,winSize):
        self.padding = int(math.log(min(winSize),2))
        self.squareSize = (min(winSize) - self.padding) // 8
        self.xOffset = (winSize[0] - (self.squareSize * 8)) // 2
        self.yOffset = (winSize[1] - (self.squareSize * 8)) // 2
        self.images.updateSize(self.squareSize,self.xOffset,self.yOffset)



    def display(self):
        self.window.fill(self.colors["bgColor"])
        for x in range(8):
            for y in range(8):
                rect = ((x * self.squareSize) + self.xOffset, (y * self.squareSize) + self.yOffset,
                    self.squareSize, self.squareSize)
                pygame.draw.rect(self.window,self.colors[self.board.colors[x][y]],rect)
        self.images.blit(self.board.blit())



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
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = event.pos
                    print((x - self.xOffset) // self.squareSize, (y - self.yOffset) // self.squareSize)

                if event.type == pygame.VIDEORESIZE:
                    self.resize(self.window.get_size())

            if not self.running:
                break

            x,y = pygame.mouse.get_pos()
            x = (x - self.xOffset) // self.squareSize
            y = (y - self.yOffset) // self.squareSize
            if (x >= 0) and (x <= 7) and (y >= 0) and (y <= 7):
                self.board.colors[self.lastX][self.lastY] = self.board.colors[self.lastX][self.lastY][0:5]
                self.board.colors[x][y] += "mouse"
                self.lastX = x
                self.lastY = y
            else:
                self.board.colors[self.lastX][self.lastY] = self.board.colors[self.lastX][self.lastY][0:5]

            self.display()
            pygame.display.flip()
            pygame.event.pump()
            self.clock.tick(self.tick)





kwargs = {"name":"Chess","winSize":(1000,800),"tick":60}

p = App(**kwargs)
