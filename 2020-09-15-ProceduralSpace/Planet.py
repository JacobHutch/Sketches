from Body import Body
import random
class Planet(Body):
	def __init__(self,system):
		super(Planet,self).__init__(system)
		self.dataGen()

	def dataGen(self):
		self.__mass = random.randint(1,10)
		self.__radius = random.randint(1,10)
		self.__position = [random.randint(-200,200),random.randint(-200,200)]

	def getData(self):
		return [self.__mass,self.__radius,self.__position]
