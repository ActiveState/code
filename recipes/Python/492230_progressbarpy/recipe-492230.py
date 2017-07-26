import Tkinter

################################################################################

class PB:

    # Create Progress Bar
    def __init__(self, width, height):
        self.__root = Tkinter.Toplevel()
        self.__root.resizable(False, False)
        self.__root.title('Progress Bar')
        self.__canvas = Tkinter.Canvas(self.__root, width=width, height=height)
        self.__canvas.grid()
        self.__width = width
        self.__height = height

    # Open Progress Bar
    def open(self):
        self.__root.deiconify()

    # Close Progress Bar
    def close(self):
        self.__root.withdraw()

    # Update Progress Bar
    def update(self, ratio):
        self.__canvas.delete(Tkinter.ALL)
        self.__canvas.create_rectangle(0, 0, self.__width * ratio, \
                                       self.__height, fill='blue')
        self.__root.update()
