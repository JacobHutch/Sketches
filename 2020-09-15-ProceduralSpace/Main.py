import pygame
import sys
sys.path.append("../Shared/Python")
from Frame import App
from System import System

class App:
    def __init__(self,name="Procedural System",winSize=(500,500),tick=60):
        self.running = True
        self.clock = pygame.time.Clock()
        self.tick = tick

        self.__xdis = winSize[0]//2
        self.__ydis = winSize[1]//2
        self.__zoomScale = 0.5
        self.__zoomStep = 1.1
        self.__system = System(50,90)

        pygame.init()
        self.window = pygame.display.set_mode(winSize)
        self.mainloop()

    def mainloop(self):
        while self.running:
            #keyboard processing
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            if keys[pygame.K_i]:
                self.__zoomScale = min(self.__zoomScale * self.__zoomStep, 1)
            if keys[pygame.K_o]:
                self.__zoomScale = max(self.__zoomScale / self.__zoomStep, 0.01)

            #event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False

            #not sure if redundant
            if not self.running:
                break

            self.window.fill("black")

            #draw
            self.__system.nextFrame()
            self.display()

            pygame.display.flip()
            pygame.event.pump()
            self.clock.tick(self.tick)

    def display(self):
        for b in self.__system.getBodies():
            d = b.getData()
            pygame.draw.circle(self.window,d[5],((d[2][0] * self.__zoomScale) + self.__xdis,(d[2][1] * self.__zoomScale) + self.__ydis),d[1] * self.__zoomScale)


kwargs = {"name":"Testing","winSize":(1000,800),"tick":60}

p = App(**kwargs)
