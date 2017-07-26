#!/usr/bin/env python
#title			:wastedmoney.py
#description	        :Calculate the amount of money you waste each day.
#author                 :bgw
#date			:20120124
#version		:0.2
#usage			:python wastedmoney.py
#notes			:
#python_version	        :2.6.6
#==============================================================================

from Tkinter import *


root = Tk()
root.title("Wasted Money Calculator")
root.geometry("275x200")
root.grid()

def callback(event):
    field0 = varText.get()
    print field0
    if field0 == 0:
        initAmount.delete(0, END)
    return

def callback1(event):
    field0 = varText.get()
    print field0
    return

def callback2(event):
    field2 = varText2.get()
    an_item.delete(0, END)
    return

def calculateAmount():
    field1 = varText.get()
    weekly_sum.delete(0, END)
    weekly_sum.insert(0, int(field1 * 7))
    field2 = varText.get()
    monthly_sum.delete(0, END)
    monthly_sum.insert(0, int(field2 * 31))
    field3 = varText.get()
    yearly_sum.delete(0, END)
    yearly_sum.insert(0, int(field3 * 356))
    field4 = varText.get()
    five_year_sum.delete(0, END)
    five_year_sum.insert(0, int((field4 * 1825) + 1))
    field5 = varText.get()
    ten_year_sum.delete(0, END)
    ten_year_sum.insert(0, int((field5 * 3650) + 1))
    return

Label(root, text="I spend $").grid(sticky=W, row=0)

varText = IntVar()
initAmount = Entry(root, textvariable=varText, width=10, bg = "pale green")
initAmount.bind("<FocusIn>", callback)
initAmount.bind("<FocusOut>", callback1)
initAmount.grid(sticky=W, row=0, column=1)

Label(root, text="everyday to buy").grid(sticky=W, column=2, row=0)

varText2 = StringVar()
varText2.set("Item")
an_item = Entry(root, textvariable=varText2, bg = "pale green")
an_item.bind("<FocusIn>", callback2)
an_item.grid(sticky=W, row=1, columnspan=3)

Label(root, text="That adds up to be...").grid(sticky=W, row=3, columnspan=3)

Button(root, text="Calculate", width=10, command=calculateAmount).grid(sticky=W, row=2, columnspan=3)

Label(root, text="per week").grid(sticky=W, row=4, column=0)

varText1 = IntVar(None)
weekly_sum = Entry(root, textvariable=varText1, takefocus=0, width=15, bg = "pale green")
weekly_sum.grid(sticky=W, row=4, column=2)

Label(root, text="per month").grid(sticky=W, row=5, columnspan=3)

varText1 = IntVar(None)
monthly_sum = Entry(root, textvariable=varText1, takefocus=0, width=15, bg = "pale green")
monthly_sum.grid(sticky=W, row=5, column=2)

Label(root, text="per year").grid(sticky=W, row=6, columnspan=3)

varText1 = IntVar(None)
yearly_sum = Entry(root, textvariable=varText1, takefocus=0, width=15, bg = "pale green")
yearly_sum.grid(sticky=W, row=6, column=2)

Label(root, text="over a five years").grid(sticky=W, row=7, columnspan=3)

varText1 = IntVar(None)
five_year_sum = Entry(root, textvariable=varText1, takefocus=0, width=15, bg = "pale green")
five_year_sum.grid(sticky=W, row=7, column=2)

Label(root, text="and over a ten years.").grid(sticky=W, row=8, columnspan=3)

varText1 = IntVar(None)
ten_year_sum = Entry(root, textvariable=varText1, takefocus=0, width=15, bg = "pale green")
ten_year_sum.grid(sticky=W, row=8, column=2)


root.mainloop()
