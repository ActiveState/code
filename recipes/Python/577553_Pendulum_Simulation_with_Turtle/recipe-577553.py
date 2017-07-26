from math import sin, pi
from time import sleep
from turtle import *

GA = 9.80665 # Gravitational Acceleration (meters per second squared)
FORM = 'Time={:6.3f}, Angle={:6.3f}, Speed={:6.3f}'

def main():
    length = 9.0            # Of pendulum (meters)
    ngol = - GA / length    # Negative G over L
    total_time = 0.0        # Seconds
    angle = 1.0             # Initial angle of pendulum (radians)
    speed = 0.0             # Initial angular velocity (radians/second)
    time_step = 0.05        # Seconds
    while total_time < 30.0:
        total_time += time_step
        speed += ngol * sin(angle) * time_step
        angle += speed * time_step
        #print(FORM.format(total_time, angle, speed))
        if draw(angle, length): break
        sleep(time_step)

def init():
    setup()
    mode('logo')
    radians()
    speed(0)
    hideturtle()
    tracer(False)
    penup()

def draw(angle, length):
    if speed() != 0: return True
    clear()
    setheading(angle + pi)
    pensize(max(round(length), 1))
    pendown()
    forward(length * 25)
    penup()
    dot(length * 10)
    home()
    update()

if __name__ == '__main__':
    init()
    main()
    bye()
