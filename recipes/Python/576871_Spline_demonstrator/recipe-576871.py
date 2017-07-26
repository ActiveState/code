import Tkinter
from Tkinter import*

def mod(a,b):
    return ( a % b)

def StandardKnot():
    global m
    knot = []
    L = len(points) - 2
    if L <= m -2 :
        print 'make more points than m'
        return []
    for i in range(m - 1):
        knot.append(0)
    for i in range(L - m + 3):
        knot.append(i)
    for i in range(m):
        knot.append(L - m + 3)
    return knot

def Nopen(k,m,t,knot):
    if m <= 1:
        if t < knot[k] or t >= knot[k + 1]:
            Sum = 0.0
        else:
            Sum = 1.0
    else:
        d = knot[k+m-1]-knot[k]
        if d <> 0:
            Sum = (t-knot[k])*Nopen(k,m-1,t,knot)/d
        else:
            Sum = 0.0
        d = knot[k+m] - knot[k+1]
        if d <> 0:
            Sum = Sum + (knot[k+m] - t)*Nopen(k + 1,m-1,t,knot)/d
    return Sum

def Nclosed(k,m,t,knot):
    L = len(points)
    z = mod(t-k,L)
    if z <= 0:
        z += L
    return Nopen(0,m,z,knot)

def P(t,knot,Ncycle):
    L = len(points)
    SumX = 0.0
    SumY = 0.0
    for k in range(L):
        n = Ncycle(k,m,t,knot)
        SumX = SumX + n * points[k][0]
        SumY = SumY + n * points[k][1]
    return [SumX,SumY]

def plot():
    global m
    global points
    if lOpen:
       knot = StandardKnot()
       if len(knot) == 0:
           return
       print knot
       print points
       x = points[0][0]
       y = points[0][1]
       t = 0.0
       step = 0.1
       L = len(points)
       while t <= L - m  + 1:
           p = P(t,knot,Nopen)
           C.create_line(x, y, p[0], p[1])
           x = p[0]
           y = p[1]
           t = t + step
    else:
       L = len(points)
       knot = range(L) 
       print knot
       print points
       p = P(0.0,knot,Nclosed)
       x = p[0]
       y = p[1]
       step = 0.1
       t = step
       L = len(points)
       while t <= L:
           p = P(t,knot,Nclosed)
           C.create_line(x, y, p[0], p[1])
           x = p[0]
           y = p[1]
           t = t + step

def Spaceout():
    global points
    newpoints = []
    L = len(points)
    if lOpen:
       newpoints.append(points[0])
       knot = StandardKnot()
       if len(knot) == 0:
           return
       for t in range( 1, L - m  + 2):
           p = P(t - 0.5,knot,Nopen)
           x = points[t][0] - p[0]
           y = points[t][1] - p[1]
           newpoints.append([points[t][0] + x,points[t][1] + y])
       newpoints.append(points[-1])    
    else:
       knot = range(L) 
       for t in range(L):
           p = P(mod(t + 1.5,L),knot,Nclosed)
           x = points[t][0] - p[0]
           y = points[t][1] - p[1]
           newpoints.append([points[t][0] + x,points[t][1] + y])
    points = newpoints       
    plot()    

def do_mouse(eventname):
    def mouse_binding(event):
        global points
        if eventname == "Button-1":
            x = event.x
            y = event.y
            print x, y
            if x > 50 and y > 50:
                points.append([x,y])
                C.create_oval(x - 6,y - 6, x + 6, y + 6)
                C.create_text(x, y, text = '%d' %(len(points)))
    fram.bind_all( '<%s>' %eventname, mouse_binding)

def wipe():
    global points
    C.delete( ALL)
    points = []

def fetch():
    global m
    m = mEntry.get()
    m = int(m)
    print 'm is now %d' %m

def CycleClosed(i):
    global lOpen
    lOpen = i
    if lOpen:
        print 'Cycle is open'
    else:
        print 'Cycle is closed'

def Blending():
    global points
    L = len(points)
    if L <= m:
        print 'Make some more points first!'
        return
    if lOpen:
       knot = StandardKnot()
       if len(knot) == 0:
           return
    else:   
       knot = range(L)
    print knot
    x0 = ScreenW * 0.2
    y0 = ScreenH * 0.2
    scaley = ScreenH * 0.7
    scalex = ScreenW / L * 0.7
    for k in knot:
        x1 = k * scalex + x0
        y1 = ScreenH - y0
        C.create_line(x1, y1, x1, y1 + 20)
    for k in range(L):
        t = 0.0
        step = 0.1
        x1 = x0
        y1 = y0
        if lOpen:
            z = L - m + 1
        else:
            z = L
        while t <= z:
            if lOpen:
               p = Nopen(k,m,t,knot)
            else:   
               p = Nopen(0,m,mod(t-k,L),knot)
            x2 = t * scalex + x0
            y2 = ScreenH - p * scaley - y0
            C.create_line(x1, y1, x2, y2)
            x1 = x2
            y1 = y2
            t = t + step

m = 3
lOpen = True
ScreenH = 600
ScreenW = 800
root = Tk()
root.title('Left click to add some points, then click [Plot] to draw the b-spline.')
fram = Frame(root)
rad1 = Radiobutton(fram, text = 'Open',value=1,command=(lambda : CycleClosed(True)))
rad1.pack(side = LEFT)
rad2 = Radiobutton(fram, text = 'Closed',value=0,command=(lambda : CycleClosed(False)))
rad2.pack(side = LEFT)
rad1.select()
Label(fram, text = 'M:').pack(side = LEFT,padx = 20)
mEntry = Entry(fram)
mEntry.insert(0,m)
mEntry.focus()
mEntry.bind('<Return>', (lambda event: fetch()))
mEntry.pack(side = LEFT)
butt1 = Button(fram, text = '  Plot  ',command = plot)
butt1.pack(side = LEFT)
butt3 = Button(fram, text = '  Wipe  ',command = wipe)
butt3.pack(side = LEFT)
butt4 = Button(fram, text = 'Blending',command = Blending)
butt4.pack(side = LEFT)
butt5 = Button(fram, text = 'Spaceout',command = Spaceout)
butt5.pack(side = LEFT)
fram.pack(side = TOP)
C = Canvas(root, width = ScreenW, height = ScreenH)
C.pack()
do_mouse('Button-1')
do_mouse('Button-3')
points = []
root.mainloop()
