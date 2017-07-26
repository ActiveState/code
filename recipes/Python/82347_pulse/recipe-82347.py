import commands
import time
import os,sys,string
def main(comd,inc=60):
    while 1:
        os.system(comd)
        time.sleep(inc)



if __name__ == '__main__' :

    if len(sys.argv) <= 1:
        print "usage: " + sys.argv[0] + " command [increment]"
        sys.exit(1)
    comd = sys.argv[1]
    if len(sys.argv) < 3:
        main(comd)
    else:
        inc = string.atoi(sys.argv[2])
        main(comd,inc)
