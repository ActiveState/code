from physics import *
from Tkinter import *
from random import randint
from traceback import format_exc

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
BALLS = 10
BALL_RADIUS = 10
WALL_SPACE = 50
WALL_FORCE = 500
SPEED_LIMIT = 250
START_SPACE = 20
FPS = 40
BACKGROUND = 'white'
BALL_COLOR = 'red'

def main():
    initialise()
    mainloop()

def initialise():
    global balls, x, y, screen, lock
    space = WALL_SPACE + BALL_RADIUS
    balls = []
    for ball in xrange(BALLS):
        table = randint(0, 3)
        if table >> 1:
            x = randint(space, SCREEN_WIDTH - space)
            y = -START_SPACE if table & 1 else START_SPACE + SCREEN_HEIGHT
        else:
            x = -START_SPACE if table & 1 else START_SPACE + SCREEN_WIDTH
            y = randint(space, SCREEN_HEIGHT - space)
        balls.append(Ball(x, y, BALL_RADIUS))
    root = Tk()
    root.resizable(False, False)
    root.title('Space Balls')
    x = (root.winfo_screenwidth() - SCREEN_WIDTH) / 2
    y = (root.winfo_screenheight() - SCREEN_HEIGHT) / 2
    root.geometry('%dx%d+%d+%d' % (SCREEN_WIDTH, SCREEN_HEIGHT, x, y))
    root.bind_all('<Escape>', lambda event: event.widget.quit())
    root.bind('<Configure>', move)
    screen = Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, background=BACKGROUND)
    screen.after(1000 / FPS, update)
    screen.after(10000 / FPS, unlock)
    screen.pack()
    lock = True

def move(event):
    global x, y
    if not lock:
        diff = Vector(x - event.x, y - event.y)
        screen.move(ALL, diff.x, diff.y)
        for ball in balls:
            ball.pos += diff
        x, y = event.x, event.y

def update():
    try:
        ident = screen.after(1000 / FPS, update)
        for mutate in container, governor:
            for ball in balls:
                mutate(ball)
        for index, ball_1 in enumerate(balls[:-1]):
            for ball_2 in balls[index+1:]:
                ball_1.crash(ball_2)
        for ball in balls:
            ball.move(FPS)
        screen.delete(ALL)
        for ball in balls:
            x1 = ball.pos.x - BALL_RADIUS
            y1 = ball.pos.y - BALL_RADIUS
            x2 = ball.pos.x + BALL_RADIUS
            y2 = ball.pos.y + BALL_RADIUS
            screen.create_oval(x1, y1, x2, y2, fill=BALL_COLOR)
    except:
        screen.after_cancel(ident)
        screen.delete(ALL)
        screen.create_text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, text=format_exc(), font='Courier 10', fill='red')

def container(ball):
    space = WALL_SPACE + BALL_RADIUS
    force = float(WALL_FORCE) / FPS
    if ball.pos.x <= space:
        ball.vel.x += force
    elif ball.pos.x >= SCREEN_WIDTH - space:
        ball.vel.x -= force
    if ball.pos.y <= space:
        ball.vel.y += force
    elif ball.pos.y >= SCREEN_HEIGHT - space:
        ball.vel.y -= force

def governor(ball):
    if abs(ball.vel) > SPEED_LIMIT:
        ball.vel = ball.vel.unit() * SPEED_LIMIT

def unlock():
    global lock
    lock = False

if __name__ == '__main__':
    main()
