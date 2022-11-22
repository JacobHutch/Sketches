import pygame, math, time
from Images import Images
from Board import Board
#from Pieces import Piece, Board

class App:
    def __init__(self,name="Pygame App",winSize=(500,500),tick=60):
        self.running = True
        self.clock = pygame.time.Clock()
        self.tick = tick

        self.compositeColors()

        #self.playerCol = "w"

        self.lastX = 0
        self.lastY = 0

        self.board = Board()

        pygame.display.init()
        self.window = pygame.display.set_mode(winSize, pygame.RESIZABLE)
        pygame.display.set_caption(name)
        self.images = Images(self.window)
        self.resize(winSize)
        self.mainloop()



    # ## I came back to this and this is weird
    # The color system might be kinda confusing, so it could be changed later.
    # colorPalette defines the base colors for the program; bgColor, white, and
    # black are self explanatory, highlight is the color of a square when the
    # mouse moves over it, and the rest (marked with "m-") are modifiers.
    #
    # compositeColors() creates the true color palette for the program, with
    # colors holding 2 * 2 * m, with m being the number of modifiers. See
    # parseColor() for details about referencing each color.
    def compositeColors(self):
        self.colorPalette = {}
        self.colorPalette["bgColor"] = (64,64,128)
        self.colorPalette["white"] = (255,230,180)
        self.colorPalette["black"] = (64,64,46)
        self.colorPalette["highlight"] = (255,255,255,0.35)
        self.colorPalette["m-none"] = (0,0,0,0.0)
        self.colorPalette["m-move"] = (0,128,255,0.5)
        self.colorPalette["m-attack"] = (255,0,0,0.75)
        self.colorPalette["m-special"] = (0,255,0,0.5)

        self.colors = []

        wr,wg,wb = self.colorPalette["white"]
        br,bg,bb = self.colorPalette["black"]
        hr,hg,hb,ha = self.colorPalette["highlight"]
        for c in self.colorPalette:
            if c[:2] == "m-":
                r,g,b,a = self.colorPalette[c]
                r = round((wr * (1 - a)) + (r * a))
                g = round((wg * (1 - a)) + (g * a))
                b = round((wb * (1 - a)) + (b * a))
                self.colors.append((r,g,b))

                r = round((r * (1 - ha)) + (hr * ha))
                g = round((g * (1 - ha)) + (hg * ha))
                b = round((b * (1 - ha)) + (hb * ha))
                self.colors.append((r,g,b))

                r,g,b,a = self.colorPalette[c]
                r = round((br * (1 - a)) + (r * a))
                g = round((bg * (1 - a)) + (g * a))
                b = round((bb * (1 - a)) + (b * a))
                self.colors.append((r,g,b))

                r = round((r * (1 - ha)) + (hr * ha))
                g = round((g * (1 - ha)) + (hg * ha))
                b = round((b * (1 - ha)) + (hb * ha))
                self.colors.append((r,g,b))
        '''for i,j in enumerate(self.colors):
            print(i,j)'''



    # In board, colors are stored as a list, shown here with ranges:
    # [0:1, 0:1, 0:(m-1)] where m stands for the number of color modifiers.
    # list[0] stands for whether or not the square is highlighted, list[1]
    # means white or black, and list[2] is which modifier is active.
    # combining these bitwise as shown below will create an index for the
    # correct color combination of the 3 values.
    def parseColor(self,colorData):
        return self.colors[(colorData[2] << 2) | (colorData[1] << 1) | colorData[0]]



    def getOffsetCoords(self,pos):
        x,y = pos
        return ((x - self.xOffset) // self.squareSize, (y - self.yOffset) // self.squareSize)



    def resize(self,winSize):
        print("Resize: " + str(winSize))
        self.padding = int(math.log(min(winSize),2))
        self.squareSize = (min(winSize) - self.padding) // 9
        self.xOffset = (winSize[0] - (self.squareSize * 8)) // 2
        self.yOffset = (winSize[1] - (self.squareSize * 9)) // 2
        self.images.updateSize(self.squareSize,self.xOffset,self.yOffset)



    def display(self):
        self.window.fill(self.colorPalette["bgColor"])
        for x in range(8):
            for y in range(8):
                rect = ((x * self.squareSize) + self.xOffset, (y * self.squareSize) + self.yOffset,
                    self.squareSize, self.squareSize)
                pygame.draw.rect(self.window,self.parseColor(self.board.colors[x][y]),rect)
        self.images.blit(self.board.blit())
        pygame.display.flip()



    def mainloop(self):
        while self.running:
            #keyboard processing
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if keys[pygame.K_r]:
                self.resize(self.window.get_size())

            #event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = self.getOffsetCoords(event.pos)
                    if (x >= 0) and (x <= 7) and (y >= 0) and (y <= 7):
                        if self.board.selectSquare([x,y]) == 1:
                            self.display()
                            time.sleep(0.5)
                            self.board.opponent.move()
                            self.board.updateMoves()

                if event.type == pygame.VIDEORESIZE:
                    self.resize([event.w,event.h])

            if not self.running:
                break

            x,y = self.getOffsetCoords(pygame.mouse.get_pos())
            if (x >= 0) and (x <= 7) and (y >= 0) and (y <= 7):
                self.board.colors[self.lastX][self.lastY][0] = 0
                if self.board.colors[x][y][0] == 0:
                    self.board.colors[x][y][0] = 1
                    self.lastX = x
                    self.lastY = y
            else:
                self.board.colors[self.lastX][self.lastY][0] = 0

            self.display()
            pygame.event.pump()
            self.clock.tick(self.tick)





kwargs = {"name":"Chess","winSize":(1000,800),"tick":60}

p = App(**kwargs)
