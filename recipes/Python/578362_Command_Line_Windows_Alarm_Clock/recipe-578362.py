try:
    import os
    import sys
    import time
    import msvcrt
    import winsound
except ImportError, error:
    sys.stdout.write('ImportError: %s' % error)
    sys.exit(1)

def main():
    try:
        arg = time.strptime(sys.argv[1], '%H:%M')
        arg_sec = (arg.tm_hour * 60 + arg.tm_min) * 60
        now = time.localtime()
        now_sec = (now.tm_hour * 60 + now.tm_min) * 60 + now.tm_sec
        alarm(arg_sec - now_sec + (86400 if arg_sec <= now_sec else 0))
    except:
        sys.stdout.write('Usage: %s HH:MM' % os.path.basename(sys.argv[0]))

def alarm(seconds):
    time.sleep(seconds)
    while msvcrt.kbhit():
        msvcrt.getch()
    while not msvcrt.kbhit():
        winsound.Beep(440, 250)
        time.sleep(0.25)

if __name__ == '__main__':
    main()
