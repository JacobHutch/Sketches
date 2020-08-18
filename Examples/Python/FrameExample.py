import tkinter as tk
import sys
sys.path.append("../../Shared/Python")
from Frame import App

class ExampleProgram(App):
	def __init__(self,**options):
		super(ExampleProgram,self).__init__(**options)
		keys = {"q":self.kill}
		self.bindKeys(**keys)
		self.__run()

	def __run(self):
		#optional user-defined event loop:
		self.__eventLoop()

		self._ui.mainloop()

	def __eventLoop(self):
		#Whatever user-defined calculations can go here
		#e.g. scripting or updating a counter
		print("x:"+str(self._ui.winfo_pointerx())+" y:"+str(self._ui.winfo_pointery()))

		#Calls function again after 16ms to create a loop
		self._ui.after(16,self.__eventLoop)

kwargs = {"name":"Testing","size":(600,400),
			"bg":"#45672f","res":(0,0)}

Ex = ExampleProgram(**kwargs)
