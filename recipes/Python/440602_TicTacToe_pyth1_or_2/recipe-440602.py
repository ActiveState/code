print "Welcome to TicTacToe (v.3)"
print "In this version I added a computer"

xwins = 0
owins = 0
tiewins = 0

def xturn():                        #player x's move
    global pc
    global n
    global z
    if z == 0:
        ocheck()
    if n == 9:
        
        global a
        global b
        global c
        global d
        global e
        global f
        global g
        global h
        global i

        x = input ("Player X, type the number you want to place an X: ")
        print "X = ",x

        if x == 1:
            xtest(a)
            a = "X"
        elif x == 2:
            xtest(b)
            b = "X"
        elif x == 3:
            xtest(c)
            c = "X"
        elif x == 4:
            xtest(d)
            d = "X"
        elif x == 5:
            xtest(e)
            e = "X"
        elif x == 6:
            xtest(f)
            f = "X"
        elif x == 7:
            xtest(g)
            g = "X"
        elif x == 8:
            xtest(h)
            h = "X"
        elif x == 9:
            xtest(i)
            i = "X"
        else:
            print "That is not a valid entry, please enter an interger between 1-9"
            xturn()
            
        if pc == 2:
            print
            print a,"|",b,"|",c
            print "---------"
            print d,"|",e,"|",f
            print "---------"
            print g,"|",h,"|",i
            print
            z = 0
            oturn()
        elif pc == 1:
            z = 0
            ocomputer()

def oturn():                                                # player o's move
    global n
    global z
    if z == 0:
        xcheck()
    if n == 9:

        global a
        global b
        global c
        global d
        global e
        global f
        global g
        global h
        global i

        o =  input ("Player O, type the number you want to place an O: ")
        print "O = ",o

        if o == 1:
            otest(a)
            a = "O"
        elif o == 2:
            otest(b)
            b = "O"
        elif o == 3:
            otest(c)
            c = "O"
        elif o == 4:
            otest(d)
            d = "O"
        elif o == 5:
            otest(e)
            e = "O"
        elif o == 6:
            otest(f)
            f = "O"
        elif o == 7:
            otest(g)
            g = "O"
        elif o == 8:
            otest(h)
            h = "O"
        elif o == 9:
            otest(i)
            i = "O"
        else:
            print "That is not a valid entry, please enter an interger between 1-9"
            oturn()
        print
        print
        print a,"|",b,"|",c
        print "---------"
        print d,"|",e,"|",f
        print "---------"
        print g,"|",h,"|",i
        print
        z = 0
        xturn()

def xcheck():                                                   #checks to see if last move made x win                               
    global z
    global pc
    if   a == "X" and b == "X" and c == "X":
        xwin()
    elif b == "X" and e == "X" and h == "X":
        xwin()
    elif d == "X" and e == "X" and f == "X":
        xwin()
    elif a == "X" and d == "X" and g == "X":
        xwin()
    elif g == "X" and h == "X" and i == "X":
        xwin()
    elif c == "X" and f == "X" and i == "X":
        xwin()
    elif a == "X" and e == "X" and i == "X":
        xwin()
    elif c == "X" and e == "X" and g == "X":
        xwin()
    elif a != 1 and b != 2 and c != 3 and d != 4 and e != 5 and f != 6 and g != 7 and h != 8 and i != 9:
        tie()
    else:
        z = 1
        if pc == 2:
            oturn()
        elif pc == 1:
            ocomputer()

def ocheck():                                       #checks to see if last move made o win 
    global z
    if   a == "O" and b == "O" and c == "O":
        owin()
    elif b == "O" and e == "O" and h == "O":
        owin()
    elif d == "O" and e == "O" and f == "O":
        owin()
    elif a == "O" and d == "O" and g == "O":
        owin()
    elif g == "O" and h == "O" and i == "O":
        owin()
    elif c == "O" and f == "O" and i == "O":
        owin()
    elif a == "O" and e == "O" and i == "O":
        owin()
    elif c == "O" and e == "O" and g == "O":
        owin()
    elif a != 1 and b != 2 and c != 3 and d != 4 and e != 5 and f != 6 and g != 7 and h != 8 and i != 9:
        tie()
    else:
        z = 1
        xturn()

def otest(num):                                         #checks to see if spot is taken for o's turn
    if num == "X" or num == "O":
        print "This spot has been taken, enter a different spot"
        oturn()

def xtest(num):                                          #check to see if spot is taken for x's turn
    if num == "X" or num == "O":
        print "This spot has been taken, enter a different spot"
        xturn()

def owin():             #executes if o won (from xheck)
    global pc
    global owins
    print "Congratulations O, you have won!"
    owins = owins + 1
    if pc == 2:
        newgame()
    elif pc == 1:
        print
        print a,"|",b,"|",c
        print "---------"
        print d,"|",e,"|",f
        print "---------"
        print g,"|",h,"|",i
        print
        newgame()
        
def xwin():                                         #executes if x won (from ocheck)
    global n
    global xwins
    if n == 9:
        print "Congratulations X, you have won!"
        xwins = xwins + 1
        if pc == 2:
            newgame()
        elif pc == 1:
            print
            print a,"|",b,"|",c
            print "---------"
            print d,"|",e,"|",f
            print "---------"
            print g,"|",h,"|",i
            print
            newgame()

def newgame():                                  #asks is player wants to play another game
    global xwins
    global owins
    global tiewins
    global n
    if n == 9:
        print "X has won",xwins,"times, O has won",owins,"times, and there has been",tiewins,"ties."
        t = raw_input("Do you want to play again? 'y' yes 'n' no: ")
        if t == "y":
            first()
        elif t == "n":
            n = 0
            end()
        else:
            print "That is not a valid entry"
            newgame()
    
def ocomputer():                                    #ocomputer's choice
    global pc
    global n
    global z
    global a
    global b
    global c
    global d
    global e
    global f
    global g
    global h
    global i
    global x

    if z == 0:
        xcheck()
    if n == 9:
        
        if e == 5:                                  #goes to center if spot open
            e = "O"
            
        elif a == 1 and b == "O" and c == "O":          #checks for open spot for immediate win
            a = "O"
        elif a == 1 and d == "O" and g == "O":
            a = "O"
        elif a == 1 and e == "O" and i == "O":
            a = "O"
        elif b == 2 and e == "O" and h == "O":
            b = "O"
        elif b == 2 and a == "O" and c == "O":
            b = "O"
        elif c == 3 and b == "O" and a == "O":
            c = "O"
        elif c == 3 and f == "O" and i == "O":
            c = "O"
        elif c == 3 and e == "O" and g == "O":
            c = "O"
        elif d == 4 and e == "O" and f == "O":
            d = "O"
        elif d == 4 and a == "O" and g == "O":
            d = "O"
        elif f == 6 and c == "O" and i == "O":
            f = "O"
        elif f == 6 and e == "O" and d == "O":
            f = "O"
        elif g == 7 and d == "O" and a == "O":
            g = "O"
        elif g == 7 and e == "O" and c == "O":
            g = "O"
        elif g == 7 and h == "O" and i == "O":
            g = "O"
        elif h == 8 and e == "O" and b == "O":
            h = "O"
        elif h == 8 and i == "O" and g == "O":
            h = "O"
        elif i == 9 and h == "O" and g == "O":
            i = "O"
        elif i == 9 and e == "O" and a == "O":
            i = "O"
        elif i == 9 and f == "O" and c == "O":
            i = "O"

        elif a == 1 and b == "X" and c == "X":                  # checks for immediate loss
            a = "O"
        elif a == 1 and d == "X" and g == "X":
            a = "O"
        elif a == 1 and e == "X" and i == "X":
            a = "O"
        elif b == 2 and e == "X" and h == "X":
            b = "O"
        elif b == 2 and a == "X" and c == "X":
            b = "O"
        elif c == 3 and b == "X" and a == "X":
            c = "O"
        elif c == 3 and f == "X" and i == "X":
            c = "O"
        elif c == 3 and e == "X" and g == "X":
            c = "O"
        elif d == 4 and e == "X" and f == "X":
            d = "O"
        elif d == 4 and a == "X" and g == "X":
            d = "O"
        elif f == 6 and c == "X" and i == "X":
            f = "O"
        elif f == 6 and e == "X" and d == "X":
            f = "O"
        elif g == 7 and d == "X" and a == "X":
            g = "O"
        elif g == 7 and e == "X" and c == "X":
            g = "O"
        elif g == 7 and h == "X" and i == "X":
            g = "O"
        elif h == 8 and e == "X" and b == "X":
            h = "O"
        elif h == 8 and i == "X" and g == "X":
            h = "O"
        elif i == 9 and h == "X" and g == "X":
            i = "O"
        elif i == 9 and e == "X" and a == "X":
            i = "O"
        elif i == 9 and f == "X" and c == "X":
            i = "O"
        elif e == 5 and a == "X" and i == "X":
            e = "O"
        elif e == 5 and b == "X" and h == "X":
            e = "O"
        elif e == 5 and c == "X" and g == "X":
            e = "O"
        elif e == 5 and f == "X" and d == "X":
            e = "O"

        elif a == "X" and f == "X" and c == 3:
            c = "O"
        elif a == "X" and h == "X" and g == 7:
            g = "O"
        elif a == "X" and i == "X" and b == 2:
            b = "O"
        elif b == "X" and f == "X" and c == 3:
            c = "O"
        elif b == "X" and h == "X" and f == 6:
            f = "O"
        elif b == "X" and d == "X" and a == 1:
            a = "O"
        elif b == "X" and g == "X" and a == 1:
            a = "O"
        elif c == "X" and d == "X" and a == 1:
            a = "O"
        elif c == "X" and g == "X" and b == 2:
            b = "O"
        elif c == "X" and h == "X" and i == 9:
            i = "O"
        elif d == "X" and f == "X" and b == 2:
            b = "O"
        elif d == "X" and i == "X" and g == 7:
            a = "O"
        elif d == "X" and h == "X" and g == 7:
            g = "O"
        elif f == "X" and g == "X" and i == 9:
            i = "O"
        elif f == "X" and h == "X" and i == 9:
            i = "O"

        elif c == 3:
            c = "O"
        elif a == 1:
            a = "O"
        elif g == 7:
            g = "O"
        elif i == 9:
            i = "O"
        elif b == 2:
            b = "O"
        elif d == 4:
            d = "O"
        elif f == 6:
            f = "O"
        elif h == 8:
            h = "O"

        print
        print a,"|",b,"|",c
        print "---------"
        print d,"|",e,"|",f
        print "---------"
        print g,"|",h,"|",i
        print
    
        z = 0
        xturn()

def tie():                                          #executes if tie game(from x/o check)
    global tiewins
    print "Tie game! You are both losers."
    tiewins = tiewins + 1
    newgame()

def end():                                          #executes if player wants to quit(from newgame)
    global n
    n = 0
    print "Good Bye"
    
def first():                #check to see if end game loops back to here
    global z
    global t
    global w
    global pc
    global a
    global b
    global c
    global d
    global e
    global f
    global g
    global h
    global i
    global x
    global o
    global t
    global n

    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    x = 0
    o = 0
    z = 1
    
    t = 0
    if n != 0:
        pc = input ("Do you want to play a '1' player or '2' player game? ")

        if pc == 1:
            print
            print a,"|",b,"|",c
            print "---------"
            print d,"|",e,"|",f
            print "---------"
            print g,"|",h,"|",i
            print
            n = 9
            xturn()

        if pc == 2:
            n = 9
            w = raw_input ("Who shall go first, 'x' player or 'o' player: ")
            print
            print a,"|",b,"|",c
            print "---------"
            print d,"|",e,"|",f
            print "---------"
            print g,"|",h,"|",i
            print
            if w == "o":
                oturn()
            elif w == "x":
                xturn()
            else:
                print "That is not a valid entry"
                first()

n = 9
first()
