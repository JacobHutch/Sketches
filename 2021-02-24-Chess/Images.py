import pygame

class Images:
    def __init__(self,surface):
        self.surface = surface
        self.imagesPrime = {}
        self.imagesPrime["wp"] = pygame.image.load("Icons/wp.png")
        self.imagesPrime["wr"] = pygame.image.load("Icons/wr.png")
        self.imagesPrime["wh"] = pygame.image.load("Icons/wh.png")
        self.imagesPrime["wb"] = pygame.image.load("Icons/wb.png")
        self.imagesPrime["wq"] = pygame.image.load("Icons/wq.png")
        self.imagesPrime["wk"] = pygame.image.load("Icons/wk.png")
        self.imagesPrime["bp"] = pygame.image.load("Icons/bp.png")
        self.imagesPrime["br"] = pygame.image.load("Icons/br.png")
        self.imagesPrime["bh"] = pygame.image.load("Icons/bh.png")
        self.imagesPrime["bb"] = pygame.image.load("Icons/bb.png")
        self.imagesPrime["bq"] = pygame.image.load("Icons/bq.png")
        self.imagesPrime["bk"] = pygame.image.load("Icons/bk.png")



    def updateSize(self,squareSize,xOff,yOff):
        self.images = self.imagesPrime.copy()
        self.squareSize = squareSize
        self.xOffset = xOff
        self.yOffset = yOff
        for i in self.images:
            self.images[i] = pygame.transform.scale(self.images[i], (self.squareSize,self.squareSize))



    def blit(self,coordinates):
        for c in coordinates:
            self.surface.blit(self.images[c[0]], ((c[1] * self.squareSize) + self.xOffset, (c[2] * self.squareSize) + self.yOffset))
