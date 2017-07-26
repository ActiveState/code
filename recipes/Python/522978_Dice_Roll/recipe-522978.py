from random import choice as _choice

class die:
  def __init__(self, sides=6):
    try: self.sides = range(1,sides+1)
    except TypeError: self.sides = list(sides)
  
  def __str__(self):
    return str(_choice(self.sides))

'''
#to roll
#default
print die()
#custom number
print die(12)
#custom sides
print die(('yes','no','maybe'))
#changing die
changing=['something','something else','also something']
print die(changing)
changing+=['something new!']
print die(changing)
'''
