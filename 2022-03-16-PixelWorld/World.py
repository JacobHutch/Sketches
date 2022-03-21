import random

class World:
    def __init__(self,queue,worldSize):
        self.queue = queue
        self.worldSize = worldSize

        self.genWorld()



    def genWorld(self):
        self.world = []
        for i in range(self.worldSize[0]):
            row = []
            for j in range(self.worldSize[1]):
                randi = random.randint(0,191)
                col = [191,randi,0]
                random.shuffle(col)
                row.append(Tile(tuple(col)))
            self.world.append(row)
        self.pushWorld()



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
