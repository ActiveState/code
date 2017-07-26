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
        alarm(*map(float, sys.argv[1:]))
    except:
        sys.stdout.write('Usage: %s <hours> <minutes> <seconds>' % os.path.basename(sys.argv[0]))

def alarm(hours, minutes, seconds):
    time.sleep(abs(hours * 3600 + minutes * 60 + seconds))
    while msvcrt.kbhit():
        msvcrt.getch()
    while not msvcrt.kbhit():
        winsound.Beep(440, 250)
        time.sleep(0.25)

if __name__ == '__main__':
    main()
