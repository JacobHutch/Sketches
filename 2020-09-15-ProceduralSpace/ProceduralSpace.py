import tkinter as tk
import sys
sys.path.append("../Shared/Python")
from Frame import App
from System import System

class Procedural(App):
	def __init__(self,**options):
		super(Procedural,self).__init__(**options)
		keys = {"q":self.kill,"i":self.__zoomIn,"o":self.__zoomOut}
		self.bindKeys(**keys)

		self._ui.state("zoomed")

		self._ui.grid_rowconfigure(0,weight=1)
		self._ui.grid_columnconfigure(0,weight=1)

		self.__frame = tk.Frame(self._ui,bg="#FF0000",bd=-2)
		self.__frame.grid(row=0,column=0,sticky="NSEW")
		self.__frame.grid_rowconfigure(0,weight=1)
		self.__frame.grid_columnconfigure(0,weight=1)

		self.__canvas = tk.Canvas(self.__frame,bg="#000000",bd=-2)
		self.__canvas.grid(row= 0,column=0,sticky="NSEW")
		self.__canvas.bind("<Configure>",self.__resize)

		self.__xdis = self.__canvas.winfo_width()//2
		self.__ydis = self.__canvas.winfo_height()//2
		self.__zoomScale = 1
		self.__zoomStep = 5

		self.__system = System(2,1,3)
		self._ui.title(self.__system.getName())

		self.__run()

	def __run(self):
		self.__eventLoop()
		self._ui.mainloop()

	def __eventLoop(self):
		self.__system.nextFrame()
		self.display(["body"])
		self._ui.after(10,self.__eventLoop)

	def __resize(self,event=None):
		self.__xdis = self.__canvas.winfo_width()//2
		self.__ydis = self.__canvas.winfo_height()//2
		self.display(["body"])

	def __zoomIn(self,event=None):
		self.__zoomScale = min(self.__zoomScale * self.__zoomStep, 1)
		self.__resize()

	def __zoomOut(self,event=None):
		self.__zoomScale = max(self.__zoomScale / self.__zoomStep, 0.01)
		self.__resize()

	def display(self,tags):
		for t in tags:
			self.__canvas.delete(t)
		if "body" in tags:
			for b in self.__system.getBodies():
				d = b.getData()
				self.__canvas.create_oval(((d[2][0]-d[1])*self.__zoomScale)+self.__xdis,((d[2][1]-d[1])*self.__zoomScale)+self.__ydis,
					((d[2][0]+d[1])*self.__zoomScale)+self.__xdis,((d[2][1]+d[1])*self.__zoomScale)+self.__ydis,fill=d[5],width=0,tags="body")

		if "orbit" in tags:
			for b in self.__system.getBodies():
				d = b.getData()
				dist = ((d[2][0] ** 2) + (d[2][1] ** 2)) ** 0.5
				self.__canvas.create_oval(-dist+self.__xdis,-dist+self.__ydis,dist+self.__xdis,dist+self.__ydis,fill="",outline=d[5],tags="orbit")

kwargs = {"name":"Testing","size":(1000,800),
			"bg":"#45672f","res":(1,1)}

p = Procedural(**kwargs)
