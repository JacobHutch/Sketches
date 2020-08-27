import tkinter as tk
import sys
sys.path.append("../Shared/Python")
from Frame import App
import random as rand
import time

class Program(App):
	def __init__(self,**options):
		super(Program,self).__init__(**options)
		keys = {"q":self.kill}
		self.bindKeys(**keys)

		self.__running = 0
		self.__randomTime = 0
		self.__elapsedTime = 0

		self.__frame = tk.Frame(self._ui,bg="#CFCFCF")
		self.__frame.grid(row=0,column=0,sticky="NSEW")
		self.__frame.grid_rowconfigure(0,weight=1)
		self.__frame.grid_columnconfigure(0,weight=1)

		self.__button = tk.Button(self.__frame,command=self.__click,text="Click to Run")
		self.__button.grid(row=0,column=0)

		self._ui.grid_rowconfigure(0,weight=1)
		self._ui.grid_columnconfigure(0,weight=1)

		self.__run()

	def __run(self):
		self.__eventLoop()
		self._ui.mainloop()

	def __eventLoop(self):

		self._ui.after(16,self.__eventLoop)

	def __click(self):
		if(self.__running == -1):
			self.__elapsedTime = ((time.time() - self.__elapsedTime) * 1000) - 75 #estimated error, because other processes are running
			self.__running = 0
			self.__button["text"] = str(format(self.__elapsedTime,"0.2f"))+" ms"
			self.__frame["bg"] = "#CFCFCF"

		elif(self.__running == 0):
			self.__running = 1
			self.__button["text"] = "Running..."
			self.__frame["bg"] = "#00FF00"
			self.__randomTime = rand.randint(100,10000)
			self._ui.after(self.__randomTime,self.__react)

	def __react(self):
		self.__running = -1
		self.__frame["bg"] = "#FF0000"
		self.__elapsedTime = time.time()

kwargs = {"name":"Testing","size":(600,400),
			"bg":"#00CCCC","res":(0,0)}

Prog = Program(**kwargs)
