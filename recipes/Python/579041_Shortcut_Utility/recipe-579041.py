# Shortcut Utility
# FB - 20150329
# Create a file named "SHORTCUTS.CSV"
# in the same directory as this script
# which should contain lines in the format:
# target,description
# Example:
# c:\,c: drive
# c:\windows,windows directory
# c:\windows\notepad.exe,notepad
# C:\Users\desktop.ini,desktop.ini
# http://google.com,google

import Tkinter as tk
import os

targets = []
descriptions = []
targetTypes = [] # url/file/dir

def LoadCSV():
    f = open('SHORTCUTS.CSV','r')
    lines = f.readlines()
    for line in lines:
        lineList = line.strip().split(',')
        target = lineList[0]
        targets.append(target)
        descriptions.append(lineList[1])
        if target.lower().startswith('http'):
            targetTypes.append('url')
        elif os.path.isfile(target):
            targetTypes.append('file')
        elif os.path.isdir(target):
            targetTypes.append('dir')

class App:
    def __init__(self, root):
        self.root = root
        LoadCSV()
        for i, description in enumerate(descriptions):
            color = "#000000"
            if targetTypes[i] == "url":
                color = "#ff0000"
            elif targetTypes[i] == "file":
                color = "#00ff00"
            elif targetTypes[i] == "dir":
                color = "#0000ff"
            link = tk.Label(text = description, foreground = color)
            link.bind("<1>", lambda event, text = description: self.click_link(event, text))
            link.pack()

    def click_link(self, event, description):
        for i, desc in enumerate(descriptions):
            if description == desc:
                if targetTypes[i] == "url":
                    os.system('explorer ' + targets[i])
                elif targetTypes[i] == "file":
                    os.system(targets[i])
                elif targetTypes[i] == "dir":
                    os.system('explorer ' + targets[i])
                break

root = tk.Tk()
app = App(root)
root.mainloop()
