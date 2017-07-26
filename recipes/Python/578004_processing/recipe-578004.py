import itertools
import time
import tkinter
import vector

################################################################################

class Polygon:

    "Polygon(*vertices) -> Polygon"

    __slots__ = 'vertices'

    def __init__(self, *vertices):
        "Initializes polygon with a list of vertices."
        self.vertices = vertices

    def translate(self, offset):
        "Moves the polygon by the specified offset."
        for vertex in self.vertices:
            vertex += offset

    def rotate(self, direction):
        "Rotates the polygon by a vector's direction."
        for vertex in self.vertices:
            vertex.direction += direction

    def scale(self, factor):
        "Increases or decreases size of the polygon."
        for vertex in self.vertices:
            vertex *= factor

    def copy(self):
        "Copies the polygon by copying its vertices."
        return Polygon(*(vertex.copy() for vertex in self.vertices))

################################################################################

class Graphics:

    "Graphics(canvas) -> Graphics"

    __slots__ = 'canvas'

    def __init__(self, canvas):
        "Initializes graphics by wrapping a canvas."
        self.canvas = canvas

    def draw(self, polygon, fill, outline):
        "Draws a polygon on the underlying canvas."
        self.canvas.create_polygon(*itertools.chain(*polygon.vertices),
                                   fill=fill, outline=outline)

    def write(self, x, y, text, fill):
        "Writes the text to bottom-left of location."
        self.canvas.create_text(x, y, text=text, fill=fill, anchor=tkinter.NW)

    def clear(self):
        "Clears canvas of all objects shown on it."
        self.canvas.delete(tkinter.ALL)

    def fill(self, background):
        "Fills in the canvas with the given color."
        self.canvas.configure(background=background)

################################################################################

class Process(tkinter.Frame):

    "Process(master, width, height) -> Process"

    FRAMESKIP = 5   # How many frames should skip before issuing speed warning?
    RENDER_EACH_SECOND = 15 # How often should the DISPLAY be updated / second?
    UPDATE_EACH_SECOND = 30 # How often should the PHYSICS be updated / second?

    @classmethod
    def main(cls, width, height):
        "Creates a process in a window and executes it."
        tkinter.NoDefaultRoot()
        root = tkinter.Tk()
        root.title('Processing 1.1')
        root.resizable(False, False)
        view = cls(root, width, height)
        view.grid()
        root.mainloop()

    ########################################################################

    def __init__(self, master, width, height):
        "Initializes process and starts simulation loops."
        super().__init__(master)
        canvas = tkinter.Canvas(self, width=width, height=height,
                                background='white', highlightthickness=0)
        canvas.bind('<1>', self.mouse_pressed)
        canvas.grid()
        graphics = Graphics(canvas)
        self.setup(graphics.fill)
        render = 1 / self.RENDER_EACH_SECOND
        update = 1 / self.UPDATE_EACH_SECOND
        self.__loop(lambda: self.render(graphics), render, time.clock(), 0)
        self.__loop(lambda: self.update(update), update, time.clock(), 0)

    def __loop(self, method, interval, target, errors):
        "Runs the method after each interval has passed."
        method()
        target += interval
        ms = int((target - time.clock()) * 1000)
        if ms >= 0:
            self.after(ms, self.__loop, method, interval, target, 0)
        elif errors == self.FRAMESKIP:
            self.speed_warning()
            self.after_idle(self.__loop, method, interval, target, 0)
        else:
            self.after_idle(self.__loop, method, interval, target, errors + 1)

    ########################################################################
    
    def setup(self, background):
        "This method is called before render and update."
        raise NotImplementedError()

    def render(self, graphics):
        "This method is called when screen should render."
        raise NotImplementedError()

    def update(self, interval):
        "This method is called when physics should update."
        raise NotImplementedError()

    def mouse_pressed(self, event):
        "This method is called when left-clicking mouse."
        raise NotImplementedError()

    def speed_warning(self):
        "This method is called when code is running slow."
        raise NotImplementedError()

################################################################################

import recipe576904; recipe576904.bind_all(globals())
