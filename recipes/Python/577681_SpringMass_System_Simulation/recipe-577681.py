# Damped spring-mass system driven by sinusoidal force
# FB - 201105017
import math
from PIL import Image, ImageDraw
imgx = 800
imgy = 600
image = Image.new("RGB", (imgx, imgy))
draw = ImageDraw.Draw(image)

# Second Order ODE (y'' = f(x, y, y')) Solver using Euler method
# n : number of steps (higher the better)
# xa: initial value of independent variable
# xb: final value of independent variable
# ya: initial value of dependent variable
# y1a: initial value of first derivative of dependent variable
# Returns value of y, y1 at xb. 
def Euler2(f, xa, xb, ya, y1a, n):
      h = (xb - xa) / float(n)
      x = xa
      y = ya
      y1 = y1a
      for i in range(n):
          y1 += h * f(x, y, y1)
          y += h * y1
          x += h
      return [y, y1]

# Damped spring-mass system driven by sinusoidal force
# y'' = (F0 * math.cos(omega * t - phi) - b * y' - k * y) / m
# y'' : acceleration
# y' : velocity
# y : position
m = 2.0 # mass (kg)
F0 = 4.76 # force amplitude constant (N)
omega = 0.36 # angular frequency (rad/s)
phi = 0.0 # phase constant (rad)
b = 0.0 # friction constant (Ns/m)
k = 20.0 # spring constant (N/m)
def f(x, y, y1):
    return (F0 * math.cos(omega * x - phi) - b * y1 - k * y) / m

yaSim = 0.0 # initial position (m)
y1aSim = 0.0 # initial velocity (m/s)
n = 1000 # number of steps for Euler method
xaSim = 0.0 # initial time of simulation (s)
xbSim = 100.0 # final time of simulation (s)
xdSim = xbSim - xaSim # deltaT of simulation
nSim = 1000 # number of time steps of simulation

# find min and max values of position (needed for the graph)
ya = yaSim
y1a = y1aSim
yMin = ya
yMax = ya
for i in range(nSim):
    xa = xaSim + xdSim * i / nSim
    xb = xaSim + xdSim * (i + 1) / nSim
    y_y1 = Euler2(f, xa, xb, ya, y1a, n)
    ya = y_y1[0]
    y1a = y_y1[1]
    if ya < yMin:
        yMin = ya
    if ya > yMax:
        yMax = ya

# draw the graph
ya = yaSim
y1a = y1aSim
for i in range(nSim):
    xa = xaSim + xdSim * i / nSim
    xb = xaSim + xdSim * (i + 1) / nSim
    kxa = (imgx - 1) * (xa - xaSim) / xdSim
    kya = (imgy - 1) * (ya - yMin) / (yMax - yMin)
    y_y1 = Euler2(f, xa, xb, ya, y1a, n)
    ya = y_y1[0]
    y1a = y_y1[1]
    kxb = (imgx - 1) * (xb - xaSim) / xdSim
    kyb = (imgy - 1) * (ya - yMin) / (yMax - yMin)
    draw.line((kxa, kya, kxb, kyb), (0, 255, 0)) # (r, g, b)

image.save("Spring_mass system simulation.png", "PNG")
