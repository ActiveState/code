__author__ = 'Peter'

'''
This is a simulator for Conway's game of life (google to find the rules:
v4 with additional functionality over v3:
    - load or save boards to/from files: OK
    - random fill (with variable density): OK
    - improved layout and added menu bar: OK
    - warp yes/no: OK
    - show / hide grid: OK
    - increase / decrease speed: OK
    - improved code (PEP 8, and logical improvements, especially in modifying mutable objects in functions): OK
'''

import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.font as tkfont
import tkinter.simpledialog as tkd
import sys
import random


def load_board_from_file(filename=None):
    if filename is None:
        filename = tkf.askopenfilename(defaultextension='.gol',
                                       filetypes=(('game of life files', '*.gol'), ('All files', '*.*')))
    board_f = open(filename, 'r')
    row = board_f.readline().strip('\n')
    y = 1
    bd = []
    while row != "":
        bd.append(list(row))
        y += 1
        row = board_f.readline().strip('\n')
    board_f.close()

    # TODO insert some tests here to check if the selected file meets the required file

    return bd, filename


def create_random_board(density):

    for row in range(len(board)):
        for col in range(len(board[0])):
            r = random.randrange(100)
            if r > density:
                board[row][col] = "."
            else:
                board[row][col] = "#"


def clear():
    global step
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(cols):
            board[row][col] = "."
    step = 0
    display_board(board)


def count_surrounding(row, col, bd):
    count = 0
    rows = len(bd)
    cols = len(bd[0])
    w = warp.get()
    for rr in range(row-1, row+2):
        if rr < 0:
            r = rows-1
        elif rr > rows-1:
            r = 0
        else:
            r = rr
        for cc in range(col-1, col+2):
            if cc < 0:
                c = cols-1
            elif cc > cols-1:
                c = 0
            else:
                c = cc
            if not (r == row and c == col):  # de cel in kwestie overslaan!
                if bd[r][c] == "#":
                    if not ((rr != r or cc != c) and w == 0):
                        count += 1
                    # if warping is off, then cells at the other side shouldn't be counted
    return count


def lifecycle(before):
    rows = len(before)
    cols = len(before[0])
    after = []
    for row in range(rows):         # initialize after
        after.append(list("."*cols))

    for row in range(rows):
        for col in range(cols):
            cs = count_surrounding(row, col, before)
            if before[row][col] == "#" and cs < 2:
                after[row][col] = "."
            elif before[row][col] == "#" and cs > 3:
                after[row][col] = "."
            elif before[row][col] == "." and cs == 3:
                after[row][col] = "#"
            else:
                after[row][col] = before[row][col]
    return after


def countliving():
    return str(alive)


def switch_cell(event):      # turn cell on or off with mouse click
    global alive
    cx = event.x
    cy = event.y
    bx = cx//sz
    by = cy//sz
    if bx < len(board[0]) and by < len(board):
        if board[by][bx] == ".":
            board[by][bx] = "#"
        else:
            board[by][bx] = "."
        display_board(board)


def display_board(bd):
    MyCanvas.delete(tk.ALL)
    cols = len(bd[0])
    rows = len(bd)
    counter = 0
    colors = ['grey', 'orange']
    ol_color = colors[showgrid.get()]
    for x in range(cols):
        for y in range(rows):
            rect = (x*sz, y*sz, (x+1)*sz, (y+1)*sz)
            if bd[y][x] == "#":
                MyCanvas.create_rectangle(rect, outline="black", fill="orange")
                counter += 1
            else:
                MyCanvas.create_rectangle(rect, outline=ol_color)
    stats = "living cells: " + str(counter) + "\n\ngeneration: " + str(step)
    MyCanvas.create_text((10, 10), text=stats, fill='white', anchor='nw', )  # show stats on canvas
    statreport.configure(text=stats)                                         # update stats in widget


def life(from_startbutton=False, from_stepbutton=False):
    global step
    global board
    global pauze
    global alive
    step += 1
    board = lifecycle(board)
    display_board(board)         # draw board and count living cells
    if from_startbutton is True:     # function has been called from start button and not from recursion (root.after...)
        pauze = False            # necessary for restart the startbutton is pressed after the pauzebutton
    checkpauze(pauze)
    if step <= steps and not pauze and not from_stepbutton:
        delay = speedcontrol.get()
        root.after(delay, life)  # root.after(delay, life()) is WRONG:  The function life needs to be passed as argument
                                 # life() will pass the result of life, i.e. execute it, before root.mainloop()


def checkpauze(p=False):
    global pauze
    pauze = p


def save_board_to_file(bd):
    filename = tkf.asksaveasfilename(defaultextension='.gol',
                                     filetypes=(('game of life files', '*.gol'), ('All files', '*.*')))
    if filename:
        f = open(filename, 'w')
        for row in range(len(bd)):
            f.write(''.join(board[row]) + '\n')
        f.close()


def load_board(file=None):      # filename passed when reopening (resetting) same file
    global board
    global step
    global openfile
    board = []
    board, openfile = load_board_from_file(file)
    step = 1
    display_board(board)


def rand_board():
    global board
    global step
    global openfile
    density = tkd.askinteger('Density', 'enter a cell density between 0 and 100')
    create_random_board(density)
    step = 1
    openfile = 'empty_board.gol'
    display_board(board)


def makemenu(win):
    top = tk.Menu(win)  # win=top-level window
    win.config(menu=top)  # set its menu option
    filemenu = tk.Menu(top)
    filemenu.add_command(label='Open...', command=load_board, underline=0)
    filemenu.add_command(label='Save...', command=lambda: save_board_to_file(board), underline=0)
    filemenu.add_command(label='Quit', command=sys.exit, underline=0)
    top.add_cascade(label='File', menu=filemenu, underline=0)
    edit = tk.Menu(top, tearoff=False)
    edit.add_command(label='Clear', command=clear, underline=0)
    edit.add_command(label='Randomize', command=rand_board, underline=0)
    edit.add_separator()
    top.add_cascade(label='Edit', menu=edit, underline=0)


#########  main program ###########

alive = 0
sz = 12                                 # cell size for visualization
steps = 1000                              # run a number of steps
                            # milliseconds
step = 1
board, openfile = load_board_from_file('empty_board.gol')
#warp = 0
#warp = tk.IntVar()                                # warp around the edges ?
pauze = False                               # p = pauze status false at program start

root = tk.Tk()
root.title("Conway's Game of Life")
makemenu(root)
ui = tk.Frame(root, bg='white')                       # user interface
ui2 = tk.Frame(root, bg='white')
#      Define the user interaction widgets
MyCanvas = tk.Canvas(root, width=len(board[0])*sz + 1, height=len(board)*sz+1, highlightthickness=0, bd=0, bg='grey')
warp = tk.IntVar()                                # warp around the edges ?
showgrid = tk.IntVar()
# quitbutton = tk.Button(ui, text='QUIT', width=10, command=sys.exit)
startbutton = tk.Button(ui, text='START', width=10, command=lambda: life(from_startbutton=True))
pauzebutton = tk.Button(ui, text='PAUSE', width=10, command=lambda: checkpauze(p=True))
stepbutton = tk.Button(ui, text='STEP', width=10, command=lambda: life(from_stepbutton=True))
clearbutton = tk.Button(ui, text='CLEAR', width=10, command=clear)
# savebutton = tk.Button(ui, text='SAVE', width=10, command=lambda: save_board_to_file(board))
# loadbutton = tk.Button(ui, text='LOAD', width=10, command=load_board)
restartbutton = tk.Button(ui, text='RESET', width=10, command=lambda: load_board(openfile))
randombutton = tk.Button(ui, text='RANDOMIZE', width=10, command=rand_board)
statreport = tk.Label(root, text="      ", bg='white', justify=tk.LEFT, relief=tk.GROOVE,
                      font=tkfont.Font(weight='bold'))
speedcontrol = tk.Spinbox(ui2, width=5, values=(5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 1000))
speedcontrol_label = tk.Label(ui2, text='Delay between steps:', bg='white')
warpcontrol = tk.Checkbutton(ui2, text='Warp around edges? ', variable=warp, bg='white')
showgridcontrol = tk.Checkbutton(ui2, text='show grid? ', variable=showgrid, bg='white',
                                 command=lambda: display_board(board))
                                 # board must be redrawn, because toggle grid will not be shown before start is pressed
                                 # because display_board(board) sits inside life()
showgridcontrol.select()
# quitbutton.grid(row=0, column=0, padx=10, pady=10)
startbutton.grid(row=1, column=0, padx=10, pady=10)
pauzebutton.grid(row=2, column=0, padx=10, pady=10)
stepbutton.grid(row=3, column=0, padx=10, pady=10)
clearbutton.grid(row=4, column=0, padx=10, pady=10)
# savebutton.grid(row=5, column=0, padx=10, pady=10)
# loadbutton.grid(row=6, column=0, padx=10, pady=10)
restartbutton.grid(row=7, column=0, padx=10, pady=10)
randombutton.grid(row=8, column=0, padx=10, pady=10)
speedcontrol_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky=tk.NW)
speedcontrol.grid(row=0, column=2, padx=10, pady=5, sticky=tk.NW)
warpcontrol.grid(row=1, column=3, columnspan=3, padx=10, ipadx=5, sticky=tk.NW)
showgridcontrol.grid(row=0, column=3, columnspan=2, padx=10, pady=5, ipadx=5, sticky=tk.NW)


#       Put everything on the screen
display_board(board)
MyCanvas.bind("<Button-1>", switch_cell)
ui.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)
MyCanvas.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
ui2.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH, anchor=tk.W)
statreport.pack(side=tk.RIGHT, expand=tk.NO, fill=tk.NONE)
root.mainloop()
