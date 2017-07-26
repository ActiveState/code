import msvcrt

while 1:
    print 'Testing..'
    # body of the loop ...
    if msvcrt.kbhit():
	if ord(msvcrt.getch()) == 27:
	    break


"""
Here the key used to exit the loop was <ESC>, chr(27).

You can use the following variation for special keys:

    if ord(msvcrt.getch()) == 0:
        if ord(msvcrt.getch()) == 59:    # <F1> key
            break

With the following, you can discover the codes for the special keys:
    if ord(msvcrt.getch()) == 0:
        print ord(msvcrt.getch())
        break
	    
Use getche() if you want the key pressed be echoed."""
