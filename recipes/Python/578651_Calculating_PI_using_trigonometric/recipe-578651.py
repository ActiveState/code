# Calculating PI using trigonometric iterations
# FB36 - 20130825
import math

x = 1.0
y = 1.0
z = 1.0
w = 1.0
v = 1.0
u = 1.0

for i in range(30):

    x = math.sin(x) + x
    y = math.cos(y) + y
    z = math.cos(z) + math.sin(z) + z
    w = math.cos(w) - math.sin(w) + w
    v =  math.cos(v) * math.sin(v) + v
    u =  math.cos(u) / math.sin(u) + u
    
    print i
    print x, y * 2.0, z * 4.0 / 3.0, w * 4.0, v * 2.0, u * 2.0
    print
