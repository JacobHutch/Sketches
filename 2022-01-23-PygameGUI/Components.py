import pygame
import numpy as np

class UF:
    def clamp(val,minv,maxv):
        return min(max(val,minv),maxv)

    def closest(val,points):
        ret = points[0]
        dist = abs(val - points[0])
        for p in points:
            newp = abs(val - p)
            if newp < dist:
                dist = newp
                ret = p
        return ret





class Slider:
    def __init__(self,surface,valRef,pos=(0,0),width=50,height=10,min=0,max=10,snap=False,step=1):
        self.surface = surface
        self.valRef = valRef
        self.val = valRef[0]
        self.width = width
        self.height = height
        self.min = min
        self.max = max
        self.snap = snap
        self.step = step
        self.stepLen = width / (self.step + 1)
        self.rpos = pos[0]-(height // 6)

        if snap:
            if step < 0:
                raise Exception("Step cannot be lower than 0!!")

        self.drag = False

        self.rectColor = (0,127,255)
        self.clickedColor = (0,95,220)
        self.currentColor = self.rectColor

        self.reposition(pos)
        self.move(self.rpos)



    def reposition(self,pos):
        self.pos = pos
        self.resize(self.width,self.height)



    def resize(self,width,height):
        self.width = width
        self.height = height
        self.rwidth = self.height // 3
        self.clampxmin = self.pos[0] - (self.height // 6)
        self.clampxmax = self.pos[0] + self.width - (self.height // 6)
        self.woffset = self.height // 6
        self.lineStart = (self.pos[0],self.pos[1]+(self.height//2))
        self.lineEnd = (self.pos[0]+self.width,self.pos[1]+(self.height//2))

        self.lines = []
        self.pad = self.height//12
        self.lineyStart = self.lineStart[1] + self.pad
        self.lineyEnd = self.lineEnd[1] - self.pad
        self.linePoints = np.linspace(self.pos[0],self.pos[0]+self.width,self.step+2)
        if self.stepLen < (self.height//3):
            points = np.concatenate((points[:1], points[-1:]))
        else:
            points = self.linePoints

        for i in points:
            start = (i,self.lineyStart)
            end = (i,self.lineyEnd)
            self.lines.append((start,end))



    def move(self,rpos):
        self.rpos = rpos
        self.rect = pygame.Rect(self.rpos,self.pos[1],self.rwidth,self.height)

        relx = self.rpos - self.clampxmin
        self.percent = relx / self.width
        if not self.snap:
            self.val = ((percent * (self.max - self.min)) + self.min)
            self.valRef[0] = self.val



    def drawLines(self):
        pygame.draw.line(self.surface,(0,0,0),self.lineStart,self.lineEnd)
        for l in self.lines:
            pygame.draw.line(self.surface,(0,0,0),l[0],l[1])



    def drawRect(self):
        pygame.draw.rect(self.surface,self.currentColor,self.rect)




    def draw(self):
        self.drawRect()
        self.drawLines()




    def eventHandle(self,event):
        if (event.type == pygame.MOUSEBUTTONDOWN) and self.rect.collidepoint(event.pos):
            self.currentColor = self.clickedColor
            self.drag = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.drag = False
            self.currentColor = self.rectColor
            if self.snap:
                self.move(UF.closest(self.rpos+self.woffset,self.linePoints)-self.woffset)
                self.val = ((self.percent * (self.max - self.min)) + self.min)
                self.valRef[0] = self.val

        if self.drag:
            x,y = pygame.mouse.get_pos()
            x -= self.woffset
            self.move(UF.clamp(x,self.clampxmin,self.clampxmax))





class TextBox:
    def __init__(self,initialText):
        pass





if __name__ == "__main__":
    print(UF.clamp(5,-6,7))
