import os, sys, time

def main():
    if len(sys.argv) != 4:
        print os.path.basename(sys.argv[0]),
        print '<hours> <minutes> <seconds>'
    else:
        try:
            timer(*[int(x) for x in sys.argv[1:]])
        except Exception, error:
            print error

def timer(hours, minutes, seconds):
    time.sleep(abs(hours * 3600 + minutes * 60 + seconds))
    while True:
        print '\x07',

if __name__ == '__main__':
    main()
