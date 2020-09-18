import random
from Star import Star
from Planet import Planet
class System:
	def __init__(self,recursion=2,minbodies=0,maxbodies=10):
		self.__recursion = recursion
		self.__minBodies = minbodies
		self.__maxBodies = maxbodies
		self.__nameGen()
		self.__systemInit()

	def __nameGen(self):
		self.__name = "Test System"

	def __systemInit(self):
		self.__bodies = []
		randNum = random.choices([1,2,3],weights=(90,9,1))[0]
		for s in range(randNum):
			self.__bodies.append(Star(self))
		for p in range(self.__minBodies,self.__maxBodies):
			self.__bodies.append(Planet(self))

	def getName(self):
		return self.__name

	def getBodies(self):
		return self.__bodies

s = System(2,0,10)
