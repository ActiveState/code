# -*- coding: utf-8 -*-

'''
Click counter

Left click: +1
Right click: -1
Middle click: Reset
'''

import pyHook
import pythoncom

print(__doc__)

click = 0

def left_down(event):
    global click
    click += 1
    print(click)
    return True

def right_down(event):
    global click
    click -= 1
    print(click)
    return True    

def middle_down(event):
    global click
    click = 0
    print(click)
    return True     

hm = pyHook.HookManager()
hm.SubscribeMouseLeftDown(left_down)
hm.SubscribeMouseRightDown(right_down)
hm.SubscribeMouseMiddleDown(middle_down)
hm.HookMouse()
pythoncom.PumpMessages()
hm.UnhookMouse()
