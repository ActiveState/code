from visual import *
#VPython copes with 2 objects mooving BUT only if make it flip-flop between them!
# I have re-cycled a program from the VPython tutorial "A Ball in a Box".
#Try as I might I can't get a 'colission event' to react!
#
#    #Setting the seen, a hollow box created from 6 thin boxes.             #
wallR = box(pos=(6,0,0), size=(0.1,12,12), color=color.green, opacity=0.2)  #
walll = box(pos=(-6,0,0), size=(0.1,12,12), color=color.green, opacity=0.2) #
wallt = box(pos=(0,6,0), size=(12,0.1,12), color=color.red, opacity=0.2)    #
wallbt = box(pos=(0,-6,0), size=(12,0.1,12), color=color.red, opacity=0.2)  #
wallbk = box(pos=(0,0,-6), size=(12,12,0.1), color=color.blue, opacity=0.2) #
wallf = box(pos=(0,0,6), size=(12,12,0.1), color=color.white, opacity=0.2)  #
#
    #Creating 2 balls; position,size,colour,tail,velocity.  #
cyanball = sphere(pos=(5,5,5), radius=0.5, color=color.cyan)#
cyanball.trail = curve(color=cyanball.color)                #
cyanball.velocity = vector(3,3,3)                           #
#                                                           #
redball = sphere(pos=(-5,-5,-5), radius=0.5, color=color.red)#
redball.trail = curve(color=redball.color)                  #
redball.velocity = vector(-3,-3,-3)                         #
#
deltat = 0.005  #settig the timing.
t = 0           #
#
while t < 20:
    p=0   #Setting up 2 values for the flip-flop. At the end of each nested 'While'
    k = 0 #P will be incramented (p=p+1). K is the remainder of P/2 (k=p%2).
          #If k = 0 Flip! If k != 0 Flop!
    while k==0:
       #flipping & Running cyanball!
        cyanball.pos = cyanball.pos + cyanball.velocity*deltat
        cyanball.trail.append(pos=cyanball.pos, retain=200)
        if cyanball.pos.x < -5.6:                       #Testing for collisions
            cyanball.velocity.x = -cyanball.velocity.x  #with eack wall & bouncing!
        if cyanball.pos.x > 5.6:
            cyanball.velocity.x = -cyanball.velocity.x
        if cyanball.pos.y < -5.6:
            cyanball.velocity.y = -cyanball.velocity.y
        if cyanball.pos.y > 5.6:
            cyanball.velocity.y = -cyanball.velocity.y
        if cyanball.pos.z < -5.6:
            cyanball.velocity.z = -cyanball.velocity.z
        if cyanball.pos.z > 5.6:
            cyanball.velocity.z = -cyanball.velocity.z
        t = t + deltat
        p = p + 1
        k = p % 2
        rate(400)
       
    while k!=0:
         #Flopping & Running redball!
        redball.pos = redball.pos + redball.velocity*deltat
        redball.trail.append(pos=redball.pos, retain=200)
         
        if redball.pos.x < -5.6:
            redball.velocity.x  = -redball.velocity.x
        if redball.pos.x > 5.6:
            redball.velocity.x = -redball.velocity.x
        if redball.pos.y < -5.6:
            redball.velocity.y = -redball.velocity.y
        if redball.pos.y > 5.6:
            redball.velocity.y = -redball.velocity.y
        if redball.pos.z < -5.6:
            redball.velocity.z = -redball.velocity.z
        if redball.pos.z > 5.6:
            redball.velocity.z = -redball.velocity.z
        t = t + deltat
        p=p+1
        k = p % 2
        rate(400)
