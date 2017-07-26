"""
If you've saved all...
  Terminal output of the "Bash completed man and info pages generation" recipe
the bash.py from

http://code.activestate.com/recipes/577854-bash-completed-man-and-info-pages-generation/

Then modify the log file to have no extra lines or anything foriegn but
the output (again, NO PROMPTS, etc)

run this script without arguments and it generates a file "new_bash.py.log"
from a MUST exist "bash.py.log" in the pwd.
If a file named that already exist this WILL rewrite the file (no bkups).

"""
zero = "3 of 3181 : ./"                                                 #0
one = "No manual entry for [["                                          #1
two = "info: Writing node (*manpages*)7z..."                            #2
three = "info: Done."                                                   #3
four = "man: ./: Is a directory"                                        #4
five = "info: No menu item `[[' in node `(dir)Top'."                    #5
six = "gzip: stdout: Broken pipe"                                       #6
seven = "<standard input>:104: warning [p 1, 4.7i, div `3tbd6,1', 0.2i]: can't break line" #7
eight = "man: can't open /usr/share/man/tc-cbq.8: No such file or directory"               #8
ids = (0,   1,    2,   3,     4,    5,    6,   7,     8)
ini = (zero, one, two, three, four, five, six, seven, eight)
mine = zero



def chk(line):
    dat = line.split(" ")
    if len(dat) > 1:
        if len(dat[0]) > 1:

            if dat[0].isdigit():
                return zero
            if dat[0] == "No":
                return one
            if dat[0] == "info:":

                if dat[1][0] == "D":
                    return two
                elif dat[1][0] == "W":
                    return three
                else:
                    return five
            if dat[0] == "man:":
                #print dat[0], dat[1]
                if dat[1] == "can't":
                    return eight
                else:
                    return four
            if dat[0] == "gzip:":
                return six
            if dat[0][0] == "<":
                return seven

man1, man2, man3 = [], [], []
info1, info2, info3 = [], [], []
pipe1, pipe2 = [], []

def deal(f):
    __f = open(f)
    lines = __f.readlines()
    __f.close()

    #man1, man2, man3 = one, four, eight
    #info1, info2, info3 = two, three, five
    #pipe1, pipe2 = six, seven
    for t in lines:
        if chk(t) is zero:
            pass#print "passing..."
        if chk(t) is one:
            man1.append(t)
        if chk(t) is two:
            info1.append(t)
        if chk(t) is three:
            info2.append(t)
        if chk(t) is four:
            man2.append(t)
        if chk(t) is five:
            info3.append(t)
        if chk(t) is six:
            pipe1.append(t)
        if chk(t) is seven:
            pipe2.append(t)
        if chk(t) is eight:
            man3.append(t)

def hmm(ls):
    hm = ""
    for t in ls:
        hm += t
    return hm
def main(f, d):
    deal(f)
    lses = [man1, man2, man3, info1, info2, info3, pipe1, pipe2]
    hm = ""
    for l in lses:
        hm += hmm(l)
        print l[0], len(l)    #the only print statement...
    nf = open(d, 'w')
    nf.write(hm)
    nf.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process the messy log to new less messy file.')
    parser.add_argument('-src', metavar='s', default="bash.py.log", help='src log file')
    parser.add_argument('-dest', metavar='d', default="new_bash.py.log", help='dest log file')

    args = parser.parse_args()

    main(args.src, args.dest)











"""
1 of 3181 : :
2 of 3181 : !
3 of 3181 : ./
No manual entry for !
No manual entry for ./
No manual entry for [[
info: Writing node (*manpages*):...
info: Writing node (*manpages*)[...
info: Writing node (*manpages*)7z...
info: Done.
info: Done.
info: Done.
man: ./: Is a directory
man: ./: Is a directory
man: ./: Is a directory
info: No menu item `!' in node `(dir)Top'.
info: No menu item `./' in node `(dir)Top'.
info: No menu item `[[' in node `(dir)Top'.
gzip: stdout: Broken pipe
gzip: stdout: Broken pipe
gzip: stdout: Broken pipe
<standard input>:81: warning [p 1, 4.7i, div `3tbd2,1', 0.3i]: can't break line
<standard input>:92: warning [p 1, 4.7i, div `3tbd4,1', 0.3i]: can't break line
<standard input>:104: warning [p 1, 4.7i, div `3tbd6,1', 0.2i]: can't break line
man: can't open /usr/share/man/tc-cbq.8: No such file or directory
man: can't open /usr/share/man/tc-cbq.8: No such file or directory
man: can't open /usr/share/man/tc-cbq.8: No such file or directory
"""
