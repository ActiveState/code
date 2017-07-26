# Synchronized Chaos using Lorenz Attractor
# FB - 201108011
import random

delta = float(10) # Prandtl number
r = float(28)
b = float(8) / 3
h = 1e-3 # time step
def Lorenz(x, y, z):
    dx_dt = delta * (y - x)
    dy_dt = r * x - y - x * z
    dz_dt = x * y - b * z
    x += dx_dt * h
    y += dy_dt * h
    z += dz_dt * h
    return (x, y, z)

maxIt = 2000
size = 30

# initial state of the driver system
x = random.random() * size * 2 - 1
y = random.random() * size * 2 - 1
z = random.random() * size * 2 - 1

# initial state of the sub-system
# x1 = random.random() * size * 2 - 1
y1 = random.random() * size * 2 - 1
z1 = random.random() * size * 2 - 1

for i in range(maxIt):
    (x, y, z) = Lorenz(x, y, z)
    # x variable of the driver is chosen as driver signal
    (x1, y1, z1) = Lorenz(x, y1, z1)
    # 2 y and 2 z values should become synched w/ time
    print '(%04i, %+07.3f, %+07.3f, %+07.3f, %+07.3f)' % (i, y, y1, z, z1)
