# color module #
# color.py #

def default():
    import os
    os.system("color 07")
# default CMD black background with white text

def matrix():
    import os
    os.system("color 0a")
# black background with bright green text

def sky():
    import os
    os.system("color bf")
# sky-blue background with white text

def egypt():
    import os
    os.system("color 0e")
# black background with yellow text

def evil():
    import os
    os.system("color 0c")
# black background with red text

def fire():
    import os
    os.system("color ce")
# red background with yellow text

def metallic():
    import os
    os.system("color 08")
# black background with grey text

def metal():
    import os
    os.system("color 80")
# grey background with black text

def gillette():
    import os
    os.system("color 1e")
# blue background with yellow text

def bee():
    import os
    os.system("color e0")
# yellow background with black text

def set(c):
    import os
    colorprep = "color %s" % c
    color = colorprep
    os.system(color)
# custom color scheme | ie. "set(4a)"
# see "color.directory()"

def directory():
    import os
    os.system("color color")
# displays color variables
