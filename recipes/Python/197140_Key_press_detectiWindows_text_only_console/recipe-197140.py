def keypress(): 
    """
    Waits for the user to press a key. Returns the ascii code 
    for the key pressed or zero for a function key pressed.
    """                             
    import msvcrt               
    while 1:
        if msvcrt.kbhit():              # Key pressed?
            a = ord(msvcrt.getch())     # get first byte of keyscan code     
            if a == 0 or a == 224:      # is it a function key?
                msvcrt.getch()          # discard second byte of key scan code
                return 0                # return 0
            else:
                return a                # else return ascii code


def funkeypress():
    """
    Waits for the user to press any key including function keys. Returns 
    the ascii code for the key or the scancode for the function key.
    """
    import msvcrt
    while 1:
        if msvcrt.kbhit():                  # Key pressed?
            a = ord(msvcrt.getch())         # get first byte of keyscan code  
            if a == 0 or a == 224:          # is it a function key?
                b = ord(msvcrt.getch())     # get next byte of key scan code
                x = a + (b*256)             # cook it.
                return x                    # return cooked scancode
            else:
                return a                    # else return ascii code

def anykeyevent():
    """
    Detects a key or function key pressed and returns its ascii or scancode.
    """
    import msvcrt
    if msvcrt.kbhit():
        a = ord(msvcrt.getch())
        if a == 0 or a == 224:
            b = ord(msvcrt.getch())
            x = a + (b*256)
            return x
        else:
            return a

# -----------------------------------------------------------------------------
                         # demo applications.

def about(): return\
    """
    Keys reported: ENTER, comma, period, greater-than, less-than.
    Upper and lower case keys:  A, C, H, Q.
    Function Keys: F1, SHIFT-F1, CTRL-F1, ALT-F1, Left arrow,
    right arrow, page up, page down.

    Any other keys are assigned to print "Default"
    Pressing ESC or Q will initiate exit query.
    Pressing A will print this text.
    """

def keycommands(x):
    if x == 13:                                 # ENTER
        print 'ENTER pressed'
        return True
    if x in map(ord,'aA'):                      # A
        print about()
        return True
    if x in map(ord,'cC'):                      # C
        print 'Continue'
        return True
    if x in map(ord,'hH'):                      # H
        print 'HELP'
        return True
    if x in map(ord,'qQ') or x == 27:           # Q or ESC
        print 'Press any key to exit.'
        keypress()
        print 'Bye'
        return False                             
    if x == ord(','):                           # ,
        print 'Comma'
        return True
    if x == ord('.'):                           # .
        print 'Period'
        return True
    if x == ord('>'):                           # >
        print 'Greater Than'
        return True
    if x == ord('<'):                           # <
        print 'Less Than'
        return True
    if x == 15104:                              # F1
        print 'F1'
        return True
    if x == 21504:                              # SHIFT-F1
        print 'SHIFT-F1'
        return True
    if x == 24064:                              # CTRL-F1
        print 'CNTRL-F1'
        return True
    if x == 26624:                              # ALT-F1
        print 'ALT-F1'
        return True
    if x == 18912:                              # PAGE UP
        print 'PAGE UP'
        return True
    if x == 20960:                              # PAGE DOWN
        print 'PAGE DOWN'
        return True
    if x == 19424:                              # LEFT ARROW KEY
        print 'LEFT ARROW KEY'
        return True
    if x == 19936:                              # RIGHT ARROW KEY
        print 'RIGHT ARROW KEY'
        return True
    print 'Default'                             # Any remaining keys
    return True

def validating(x):
    if x in map(ord,'hH'):          # query if help is needed
        print 'Would you like to see the help menu? <y/n>',
        if keypress() in map(ord,'yY'):
            return ord('h')         # help needed
        else:  return ord('c')      # help not needed
    if x in map(ord,'qQ'):          # query if quitting is requested
        print 'Would you like to quit? <y/n>',
        if keypress() in map(ord,'yY'):
            return ord('q')         # quit
        else: return ord('c')       # don't quit
    return x                        # otherwise, x is any key other than H,Q.

                    #################################
                    # The keypress interpreter demo #
                    #################################
def commandloop():                  
    print 'Keypress interpreter utility.'
    print about()
    print 'Waiting...'
    interpreting=True
    while interpreting:
        interpreting=keycommands(validating(funkeypress()))

                   ####################################
                   # The IBM scancode display utility #
                   ####################################
def scancode():                     
    print 'IBM scancode utility.\nPress CTRL-C to quit.'
    while 1:
        x=funkeypress()
        print 'Dec: %d Hex: %x' % (x,x)

                         ########################
                         # The Exit key example #
                         ########################
def exitkey():                      
    x = True
    while x != 20448:               # END key?
        print 'o',
        x = anykeyevent()           # key?
        if x == 20448 : break       # if END key touched, then break.
        elif x == None: continue    # if no key touched, continue printing.
        else:                       # if other key touched, prompt user.
            print '\nPress END key to exit. Other key to continue printing.'
            x = funkeypress()

#------------------------------------------------------------------------------
                                 # The main loop.

if __name__ == '__main__':          
    while 1:
        print """Please select one from the menu:
        [1] Keypress interpreter demo.
        [2] IBM scancode utility.
        [3] Exit key example\n"""    
        x=keypress()
        if x == ord('1'): commandloop()
        if x == ord('2'): scancode()
        if x == ord('3'): exitkey()
        print 'Press q to quit.\n'
        if keypress() in map(ord,'qQ'):
            break
        else:
            continue
        
