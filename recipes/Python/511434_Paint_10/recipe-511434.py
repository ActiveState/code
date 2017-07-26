HOST = '127.0.0.1'
PORT = 8080

from Tkinter import *
import tkColorChooser

import socket
import thread
import spots

################################################################################

def main():
    global hold, fill, draw, look
    hold = []
    fill = '#000000'
    connect()
    root = Tk()
    root.title('Paint 1.0')
    root.resizable(False, False)
    upper = LabelFrame(root, text='Your Canvas')
    lower = LabelFrame(root, text='Their Canvas')
    draw = Canvas(upper, bg='#ffffff', width=400, height=300, highlightthickness=0)
    look = Canvas(lower, bg='#ffffff', width=400, height=300, highlightthickness=0)
    cursor = Button(upper, text='Cursor Color', command=change_cursor)
    canvas = Button(upper, text='Canvas Color', command=change_canvas)
    draw.bind('<Motion>', motion)
    draw.bind('<ButtonPress-1>', press)
    draw.bind('<ButtonRelease-1>', release)
    draw.bind('<Button-3>', delete)
    upper.grid(padx=5, pady=5)
    lower.grid(padx=5, pady=5)
    draw.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
    look.grid(padx=5, pady=5)
    cursor.grid(row=1, column=0, padx=5, pady=5, sticky=EW)
    canvas.grid(row=1, column=1, padx=5, pady=5, sticky=EW)
    root.mainloop()

################################################################################

def connect():
    try:
        start_client()
    except:
        start_server()
    thread.start_new_thread(processor, ())

def start_client():
    global QRI
    server = socket.socket()
    server.connect((HOST, PORT))
    QRI = spots.qri(server)

def start_server():
    global QRI
    server = socket.socket()
    server.bind(('', PORT))
    server.listen(1)
    QRI = spots.qri(server.accept()[0])

def processor():
    while True:
        ID, (func, args, kwargs) = QRI.query()
        getattr(look, func)(*args, **kwargs)

def call(func, *args, **kwargs):
    try:
        QRI.call((func, args, kwargs), 0.001)
    except:
        pass

################################################################################

def change_cursor():
    global fill
    color = tkColorChooser.askcolor(color=fill)[1]
    if color is not None:
        fill = color

def change_canvas():
    color = tkColorChooser.askcolor(color=draw['bg'])[1]
    if color is not None:
        draw['bg'] = color
        draw.config(bg=color)
        call('config', bg=color)

################################################################################

def motion(event):
    if hold:
        hold.extend([event.x, event.y])
        event.widget.create_line(hold[-4:], fill=fill, tag='TEMP')
        call('create_line', hold[-4:], fill=fill, tag='TEMP')

def press(event):
    global hold
    hold = [event.x, event.y]

def release(event):
    global hold
    if len(hold) > 2:
        event.widget.delete('TEMP')
        event.widget.create_line(hold, fill=fill, smooth=True)
        call('delete', 'TEMP')
        call('create_line', hold, fill=fill, smooth=True)
    hold = []

def delete(event):
    event.widget.delete(ALL)
    call('delete', ALL)

################################################################################

if __name__ == '__main__':
    main()
