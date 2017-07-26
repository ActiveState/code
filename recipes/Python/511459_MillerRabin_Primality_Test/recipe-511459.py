from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import math
import random
import string

#-----------------------------------------------
def millerTest(a, i, n):
	if i == 0:
		return 1
	x = millerTest(a, i / 2, n)
	if x == 0:
		return 0
	y = (x * x) % n
	if ((y == 1) and (x != 1) and (x != (n - 1))):
		return 0
	if (i % 2) != 0:
		y = (a * y) % n
	return y

#-----------------------------------------------
class MainApp:

	def __init__(self):
		self.root = Tk()
		self.initGui()
		self.root.title("Miller-Rabin")
		self.root.resizable(0, 0)
		self.root.update()
		self.root.mainloop()
		
	def initGui(self):
		body = Frame(self.root)
		body.pack(padx = 5, pady = 5)
		Label(body , text = "Number:").grid(row = 0, sticky = W)
		self.ent1 = Entry(body)
		self.ent1.grid(row = 0, column = 1)
		Button(body, text = "Check Primality", command = self.checkPrimality).grid(row = 1, sticky = E, column = 1, pady = 5)
	
	def checkPrimality(self):
		n = string.atoi(self.ent1.get())
		if millerTest(random.randint(2, n - 2), n - 1, n) == 1:
			tkMessageBox.showinfo(message = "%d is prime" % n)
		else:
			tkMessageBox.showinfo(message = "%d is NOT prime" % n)
	
#-----------------------------------------------
if __name__ == "__main__" : MainApp()
   
