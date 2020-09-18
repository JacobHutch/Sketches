from abc import ABC, abstractmethod
import random
class Body(ABC):
	@abstractmethod
	def __init__(self,system):
		self.__system = system
		self.nameGen()

	def printInfo(self):
		print("Name: "+self.__name)

	def nameGen(self):
		prefix = self.__system.getName()
		self.__name = prefix

	@abstractmethod
	def dataGen(self):
		pass
