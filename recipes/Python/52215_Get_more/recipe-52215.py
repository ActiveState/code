import sys, traceback

def print_exc_plus():
    """
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame.
    """
    tb = sys.exc_info()[2]
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()
    traceback.print_exc()
    print "Locals by frame, innermost last"
    for frame in stack:
        print
        print "Frame %s in %s at line %s" % (frame.f_code.co_name,
                                             frame.f_code.co_filename,
                                             frame.f_lineno)
        for key, value in frame.f_locals.items():
            print "\t%20s = " % key,
            #We have to be careful not to cause a new error in our error
            #printer! Calling str() on an unknown object could cause an
            #error we don't want.
            try:                   
                print value
            except:
                print "<ERROR WHILE PRINTING VALUE>"
        
        
if __name__ == '__main__':
    #A simplistic demonstration of the kind of problem this approach can help
    #with. Basically, we have a simple function which manipulates all the
    #strings in a list. The function doesn't do any error checking, so when
    #we pass a list which contains something other than strings, we get an
    #error. Figuring out what bad data caused the error is easier with our
    #new function.
    
    data = ["1", "2", 3, "4"] #Typo: We 'forget' the quotes on data[2]
    def pad4(seq):
        """
        Pad each string in seq with zeros, to four places. Note there
        is no reason to actually write this function, Python already
        does this sort of thing much better.
        Just an example.
        """
        return_value = []
        for thing in seq:
            return_value.append("0" * (4 - len(thing)) + thing)
        return return_value

    #First, show the information we get from a normal traceback.print_exc().    
    try:
        pad4(data)
    except:
        traceback.print_exc()
    print
    print "----------------"
    print

    #Now with our new function. Note how easy it is to see the bad data that
    #caused the problem. The variable 'thing' has the value 3, so we know
    #that the TypeError we got was because of that. A quick look at the
    #value for 'data' shows us we simply forgot the quotes on that item.
    try:
        pad4(data)
    except:
        print_exc_plus()
