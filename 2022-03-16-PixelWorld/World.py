import random

class World:
    def __init__(self,queue,worldSize):
        self.queue = queue
        self.worldSize = worldSize

        self.genWorld()



    def genWorld(self):
        self.world = []
        self.grassGen()
        self.pushWorld()



    def randomGen(self):
        for i in range(self.worldSize[0]):
            row = []
            for j in range(self.worldSize[1]):
                randi = random.randint(0,127)
                col = [127,randi,0]
                random.shuffle(col)
                row.append(Tile(tuple(col)))
            self.world.append(row)



    def grassGen(self):
        perlinVecs = self.genPerlinVecs(80,80)
        perlinNoise = self.samplePerlinField(perlinVecs,self.worldSize[0],self.worldSize[1],0.34,0.34,0,0)
        for i in range(self.worldSize[0]):
            row = []
            for j in range(self.worldSize[1]):
                lum = perlinNoise[i][j]
                col = [lum,lum,lum]
                row.append(Tile(tuple(col)))
            self.world.append(row)



    def genPerlinVecs(self,sizeX,sizeY):
        vecs = []
        for i in range(sizeX):
            row = []
            for j in range(sizeY):
                rand = random.uniform(0,1)
                band = (1 - (rand**2)) ** 0.5
                row.append((rand,band))
            vecs.append(row)
        return vecs


    #scales and offsets should be in range 0.0 <= n <= 1.0
    #offsets will be clamped to avoid out of bound errors
    def samplePerlinField(self,vecs,sizeX,sizeY,scaleX,scaleY,offsetX,offsetY):
        vecX = len(vecs)
        vecY = len(vecs[0])
        stepX = (vecX / sizeX) * scaleX
        stepY = (vecY / sizeY) * scaleY

        noise = []
        for i in range(sizeX):
            row = []
            posX = i * stepX
            for j in range(sizeY):
                posY = j * stepY
            noise.append(row)
        return noise



    def samplePerlinPoint(self,vecs,x,y):
        pass



    def pushWorld(self):
        colors = []
        for i in self.world:
            row = []
            for j in i:
                row.append(j.color)
            colors.append(row)

        try:
            self.queue.put_nowait(colors)
        except:
            try:
                self.queue.get()
            except:
                pass
            self.queue.put_nowait(colors)





class Tile:
    def __init__(self,color):
        self.color = color
