import random, math

class World:
    def __init__(self,queue,worldSize):
        self.queue = queue
        self.worldSize = worldSize

        self.genWorld()



    def genWorld(self):
        self.world = []
        self.grassGen()
        #self.randomGen()
        self.pushWorld()



    def randomGen(self):
        for i in range(self.worldSize[0]):
            row = []
            for j in range(self.worldSize[1]):
                randi = random.randint(0,255)
                #col = [255,randi,0]
                col = [randi,randi,randi]
                random.shuffle(col)
                row.append(Tile(tuple(col)))
            self.world.append(row)



    def grassGen(self):
        perlinVecs = self.genPerlinVecs(80,80)
        perlinNoise = self.samplePerlinField(perlinVecs,self.worldSize[0],self.worldSize[1],0.07,0.07,0,0)
        for i in range(self.worldSize[0]):
            row = []
            for j in range(self.worldSize[1]):
                lum = (perlinNoise[i][j] + 1) / 2
                r = int(lum * lum * random.randint(63,191))
                g = int(lum * random.randint(127,255))
                b = int(((1 - lum) ** 2) * random.randint(0,31))
                col = [lum*256,lum*256,lum*256]
                row.append(Tile(tuple(col)))
            self.world.append(row)



    def genPerlinVecs(self,sizeX,sizeY):
        vecs = []
        for i in range(sizeX):
            row = []
            for j in range(sizeY):
                theta = random.uniform(0,360)
                rand = math.cos(theta)
                band = math.sin(theta)
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

                if (posX != int(posX)) or (posY != int(posY)):
                    corners = []
                    corners.append([int(posX), int(posY)])
                    corners.append([int(posX)+1, int(posY)])
                    corners.append([int(posX), int(posY)+1])
                    corners.append([int(posX)+1, int(posY)+1])

                    cVecs = []
                    for p in corners:
                        cVecs.append([posX - p[0], posY - p[1]])

                    dots = []
                    for n in range(4):
                        x,y = corners[n]
                        dots.append(self.dot2D(vecs[x][y],cVecs[n]))

                    x,y = corners[0]
                    dx = self.smooth(posX - x)
                    dy = self.smooth(posY - y)
                    row.append(self.lerp(self.lerp(dots[0],dots[1],dx),self.lerp(dots[2],dots[3],dx),dy))
                else:
                    row.append(0)
            noise.append(row)
        return noise



    def samplePerlinPoint(self,vecs,x,y):
        pass



    def dot2D(self,a,b):
        return (a[0] * b[0]) + (a[1] * b[1])



    def normalize2D(self,a):
        mag = ((a[0] ** 2) + (a[1] ** 2)) ** 0.5
        return [a[0]/mag, a[1]/mag]



    def lerp(self,a,b,t):
        return a + ((b - a) * t)



    def smooth(self,x):
        return (((((6 * x) - 15) * x) + 10) * x * x * x)



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
