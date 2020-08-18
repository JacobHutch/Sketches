'''
Simple TKinter Base Frame Object

Options:
name - "Title"
size - (x,y) -> int only
bg   - "#rrggbb" -> standard hex 8bpc
res  - (x-> 0 or 1, y-> 0 or 1) -> is the window resizable
'''

import tkinter as tk

class App:
	def __init__(self,**options):

		#Option variables initialization
		self._name = options.get('name', 'Test')
		self._size = options.get('size',(100,100))
		self._bg = options.get('bg','#000000')
		self._res = options.get('res',(0,0))

		#Main window creation
		self._ui = tk.Tk()
		self._ui.title(self._name)
		self._ui.geometry(str(self._size[0])+'x'+str(self._size[1]))
		self._ui['background'] = self._bg
		self._ui.resizable(self._res[0],self._res[1])

	def bindKeys(self,**keyBindList):
		for char in keyBindList:
			self._ui.bind_all('<'+char+'>',keyBindList[char])

	def getUi(self):
		return self._ui

	def getBg(self):
		return self._bg

	def setSize(self, size=None):
		if size == None:
			size = self._size
		size = str(size[0])+'x'+str(size[1])
		self._ui.geometry(size)

	def kill(self, event=None):
		self._ui.destroy()
