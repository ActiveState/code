from ctypes import *
s = "I'm immutable"
p = cast(c_char_p(s),POINTER(c_char))
p[4] = " "
p[5] = " "
print s
