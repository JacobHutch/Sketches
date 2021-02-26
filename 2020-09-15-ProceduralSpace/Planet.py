from Body import Body
import random
class Planet(Body):
	def __init__(self,system,n):
		super(Planet,self).__init__(system,n)
		self.dataGen()
		self.colorGen()

	def dataGen(self):
		self._mass = random.uniform(10,20)
		self._radius = random.randint(10,20)
		self._position = [random.randint(-500,500),random.randint(-500,500)]
		self._velocity = [random.uniform(0,1),random.uniform(0,1)]
		self._acceleration = [0,0]

	def colorGen(self):
		r = random.randint(0,127)
		g = random.randint(27,187)
		b = random.randint(27,177)
		r = hex(r).split('x')[-1].zfill(2)
		g = hex(g).split('x')[-1].zfill(2)
		b = hex(b).split('x')[-1].zfill(2)
		self._color = "#"+r+g+b
