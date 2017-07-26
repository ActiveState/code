# IMPORT
import Tkinter
import tkMessageBox
import tkSimpleDialog
import random
import time

# CUSTOM
import physics
from opt import *

################################################################################

# PROGRAM INITIALIZATION FUNCTIONS

def main():
    "Start the program."
    global run
    run = False
    initialize()
    show_start()
    run = True
    Tkinter.mainloop()

def initialize():
    "Build the program's drawing surface."
    global root, screen
    root = Tkinter.Tk()
    root.title(STR.GM_NAME)
    root.resizable(False, False)
    x = (root.winfo_screenwidth() - MNU.SCR_W) / 2
    y = (root.winfo_screenheight() - MNU.SCR_H) / 2
    root.geometry('%dx%d+%d+%d' % (MNU.SCR_W, MNU.SCR_H, x, y))
    screen = Tkinter.Canvas(root, highlightthickness=0)
    screen.pack()

def show_start():
    "Display the start menu to the user."
    x, y = map(int, root.geometry().split('+')[1:])
    if run:
        width, height = map(int, root.geometry().split('+')[0].split('x'))
        x += (width - MNU.SCR_W) / 2
        y += (height - MNU.SCR_H) / 2
    root.geometry('%dx%d+%d+%d' % (MNU.SCR_W, MNU.SCR_H, x, y))
    screen.config(width=MNU.SCR_W, height=MNU.SCR_H, background=CLR.MENU_BG)
    screen.delete(Tkinter.ALL)
    screen.create_text(MNU.SCR_W / 2, MNU.SCR_H / 2, text=format_HST(), font=FNT.HS_TEXT, fill=CLR.HS_TEXT)
    button = screen.create_text(MNU.SCR_W / 2, MNU.START, text=STR.PLAY_BT, font=FNT.BT_NORM, fill=CLR.BT_NORM)
    screen.tag_bind(button, '<Enter>', bt_high)
    screen.tag_bind(button, '<Leave>', bt_norm)
    screen.tag_bind(button, '<1>', start_session)

################################################################################

# HST PREPARATION FUNCTIONS

def format_HST():
    "Properly format HST into a string."
    verify_HST()
    lines = []
    for key in sorted(HST, reverse=True):
        score = ' ' + str(key)
        for name in HST[key]:
            lines.append((name[:MNU.N_LEN] + ' ').ljust(MNU.HST_W - len(score), STR.T_SPACE) + score)
    return '\n'.join(lines)

def verify_HST():
    "Check the HST data structure."
    try:
        names = 0
        for key in HST:
            assert isinstance(key, int)
            assert isinstance(HST[key], list)
            for name in HST[key]:
                assert isinstance(name, str)
                names += 1
                assert names <= MNU.HST_H
        assert names == MNU.HST_H
    except:
        root.withdraw()
        tkMessageBox.showerror('Error', 'The high score table is corrupt.')
        raise SystemExit, 1

################################################################################

# MENU SUPPORT FUNCTIONS

def bt_high(event):
    "Highlight a button."
    screen.itemconfig(Tkinter.CURRENT, fill=CLR.BT_HIGH, font=FNT.BT_HIGH)

def bt_norm(event):
    "Normalize a button."
    screen.itemconfig(Tkinter.CURRENT, fill=CLR.BT_NORM, font=FNT.BT_NORM)

def start_session(event):
    "Setup the program for a session."
    x, y = map(int, root.geometry().split('+')[1:])
    width, height = map(int, root.geometry().split('+')[0].split('x'))
    x += (width - GAM.SCR_W) / 2
    y += (height - GAM.SCR_H) / 2
    root.geometry('%dx%d+%d+%d' % (GAM.SCR_W, GAM.SCR_H, x, y))
    screen.config(width=GAM.SCR_W, height=GAM.SCR_H, background=CLR.GAME_BG)
    screen.delete(Tkinter.ALL)
    build_balls()
    build_world()
    build_loops()

################################################################################

# SESSION SETUP FUNCTIONS

def build_balls():
    "Build some non-overlapping balls."
    global balls
    balls = []
    sides = set()
    for ball in xrange(GAM.B_ALL):
        x = -GAM.B_OFF if random.randint(0, 1) else GAM.B_OFF + GAM.SCR_W
        y = random.randint(GAM.B_RAD, GAM.SCR_H - GAM.F_OFF - GAM.B_RAD) / GAM.B_RAD * GAM.B_RAD
        while (x, y) in sides:
            x = -GAM.B_OFF if random.randint(0, 1) else GAM.B_OFF + GAM.SCR_W
            y = random.randint(GAM.B_RAD, GAM.SCR_H - GAM.F_OFF - GAM.B_RAD) / GAM.B_RAD * GAM.B_RAD
        sides.add((x, y))
        balls.append(physics.Ball(x, y, GAM.B_RAD))
        balls[-1].type = 0
    balls = tuple(balls)

def build_world():
    "Build the program's environment."
    global clock_xy
    x = GAM.W_OFF - 1
    y = GAM.SCR_H - GAM.F_OFF + 2
    screen.create_rectangle(-1, -1, x, y, fill=CLR.FORCE)
    screen.create_rectangle(GAM.SCR_W - x, -1, GAM.SCR_W, y, fill=CLR.FORCE)
    screen.create_line(0, y, GAM.SCR_W, y, fill=CLR.FLOOR, width=3)
    clock_xy = x / 2, (y + GAM.SCR_H) / 2
    screen.create_text(clock_xy, text=f_time(TMR.LIMIT), tag='timer')
    screen.bind('<1>', click)

def build_loops():
    "Build the program's three loops."
    global world_h, frame_h, clock_h, start, world, frame, clock
    world_h = screen.after(1000 / TMR.P_FPS, update_world)
    frame_h = screen.after(1000 / TMR.S_FPS, update_frame)
    clock_h = screen.after(1000, update_clock)
    start = time.clock()
    world = 1.0
    frame = 1.0
    clock = 0

################################################################################

# PROGRAM LOOP FUNCTIONS

def update_world():
    "Crash, move, and mutate the balls."
    global world_h, world
    for index, ball_1 in enumerate(balls[:-1]):
        for ball_2 in balls[index+1:]:
            ball_1.crash(ball_2)
    for ball in balls:
        ball.err *= PHY.B_BONUS
        ball.correct()
        governor(ball)
        ball.move(TMR.P_FPS)
        for mutate in wall, floor, gravity, friction:
            mutate(ball)
    world += 1
    world_h = screen.after(int((start + world / TMR.P_FPS - time.clock()) * 1000), update_world)

def update_frame():
    "Draw the contents of the screen."
    global frame_h, frame
    screen.delete('ball')
    for num, ball in enumerate(balls):
        x1 = ball.pos.x - ball.rad
        y1 = ball.pos.y - ball.rad
        x2 = ball.pos.x + ball.rad
        y2 = ball.pos.y + ball.rad
        screen.create_oval(x1, y1, x2, y2, fill=CLR.CYCLE[ball.type], tag=(num, 'ball'))
    frame += 1
    frame_h = screen.after(int((start + frame / TMR.S_FPS - time.clock()) * 1000), update_frame)

def update_clock():
    "Update the clock on the screen."
    global clock_h, clock
    screen.delete('timer')
    clock += 1
    screen.create_text(clock_xy, text=f_time(TMR.LIMIT - clock), tag='timer')
    if TMR.LIMIT - clock:
        clock_h = screen.after(int((start + clock + 1 - time.clock()) * 1000), update_clock)
    else:
        lose(True)

################################################################################

# VELOCITY MUTATOR FUNCTIONS

def governor(ball):
    "Simulate speed governor."
    if abs(ball.vel) > PHY.S_LIMIT:
        ball.vel = ball.vel.unit() * PHY.S_LIMIT

def wall(ball):
    "Simulate a force-field wall."
    space = GAM.W_OFF + ball.rad
    force = float(PHY.W_FORCE) / TMR.P_FPS
    if ball.pos.x <= space:
        ball.vel.x += force
    elif ball.pos.x >= GAM.SCR_W - space:
        ball.vel.x -= force

def floor(ball):
    "Simulate a floor."
    floor_height = GAM.SCR_H - GAM.F_OFF - ball.rad
    if ball.pos.y >= floor_height:
        ball.pos.y = floor_height
        ball.vel.y *= -1

def gravity(ball):
    "Simulate gravity."
    ball.vel.y += float(PHY.G_FORCE) / TMR.P_FPS

def friction(ball):
    "Simulate friction."
    ball.vel *= (PHY.F_FORCE / 1000.0) ** (1.0 / TMR.P_FPS)

################################################################################

# SESSION INTERACTION FUNCTIONS

def click(event):
    "Change a ball's color."
    global blink_h, blink
    try:
        ball = balls[int(screen.gettags(screen.find_withtag(Tkinter.CURRENT))[0])]
        ball.type = (ball.type + 1) % len(CLR.CYCLE)
        if sum(map(lambda ball: ball.type, balls)) == (len(CLR.CYCLE) - 1) * len(balls):
            screen.after_cancel(world_h)
            screen.after_cancel(frame_h)
            screen.after_cancel(clock_h)
            screen.delete('ball')
            blink = screen.create_text(GAM.SCR_W / 2, GAM.SCR_H / 2, text=STR.MS_TEXT, font=FNT.MS_TEXT, fill=CLR.MS_TEXT)
            blink_h = screen.after(TMR.MS_FF, toggle_text)
            screen.after(TMR.DELAY, win if TMR.LIMIT - clock >= min(HST) else lose)
    except:
        pass

def toggle_text():
    "Blink the winning text."
    global blink_h, blink
    blink_h = screen.after(TMR.MS_FF, toggle_text)
    blink = screen.delete(blink) if blink else screen.create_text(GAM.SCR_W / 2, GAM.SCR_H / 2, text=STR.MS_TEXT, font=FNT.MS_TEXT, fill=CLR.MS_TEXT)

def win():
    "Add name to HST and return to menu."
    name = tkSimpleDialog.askstring(STR.VICT_TI, '\n'.join(STR.VICT_MS)) or STR.DEFAULT
    score = TMR.LIMIT - clock
    if score in HST:
        HST[score].insert(0, name)
    else:
        HST[score] = [name]
    loser = min(HST)
    if len(HST[loser]) > 1:
        del HST[loser][-1]
    else:
        del HST[loser]
    screen.after_cancel(blink_h)
    show_start()

################################################################################

# SESSION TIMER FUCTIONS

def f_time(seconds):
    "Return time with correct format."
    return '%02d:%02d' % (seconds / 60, seconds % 60)

def lose(real=False):
    "End the session and get input."
    restart = tkMessageBox.askquestion(STR.LOSE_TI, STR.LOSE_MS) == 'yes'
    if real:
        screen.after_cancel(world_h)
        screen.after_cancel(frame_h)
    else:
        screen.after_cancel(blink_h)
    if restart:
        start_session(None)
    else:
        show_start()

################################################################################

if __name__ == '__main__':
    main()
