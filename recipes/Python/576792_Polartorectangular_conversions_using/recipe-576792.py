def to_polar(x, y):
    'Rectangular to polar conversion using ints scaled by 100000. Angle in degrees.'
    theta = 0
    for i, adj in enumerate((4500000, 2656505, 1403624, 712502, 357633, 178991, 89517, 44761)):
        sign = 1 if y < 0 else -1
        x, y, theta = x - sign*(y >> i) , y + sign*(x >> i), theta - sign*adj
    return theta, x * 60726 // 100000

def to_rect(r, theta):
    'Polar to rectangular conversion using ints scaled by 100000. Angle in degrees.'
    x, y = 60726 * r // 100000, 0
    for i, adj in enumerate((4500000, 2656505, 1403624, 712502, 357633, 178991, 89517, 44761)):
        sign = 1 if theta > 0 else -1
        x, y, theta = x - sign*(y >> i) , y + sign*(x >> i), theta - sign*adj
    return x, y

if __name__ == '__main__':
    print(to_rect(471700, 5799460))     # r=4.71700  theta=57.99460
    print(to_polar(250000, 400000))     # x=2.50000  y=4.00000
