# ORIGINAL IMPORTS

import random
from Tkinter import *

# GAME IMPORTS

import time
import tkSimpleDialog
import tkMessageBox
import zlib

################################################################################

# ORIGINAL VARIABLES

WIDTH = 500                                 # OF SCREEN IN PIXELS
HEIGHT = 500                                # OF SCREEN IN PIXELS
BALLS = 20                                  # IN SIMULATION
WALL = 50                                   # FROM SIDE IN PIXELS
WALL_FORCE = 500                            # ACCELERATION PER MOVE
SPEED_LIMIT = 5000                          # FOR BALL VELOCITY
BALL_RADIUS = 15                            # FOR BALLS IN PIXELS
OFFSET_START = 100                          # FROM WALL IN PIXELS
FRAMES_PER_SEC = 40                         # SCREEN UPDATE RATE
FLOOR_COLOR = 'blue'                        # COLOR OF GAME FLOOR
FORCE_COLOR = 'light green'                 # COLOR OF FORCE FIELDS
COLORS = '#FF0000', '#FF7F00', '#FFFF00', \
         '#00FF00', '#0000FF', '#FF00FF'    # COLOR CYCLE OF BALLS
TITLE = "Mark's Game (Version 1)"           # TITLE OF PROGRAM

# GAME VARIABLES

TIME_LIMIT = 600                            # IN SECONDS
SAMPLE_HST = {540: ['Wiz-Kid'],
              480: ['Speed Daemon'],
              420: ['[SW] O B 1'],
              360: ['1337 Spartan'],
              300: ['<<SHIFTED>>'],
              240: ['NovaSuperNova'],
              180: ['[ZT] Berserk Fury'],
              120: ['[ZT] Shadow'],
              60: ['newbie123'],
              0: ['SiriuS']}                # DATABASE DEMO
HST_WIDTH = 30                              # IN CHARACTERS
MAX_NAME_WIDTH = 20                         # IN CHARACTERS
HST_SEP = '.'                               # JOINS NAME AND SCORE
HST_COLOR = 'green'                         # COLOR OF HIGH SCORES
HST_BACK = 'black'                          # HST BACKGROUND
B1_COLOR = 'blue'                           # BUTTON FONT COLOR
B2_COLOR = 'red'                            # BUTTON SELECT COLOR
GAME_COLOR = 'white'                        # BACKGROUND COLOR
WIN_TEXT = 'YOU WIN'                        # VICORY MESSAGE
WIN_COLOR = 'red'                           # TEXT COLOR
BLINK_RATE = 500                            # IN MILLISECONDS
PAUSE_TIME = 2250                           # IN MILLISECONDS
HST_FILE = 'HST.dat'                        # HIGH SCORE FILENAME

################################################################################

# PROGRAM INITIALIZATION FUNCTIONS

def main():
    # Start the program.
    make_root()
    high_score_table()
    mainloop()

def make_root():
    # Make root window and canvas.
    global root, graph
    root = Tk()
    root.resizable(False, False)
    root.title(TITLE)
    root.protocol('WM_DELETE_WINDOW', quit_game)
    root.bind_all('<Escape>', quit_game)
    left = (root.winfo_screenwidth() - WIDTH) / 2
    top = (root.winfo_screenheight() - HEIGHT) / 2
    root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, left, top))
    graph = Canvas(root, width=WIDTH, height=HEIGHT)
    graph.pack()

def high_score_table():
    global HS_database
    # Create high score table.
    if not globals().has_key('HS_database'):
        HS_database = load_HST()
    string = format_HST(HS_database)
    graph.create_text(WIDTH / 2, HEIGHT / 2, text=string, font='Courier 15', fill=HST_COLOR, tag='HST')
    graph.create_text(WIDTH / 2, 75, text='Start Game', font='Helvetica 25', fill=B1_COLOR, tag='start')
    graph.tag_bind('start', '<Any-Enter>', select_start)
    graph.tag_bind('start', '<Any-Leave>', deselect_start)
    graph.tag_bind('start', '<1>', start_game)
    graph['background'] = HST_BACK

################################################################################

# PROGRAM TERMINATION FUNCTION

def quit_game(event=None):
    # Save HST and quit program.
    file(HST_FILE, 'wb').write(zlib.compress(repr(HS_database), 9))
    root.quit()

################################################################################

# HST PREPARATION FUNCTIONS

def load_HST():
    # Load (H)igh (S)core (T)able.
    try:
        database = eval(zlib.decompress(file(HST_FILE, 'rb').read()))
        names = 0
        records = sum(map(len, SAMPLE_HST.values()))
        for key in database.keys():
            assert isinstance(key, int)
            assert isinstance(database[key], list)
            for name in database[key]:
                assert isinstance(name, str)
                names += 1
                assert names <= records
        assert names == records
        return database
    except:
        return SAMPLE_HST

def format_HST(database):
    # Format HST database to string.
    lines = []
    for key in sorted(database.keys(), reverse=True):
        score = ' ' + str(key)
        for name in database[key]:
            lines.append((name[:MAX_NAME_WIDTH] + ' ').ljust(HST_WIDTH - len(score), HST_SEP) + score)
    return '\n'.join(lines)

################################################################################

# MENU SUPPORT FUNCTIONS

def select_start(event):
    # Highlight start button.
    graph.itemconfig('start', fill=B2_COLOR)

def deselect_start(event):
    # Deselect the start button.
    graph.itemconfig('start', fill=B1_COLOR)

def start_game(event):
    # Start game play.
    graph.delete(ALL)
    initialise()

################################################################################

# GAME SETUP FUNCTIONS

def initialise():
    # Setup simulation variables.
    build_balls()
    build_graph()

def build_balls():
    # Create balls variable.
    global balls
    balls = tuple(Ball(WIDTH, HEIGHT, OFFSET_START, FRAMES_PER_SEC) for ball in xrange(BALLS))
    move()
    while len(set(tuple(ball.position) for ball in balls)) != BALLS:
        balls = tuple(Ball(WIDTH, HEIGHT, OFFSET_START, FRAMES_PER_SEC) for ball in xrange(BALLS))
        move()

def build_graph():
    # Build GUI environment.
    global frame_handle, y, x, start, sec, timer_text, clock_handle
    frame_handle = graph.after(1000 / FRAMES_PER_SEC, update)
    graph.bind('<1>', change)
    graph['background'] = GAME_COLOR
    # Draw environment.
    y = HEIGHT - WALL + BALL_RADIUS + 2
    graph.create_rectangle((0, 0, WALL - BALL_RADIUS, y), fill=FORCE_COLOR)
    graph.create_rectangle((WIDTH - WALL + BALL_RADIUS, 0, WIDTH, y), fill=FORCE_COLOR)
    graph.create_line((0, y, WIDTH, y), fill=FLOOR_COLOR, width=3)
    # Prepare timer data.
    x = (WALL - BALL_RADIUS) / 2
    y = (y + HEIGHT) / 2
    start = time.clock()
    sec = 0
    timer_text = graph.create_text(x, y, text=f_time(TIME_LIMIT))
    clock_handle = graph.after(1000, update_clock)

################################################################################

# ANIMATION LOOP FUNCTIONS
    
def update():
    # Main simulation loop.
    global frame_handle
    frame_handle = graph.after(1000 / FRAMES_PER_SEC, update)
    draw()
    move()

def draw():
    graph.delete('ball')
    # Draw all balls.
    for n, ball in enumerate(balls):
        x1 = ball.position.x - BALL_RADIUS
        y1 = ball.position.y - BALL_RADIUS
        x2 = ball.position.x + BALL_RADIUS
        y2 = ball.position.y + BALL_RADIUS
        graph.create_oval((x1, y1, x2, y2), fill=COLORS[ball.color], tags=(n, 'ball'))
        graph.create_text(ball.position.x, ball.position.y, text=str(n+1), tag=(n, 'ball'))

def move():
    # Move all balls.
    for force in simulate_wall, simulate_gravity, simulate_friction:
        for ball in balls:
            force(ball)
    for ball in balls:
        ball.update_velocity(balls)
    for ball in balls:
        ball.move()

################################################################################

# VELOCITY MUTATOR FUNCTIONS

def simulate_wall(ball):
    # Create viewing boundaries.
    if ball.position.x < WALL:
        ball.velocity.x += WALL_FORCE
    elif ball.position.x > WIDTH - WALL:
        ball.velocity.x -= WALL_FORCE

    if ball.position.y >= HEIGHT - WALL:
        ball.velocity.y *= -1
        ball.position.y = HEIGHT - WALL

def simulate_gravity(ball):
    # Create a pull.
    ball.velocity.y += 50

def simulate_friction(ball):
    # Slow velocity down.
    ball.velocity *= .9

def limit_speed(ball):
    # Limit ball speed.
    if ball.velocity.mag() > SPEED_LIMIT:
        ball.velocity /= ball.velocity.mag() / SPEED_LIMIT

################################################################################

# GAME INTERACTION FUNCTIONS

def change(event):
    # Change color of balls.
    try:
        ball = balls[int(graph.gettags(graph.find_withtag(CURRENT))[0])]
        ball.color = (ball.color + 1) % len(COLORS)
        if sum(map(lambda ball: ball.color, balls)) == len(COLORS) * BALLS - BALLS:
            do_win_action()
    except:
        pass

def do_win_action():
    # Cause the game to win.
    global win, blink_handle
    graph.after_cancel(frame_handle)
    graph.after_cancel(clock_handle)
    graph.delete('ball')
    win = graph.create_text(WIDTH / 2, HEIGHT / 2, text=WIN_TEXT, font='Helvetica 50', fill=WIN_COLOR)
    blink_handle = graph.after(BLINK_RATE, blink)
    graph.after(PAUSE_TIME, enter_high_score if TIME_LIMIT - sec >= min(HS_database.keys()) else do_lose_action)

def blink():
    # Blink the WIN_TEXT.
    global win, blink_handle
    blink_handle = graph.after(BLINK_RATE, blink)
    if win:
        graph.delete(win)
        win = None
    else:
        win = graph.create_text(WIDTH / 2, HEIGHT / 2, text=WIN_TEXT, font='Helvetica 50', fill=WIN_COLOR)

def enter_high_score():
    # Display a dialog box.
    name = tkSimpleDialog.askstring('High Score', 'Please enter your name\nfor the high score table.') or 'No Name'
    # Update the database.
    my_key = TIME_LIMIT - sec
    if HS_database.has_key(my_key):
        HS_database[my_key].insert(0, name)
    else:
        HS_database[my_key] = [name]
    low_key = min(HS_database.keys())
    if len(HS_database[low_key]) > 1:
        del HS_database[low_key][-1]
    else:
        del HS_database[low_key]
    # Restart the game.
    graph.after_cancel(blink_handle)
    graph.delete(ALL)
    high_score_table()

################################################################################

# GAME TIMER FUNCTIONS

def update_clock():
    # Update clock on screen.
    global timer_text, sec, clock_handle
    graph.delete(timer_text)
    sec += 1
    timer_text = graph.create_text(x, y, text=f_time(TIME_LIMIT - sec))
    if TIME_LIMIT - sec:
        clock_handle = graph.after(int((start + sec + 1 - time.clock()) * 1000), update_clock)
    else:
        do_lose_action(True)

def f_time(secs):
    # Format time correctly.
    return '%02d:%02d' % (secs / 60, secs % 60)

def do_lose_action(real=False):
    # Cause the game to lose.
    answer = tkMessageBox.askquestion('GAME OVER', 'Do you want to try again?')
    graph.after_cancel(frame_handle if real else blink_handle)
    graph.delete(ALL)
    if answer == 'yes':
        initialise()
    else:
        high_score_table()

################################################################################

# VECTOR MATHEMATICS CLASS

class TwoD:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self):
        return 'TwoD(%s, %s)' % (self.x, self.y)

    def __add__(self, other):
        return TwoD(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return TwoD(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return TwoD(self.x * other, self.y * other)

    def __div__(self, other):
        return TwoD(self.x / other if other else self.x, self.y / other if other else self.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __idiv__(self, other):
        self.x /= other
        self.y /= other
        return self

    def mag(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5

################################################################################

# BALL IMPLEMENTATION CLASS

class Ball:

    def __init__(self, width, height, offset, move_divider):
        self.velocity = TwoD(0, 0)
        self.position = TwoD(*(-offset if random.randint(0, 1) else width + offset, random.randint(0, height)))
        self.move_divider = move_divider * 5
        self.color = 0

    def update_velocity(self, balls):
        vector = TwoD(0, 0)
        for ball in balls:
            if ball is not self:
                if (self.position - ball.position).mag() < (BALL_RADIUS * 2 + 2):
                    vector -= (ball.position - self.position)
        self.__temp = vector * self.velocity.mag() / vector.mag() * 10

    def move(self):
        self.velocity += self.__temp
        limit_speed(self)
        self.position += self.velocity / self.move_divider

################################################################################

# Begin execution of the game.
if __name__ == '__main__':
    main()
