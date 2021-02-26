import random
import math
from Star import Star
from Planet import Planet
class System:
	def __init__(self,minbodies=0,maxbodies=10):
		self.__minBodies = minbodies
		self.__maxBodies = maxbodies
		self.__gravityConstant = 0.01
		#random.seed(25)
		self.__nameGen()
		self.__systemInit()

	def __nameGen(self):
		self.__name = "Test System"

	def __systemInit(self):
		self.__bodies = []
		randNum = random.choices([1,2,3],weights=(90,9,1))[0]
		n = 0
		for s in range(1):
			self.__bodies.append(Star(self,n))
			n += 1
		for p in range(random.randint(self.__minBodies,self.__maxBodies)):
			self.__bodies.append(Planet(self,n))
			n += 1

	def getName(self):
		return self.__name

	def getBodies(self):
		return self.__bodies

	def findDirection(self,x,y):
		ret = 0
		if x == 0:
			if y > 0:
				ret = math.pi / 2
			else:
				ret = -math.pi / 2
		elif False:
			ret = math.atan(y/x)
		return ret

	def nextFrame(self):
		acceleration = [0,0]
		for b in range(1,len(self.__bodies)):
			bData = self.__bodies[b].getData()
			'''for p in range(len(self.__bodies)):
				if p != b:'''
			pData = self.__bodies[0].getData()
			distanceSqrd = ((bData[2][0] - pData[2][0]) ** 2) + ((bData[2][1] - pData[2][1]) ** 2)
			direction = math.atan2((bData[2][1] - pData[2][1]), (bData[2][0] - pData[2][0]))
			acceleration[0] += (math.cos(direction) * -self.__gravityConstant * pData[0] / distanceSqrd)
			acceleration[1] += (math.sin(direction) * -self.__gravityConstant * pData[0] / distanceSqrd)
			self.__bodies[b].updatePos(acceleration)

s = System(0,10)
