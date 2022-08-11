import random, math, queue

class World:
    def __init__(self,queue,worldSize):
        self.queue = queue
        self.worldSize = worldSize

        self.genWorld()



    def genWorld(self):
        self.world = []
        #self.grassGen()
        #self.randomGen()
        self.wfcGen()
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
                col = [r,g,b]
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



    #Simple 4-color map theorem:
    #domain: red, yellow, green, and blue tiles
    #constraints: no color can border itself
    #superposed is combo of colors, black is contradiction
    #entropy will be the number of values in the domain
    def wfcGen(self):
        #0-red, 1-yellow, 2-green, 3-blue
        domain = [0,1,2,3]
        #map of nodes, each node is [domain,color,entropy]
        nodes = []
        for i in range(self.worldSize[0]):
            row = []
            for j in range(self.worldSize[1]):
                row.append([domain,self.colorNode(domain),4])
            nodes.append(row)
        self.colorWorld(nodes)
        self.collapseWF(nodes)



    def colorNode(self,domain):
        cols = {0:(255,0,0),1:(255,255,0),2:(0,255,0),3:(0,0,255)}
        if len(domain) == 0: #contradiction state
            final = (0,0,0)
        else:
            count = len(domain)
            fr,fg,fb = 0,0,0
            for n in range(count):
                r,g,b = cols[domain[n]]
                fr += r/count
                fg += g/count
                fb += b/count
            final = [round(fr),round(fg),round(fb)]
        return final



    def colorWorld(self,nodes):
        self.world = []
        for i in range(self.worldSize[0]):
            row = []
            for j in range(self.worldSize[1]):
                row.append(Tile(nodes[i][j][1]))
            self.world.append(row)
        self.pushWorld()



    def collapseWF(self,nodes):
        for n in range((self.worldSize[0]*self.worldSize[1])-1):
            lowest = []
            entropy = 0
            for i in range(self.worldSize[0]):
                for j in range(self.worldSize[1]):
                    node = nodes[i][j]
                    if node[2] <= 4:
                        if len(lowest) == 0:
                            lowest.append((i,j))
                            entropy = node[2]
                        elif node[2] < entropy:
                            lowest = []
                            lowest.append((i,j))
                            entropy = node[2]
                        elif node[2] == entropy:
                            lowest.append((i,j))
            self.collapseNode(random.choice(lowest),nodes)



    def collapseNode(self,pos,nodes):
        x,y = pos
        node = nodes[x][y]
        domain = node[0]
        val = random.choice(domain)
        node[0] = [val]
        node[1] = self.colorNode(node[0])
        node[2] = 5
        nodes[x][y] = node
        self.colorWorld(nodes)



    #Utility Functions

    def dot2D(self,a,b):
        return (a[0] * b[0]) + (a[1] * b[1])



    def normalize2D(self,a):
        mag = ((a[0] ** 2) + (a[1] ** 2)) ** 0.5
        return [a[0]/mag, a[1]/mag]



    def lerp(self,a,b,t):
        return a + ((b - a) * t)



    def lerp3D(self,a,b,t):
        ax,ay,az = a
        bx,by,bz = b
        nx = ax + ((bx - ax) * t)
        ny = ay + ((by - ay) * t)
        nz = az + ((bz - az) * t)
        return [nx,ny,nz]



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
