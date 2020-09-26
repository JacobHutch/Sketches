from abc import ABC, abstractmethod
import random
class Body(ABC):
	@abstractmethod
	def __init__(self,system,n):
		self.__system = system
		self.nameGen(n)

	@abstractmethod
	def dataGen(self):
		pass

	def printInfo(self):
		print("Name: "+self.__name)

	def nameGen(self,n):
		prefix = self.__system.getName()
		self.__name = prefix + str(n)

	def collision(self):
		pass

	def updatePos(self,acceleration):
		self._velocity[0] += acceleration[0]
		self._velocity[1] += acceleration[1]
		self._position[0] += self._velocity[0]
		self._position[1] += self._velocity[1]

	def getData(self):
		return [self._mass,self._radius,self._position,self._velocity,self._acceleration,self._color]
