# Program to do drawing using Python turtle graphics.
# turtle_drawing.py v0.1
# Author: Vasudev Ram
# http://jugad2.blogspot.in/p/about-vasudev-ram.html
# Copyright (C) 2016 Vasudev Ram.

import turtle

# Create and set up screen and turtle.

t = turtle
# May need to tweak dimensions below for your screen.
t.setup(600, 600)
t.Screen()
t.title("Turtle Drawing Program - by Vasudev Ram")
t.showturtle()

# Set movement step and turning angle.
step = 160
angle = 45

def forward():
    '''Move forward step positions.'''
    print "forward", step
    t.forward(step)

def back():
    '''Move back step positions.'''
    print "back", step
    t.back(step)

def left():
    '''Turn left by angle degrees.'''
    print "left", angle
    t.left(angle)

def right():
    '''Turn right by angle degrees.'''
    print "right", angle
    t.right(angle)

def home():
    '''Go to turtle home.'''
    print "home"
    t.home()

def clear():
    '''Clear drawing.'''
    print "clear"
    t.clear()

def quit():
    print "quit"
    t.bye()

t.onkey(forward, "Up")
t.onkey(left, "Left")
t.onkey(right, "Right")
t.onkey(back, "Down")
t.onkey(home, "h")
t.onkey(home, "H")
t.onkey(clear, "c")
t.onkey(clear, "C")
t.onkey(quit, "q")
t.onkey(quit, "Q")

t.listen()
t.mainloop()
