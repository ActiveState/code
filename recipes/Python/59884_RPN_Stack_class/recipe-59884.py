"""
rb_stack 1.0:  A (less and less) simple stack class.
Copyright (C) 2000 Gordon Worley.

To contact me, please visit my Web site at <http://www.rbisland.cx/> or e-mail me at <redbird@rbisland.cx>.

History:

1.0 - Added trigonometric functions and inverse.
0.9 - Updated for Python 2.0.  Uses the new self modifying math operators (+=, *=, **=, etc.).
0.8 - Added neg_all() to RPN_Stack.
0.7.9 - Oops, found bug in do all methods.  Called flush() as an attribute rather than as a function.
0.7.8 - Added negation function.
0.7.7 - Added functions to do operations to all registers in stack.
0.7.1 - Removed some error handeling.  Eventually all will be removed to make it easier for implimentations to display errors.
0.7 - Added math to RPN_Stack.  Removed math from rpn.py.
0.6.5 - Added flush to Stack.
0.6.4 - Found and squashed bug in roll up/down functions in Stack.
0.6.3 - Pop now allows multiple pops using extra optional argument.
0.6.2 - Added register roll functions to RPN_Stack.
0.6 - Created RPN_Stack to add RPN specific stack functions.  Moved flip_xy to RPN_Stack.
0.5.3 - Added flip_xy
0.5.2 - Added stack roll functions.
0.5 - Complete rewrite.  Thanks to Programming Python for some sample code in building this stack class.
0.1 - A few bug fixes and added flip_xy.  Initial release.
0.0 - Just a few built-in methods overridden.
"""
import math  #this is just until I can get it to import only in RPN_Stack

class Stack:
       
        def __init__(self, start=[]):
                self.stack = []
                for x in start: self.push(x)
                self.reverse()

        #these first few carry out basic stack functions.  always necessary

        def push(self, item):
                self.stack = [item] + self.stack

        def pop(self, num_of_loops=1):
                x=[]
                curr_loop=0
                while curr_loop < num_of_loops:
                        try:
                                x, self.stack = x + [self.stack[0]], self.stack[1:]
                        except:
                                pass #return "error:  stack underflow"
                        curr_loop += 1
                return tuple(x)

        def empty(self):  #returns true if stack is empty
                return not self.stack
               
        def flush(self):
                self.stack = []
               
        #some extra stack functions that make things nicer
       
        def roll_down(self):
                try:
                        self.stack=self.stack[1:]+[self.stack[0]]
                except:
                        print "error:  stack underflow"

        def roll_up(self):
                try:
                        self.stack=[self.stack[-1]]+self.stack[:-1]
                except:
                        print "error:  stack underflow"
                       
        #okay, enough of that.  now to overload opperators

        def __repr__(self):
                return '%s' % self.stack

        def __cmp__(self, other):
                return cmp(self.stack, other.stack)

        def __len__(self):
                return len(self.stack)

        def __add__(self, other):
                return Stack(self.stack + other.stack)

        def __mul__(self, reps):
                return Stack(self.stack * reps)

        def __getitem__(self, index):
                return self.stack[index]

        def __getslice__(self, low, high):
                return Stack(self.stack[low:high])

        def __getattr__(self, name):
                return getattr(self.stack, name)



class RPN_Stack(Stack):
               
        def getx(self):  #get x register (bottom)
                try:
                        self.stack[0]
                except:
                        return "error:  stack underflow"
                return self.stack[0]
       
        def gety(self):  #get y register
                try:
                        self.stack[1]
                except:
                        return "error:  stack underflow"
                return self.stack[1]

        def getz(self):  #get z register
                try:
                        self.stack[2]
                except:
                        return "error:  stack underflow"
                return self.stack[2]

        def gett(self):  #get t register (top)
                try:
                        self.stack[3]
                except:
                        return "error:  stack underflow"
                return self.stack[3]
               
        #roll the stack around
               
        def roll_regs_down(self):
                try:  #try with all four registers
                        self.stack[0], self.stack[1], self.stack[2], self.stack[3]=self.stack[1], self.stack[2], self.stack[3], self.stack[0]
                except:
                        try:  #well, maybe there are just three
                                self.stack[0], self.stack[1], self.stack[2]=self.stack[1], self.stack[2], self.stack[0]
                        except:  #if there aren't two, the stack is too small
                                self.flip_xy()
       
        def roll_regs_up(self):
                try:  #try with all four registers
                        self.stack[0], self.stack[1], self.stack[2], self.stack[3]=self.stack[3], self.stack[0], self.stack[1], self.stack[2]
                except:
                        try:  #well, maybe there are just three
                                self.stack[0], self.stack[1], self.stack[2]=self.stack[2], self.stack[0], self.stack[1]
                        except:  #if there aren't two, the stack is too small
                                self.flip_xy()
               
        def flip_xy(self):  #flip the x and y registers
                try:
                        self.stack[0], self.stack[1] = self.stack[1], self.stack[0]
                except:
                        print "error:  stack underflow"
                       
        #do some math
       
        def add(self):
                newx = self.gety() + self.getx()
                self.pop(2); self.push(newx)
               
        def sub(self):
                newx = self.gety() - self.getx()
                self.pop(2); self.push(newx)
       
        def mul(self):
                newx = self.gety() * self.getx()
                self.pop(2); self.push(newx)
       
        def div(self):
                newx = self.gety() / self.getx()
                self.pop(2); self.push(newx)
       
        def modulo(self):
                newx = self.gety() % self.getx()
                self.pop(2); self.push(newx)
       
        def pow(self):  #raise y register to the x power
                newx = self.gety()**self.getx()
                self.pop(2); self.push(newx)
               
        def neg(self):  #negate
                newx = -self.getx()
                self.pop(); self.push(newx)
               
        def sin(self):
                newx = math.sin(self.getx())
                self.pop(); self.push(newx)
               
        def cos(self):
                newx = math.cos(self.getx())
                self.pop(); self.push(newx)
       
        def tan(self):
                newx = math.tan(self.getx())
                self.pop(); self.push(newx)
       
        def arcsin(self):
                newx = math.asin(self.getx())
                self.pop(); self.push(newx)
               
        def arccos(self):
                newx = math.acos(self.getx())
                self.pop(); self.push(newx)
       
        def arctan(self):
                newx = math.atan(self.getx())
                self.pop(); self.push(newx)
               
        def inverse(self):
                newx = 1 / self.getx()
                self.pop(); self.push(newx)
       
        #same as above, but acting over whole list
       
        def add_all(self):
                newx=self.getx()
                for x in self.stack[1:]:
                        newx += x
                self.flush(); self.push(newx)
               
        def sub_all(self):
                newx=self.getx()
                for x in self.stack[1:]:
                        newx -= x
                self.flush(); self.push(newx)
       
        def mul_all(self):
                newx=self.getx()
                for x in self.stack[1:]:
                        newx *= x
                self.flush(); self.push(newx)
       
        def div_all(self):
                newx=self.getx()
                for x in self.stack[1:]:
                        newx /= x
                self.flush(); self.push(newx)
       
        def modulo_all(self):
                newx=self.getx()
                for x in self.stack[1:]:
                        newx %= x
                self.flush(); self.push(newx)
               
        def pow_all(self):
                newx=self.getx()
                for x in self.stack[1:]:
                        newx **= x
                self.flush(); self.push(newx)
               
        def neg_all(self):
                index=0
                while index < len(self.stack):
                        self.stack[index] = -self.stack[index]
                        index += 1
       
        def sin_all(self):
                index = 0
                while index < len(self.stack):
                        self.stack[index] = math.sin(self.stack[index])
                        index += 1

        def cos_all(self):
                index = 0
                while index < len(self.stack):
                        self.stack[index] = math.cos(self.stack[index])
                        index += 1
                       
        def tan_all(self):
                index = 0
                while index < len(self.stack):
                        self.stack[index] = math.tan(self.stack[index])
                        index += 1
                       
        def arcsin_all(self):
                index = 0
                while index < len(self.stack):
                        self.stack[index] = math.asin(self.stack[index])
                        index += 1

        def arccos_all(self):
                index = 0
                while index < len(self.stack):
                        self.stack[index] = math.acos(self.stack[index])
                        index += 1
                       
        def arctan_all(self):
                index = 0
                while index < len(self.stack):
                        self.stack[index] = math.atan(self.stack[index])
                        index += 1
                       
        def inverse_all(self):
                index = 0
                while index < len(self.stack):
                        self.stack[index] = 1 / self.stack[index]
                        index += 1
