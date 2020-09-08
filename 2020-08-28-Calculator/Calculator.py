import tkinter as tk
import sys
sys.path.append("../Shared/Python")
from Frame import App
import random as rand
import time
import functools

class Program(App):
	def __init__(self,**options):
		super(Program,self).__init__(**options)
		keys = {"q":self.kill}
		self.bindKeys(**keys)

		self.__layout = []
		self.__calcPhase = 0
		self.__firstNumber = "0"
		self.__secondNumber = ""

		#Feels unecessary but I don't want to type 0s in
		self.__buttons = ["1","2","3","4","5","6","7","8","9","0","C","<","+","-","*","/","=",".","CE","+/-"]
		self.__buttons = dict.fromkeys(self.__buttons,None)

		self.__frame = tk.Frame(self._ui,bg="#CFCFCF")
		self.__frame.grid(row=0,column=0,sticky="NSEW")

		self.__textFrame = tk.Frame(self.__frame,bg="#CFCFCF",relief="sunken",borderwidth=5)
		self.__textFrame.grid(row=0,column=0,columnspan=4,sticky="NSEW")
		self.__textFrame.grid_rowconfigure(0,weight=1)
		self.__textFrame.grid_rowconfigure(1,weight=1)
		self.__textFrame.grid_columnconfigure(0,weight=1)

		self.__primaryTextBox = tk.Label(self.__textFrame,text="0",font=("",30),anchor="se")
		self.__secondaryTextBox = tk.Label(self.__textFrame,text="",fg="#3F3F3F",font=("",20),anchor="se")
		self.__secondaryTextBox.grid(row=0,column=0,sticky="NSEW")
		self.__primaryTextBox.grid(row=1,column=0,sticky="NSEW")

		self.__readLayout(options["file"])
		self.__createButtons()

		self._ui.grid_rowconfigure(0,weight=1)
		self._ui.grid_columnconfigure(0,weight=1)

		self.__frame.bind("<Configure>",self.__resize)

		self.__run()

	def __run(self):
		self.__eventLoop()
		self._ui.mainloop()

	def __eventLoop(self):

		self._ui.after(16,self.__eventLoop)

	def __readLayout(self,filepath):
		infile = open(filepath,"r")
		line = infile.readline()
		count = 0
		while(line != ""):
			self.__frame.grid_rowconfigure(count,weight=1)
			line = line.replace("\n","")
			self.__layout.append(line.split(","))
			count += 1
			line = infile.readline()
		for x in range(max([len(self.__layout[i]) for i in range(len(self.__layout))])):
			self.__frame.grid_columnconfigure(x,weight=1)

	def __createButtons(self):
		for b in self.__buttons:
			self.__buttons[b] = tk.Button(self.__frame,text=b,command=functools.partial(self.__buttonPress,b))
			r = 0
			for x in self.__layout:
				if b in x:
					break
				r += 1
			self.__buttons[b].grid(row=r,column=self.__layout[r].index(b),sticky="NSEW")

	def __resize(self,event):
		self._ui.update()
		print("resize",event)
		print(self.__buttons["1"].winfo_height())
		h = int(self.__buttons["1"].winfo_height()/4)
		for b in self.__buttons:
			self.__buttons[b]["font"] = ("",h)
		self.__primaryTextBox["font"] = ("",h*2)
		self.__secondaryTextBox["font"] = ("",h)

	def __buttonPress(self,button):
		try:
			float(button)

			if(self.__calcPhase == 0):
				self.__firstNumber = ""
				self.__secondaryTextBox["text"] = ""
				self.__calcPhase = 1

			if(self.__calcPhase == 1):
				self.__firstNumber += button
				self.__primaryTextBox["text"] = self.__firstNumber

			else:
				if(self.__calcPhase == 2):
					self.__secondNumber = ""
					self.__calcPhase = 3

				if(self.__calcPhase == 3):
					self.__secondNumber += button
					self.__primaryTextBox["text"] = self.__secondNumber

		except:
			if(button == "C"):
				self.__calcPhase = 0
				self.__firstNumber = "0"
				self.__secondNumber = ""
				self.__primaryTextBox["text"] = self.__firstNumber
				self.__secondaryTextBox["text"] = ""

			if(button == "CE"):
				if(self.__calcPhase == 1):
					self.__firstNumber = ""
					self.__primaryTextBox["text"] = "0"

				if((self.__calcPhase == 2) or (self.__calcPhase == 3)):
					self.__secondNumber = "0"
					self.__primaryTextBox["text"] = self.__secondNumber

			if((button == "+") or (button == "-") or (button == "*") or (button == "/")):
				if(self.__calcPhase == 1):
					self.__calcPhase = 2
					self.__secondNumber = self.__firstNumber
					self.__firstNumber += button
					self.__secondaryTextBox["text"] = self.__firstNumber

				elif(self.__calcPhase == 2):
					self.__firstNumber = self.__firstNumber[:-1] + button
					self.__secondaryTextBox["text"] = self.__firstNumber

			if(button == "="):
				if((self.__calcPhase == 2) or (self.__calcPhase == 3)):
					self.__calcPhase = 0
					self.__firstNumber += self.__secondNumber
					self.__primaryTextBox["text"] = eval(self.__firstNumber)
					self.__firstNumber += "="
					self.__secondaryTextBox["text"] = self.__firstNumber

			if(button == "+/-"):
				if(self.__calcPhase == 1):
					self.__firstNumber = "-" + self.__firstNumber
					self.__primaryTextBox["text"] = self.__firstNumber

				elif((self.__calcPhase == 2) or (self.__calcPhase == 3)):
					self.__secondNumber = "-" + self.__secondNumber
					self.__primaryTextBox["text"] = self.__secondNumber

kwargs = {"name":"Testing","size":(600,400),
			"bg":"#00CCCC","res":(1,1),"file":"Layout.txt"}

Prog = Program(**kwargs)
