###
simplecom1: i/o through the com1 port whose transmission parameters have already been
configured through the Windows Device Manager; limited, but requires no special support
beyond the win32file module. If you'd rather use ReadFile() directly to do your own
protocol and ignore readcom1line(), feel free! My use of this is limited to reading,
but also feel free to try win32file.WriteFile with the comhandle below.
readcom1line() accumulates received data until it gets a carriage return. No carriage
return, no readcom1line() return! Similar to keyboard prompting, but may not meet your
needs except for prototyping.
If you use this and get an Access Denied exception, it will probably be because some 
other process has the com1 port open already, or maybe your own process (possibly
Pythonwin or some other development environment) opened it and hasn't closed it,
which is just as bad. Don't let go of the open comhandle until you've closed the port!
Also, if you have the Palm Pilot True Sync manager running on com1, you'll need to Exit it
to release the com1 port. Ditto for HyperTerm or any other process that has com1 open.
###

import win32file

def clearcom1receivebuf(comhandle):
    # clear out unwanted data from previous transmissions to com1
    win32file.PurgeComm(comhandle, win32file.PURGE_RXCLEAR)

def closecom1(comhandle):
    comhandle.Close()

def opencom1():
    # returns a handle to the Windows file
    return win32file.CreateFile(u'COM1:', win32file.GENERIC_READ, \
                                0, None, win32file.OPEN_EXISTING, 0, None)

def readcom1line(comhandle):
    err = 0
    char = None
    line = ''
    while err == 0 and char != '\r':
        err, char = win32file.ReadFile(comhandle, 1, None)
        if err == 0:
            if char == '\n':
                pass # eat newlines
            else:
                line = line + char
        else:
            break
    return line

if __name__ == '__main__':
    # demo
    comhandle = opencom1()
    print readcom1line(comhandle)
    closecom1(comhandle)
