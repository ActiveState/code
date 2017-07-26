Most user have a lot of problem when using a terminal, so when a script must interact whit them,
 a panic take the user... 
So, EasyDialogs can help us, they contain a few basic dialog for the interaction of the user, 
string interaction, file/dir interaction, parameter interaction and more....

The following program, is a simple image converter/resizer, obviously the interaction is required, 
and with the magic of Easydialogs module, we can interact without write a single character.

#Starting with some header
import EasyDialogs
import os
import Image
import sys

# Number one dialog, this one take the parameter, tuples indicate command and description,
# First list the option (maybe with parameter if followed by ':' or '='), second list the sum of the command 
rotater = ('Rotate right', 'Rotate image by 90 degrees clockwise')
rotatel = ('Rotate left', 'Rotate image by 90 degrees anti-clockwise')
scale = ('Makethumb', 'Make a 100x100 thumbnail')
str = ['Format JPG', 'Format PNG']
cmd = [rotater, rotatel, scale]

# This dialog take some argument, the two list (argument, and command), and if user can add file or directory
optlist = EasyDialogs.GetArgv(str, cmd, addoldfile = 0, addnewfile = 0, addfolder = 1)

dir = []
format = "JPEG"
rotationr = 0
rotationl = 0
resize = 0
val = 0

# Parsing argument, we can do it also with getopt, but take it easy
for arg in optlist:
    if arg == "--Format JPG":
        format = "JPEG"
    if arg == "--Format PNG":
        format = "PNG"
    if arg == "Rotate right":
        rotationr = 1
        print rotationr
    if arg == "Rotate left":
        rotationl = 1
    if arg == "Makethumb":
        resize = 1
    if os.path.isdir(arg):
        dir.append(arg)

if len(dir) == 0:
    EasyDialogs.Message("Dir not specified")
    sys.exit(0)

# Second dialog, this open a pathfinder for chosing dir, and return the complete path
path = EasyDialogs.AskFolder("Chose destination dir")
if not path:
    sys.exit(0)

# This is for late, is ugly, but it work
for num in dir:
    for item in os.listdir(num):
        val += 1

# Obviusly if path is not a dir, we want to exit
if os.path.isdir(path) :
    pass
else:
    # Third dialog, display feedback message, very simple and usefull
    EasyDialogs.Message("Directory not found")
    sys.exit(0)
    
# Fourth Dialog, this one is nice, a progress bar, 'val' is the max value, when we reach this, the
# bar is at 100% and disappear, with ProgressBar.inc(num=1), we can increment the number

bar = EasyDialogs.ProgressBar("Resizing", val) # Val is the total number of file
for num in dir:
    for item in os.listdir(num):
        bar.inc()
        try:
            objpict = Image.open(num + "/" + item)
            if resize:
                objpict.thumbnail((100, 100, 1))
            for i in range(rotationr):
                objpict = objpict.rotate(-90)
            for i in range(rotationl):
                objpict = objpict.rotate(90)
            objpict.save(path + "/" + item + "." + format, format)
        except:
            print item + " Not a image"

# Last dialog for this recipe, another message dialog, but with three button, return 1, 0 or -1
score = EasyDialogs.AskYesNoCancel("Do you like this program?")

if score == 1:
    EasyDialogs.Message("Wwowowowow, EasyDialog rulez, ;-)")
if score == 0:
    EasyDialogs.Message("Sigh sigh sigh, i'm a loser... =(")
if score == -1:
    EasyDialogs.Message("Ehi last question was important!!!!")
