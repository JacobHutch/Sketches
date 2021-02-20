import math
import random
import pygame

class SymbolMaker:
    def __init__(self,winSize,letterWidth=3,letterHeight=6):
        self.winSize = winSize
        self.letterWidth = letterWidth
        self.letterHeight = letterHeight
        self.letterSize = self.letterWidth * self.letterHeight
        self.nodes = []
        self.letter = []
        if max(self.letterWidth,self.letterHeight) == self.letterWidth:
            self.xOffset = 1
            self.yOffset = (self.letterWidth - self.letterHeight + 2) / 2
        else:
            self.xOffset = (self.letterHeight - self.letterWidth + 2) / 2
            self.yOffset = 1
        self.edgeLength = min(winSize) / (max(self.letterWidth,self.letterHeight) + 1)

    def genLetter(self):
        nodeAmt = random.randint(1,self.letterSize-1)
        nodesChoice = []
        for i in range(nodeAmt):
            node = random.randint(0,self.letterSize-1)
            while node in nodesChoice:
                node = random.randint(0,self.letterSize-1)
            nodesChoice.append(node)

        letterNodes = [0 for i in range(self.letterSize)]
        for i in range(self.letterSize):
            if i in nodesChoice:
                letterNodes[i] = 1
        letter = []
        nodes = []
        for i in range(self.letterSize):
            nodes.append(self.positionCalc(i))
            for j in range(i+1,self.letterSize):
                if letterNodes[i] == 1 and letterNodes[j] == 1:
                    if (i%self.letterWidth == j%self.letterWidth) or (i//self.letterWidth == j//self.letterWidth):
                        letter.append((self.positionCalc(i),self.positionCalc(j)))
        self.nodes = nodes
        self.letter = letter

    def positionCalc(self,a):
        return (((a % self.letterWidth) + self.xOffset) * self.edgeLength, ((a // self.letterWidth) + self.yOffset) * self.edgeLength)

    def getNodes(self):
        return self.nodes

    def getSymbol(self):
        return self.letter

class App:
    def __init__(self,symbolOps,winSize=(500,500)):
        self.running = True
        self.drawVerts = False
        self.drawEdges = True
        self.clock = pygame.time.Clock()
        self.maker = SymbolMaker(winSize,**symbolOps)
        pygame.init()
        self.window = pygame.display.set_mode(winSize)
        self.mainloop()

    def mainloop(self):
        while self.running:
            #keyboard processing
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if keys[pygame.K_n]:
                self.maker.genLetter()
            if keys[pygame.K_v]:
                self.drawVerts = not self.drawVerts
            if keys[pygame.K_e]:
                self.drawEdges = not self.drawEdges

            #event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False

            if not self.running:
                break

            self.window.fill("white")

            if self.drawEdges:
                for line in self.maker.getSymbol():
                    pygame.draw.line(self.window,(0,0,0),*line)

            if self.drawVerts:
                for node in self.maker.getNodes():
                    pygame.draw.circle(self.window,(0,0,0),node,3)

            pygame.display.flip()
            self.clock.tick(10)

symbolOps = {"letterWidth":12,"letterHeight":6}
appOps = {"winSize":(1000,1000)}

a = App(symbolOps,**appOps)
