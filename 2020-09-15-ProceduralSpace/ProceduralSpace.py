import tkinter as tk
import sys
sys.path.append("../Shared/Python")
from Frame import App
from System import System

class Procedural(App):
	def __init__(self,**options):
		super(Procedural,self).__init__(**options)
		keys = {"q":self.kill}
		self.bindKeys(**keys)

		self._ui.grid_rowconfigure(0,weight=1)
		self._ui.grid_columnconfigure(0,weight=1)

		self.__frame = tk.Frame(self._ui,bg="#FF0000")
		self.__frame.grid(row=0,column=0,sticky="NSEW")
		self.__frame.grid_rowconfigure(0,weight=1)
		self.__frame.grid_columnconfigure(0,weight=1)

		self.__canvas = tk.Canvas(self.__frame,bg="#000000",bd=-2)
		self.__canvas.grid(row=0,column=0,sticky="NSEW")
		self.__canvas.bind("<Configure>",self.__resize)
		self.__xdis = self.__canvas.winfo_width()//2
		self.__ydis = self.__canvas.winfo_height()//2

		self.__system = System(2,0,10)
		self.display()

		self.__run()

	def __run(self):
		#self.__eventLoop()
		self._ui.mainloop()

	def __eventLoop(self):
		self._ui.after(16,self.__eventLoop)

	def __resize(self,event):
		self.__canvas.delete("body")
		self.__xdis = self.__canvas.winfo_width()//2
		self.__ydis = self.__canvas.winfo_height()//2
		self.display()

	def display(self):
		for b in self.__system.getBodies():
			d = b.getData()
			self.__canvas.create_oval(d[2][0]-d[1]+self.__xdis,d[2][1]-d[1]+self.__ydis,d[2][0]+d[1]+self.__xdis,d[2][1]+d[1]+self.__ydis,fill="#FFFFFF",tags="body")

kwargs = {"name":"Testing","size":(600,400),
			"bg":"#45672f","res":(1,1)}

p = Procedural(**kwargs)
