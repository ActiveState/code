# FB - 201104096
import math
# First Order ODE (y' = f(x, y)) Solver using Euler method
# xa: initial value of independent variable
# xb: final value of independent variable
# ya: initial value of dependent variable
# n : number of steps (higher the better)
# Returns value of y at xb. 
def Euler(f, xa, xb, ya, n):
      h = (xb - xa) / float(n)
      x = xa
      y = ya
      for i in range(n):
          y += h * f(x, y)
          x += h
      return y

# Second Order ODE (y'' = f(x, y, y')) Solver using Euler method
# y1a: initial value of first derivative of dependent variable
def Euler2(f, xa, xb, ya, y1a, n):
      h = (xb - xa) / float(n)
      x = xa
      y = ya
      y1 = y1a
      for i in range(n):
          y1 += h * f(x, y, y1)
          y += h * y1
          x += h
      return y

if __name__ == "__main__":
    print Euler(lambda x, y: math.cos(x) + math.sin(y), 0, 1, 1, 1000)
    print Euler2(lambda x, y, y1: math.sin(x * y) - y1, 0, 1, 1, 1, 1000)
