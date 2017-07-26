================================================================================
window.py
================================================================================
# This is the first version of the page class.
class page_v1:

    def __init__(self, rows, columns, default = None):
        # (page_v1, int, int, str)
        if default is None:
            default = ' '
        self.__page = list()
        for index in range(rows):
            self.__page.append(list(default[0] * columns))

    def mutate(self, row, column, string):
        # (page_v1, int, int, str)
        try:
            if row >= 0:
                for index in range(len(string)):
                    if column + index >= 0:
                        self.__page[row][column + index] = string[index]
        except:
            pass

    def access(self, row, column, length = 1):
        # (page_v1, int, int, int)
        string = str()
        try:
            for index in range(length):
                string += self.__page[row][column + index]
        except:
            pass
        return string

    def internal(self):
        # (page_v1)
        array = list()
        for row in self.__page:
            array.append(row[:])
        return array

    def __str__(self):
        # (page_v1)
        string = str()
        for row in self.__page:
            for character in row:
                string += character
            string += '\n'
        return string[:-1]

# This is the first version of a theoretical window.
class window_v1:

    def __init__(self, height, width, border = None, background = None):
        # (window_v1, int, int, str, str)
        self.__height = height
        self.__width = width
        self.__border = border
        self.__background = background
        self.__draw = True
        self.__buffer = None
        self.__contents = list()

    def append(self, instance, position, visible = True, index = None):
        # (window_v1, page_v1 OR window_v1, [int, int], bool, int)
        self.__draw = True
        if index is None:
            self.__contents.append([instance, position, visible])
        else:
            self.__contents.insert(index, [instance, position, visible])

    def remove(self, instance):
        # (window_v1, page_v1 OR window_v1)
        for index in range(len(self.__contents)):
            if instance is self.__contents[index][0]:
                self.__draw = True
                del self.__contents[index]

    def __getitem__(self, index):
        # (window_v1, int)
        self.__draw = True
        return self.__contents[index]

    def __delitem__(self, index):
        # (window_v1, int)
        self.__draw = True
        del self.__contents[index]

    def size(self, height = None, width = None):
        # (window_v1, int, int)
        if height is not None:
            self.__draw = True
            self.__height = height
        if width is not None:
            self.__draw = True
            self.__width = width
        if height is None and width is None:
            return self.__height, self.__width

    def look(self, border = 0, background = 0):
        # (window_v1, str, str)
        if border is not 0:
            self.__draw = True
            self.__border = border
        if background is not 0:
            self.__draw = True
            self.__background = background
        if border is 0 and background is 0:
            return self.__border, self.__background

    def __update(self):
        # (window_v1)
        if self.__draw:
            self.__draw = False
            self.__buffer = page_v1(self.__height, self.__width, self.__background)
            for item in self.__contents:
                if item[2]:
                    internal = item[0].internal()
                    for row in range(len(internal)):
                        for column in range(len(internal[0])):
                            self.__buffer.mutate(row + item[1][0], column + item[1][1], internal[row][column])
            if self.__border is not None:
                self.__buffer.mutate(0, 0, self.__border[0] * self.__width)
                self.__buffer.mutate(self.__height - 1, 0, self.__border[0] * self.__width)
                for row in range(1, self.__height - 1):
                    self.__buffer.mutate(row, 0, self.__border[0])
                    self.__buffer.mutate(row, self.__width - 1, self.__border[0])

    def internal(self):
        # (window_v1)
        self.__update()
        return self.__buffer.internal()

    def __str__(self):
        # (window_v1)
        self.__update()
        return str(self.__buffer)
