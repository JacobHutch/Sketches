from Body import Body
import random
class Star(Body):
	def __init__(self,system):
		super(Star,self).__init__(system)
		self.dataGen()

	def dataGen(self):
		self.__mass = random.randint(50,75)
		self.__radius = random.randint(50,75)
		self.__position = (0,0)

	def getData(self):
		return [self.__mass,self.__radius,self.__position]
