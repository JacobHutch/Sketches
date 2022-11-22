import math, random, pygame, time
import multiprocessing as mp
from Creature import Creature
from Components import Slider

class App:
    def __init__(self,title="Default Title",winSize=(500,500)):
        self.winSize = winSize
        self.title = title

        self.queue = mp.Queue(1)

        self.num = 0
        self.cnum = 0
        self.timeStart = time.time_ns()
        self.timeRunning = 0
        self.sliderVal = [7]
        self.sliderStep = 9

        self.p = mp.Process(target=Creature,kwargs={"queue":self.queue})

        if __name__=="__main__":
            self.p.start()

            self.startPygame()



    def startPygame(self):
        pygame.init()

        pygame.display.set_caption(self.title)
        self.window = pygame.display.set_mode(self.winSize)
        self.running = True
        self.clock = pygame.time.Clock()
        self.headerFont = pygame.font.SysFont("Helvetica", 30, bold=True)
        self.textFont = pygame.font.SysFont("Helvetica", 25, italic=True)

        self.components = []
        self.sliderTest = Slider(self.window,self.sliderVal,(100,600),500,50,0,10,True,self.sliderStep)
        self.components.append(self.sliderTest)

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
                    self.p.kill()
                    pygame.quit()
                    self.running = False
                for c in self.components:
                    c.eventHandle(event)

            if not self.running:
                break

            if not self.queue.empty():
                self.cnum = self.queue.get_nowait()

            self.num += 1
            self.timeRunning = time.time_ns() - self.timeStart

            cHead = self.headerFont.render("Creature Ticks:",1,(0,0,0))
            gHead = self.headerFont.render("GUI Ticks:",1,(0,0,0))
            cVal = self.textFont.render(str(self.cnum),1,(0,0,0))
            gVal = self.textFont.render(str(self.num),1,(0,0,0))

            sHead = self.headerFont.render("Seconds:",1,(0,0,0))
            sVal = self.textFont.render(str(self.timeRunning // 1000000000),1,(0,0,0))

            slHead = self.headerFont.render("Slider Value:",1,(0,0,0))
            slVal = self.textFont.render("{:0.2f}".format(self.sliderVal[0]),1,(0,0,0))

            self.window.fill((255,255,255))

            self.window.blit(cHead,(0,0))
            self.window.blit(gHead,(250,0))
            self.window.blit(cVal,(50,35))
            self.window.blit(gVal,(300,35))

            self.window.blit(sHead,(450,0))
            self.window.blit(sVal,(500,35))

            self.window.blit(slHead,(300,500))
            self.window.blit(slVal,(350,535))

            self.sliderTest.draw()

            pygame.display.flip()
            self.clock.tick(60)

appOps = {"title":"","winSize":(1000,800)}

a = App(**appOps)
