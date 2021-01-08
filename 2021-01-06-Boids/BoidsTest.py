import math
import random
import pygame

class Boid:
    def __init__(self,velocity):
        self.position = (random.randint(0,1000),random.randint(0,1000))
        self.angle = random.randint(0,359)
        self.velocity = velocity

    def update(self,position,angle):
        self.position = position
        self.angle = angle

class System:
    def __init__(self,boidOps,amount=10,size=5,length=20,radius=100,collisionRadius=20,tick=15):
        self.amount = amount
        self.size = size
        self.length = length
        self.radius = radius
        self.collisionRadius = collisionRadius
        self.tick = tick
        self.boids = [Boid(**boidOps) for i in range(amount)]

    def distance(self,a,b):
        return (((a.position[0] - b.position[0]) ** 2) + ((a.position[1] - b.position[1]) ** 2)) ** 0.5

    def updateBoids(self):
        avoidFactor = 0.2
        centerFactor = 0.005
        alignFactor = 0.05

        for boid in self.boids:            
            avoidX = 0
            avoidY = 0
            avgX = boid.position[0]
            avgY = boid.position[1]
            avoid = 0
            center = 0
            alignCos = 0
            alignSin = 0
            count = 0
            avoidCount = 0

            if boid.position[0] > 1000 or boid.position[0] < 0 or boid.position[1] > 1000 or boid.position[1] < 0:
                barrier = 180
            else:
                barrier = 0
        
            for other in self.boids:
                if (boid != other) and (self.distance(boid,other) < self.radius):
                    count += 1
                    
                    #avoid data
                    if self.distance(boid,other) < self.collisionRadius:
                        avoidCount += 1
                        avoidX += other.position[0]
                        avoidY += other.position[1]

                    #center data
                    avgX += other.position[0]
                    avgY += other.position[1]

                    #align data
                    alignCos += math.cos(math.radians(other.angle))
                    alignSin += math.sin(math.radians(other.angle))

            #avoid calc
            if avoidCount != 0:
                avoidX /= avoidCount
                avoidY /= avoidCount
                avoid = (math.degrees(math.atan2(boid.position[1] - avoidY,boid.position[0] - avoidX)) + 360) % 360
                t1 = avoid - boid.angle
                if t1 > 0:
                    t2 = abs(t1) - 360
                else:
                    t2 = 360 - abs(t1)
                if abs(t1) > abs(t2):
                    avoid = t2
                elif abs(t2) > abs(t1):
                    avoid = t1
                else:
                    avoid = random.choice([t1,t2])
            else:
                avoid = 0
                    
            if count != 0:
                #center calc
                avgX /= (count + 1)
                avgY /= (count + 1)
                center = (math.degrees(math.atan2(avgY - boid.position[1],avgX - boid.position[0])) + 360) % 360
                t1 = center - boid.angle
                if t1 > 0:
                    t2 = abs(t1) - 360
                else:
                    t2 = 360 - abs(t1)
                if abs(t1) > abs(t2):
                    center = t2
                elif abs(t2) > abs(t1):
                    center = t1
                else:
                    center = random.choice([t1,t2])

                #align calc
                alignCos /= count
                alignSin /= count
                align = (math.degrees(math.atan2(alignSin,alignCos)) + 360) % 360
                t1 = align - boid.angle
                if t1 > 0:
                    t2 = abs(t1) - 360
                else:
                    t2 = 360 - abs(t1)
                if abs(t1) > abs(t2):
                    align = t2
                elif abs(t2) > abs(t1):
                    align = t1
                else:
                    align = random.choice([t1,t2])

            #combine and calculate final movement
                newAngle = (boid.angle + barrier + (avoid * avoidFactor) + (center * centerFactor) + (align * alignFactor)) % 360
            else:
                newAngle = boid.angle + barrier
            newPos = (boid.position[0] + (boid.velocity / self.tick * math.cos(math.radians(newAngle))),boid.position[1] + (boid.velocity / self.tick * math.sin(math.radians(newAngle))))
            boid.update(newPos,newAngle)

    def resetBoids(self):
        for boid in self.boids:
            boid.update((random.randint(0,1000),random.randint(0,1000)),random.randint(0,359))

    def normalizeFactors(self,avoid,center,align):
        total = avoid + center + align
        if total != 0:
            fraction = 1.0 / total
        else:
            fraction = 1
        return (avoid / fraction, center / fraction, align / fraction)

class App:
    def __init__(self,boidOps,sysOps,winSize=(500,500)):
        self.running = True
        self.clock = pygame.time.Clock()
        self.tick = sysOps["tick"]
        self.system = System(boidOps,**sysOps)
        pygame.init()
        self.window = pygame.display.set_mode(winSize)
        self.mainloop()

    def mainloop(self):
        while self.running:
            #keyboard processing
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if keys[pygame.K_r]:
                self.system.resetBoids()

            #event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                    
            if not self.running:
                break

            self.window.fill("white")
            
            #boid update
            self.system.updateBoids()
            for boid in self.system.boids:
                pygame.draw.line(self.window,(0,0,255),boid.position,((math.cos(math.radians(boid.angle)) * self.system.length) + boid.position[0],(math.sin(math.radians(boid.angle)) * self.system.length) + boid.position[1]))
                pygame.draw.circle(self.window,(0,255,255),boid.position,5)
            pygame.display.flip()
            self.clock.tick(self.tick)

boidOps = {"velocity":100}
sysOps = {"amount":100,"size":5,"length":20,"radius":100,"collisionRadius":20,"tick":60}
appOps = {"winSize":(1000,1000)}

a = App(boidOps,sysOps,**appOps)
