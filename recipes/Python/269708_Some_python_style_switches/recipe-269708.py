#==================================================
#   1. Select non-function values:
#==================================================

location = 'myHome'  
fileLocation = {'myHome'   :path1,
                'myOffice' :path2,
                'somewhere':path3}[location]

#==================================================
#   2. Select functions:
#==================================================

functionName = input('Enter a function name')
eval('%s()'%functionName)

#==================================================
#   3. Select values with 'range comparisons':
#==================================================
#
# Say, we have a range of values, like: [0,1,2,3]. You want to get a
# specific value when x falls into a specific range:
#
# x<0   : 'return None'
# 0<=x<1: 'return 1'
# 1<=x<2: 'return 2'
# 2<=x<3: 'return 3'
# 3<=x  : 'return None'
# 
# It is eazy to construct a switch by simply making the above rules
# into a dictionary:

selector={ 
   x<0    : 'return None',
   0<=x<1 : 'return 1',
   1<=x<2 : 'return 2',
   2<=x<3 : 'return 3',
   3<=x   : 'return None'
   }[1]  

# During the construction of the selector, any given x will turn the
# selector into a 2-element dictionary:

selector={ 
   0 : 'return None',
   1 : #(return something you want),
   }[1]  

# This is very useful in places where a selection is to be made upon any
# true/false decision. One more example:

selector={
  type(x)==str  : "it's a str",
  type(x)==tuple: "it's a tuple",
  type(x)==dict : "it's a dict"
  } [1]

#==================================================
#   4. Select functions with 'range comparisons':
#==================================================
#
# You want to execute a specific function when x falls into a specific range:

functionName={
   x<0   : setup,
   0<=x<1: loadFiles,
   1<=x<2: importModules
   }[1]  

functionName()

#==================================================
#   5. and/or style
#==================================================
#
# x = a and 'a' or None
# 
# is same as:
#
# if a: x = 'a'
# else: x = None
# 
# More example: a switch in Basic:
#

Select Case x
   Case x<0    : y = -1 
   Case 0<=x<1 : y =  0
   Case 1<=x<2 : y =  1
   Case 2<=x<3 : y =  2
   Case Else   : y =  'n/a'
End Select  

# 
# in Python
#

y = ( (x<0)    and -1 ) or \
    ( (0<=x<1) and  0 ) or \
    ( (1<=x<2) and  1 ) or \
    ( (2<=x<3) and  2 ) or 'n/a'

  
