import msvcrt
import time
import webbrowser
import winsound

def main():
    url = raw_input('URL = ')
    while True:
        try:
            timeout = float(raw_input('Timeout = ')) * 60
            if timeout > 0:
                break
            print 'Timeout must be positive.'
        except:
            print 'Timeout must be a number.'
    while True:
        print 'Executing ...'
        start = time.clock()
        while time.clock() - start < timeout:
            webbrowser.open(url, False, False)
            time.sleep(0.5)
        getch_all(False)
        while not msvcrt.kbhit():
            winsound.Beep(1000, 500)
            time.sleep(0.5)
        getch_all(False)
        print 'Pausing ...'
        if getch_all(True) == '\x1b':
            break

def getch_all(block):
    if block:
        buf = msvcrt.getch()
    else:
        buf = str()
    while msvcrt.kbhit():
        buf += msvcrt.getch()
    return buf

if __name__ == '__main__':
    main()
