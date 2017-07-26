import Tkinter
import random
import time
import traceback
import physics

################################################################################

BALLS = 20                  # NUMBER OF SIMULATED BALLS

BALL_RADIUS = 25            # RADIUS OF BALL IN PIXELS
START_SPACE = 50            # SIDE OFFSET IN PIXELS
SCREEN_WIDTH = 500          # WIDTH OF SCREEN IN PIXELS
SCREEN_HEIGHT = 350         # HEIGHT OF SCREEN IN PIXELS
WALL_SPACE = 70             # WIDTH OF WALLS IN PIXELS
FLOOR_SPACE = 15            # HEIGHT OF FLOOR IN PIXELS

BACKGROUND = 'gray40'       # COLOR OF BACKGROUND
BALL_COLOR = ('red',
              'orange',
              'yellow')     # COLOR OF BALLS
FLOOR_COLOR = 'gray20'      # COLOR OF FLOOR
FORCE_COLOR = 'sienna4'     # COLOR OF FOURCE FIELD

FPS = 60                    # FRAMES PER SECOND
SPEED_LIMIT = 2000          # PIXELS PER SECOND
WALL_FORCE = 900            # PIXELS PER SECOND
GRAV_RATE = 100             # PIXELS PER SECOND
FRIC_RATE = 0.5             # VELOCITY PER SECOND

################################################################################

def main():
    'Setup and start demonstration.'
    initialise()
    Tkinter.mainloop()

def initialise():
    'Build balls and prepare GUI.'
    global balls, x, y, screen, lock, start, frame
    balls = []
    for ball in xrange(BALLS):
        x = -START_SPACE if random.randint(0, 1) else START_SPACE + SCREEN_WIDTH
        y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - FLOOR_SPACE - BALL_RADIUS)
        balls.append(physics.Ball(x, y, BALL_RADIUS))
    root = Tkinter.Tk()
    root.resizable(False, False)
    root.title('Explosive Embers')
    x = (root.winfo_screenwidth() - SCREEN_WIDTH) / 2
    y = (root.winfo_screenheight() - SCREEN_HEIGHT) / 2
    root.geometry('%dx%d+%d+%d' % (SCREEN_WIDTH, SCREEN_HEIGHT, x, y))
    root.bind_all('<Escape>', lambda event: event.widget.quit())
    root.bind('<Configure>', move)
    screen = Tkinter.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, background=BACKGROUND)
    screen.after(1000 / FPS, update)
    screen.after(10000 / FPS, unlock)
    screen.pack()
    floor_height = SCREEN_HEIGHT - FLOOR_SPACE + 2
    screen.create_rectangle(0, 0, WALL_SPACE - 1, floor_height, fill=FORCE_COLOR)
    screen.create_rectangle(SCREEN_WIDTH - WALL_SPACE + 1, 0, SCREEN_WIDTH, floor_height, fill=FORCE_COLOR)
    screen.create_line(0, floor_height, SCREEN_WIDTH, floor_height, width=3, fill=FLOOR_COLOR)
    lock = True
    start = time.clock()
    frame = 1.0

def move(event):
    'Simulate movement of screen.'
    global x, y
    if not lock:
        diff = physics.Vector(x - event.x, y - event.y)
        screen.move('animate', diff.x, diff.y)
        floor_height = SCREEN_HEIGHT - FLOOR_SPACE - BALL_RADIUS
        for ball in balls:
            ball.pos += diff
            if ball.pos.y >= floor_height:
                ball.vel.y += diff.y * FPS
                floor(ball)
        x, y = event.x, event.y

def update():
    'Run physics and update screen.'
    global frame
    try:
        for mutate in wall, floor, gravity, friction, governor:
            for ball in balls:
                mutate(ball)
        for index, ball_1 in enumerate(balls[:-1]):
            for ball_2 in balls[index+1:]:
                try: ball_1.crash(ball_2)
                except: pass
        for ball in balls:
            ball.move(FPS)
        screen.delete('animate')
        for ball in balls:
            x1 = ball.pos.x - ball.rad
            y1 = ball.pos.y - ball.rad
            x2 = ball.pos.x + ball.rad
            y2 = ball.pos.y + ball.rad
            screen.create_oval(x1, y1, x2, y2, fill=random.choice(BALL_COLOR), tag='animate')
        frame += 1
        screen.after(int((start + frame / FPS - time.clock()) * 1000), update)
    except:
        screen.delete(Tkinter.ALL)
        screen.create_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, text=traceback.format_exc(), font='Courier 10', fill='red', tag='animate')

def wall(ball):
    'Simulate a wall.'
    space = WALL_SPACE + BALL_RADIUS
    force = float(WALL_FORCE) / FPS
    if ball.pos.x <= space:
        ball.vel.x += force
    elif ball.pos.x >= SCREEN_WIDTH - space:
        ball.vel.x -= force

def floor(ball):
    'Simulate a floor.'
    floor_height = SCREEN_HEIGHT - FLOOR_SPACE - BALL_RADIUS
    if ball.pos.y >= floor_height:
        ball.pos.y = floor_height
        ball.vel.y *= -1

def gravity(ball):
    'Simulate gravity.'
    ball.vel.y += float(GRAV_RATE) / FPS

def friction(ball):
    'Simulate friction.'
    ball.vel *= FRIC_RATE ** (1.0 / FPS)

def governor(ball):
    'Simulate speed governor.'
    if abs(ball.vel) > SPEED_LIMIT:
        ball.vel = ball.vel.unit() * SPEED_LIMIT

def unlock():
    'Activate the "move" function.'
    global lock
    lock = False

################################################################################

if __name__ == '__main__':
    main()
