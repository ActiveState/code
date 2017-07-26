#! /usr/bin/env python
from tkinter import NoDefaultRoot, Tk, ttk, filedialog
from _tkinter import getbusywaitinterval
from tkinter.constants import *
from math import sin, pi
import base64, zlib, os

################################################################################

ICON = b'eJxjYGAEQgEBBiApwZDBzMAgxsDAoAHEQCEGBQaIOAwkQDE2UOSkiUM\
Gp/rlyd740Ugzf8/uXROxAaA4VvVAqcfYAFCcoHqge4hR/+btWwgCqoez8aj//fs\
XWiAARfCrhyCg+XA2HvV/YACoHs4mRj0ywKWe1PD//p+B4QMOmqGeMAYAAY/2nw=='

################################################################################

class GUISizeTree(ttk.Frame):

    @classmethod
    def main(cls):
        # Create the application's root.
        NoDefaultRoot()
        root = Tk()
        # Restrict sizing and add title.
        root.minsize(350, 175)
        root.title('Directory Size')
        # Create the application's icon.
        with open('tree.ico', 'wb') as file:
            file.write(zlib.decompress(base64.b64decode(ICON)))
        root.iconbitmap('tree.ico')
        os.remove('tree.ico')
        # Configure the SizeTree object.
        view = cls(root)
        view.grid(row=0, column=0, sticky=NSEW)
        # Setup the window for resizing.
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        # Enter the GUI main event loop.
        root.mainloop()

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        # Configure the progressbar.
        self.__progress = ttk.Progressbar(self, orient=HORIZONTAL)
        self.__progress.grid(row=0, column=0, columnspan=4, sticky=EW)
        # Configure the tree.
        self.__tree = ttk.Treeview(self, selectmode=BROWSE,
                                   columns=('d_size', 'f_size', 'path'))
        self.__tree.heading('#0', text=' Name', anchor=W)
        self.__tree.heading('d_size', text=' Total Size', anchor=W)
        self.__tree.heading('f_size', text=' File Size', anchor=W)
        self.__tree.heading('path', text=' Path', anchor=W)
        self.__tree.column('#0', minwidth=80, width=160)
        self.__tree.column('d_size', minwidth=80, width=160)
        self.__tree.column('f_size', minwidth=80, width=160)
        self.__tree.column('path', minwidth=80, width=160)
        self.__tree.grid(row=1, column=0, columnspan=3, sticky=NSEW)
        # Configure the scrollbar.
        self.__scroll = ttk.Scrollbar(self, orient=VERTICAL,
                                      command=self.__tree.yview)
        self.__tree.configure(yscrollcommand=self.__scroll.set)
        self.__scroll.grid(row=1, column=3, sticky=NS)
        # Configure the path button.
        self.__label = ttk.Button(self, text='Path:', command=self.choose)
        self.__label.bind('<Return>', self.choose)
        self.__label.grid(row=2, column=0)
        # Configure the directory dialog.
        head, tail = os.getcwd(), True
        while tail:
            head, tail = os.path.split(head)
        self.__dialog = filedialog.Directory(self, initialdir=head)
        # Configure the path entry box.
        self.__path = ttk.Entry(self, cursor='xterm')
        self.__path.bind('<Control-Key-a>', self.select_all)
        self.__path.bind('<Control-Key-/>', lambda event: 'break')
        self.__path.bind('<Return>', self.search)
        self.__path.grid(row=2, column=1, sticky=EW)
        self.__path.focus_set()
        # Configure the execution button.
        self.__run = ttk.Button(self, text='Search', command=self.search)
        self.__run.bind('<Return>', self.search)
        self.__run.grid(row=2, column=2)
        # Configure the sizegrip.
        self.__grip = ttk.Sizegrip(self)
        self.__grip.grid(row=2, column=3, sticky=SE)
        # Configure the grid.
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # Configure root item in tree.
        self.__root = None

    def choose(self, event=None):
        # Get a directory path via a dialog.
        path = self.__dialog.show()
        if path:
            # Fill entry box with user path.
            self.__path.delete(0, END)
            self.__path.insert(0, os.path.abspath(path))

    def select_all(self, event):
        # Select the contents of the widget.
        event.widget.selection_range(0, END)
        return 'break'

    def search(self, event=None):
        if self.__run['state'].string == NORMAL:
            # Show background work progress.
            self.__run['state'] = DISABLED
            path = os.path.abspath(self.__path.get())
            if os.path.isdir(path):
                self.__progress.configure(mode='indeterminate', maximum=100)
                self.__progress.start()
                # Search while updating display.
                if self.__root is not None:
                    self.__tree.delete(self.__root)
                tree = SizeTree(self.update, path)
                nodes = tree.total_nodes + 1
                # Build user directory treeview.
                self.__progress.stop()
                self.__progress.configure(mode='determinate', maximum=nodes)
                self.__root = self.__tree.insert('', END, text=tree.name)
                self.build_tree(self.__root, tree)
                # Indicate completion of search.
                self.__run['state'] = NORMAL
            else:
                self.shake()

    def shake(self):
        # Check frame rate.
        assert getbusywaitinterval() == 20, 'Values are hard-coded for 50 FPS.'
        # Get application root.
        root = self
        while not isinstance(root, Tk):
            root = root.master
        # Schedule beginning of animation.
        self.after_idle(self.__shake, root, 0)

    def __shake(self, root, frame):
        frame += 1
        # Get the window's location and update X value.
        x, y = map(int, root.geometry().split('+')[1:])
        x += int(sin(pi * frame / 2.5) * sin(pi * frame / 50) * 5)
        root.geometry('+{}+{}'.format(x, y))
        # Schedule next frame or restore search button.
        if frame < 50:
            self.after(20, self.__shake, root, frame)
        else:
            self.__run['state'] = NORMAL

    def build_tree(self, node, tree):
        # Make changes to the treeview and progress bar.
        text = 'Unknown!' if tree.dir_error else convert(tree.total_size)
        self.__tree.set(node, 'd_size', text)
        text = 'Unknown!' if tree.file_error else convert(tree.file_size)
        self.__tree.set(node, 'f_size', text)
        self.__tree.set(node, 'path', tree.path)
        self.__progress.step()
        # Update the display and extract any child node.
        self.update()
        for child in tree.children:
            subnode = self.__tree.insert(node, END, text=child.name)
            self.build_tree(subnode, child)

################################################################################

class SizeTree:

    "Create a tree structure outlining a directory's size."

    def __init__(self, callback, path):
        callback()
        self.path = path
        head, tail = os.path.split(path)
        self.name = tail or head
        self.children = []
        self.file_size = 0
        self.total_size = 0
        self.total_nodes = 0
        self.file_error = False
        self.dir_error = False
        try:
            dir_list = os.listdir(path)
        except OSError:
            self.dir_error = True
        else:
            for name in dir_list:
                path_name = os.path.join(path, name)
                if os.path.isdir(path_name):
                    size_tree = SizeTree(callback, path_name)
                    self.children.append(size_tree)
                    self.total_size += size_tree.total_size
                    self.total_nodes += size_tree.total_nodes + 1
                elif os.path.isfile(path_name):
                    try:
                        self.file_size += os.path.getsize(path_name)
                    except OSError:
                        self.file_error = True
            self.total_size += self.file_size

################################################################################

def convert(number):
    "Convert bytes into human-readable representation."
    if not number:
        return '0 Bytes'
    assert 0 < number < 1 << 110, 'number out of range'
    ordered = reversed(tuple(format_bytes(partition_number(number, 1 << 10))))
    cleaned = ', '.join(item for item in ordered if item[0] != '0')
    return cleaned

def partition_number(number, base):
    "Continually divide number by base until zero."
    div, mod = divmod(number, base)
    yield mod
    while div:
        div, mod = divmod(div, base)
        yield mod

def format_bytes(parts):
    "Format partitioned bytes into human-readable strings."
    for power, number in enumerate(parts):
        yield '{} {}'.format(number, format_suffix(power, number))

def format_suffix(power, number):
    "Compute the suffix for a certain power of bytes."
    return (PREFIX[power] + 'byte').capitalize() + ('s' if number != 1 else '')

PREFIX = ' kilo mega giga tera peta exa zetta yotta bronto geop'.split(' ')

################################################################################

if __name__ == '__main__':
    GUISizeTree.main()
