import pygame, math

class App:
    def __init__(self,title,winSize,baseColor,colorCount):
        self.title = title
        self.winSize = winSize
        self.winX = winSize[0]
        self.winY = winSize[1]
        self.baseColor = baseColor
        self.colorCount = colorCount

        self.xHalf = self.winSize[0] // 2
        self.yHalf = self.winSize[1] // 2
        self.center = (self.xHalf,self.yHalf)
        self.maxRadius = 300
        self.arcLen = 2 * math.pi / self.colorCount
        self.arcOffset = -(math.pi / 2)

        self.colors = self.calculateColors()
        self.circles = self.genCircles()
        self.startPygame()



    def calculateColors(self):
        colors = []
        colors.append(self.baseColor)

        r,g,b = self.baseColor
        luminosity = max(r,g,b)
        self.saturation = (max(r,g,b) - min(r,g,b))/255
        self.radius = self.maxRadius * self.saturation

        for i in range(1,self.colorCount):
            pass
        return colors



    def rgbToHue(self,color):
        hue = 0.0
        rf = color[0] / 255
        gf = color[1] / 255
        bf = color[2] / 255

        maxC = max(rf,gf,bf)

        return hue



    def hueToRgb(self,hue):
        color = (0,0,0)
        return color



    def genCircles(self):
        circles = []
        for i in range(0,self.colorCount):
            x = self.radius * math.cos((self.arcLen * i) + self.arcOffset)
            y = self.radius * math.sin((self.arcLen * i) + self.arcOffset)

            x += self.xHalf
            y += self.yHalf

            circles.append((x,y))
        return circles



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

            for i in range(self.colorCount):
                pygame.draw.circle(self.window,(0,0,0),self.circles[i],30)

            pygame.display.flip()
            self.clock.tick(60)





kopts = {"title":"Colors","winSize":(1500,800),"baseColor":(0,255,255),"colorCount":7}
app = App(**kopts)
