# Python Version: 3 or newer
# people using python 2,please replace tkinter with Tkinter
# Author: Karim Khan (k4karim27@gmail.com)


from tkinter import *
from tkinter import ttk


def calculate1(*args):
    try:
        value1 = float(width.get())
        value2 = float(lenght.get())
        area.set( value1 * value2 )
    except ValueError:
        pass
def calculate2(*args):
    try:
        value1 = float(width.get())
        value2 = float(lenght.get())
        area.set( 0.5*value1 * value2 )
    except ValueError:
        pass   
def calculate3(*args):
    try:
        value3 = float(radius.get())
        
        area.set( 3.14* value3 * value3 )
    except ValueError:
        pass
def reset():
  width_entry.delete(0, END)
  lenght_entry.delete(0, END)
  radius_entry.delete(0, END)

root = Tk()
root.title("Area Calculator")
root.geometry("290x120")

mainframe = ttk.Frame(root, padding="5 5 15 15")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

width = StringVar()
radius = StringVar()
lenght = StringVar()
area = StringVar()

width_entry = ttk.Entry(mainframe, width=5, textvariable=width)
width_entry.grid(column=1, row=1, sticky=(E))
lenght_entry = ttk.Entry(mainframe, width=5, textvariable=lenght)
lenght_entry.grid(column=2, row=1, sticky=(E))
radius_entry = ttk.Entry(mainframe, width=5, textvariable=radius)
radius_entry.grid(column=3, row=1, sticky=(E))

ttk.Label(mainframe,background="white", textvariable=area).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Circle", command=calculate3).grid(column=3, row=3, sticky=W)
ttk.Button(mainframe, text="Triangle", command=calculate2).grid(column=1, row=3, sticky=E)
ttk.Button(mainframe, text="Rectangle", command=calculate1).grid(column=2, row=3)
ttk.Button(mainframe, text="Reset", command=reset).grid(column=3, row=2, sticky=E)

ttk.Label(mainframe, text="Width").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Lenght").grid(column=2, row=1, sticky=W)
ttk.Label(mainframe, text="Radius").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="Area: ").grid(column=1, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

width_entry.focus()
lenght_entry.focus()
root.bind('<Return>', calculate1)
root.bind('<Return>', calculate2)

root.mainloop()
