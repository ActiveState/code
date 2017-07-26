import re

def cw2us(x): # capwords to underscore notation
    return re.sub(r'(?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])', r"_\g<0>", x).lower()

def mc2us(x): # mixed case to underscore notation
    return cw2us(x)

def us2mc(x): # underscore to mixed case notation
    return re.sub(r'_([a-z])', lambda m: (m.group(1).upper()), x)

def us2cw(x): # underscore to capwords notation
    s = us2mc(x)
    return s[0].upper()+s[1:]

##
## Expected output:
##
## >>> cw2us("PrintHTML")
## 'print_html'
## >>> cw2us("IOError")
## 'io_error'
## >>> cw2us("SetXYPosition")
## 'set_xy_position'
## >>> cw2us("GetX")
## 'get_x'
##
