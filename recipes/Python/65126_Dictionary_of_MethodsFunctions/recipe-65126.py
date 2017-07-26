import string

def function1():
    print "called function 1"

def function2():
    print "called function 2"

def function3():
    print "called function 3"

tokenDict = {"cat":function1, "dog":function2, "bear":function3}

# simulate, say, lines read from a file
lines = ["cat","bear","cat","dog"]

for line in lines:
    
    # lookup the function to call for each line
    functionToCall = tokenDict[line]

    # and call it
    functionToCall()
