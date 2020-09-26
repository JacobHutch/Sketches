from Body import Body
import random
import math
class Star(Body):
	def __init__(self,system,n):
		super(Star,self).__init__(system,n)
		self.dataGen()
		self.colorGen()

	def dataGen(self):
		self._mass = random.randint(50000,75000)
		self._radius = random.randint(50,75)
		self._position = [0,0]
		self._velocity = [0,0]
		self._acceleration = [0,0]

	#Taken from https://tannerhelland.com/2012/09/18/convert-temperature-rgb-algorithm-code.html
	def colorGen(self):
		temp = random.randint(10,100)

		if temp <= 66:
			r = 255
		else:
			r = temp - 60
			r = int(max(min(329.698727446 * (r ** -0.1332047592), 255), 0))

		if temp <= 66:
			g = temp
			g = int(max(min(99.4708025861 * math.log(g) - 161.1195681661, 255), 0))
		else:
			g = temp - 60
			g = int(max(min(288.1221695283 * (g ** -0.0755148492), 255), 0))

		if temp >= 66:
			b = 255
		elif temp <= 19:
			b = 0
		else:
			b = temp - 10
			b = int(max(min(138.5177312231 * math.log(b) - 305.0447927307, 255), 0))

		r = hex(r).split('x')[-1].zfill(2)
		g = hex(g).split('x')[-1].zfill(2)
		b = hex(b).split('x')[-1].zfill(2)
		self._color = "#"+r+g+b
