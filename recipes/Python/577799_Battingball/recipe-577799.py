from visual import *
#Have fun batting a ball about a room & sometimes getting funny results.
#I have 'recycled' other peoples code & modified it for my use (http://python.org/, http://www.activestate.com/)
#Both are useful sources. (Thanks to you both)
#
#make a Box
wallR = box(pos=(6,0,-6), size=(0.1,12,12), color=color.green, opacity=0.2)
walll = box(pos=(-6,0,-6), size=(0.1,12,12), color=color.green, opacity=0.2)
wallt = box(pos=(0,6,-6), size=(12,0.1,12), color=color.red, opacity=0.2)
wallbt = box(pos=(0,-6,-6), size=(12,0.1,12), color=color.red, opacity=0.2)
wallbk = box(pos=(0,0,-12), size=(12,12,0.1), color=color.blue, opacity=0.2)
#The last wall is invisible; as in the 5th wall of stage.
#
#set up Bat, which can be draged by the mouse.
scene.range = 10 # fixed size, no autoscaling
bat = sphere(pos=(0,0,0), radius=0.4, color=color.cyan)
pick = None # no object picked out of the scene yet
#
#set up Bouncy ball.
redball = sphere(pos=(5,5,-11), radius=0.5, color=color.red)
redball.trail = curve(color=redball.color)
redball.velocity = vector(5,6,7)
#
deltat = 0.005  #setting the timing.
t = 0           #
#
while t < 70:
    if scene.mouse.events:

        m1 = scene.mouse.getevent() # obtain drag or drop event

        if m1.drag and m1.pick == bat: # if clicked on the bat

            drag_pos = m1.pickpos # where on the ball the mouse was

            pick = m1.pick # pick is now True (nonzero)

            scene.cursor.visible = False # make cursor invisible

        elif m1.drop: # released the mouse button at end of drag

            pick = None # end dragging (None is False)

            scene.cursor.visible = True # cursor visible again
    if pick:

        new_pos = scene.mouse.project(normal=(0,0,1)) # project onto xy plane
        scene.cursor.visible = True # cursor visible again

        if new_pos != drag_pos: # if the mouse has moved since last position

            pick.pos += new_pos - drag_pos # offset for where the ball was clicked

            drag_pos = new_pos # update drag position

	#setting the limits of the bat movement.
    if bat.pos.x < -5.2:
        bat.pos.x = -5.2
    if bat.pos.x > 5.2:
        bat.pos.x = 5.2
    if bat.pos.y < -5.2:
        bat.pos.y = -5.2
    if bat.pos.y > 5.2:
        bat.pos.y = 5.2 
    #Getting the ball moving.        
    redball.pos = redball.pos + redball.velocity*deltat
    redball.trail.append(pos=redball.pos, retain=200)
	#Getting the ball to bounce off the ball.
    if redball.pos.x >= bat.pos.x:
        redball.velocity.x = -redball.velocity.x
    if redball.pos.y >= bat.pos.y:
        redball.velocity.y = -redball.velocity.y
	#Getting the ball to bounce off the walls.
    if redball.pos.x < -5.6:
        redball.velocity.x  = -redball.velocity.x
    if redball.pos.x > 5.6:
        redball.velocity.x = -redball.velocity.x
    if redball.pos.y < -5.6:
        redball.velocity.y = -redball.velocity.y
    if redball.pos.y > 5.6:
        redball.velocity.y = -redball.velocity.y
    if redball.pos.z < -11.6:
        redball.velocity.z = -redball.velocity.z
    if redball.pos.z > -0.4:
        redball.velocity.z = -redball.velocity.z
    t = t + deltat#moving time on.
    rate(400)#limiting the speed it all happens at on screen.
