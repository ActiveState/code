################################################################################
# Directory Pruner 3.pyw
################################################################################

package = __import__('Directory Pruner 3') # Get the source package of program.
package.main() # Call the main entry point to the Directory Pruner application.

################################################################################
# __init__.py
################################################################################

#! /usr/bin/env python

"""Module providing GUI capability to prune any directory.

The code presented in this module is for the purposes of: (1) ascertaining
the space taken up by a directory, its files, its sub-directories, and its
sub-files; (2) allowing for the removal of the sub-files, sub-directories,
files, and directory found in the first purpose; (3) giving the user a GUI
to accomplish said purposes in a convenient way that is easily accessible."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '21 February 2011'
__version__ = '$Revision: 418 $'

################################################################################

import base64
import os
import time
import tkinter
import zlib
from . import view
from . import widgets

################################################################################

ICON = b'eJxjYGAEQgEBBiApwZDBzMAgxsDAoAHEQCEGBQaIOAwkQDE2UOSkiUM\
Gp/rlyd740Ugzf8/uXROxAaA4VvVAqcfYAFCcoHqge4hR/+btWwgCqoez8aj//fs\
XWiAARfCrhyCg+XA2HvV/YACoHs4mRj0ywKWe1PD//p+B4QMOmqGeMAYAAY/2nw=='

################################################################################

def main():
    "Create an application containing a single TrimDir widget."
    tkinter.NoDefaultRoot()
    root = create_application_root()
    attach_window_icon(root, ICON)
    view = setup_class_instance(root)
    main_loop(root)

def create_application_root():
    "Create and configure the main application window."
    root = widgets.Tk()
    root.minsize(430, 215)
    root.title('Directory Pruner')
    root.option_add('*tearOff', tkinter.FALSE)
    return root

def attach_window_icon(root, icon):
    "Generate and use the icon in the window's corner."
    with open('tree.ico', 'wb') as file:
        file.write(zlib.decompress(base64.b64decode(ICON)))
    root.iconbitmap('tree.ico')
    os.remove('tree.ico')

def setup_class_instance(root):
    "Build TrimDir instance that expects resizing."
    instance = view.TrimDir(root)
    instance.grid(row=0, column=0, sticky=tkinter.NSEW)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    return instance

def main_loop(root):
    "Process all GUI events according to tkinter's settings."
    target = time.clock()
    while True:
        try:
            root.update()
        except tkinter.TclError:
            break
        target += tkinter._tkinter.getbusywaitinterval() / 1000
        time.sleep(max(target - time.clock(), 0))

################################################################################
# Directory Pruner 3/animator.py
################################################################################

#! /usr/bin/env python

"""Module for animating and displaying error messages.

The indicate_error function is the only available function in this module.
Calling it with the appropriate arguments should display an error for you."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '21 February 2011'
__version__ = '$Revision: 1 $'

################################################################################

import _tkinter
import math

################################################################################

def indicate_error(root, alternative, callback, force=False):
    "Prepare to shake the application's root window."
    if force:
        _tkinter.setbusywaitinterval(20)
    elif _tkinter.getbusywaitinterval() != 20:
        # Show error message if not running at 50 FPS.
        alternative.show()
        return callback()
    root.after_idle(_shake, root, callback)

def _shake(root, callback, frame=0):
    "Animate each step of shaking the root window."
    frame += 1
    # Get the window's location and update the X position.
    x, y = map(int, root.geometry().split('+')[1:])
    x += round(math.sin(math.pi * frame / 2.5) * \
               math.sin(math.pi * frame / 50) * 5)
    root.geometry('+{}+{}'.format(x, y))
    if frame < 50:
        # Schedule next step in the animation.
        root.after(20, _shake, root, callback, frame)
    else:
        # Enable operations after one second.
        callback()

################################################################################
# Directory Pruner 3/bytesize.py
################################################################################

#! /usr/bin/env python

"""Module for converting byte to strings and vice versa.

Various function are provided for changing byte sizes into English words.
If the conversion is exact, the string may also be converted into a number."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '21 February 2011'
__version__ = '$Revision: 1 $'

################################################################################

import math

################################################################################

# Provide a way of converting byte sizes into strings.

def convert(number):
    "Convert bytes into human-readable representation."
    if not number:
        return '0 Bytes'
    if not 0 < number < 1 << 110:
        raise ValueError('Number out of range!')
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

# Define additional operations for the TreeviewNode class.

def parse(string):
    "Convert human-readable string back into bytes."
    total = 0
    for part in string.split(', '):
        number, unit = part.split(' ')
        s = number != '1' and 's' or ''
        for power, prefix in enumerate(PREFIX):
            if unit == (prefix + 'byte' + s).capitalize():
                break
        else:
            raise ValueError('{!r} not found!'.format(unit))
        total += int(number) * 1 << 10 * power
    return total

def abbr(number):
    "Convert bytes into abbreviated representation."
    # Check value of number before processing.
    if not number:
        return '0 Bytes'
    if not 0 < number < (1 << 100) * 1000:
        raise ValueError('Number out of range!')
    # Calculate range of number and correct value.
    level = int(math.log(number) / math.log(1 << 10))
    value = number / (1 << 10 * level)
    # Move to the next level if number is high enough.
    if value < 1000:
        precision = 4
    else:
        precision = 3
        level += 1
        value /= 1 << 10
    # Format the number before returning to caller.
    if level:
        result = '{:.{}}'.format(value, precision)
        return '{} {}'.format(result, format_suffix(level, result == '1.0'))
    return '{} {}'.format(int(value), format_suffix(level, value))

################################################################################
# Directory Pruner 3/discover.py
################################################################################

#! /usr/bin/env python

"""Module for mapping out directory sizes.

Creating a SizeTree instance will automatically discover the directory size.
The directory's structure will be accessible through the tree-like structure."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '21 February 2011'
__version__ = '$Revision: 1 $'

################################################################################

import os

################################################################################

class SizeTree:

    "Create a tree structure outlining a directory's size."

    __slots__ = 'name path children file_size total_size total_nodes'.split()

    def __init__(self, path, callback=None):
        "Initialize the SizeTree object and search the path while updating."
        # Validate the search's current progress.
        if callback is not None:
            callback()
        head, tail = os.path.split(path)
        # Create attributes for this instance.
        self.name = tail or head
        self.path = path
        self.children = []
        self.file_size = 0
        self.total_size = 0
        self.total_nodes = 0
        # Try searching this directory.
        try:
            dir_list = os.listdir(path)
        except OSError:
            pass
        else:
            # Examine each object in this directory.
            for name in dir_list:
                path_name = os.path.join(path, name)
                if os.path.isdir(path_name):
                    # Create child nodes for subdirectories.
                    size_tree = SizeTree(path_name, callback)
                    self.children.append(size_tree)
                    self.total_size += size_tree.total_size
                    self.total_nodes += size_tree.total_nodes + 1
                elif os.path.isfile(path_name):
                    # Try getting the size of files.
                    try:
                        self.file_size += os.path.getsize(path_name)
                    except OSError:
                        pass
            # Add in the total file size to the total size.
            self.total_size += self.file_size

    def pop_child(self, name):
        "Return a named child or None if not found."
        for index, child in enumerate(self.children):
            if child.name == name:
                return self.children.pop(index)

    ########################################################################

    def __str__(self):
        "Return a representation of the tree formed by this object."
        lines = [self.path]
        self.__walk(lines, self.children, '')
        return '\n'.join(lines)

    @classmethod
    def __walk(cls, lines, children, prefix):
        "Generate lines based on children and keep track of prefix."
        dir_prefix, walk_prefix = prefix + '+---', prefix + '|   '
        for pos, neg, child in cls.__enumerate(children):
            if neg == -1:
                dir_prefix, walk_prefix = prefix + '\\---', prefix + '    '
            lines.append(dir_prefix + child.name)
            cls.__walk(lines, child.children, walk_prefix)

    @staticmethod
    def __enumerate(sequence):
        "Generate positive and negative indices for sequence."
        length = len(sequence)
        for count, value in enumerate(sequence):
            yield count, count - length, value

################################################################################
# Directory Pruner 3/remove.py
################################################################################

#! /usr/bin/env python

"""Module for removing files and directories.

These functions help in removing directories and files by various methods.
The core of the context menu is implemented by the provided capabilities."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '21 February 2011'
__version__ = '$Revision: 1 $'

################################################################################

import os

################################################################################

def directory_files(path, remove_directory=False, remove_path=False):
    "Remove directory at path, respecting the flags."
    for root, dirs, files in os.walk(path, False):
        # Ignore path if remove_path is false.
        if remove_path or root != path:
            for name in files:
                filename = os.path.join(root, name)
                try:
                    os.remove(filename)
                except OSError:
                    pass
            # Ignore directory if remove_directory is false.
            if remove_directory:
                try:
                    os.rmdir(root)
                except OSError:
                    pass

def files(path):
    "Remove files in path and get remaining space."
    total_size = 0
    # Find all files in directory of path.
    for name in os.listdir(path):
        pathname = os.path.join(path, name)
        if os.path.isfile(pathname):
            # Try to remove any file that may have been found.
            try:
                os.remove(pathname)
            except OSError:
                # If there was an error, try to get the filesize.
                try:
                    total_size += os.path.getsize(pathname)
                except OSError:
                    pass
    # Return best guess of space still occupied.
    return total_size

def empty_directories(path, remove_root=False, recursive=True):
    "Remove all empty directories while respecting the flags."
    if recursive:
        for name in os.listdir(path):
            try:
                empty_directories(os.path.join(path, name), True)
            except OSError:
                pass
    if remove_root:
        os.rmdir(path)

def empty_files(path, recursive=True):
    "Remove all files that are empty of any contents."
    for root, dirs, files in os.walk(path):
        if not recursive:
            del dirs[:]
        for name in files:
            filename = os.path.join(root, name)
            try:
                if not os.path.getsize(filename):
                    os.remove(filename)
            except OSError:
                pass

################################################################################
# Directory Pruner 3/runmethod.py
################################################################################

#! /usr/bin/env python

"""Module executing same method on tuple items.

The Apply class can store items and run the same method on all objects.
Results are returned as a tuple, and exeception are raised when needed."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '21 February 2011'
__version__ = '$Revision: 1 $'

################################################################################

class Apply(tuple):

    "Create a container that can run a method from its contents."

    def __getattr__(self, name):
        "Get a virtual method to map and apply to the contents."
        return self.__Method(self, name)

    ########################################################################

    class __Method:

        "Provide a virtual method that can be called on the array."

        def __init__(self, array, name):
            "Initialize the method with array and method name."
            self.__array = array
            self.__name = name

        def __call__(self, *args, **kwargs):
            "Execute method on contents with provided arguments."
            name, error, buffer = self.__name, False, []
            for item in self.__array:
                attr = getattr(item, name)
                try:
                    data = attr(*args, **kwargs)
                except Exception as problem:
                    error = problem
                else:
                    if not error:
                        buffer.append(data)
            if error:
                raise error
            return tuple(buffer)

################################################################################
# Directory Pruner 3/scheduler.py
################################################################################

#! /usr/bin/env python

"""Module for scheduling execution on single thread.

This is the core of the GUI's ability to run in a multi-threaded environment.
Calling run on a class instance ensures execution on the creating thread."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '21 February 2011'
__version__ = '$Revision: 1 $'

################################################################################

import _thread
import functools
import queue
import warnings

################################################################################

class Affinity:

    "Predecessor to AffinityLoop that might not return results."

    __slots__ = '__action', '__thread'

    def __init__(self):
        "Initialize Affinity with job queue and thread identity."
        self.__action = queue.Queue()
        self.__thread = _thread.get_ident()

    def run(self, func, *args, **keywords):
        "Try to run function with arguments on the creating thread."
        self.__action.put_nowait(functools.partial(func, *args, **keywords))
        if _thread.get_ident() == self.__thread:
            problem = False
            while not self.__action.empty():
                delegate = self.__action.get_nowait()
                try:
                    data = delegate()
                except Exception as error:
                    problem = error
            if problem:
                raise problem
            return data
        warnings.warn('Affinity did not return!')

################################################################################

class AffinityLoop:

    "Restricts code execution to thread that instance was created on."

    __slots__ = '__action', '__thread'

    def __init__(self):
        "Initialize AffinityLoop with job queue and thread identity."
        self.__action = queue.Queue()
        self.__thread = _thread.get_ident()

    def run(self, func, *args, **keywords):
        "Run function on creating thread and return result."
        if _thread.get_ident() == self.__thread:
            self.__run_jobs()
            return func(*args, **keywords)
        else:
            job = self.__Job(func, args, keywords)
            self.__action.put_nowait(job)
            return job.result

    def __run_jobs(self):
        "Run all pending jobs currently in the job queue."
        while not self.__action.empty():
            job = self.__action.get_nowait()
            job.execute()

    ########################################################################

    class __Job:

        "Store information to run a job at a later time."

        __slots__ = ('__func', '__args', '__keywords',
                     '__error', '__mutex', '__value')

        def __init__(self, func, args, keywords):
            "Initialize the job's info and ready for execution."
            self.__func = func
            self.__args = args
            self.__keywords = keywords
            self.__error = False
            self.__mutex = _thread.allocate_lock()
            self.__mutex.acquire()

        def execute(self):
            "Run the job, store any error, and return to sender."
            try:
                self.__value = self.__func(*self.__args, **self.__keywords)
            except Exception as error:
                self.__error = True
                self.__value = error
            self.__mutex.release()

        @property
        def result(self):
            "Return execution result or raise an error."
            self.__mutex.acquire()
            if self.__error:
                raise self.__value
            return self.__value

################################################################################
# Directory Pruner 3/threadlog.py
################################################################################

#! /usr/bin/env python

"""Module for starting threads that have their errors logged.

The start_thread function is the only procedure for use in this module.
When threads are started, errors will be automatically written to a file."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '21 February 2011'
__version__ = '$Revision: 1 $'

################################################################################

import _thread
import logging
import os
import sys
import traceback

################################################################################

def start_thread(function, *args, **kwargs):
    "Start a new thread and wrap with error catching."
    _thread.start_new_thread(_bootstrap, (function, args, kwargs))

def _bootstrap(function, args, kwargs):
    "Run function with arguments and log any errors."
    try:
        function(*args, **kwargs)
    except Exception:
        basename = os.path.basename(sys.argv[0])
        filename = os.path.splitext(basename)[0] + '.log'
        logging.basicConfig(filename=filename)
        logging.error(traceback.format_exc())

################################################################################
# Directory Pruner 3/treeview.py
################################################################################

#! /usr/bin/env python

"""Module for manipulating nodes in a treeview.

The Node class provides a high-level interface to work with treeview nodes.
When creating a Node instance, a Treeview instance must should be wrapped."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '21 February 2011'
__version__ = '$Revision: 1 $'

################################################################################

import sys
import tkinter
from .bytesize import convert, parse, abbr
from .view import TrimDir

################################################################################

class Node:

    "Interface to allow easier interaction with Treeview instance."

    @classmethod
    def current(cls, tree):
        "Take a tree view and return its currently selected node."
        node = tree.selection()
        return cls(tree, node[0] if node else node)

    ########################################################################

    # Standard Treeview Operations

    __slots__ = '__tree', '__node'

    def __init__(self, tree, node=''):
        "Initialize the Node object (root if node not given)."
        self.__tree = tree
        self.__node = node

    def __str__(self):
        "Return a string representation of this node."
        return '''\
NODE: {!r}
  Name: {}
  Total Size: {}
  File Size: {}
  Path {}\
'''.format(self.__node, self.name, self.total_size, self.file_size, self.path)

    def insert(self, position, text):
        "Insert a new node with text at position in current node."
        node = self.__tree.insert(self.__node, position, text=text)
        # PATCH: Store extra data about node.
        if TrimDir.SIZE:
            self.__tree.nodes[node] = dict()
        return Node(self.__tree, node)

    def append(self, text):
        "Add a new node with text to the end of this node."
        return self.insert(tkinter.END, text)

    def move(self, parent, index):
        "Insert this node under parent at index."
        self.__tree.move(self.__node, parent, index)

    def reattach(self, parent='', index=tkinter.END):
        "Attach node to parent at index (defaults to end of root)."
        self.move(parent, index)

    def detach(self):
        "Unlink this node from its parent but do not delete."
        self.__tree.detach(self.__node)

    def delete(self, get_parent=False, from_tree=True): # Internal Last Flag
        "Delete this node (optionally, return parent)."
        if self.__tree.exists(self.__node):
            parent = self.parent if get_parent else None
            # PATCH: Remove extra data about node.
            if TrimDir.SIZE:
                for child in self.children:
                    child.delete(from_tree=False)
                del self.__tree.nodes[self.__node]
            if from_tree:
                self.__tree.delete(self.__node)
            #=====================================
            return parent
        if get_parent:
            raise ValueError('Cannot return parent!')

    ########################################################################

    # Standard Treeview Properties

    @property
    def root(self):
        "Return if this is the root node."
        return self.__node == ''

    @property
    def parent(self):
        "Return the parent of this node."
        return Node(self.__tree, self.__tree.parent(self.__node))

    @property
    def level(self):
        "Return number of levels this node is under root."
        count, node = 0, self
        while not node.root:
            node = node.parent
            count += 1
        return count

    @property
    def position(self):
        "Return the position of this node in its parent."
        return self.__tree.index(self.__node)

    @property
    def expanded(self):
        "Return whether or not the node is current open."
        value = self.__tree.item(self.__node, 'open')
        return bool(value) and value.string == 'true'

    @property
    def children(self):
        "Yield back each child of this node."
        for child in self.__tree.get_children(self.__node):
            yield Node(self.__tree, child)

    ########################################################################

    # Custom Treeview Properties
    # (specific for application)

    @property
    def name(self):
        "Return the name of this node (tree column)."
        return self.__tree.item(self.__node, 'text')

    # PATCH: Custom Size
    if TrimDir.SIZE:
        # Shortened Byte Size
        def __get_total_size(self):
            return self.__tree.nodes[self.__node][TrimDir.CLMS[0]]

        def __set_total_size(self, value):
            self.__tree.nodes[self.__node][TrimDir.CLMS[0]] = value
            self.__tree.set(self.__node, TrimDir.CLMS[0], abbr(value))

        def __get_file_size(self):
            return self.__tree.nodes[self.__node][TrimDir.CLMS[1]]

        def __set_file_size(self, value):
            self.__tree.nodes[self.__node][TrimDir.CLMS[1]] = value
            self.__tree.set(self.__node, TrimDir.CLMS[1], abbr(value))
    else:
        # Complete Byte Size
        def __get_total_size(self):
            return parse(self.__tree.set(self.__node, TrimDir.CLMS[0]))

        def __set_total_size(self, value):
            self.__tree.set(self.__node, TrimDir.CLMS[0], convert(value))

        def __get_file_size(self):
            return parse(self.__tree.set(self.__node, TrimDir.CLMS[1]))

        def __set_file_size(self, value):
            self.__tree.set(self.__node, TrimDir.CLMS[1], convert(value))
    #=========================================================================

    def __get_path(self):
        return self.__tree.set(self.__node, TrimDir.CLMS[2])

    def __set_path(self, value):
        self.__tree.set(self.__node, TrimDir.CLMS[2], value)

    total_size = property(__get_total_size, __set_total_size,
                          doc="Total size of this node (first column)")

    file_size = property(__get_file_size, __set_file_size,
                         doc="File size of this node (second column)")

    path = property(__get_path, __set_path,
                    doc="Path of this node (third column)")

    ########################################################################

    # Custom Treeview Sort Order
    # (specific for application)

    def sort_name(self):
        "If the node is open, sort its children by name."
        self.__sort(lambda child: child.name)

    def sort_total_size(self):
        "If the node is open, sort its children by total size."
        self.__sort(lambda child: child.total_size)

    def sort_file_size(self):
        "If the node is open, sort its children by file size."
        self.__sort(lambda child: child.file_size)

    def sort_path(self):
        "If the node is open, sort its children by path."
        self.__sort(lambda child: child.path)

    def __sort(self, key):
        "Sort an expanded node's children by the given key."
        if self.expanded:
            nodes = list(self.children)
            order = sorted(nodes, key=key)
            if order == nodes:
                order = reversed(order)
            for child in order:
                self.__tree.move(child.__node, self.__node, tkinter.END)

################################################################################
# Directory Pruner 3/view.py
################################################################################

#! /usr/bin/env python

"""Module containing main GUI class of application.

The overly large TrimDir class is the main interface to this program.
To use Directory Pruner in other programs, create and use TrimDir objects."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '21 February 2011'
__version__ = '$Revision: 1 $'

################################################################################

import os
import tkinter
from . import animator
from . import discover
from . import remove
from . import runmethod
from . import threadlog
from . import widgets

################################################################################

class TrimDir(widgets.Frame):

    "Widget for examining size of directory with optional deletion."

    WARN = True # Should warnings be made for permanent operations?
    MENU = True # Should the (destructive) context menu be enabled?
    SIZE = True # Should directory sizes be patched for less words?

    # Give names to columns.
    CLMS = 'total_size', 'file_size', 'path'
    TREE = '#0'

    ########################################################################

    # Initialize the TrimDir object.

    __slots__ = ('__tk', '__label', '__path', '__run', '__cancel',
                 '__progress', '__tree', '__scroll_1', '__scroll_2',
                 '__grip', '__menu', '__dialog', '__error', '__warn')

    def __init__(self, master=None, **kw):
        "Initialize the TrimDir instance and configure for operation."
        super().__init__(master, **kw)
        # Initialize and configure this frame widget.
        self.capture_root()
        self.create_widgets()
        self.create_supports()
        self.create_bindings()
        self.configure_grid()
        self.configure_tree()
        self.configure_menu()
        # Set focus to path entry.
        self.__path.focus_set()

    def capture_root(self):
        "Capture the root (Tk instance) of this application."
        widget = self.master
        while not isinstance(widget, widgets.Tk):
            widget = widget.master
        self.__tk = widget

    def create_widgets(self):
        "Create all the widgets that will be placed in this frame."
        self.__label = widgets.Button(self, text='Path:', command=self.choose)
        self.__path = widgets.Entry(self, cursor='xterm')
        self.__run = widgets.Button(self, text='Search', command=self.search)
        self.__cancel = widgets.Button(self, text='Cancel',
                                       command=self.stop_search)
        self.__progress = widgets.Progressbar(self, orient=tkinter.HORIZONTAL)
        self.__tree = widgets.Treeview(self, columns=self.CLMS,
                                       selectmode=tkinter.BROWSE)
        self.__scroll_1 = widgets.Scrollbar(self, orient=tkinter.VERTICAL,
                                            command=self.__tree.yview)
        self.__scroll_2 = widgets.Scrollbar(self, orient=tkinter.HORIZONTAL,
                                            command=self.__tree.xview)
        self.__grip = widgets.Sizegrip(self)

    def create_supports(self):
        "Create all GUI elements not placed directly in this frame."
        self.__menu = widgets.Menu(self)
        self.create_directory_browser()
        self.create_error_message()
        self.create_warning_message()

    def create_directory_browser(self):
        "Find root of file system and create directory browser."
        head, tail = os.getcwd(), True
        while tail:
            head, tail = os.path.split(head)
        self.__dialog = widgets.Directory(self, initialdir=head)

    def create_error_message(self):
        "Create error message when trying to search bad path."
        options = {'title': 'Path Error',
                   'icon': tkinter.messagebox.ERROR,
                   'type': tkinter.messagebox.OK,
                   'message': 'Directory does not exist.'}
        self.__error = widgets.Message(self, **options)

    def create_warning_message(self):
        "Create warning message for permanent operations."
        options = {'title': 'Important Warning',
                   'icon': tkinter.messagebox.QUESTION,
                   'type': tkinter.messagebox.YESNO,
                   'message': '''\
You cannot undo these operations.
Are you sure you want to do this?'''}
        self.__warn = widgets.Message(self, **options)

    def create_bindings(self):
        "Bind the widgets to any events they will need to handle."
        self.__label.bind('<Return>', self.choose)
        self.__path.bind('<Control-Key-a>', self.select_all)
        self.__path.bind('<Control-Key-/>', lambda event: 'break')
        self.__path.bind('<Return>', self.search)
        self.__run.bind('<Return>', self.search)
        self.__cancel.bind('<Return>', self.stop_search)
        self.bind_right_click(self.__tree, self.open_menu)

    @staticmethod
    def select_all(event):
        "Select all of the contents in this Entry widget."
        event.widget.selection_range(0, tkinter.END)
        return 'break'

    def bind_right_click(self, widget, action):
        "Bind action to widget while considering Apple computers."
        if self.__tk.tk.call('tk', 'windowingsystem') == 'aqua':
            widget.bind('<2>', action)
            widget.bind('<Control-1>', action)
        else:
            widget.bind('<3>', action)

    def configure_grid(self):
        "Place all widgets on the grid in their respective locations."
        self.__label.grid(row=0, column=0)
        self.__path.grid(row=0, column=1, sticky=tkinter.EW)
        self.__run.grid(row=0, column=2, columnspan=2)
        self.__run.grid_remove()
        self.__cancel.grid(row=0, column=2, columnspan=2)
        self.__cancel.grid_remove()
        self.__run.grid()
        self.__progress.grid(row=1, column=0, columnspan=4, sticky=tkinter.EW)
        self.__tree.grid(row=2, column=0, columnspan=3, sticky=tkinter.NSEW)
        self.__scroll_1.grid(row=2, column=3, sticky=tkinter.NS)
        self.__scroll_2.grid(row=3, column=0, columnspan=3, sticky=tkinter.EW)
        self.__grip.grid(row=3, column=3, sticky=tkinter.SE)
        # Configure the grid to automatically resize internal widgets.
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def configure_tree(self):
        "Configure the Treeview widget."
        # Setup the headings.
        self.__tree.heading(self.TREE, text=' Name', anchor=tkinter.W,
                            command=self.sort_name)
        self.__tree.heading(self.CLMS[0], text=' Total Size', anchor=tkinter.W,
                            command=self.sort_total_size)
        self.__tree.heading(self.CLMS[1], text=' File Size', anchor=tkinter.W,
                            command=self.sort_file_size)
        self.__tree.heading(self.CLMS[2], text=' Path', anchor=tkinter.W,
                            command=self.sort_path)
        # Setup the columns.
        self.__tree.column(self.TREE, minwidth=100, width=200)
        self.__tree.column(self.CLMS[0], minwidth=100, width=200)
        self.__tree.column(self.CLMS[1], minwidth=100, width=200)
        self.__tree.column(self.CLMS[2], minwidth=100, width=200)
        # Connect the Scrollbars.
        self.__tree.configure(yscrollcommand=self.__scroll_1.set)
        self.__tree.configure(xscrollcommand=self.__scroll_2.set)
        # PATCH: Provide data store.
        if TrimDir.SIZE:
            self.__tree.nodes = dict()

    def configure_menu(self):
        "Configure the (context) Menu widget."
        # Shortcut for narrowing the search.
        self.__menu.add_command(label='Search Directory',
                                command=self.search_dir)
        self.__menu.add_separator()
        # Operations committed on directory.
        self.__menu.add_command(label='Remove Directory', command=self.rm_dir)
        self.__menu.add_command(label='Remove Files', command=self.rm_files)
        self.__menu.add_separator()
        # Operations that recurse on sub-directories.
        self.__menu.add_command(label='Remove Sub-directories',
                                command=self.rm_subdirs)
        self.__menu.add_command(label='Remove Sub-files',
                                command=self.rm_subfiles)
        self.__menu.add_separator()
        # Operations that remove empty directories and files.
        self.__menu.add_command(label='Remove Empty Directories',
                                command=self.rm_empty_dirs)
        self.__menu.add_command(label='Remove Empty Files',
                                command=self.rm_empty_files)
        # Only add "Open Directory" command on Windows.
        if hasattr(os, 'startfile'):
            self.__menu.add_separator()
            self.__menu.add_command(label='Open Directory',
                                    command=self.open_dir)

    ########################################################################

    # This property is used to control access to operations.

    def __get_operations_enabled(self):
        "Return if run button is in normal state."
        return self.__run['state'].string == tkinter.NORMAL

    def __set_operations_enabled(self, value):
        "Enable or disable run button's state according to value."
        self.__run['state'] = tkinter.NORMAL if value else tkinter.DISABLED

    operations_enabled = property(__get_operations_enabled,
                                  __set_operations_enabled,
                                  doc="Flag controlling certain operations")

    ########################################################################

    # Handle path browsing and searching actions.

    def choose(self, event=None):
        "Show directory browser and set path as needed."
        path = self.__dialog.show()
        if path:
            # Entry is cleared before absolute path is added.
            self.__path.delete(0, tkinter.END)
            self.__path.insert(0, os.path.abspath(path))

    def search(self, event=None):
        "Start search thread while GUI automatically updates."
        threadlog.start_thread(self.search_thread)

    def search_thread(self):
        "Search the path and display the size of the directory."
        if self.operations_enabled:
            self.operations_enabled = False
            # Get absolute path and check existence.
            path = os.path.abspath(self.__path.get())
            if os.path.isdir(path):
                # Enable operations after finishing search.
                self.__search(path)
                self.operations_enabled = True
            else:
                animator.indicate_error(self.__tk, self.__error,
                                        self.enable_operations)

    def __search(self, path):
        "Execute the search procedure and display in Treeview."
        self.__run.grid_remove()
        self.__cancel.grid()
        children = self.start_search()
        try:
            tree = discover.SizeTree(path, self.validate_search)
        except StopIteration:
            self.handle_stop_search(children)
        else:
            self.finish_search(children, tree)
        self.__cancel.grid_remove()
        self.__run.grid()

    ########################################################################

    # Execute various phases of a search.

    def start_search(self):
        "Edit the GUI in preparation for executing a search."
        self.__stop_search = False
        children = runmethod.Apply(treeview.Node(self.__tree).children)
        children.detach()
        self.__progress.configure(mode='indeterminate', maximum=100)
        self.__progress.start()
        return children

    def validate_search(self):
        "Check that the current search action is valid."
        if self.__stop_search:
            self.__stop_search = False
            raise StopIteration('Search has been canceled!')

    def stop_search(self, event=None):
        "Cancel a search by setting its stop flag."
        self.__stop_search = True

    def handle_stop_search(self, children):
        "Reset the Treeview and Progressbar on premature termination."
        children.reattach()
        self.__progress.stop()
        self.__progress['mode'] = 'determinate'

    def finish_search(self, children, tree):
        "Delete old children, update Progressbar, and update Treeview."
        children.delete()
        self.__progress.stop()
        self.__progress.configure(mode='determinate',
                                  maximum=tree.total_nodes+1)
        node = treeview.Node(self.__tree).append(tree.name)
        try:
            self.build_tree(node, tree)
        except StopIteration:
            pass

    ########################################################################

    # Handle Treeview column sorting events initiated by user.

    def sort_name(self):
        "Sort children of selected node by name."
        treeview.Node.current(self.__tree).sort_name()

    def sort_total_size(self):
        "Sort children of selected node by total size."
        treeview.Node.current(self.__tree).sort_total_size()

    def sort_file_size(self):
        "Sort children of selected node by file size."
        treeview.Node.current(self.__tree).sort_file_size()

    def sort_path(self):
        "Sort children of selected node by path."
        treeview.Node.current(self.__tree).sort_path()

    ########################################################################

    # Handle right-click events on the Treeview widget.

    def open_menu(self, event):
        "Select Treeview row and show context menu if allowed."
        item = event.widget.identify_row(event.y)
        if item:
            event.widget.selection_set(item)
            if self.menu_allowed:
                self.__menu.post(event.x_root, event.y_root)

    @property
    def menu_allowed(self):
        "Check if menu is enabled along with operations."
        return self.MENU and self.operations_enabled

    def search_dir(self):
        "Search the path of the currently selected row."
        path = treeview.Node.current(self.__tree).path
        self.__path.delete(0, tkinter.END)
        self.__path.insert(0, path)
        self.search()

    def rm_dir(self):
        "Remove the currently selected directory."
        if self.commit_permanent_operation:
            threadlog.start_thread(self.do_remove_directory)

    def rm_files(self):
        "Remove the files in the currently selected directory."
        if self.commit_permanent_operation:
            threadlog.start_thread(self.do_remove_files)

    def rm_subdirs(self):
        "Remove the sub-directories of the currently selected directory."
        if self.commit_permanent_operation:
            threadlog.start_thread(self.do_remove_subdirectories)

    def rm_subfiles(self):
        "Remove the sub-files of the currently selected directory."
        if self.commit_permanent_operation:
            threadlog.start_thread(self.do_remove_subfiles)

    def rm_empty_dirs(self):
        "Recursively remove empty directories from selected directory."
        if self.commit_permanent_operation:
            threadlog.start_thread(self.do_remove_empty_dirs)

    def rm_empty_files(self):
        "Recursively remove empty files from selected directory."
        if self.commit_permanent_operation:
            threadlog.start_thread(self.do_remove_empty_files)

    @property
    def commit_permanent_operation(self):
        "Check if warning should be issued before committing operation."
        return not self.WARN or self.__warn.show() == tkinter.messagebox.YES

    def open_dir(self):
        "Open up the current directory (only available on Windows)."
        os.startfile(treeview.Node.current(self.__tree).path)

    ########################################################################

    # Execute actions requested by context menu.

    def do_remove_directory(self):
        "Remove a directory and all of its sub-directories."
        self.begin_rm()
        # Get the current Treeview node and delete it.
        node = treeview.Node.current(self.__tree)
        directory_size, path = node.total_size, node.path
        position, parent = node.position, node.delete(True)
        # Delete the entire directory at path.
        remove.directory_files(path, True, True)
        if os.path.isdir(path):
            # Add the directory back to the Treeview.
            tree = discover.SizeTree(path)
            self.begin_rm_update(tree.total_nodes + 1)
            # Rebuild the Treeview under the parent.
            node = parent.insert(position, tree.name)
            self.build_tree(node, tree)
            # New directory size.
            total_size = tree.total_size
        else:
            self.begin_rm_update()
            # New directory size.
            total_size = 0
        # If the size has changed, update parent nodes.
        if directory_size != total_size:
            diff = total_size - directory_size
            self.update_parents(parent, diff)
        self.end_rm()

    def do_remove_files(self):
        "Remove all of the files in the selected directory."
        # Delete files in the directory and get its new size.
        node = treeview.Node.current(self.__tree)
        total_size = remove.files(node.path)
        # Update current and parent nodes if the size changed.
        if node.file_size != total_size:
            diff = total_size - node.file_size
            node.file_size = total_size
            node.total_size += diff
            self.update_parents(node.parent, diff)

    def do_remove_subdirectories(self):
        "Remove all subdirectories in the directory."
        self.begin_rm()
        # Remove all the children nodes in Viewtree.
        node = treeview.Node.current(self.__tree)
        for child in node.children:
            child.delete()
        # Delete all of the subdirectories and their files.
        remove.directory_files(node.path, True)
        # Find out what subdirectories could not be deteled.
        tree = discover.SizeTree(node.path)
        self.begin_rm_update(tree.total_nodes)
        if tree.total_nodes:
            # Rebuild the Viewtree as needed.
            self.build_tree(node, tree, False)
            # Fix node and prepare to update parents.
            diff = node.total_size - tree.total_size
            node.total_size = tree.total_size
        else:
            # Fix node and prepare to update parents.
            diff = node.file_size - node.total_size
            node.total_size = node.file_size
        # Update parents with new size.
        self.update_parents(node.parent, diff)
        self.end_rm()

    def do_remove_subfiles(self):
        "Remove all subfiles while keeping subdirectories in place."
        self.begin_rm()
        node = treeview.Node.current(self.__tree)
        remove.directory_files(node.path)
        self.synchronize_tree(node)

    def do_remove_empty_dirs(self):
        "Remove all empty directories from selected directory."
        self.begin_rm()
        node = treeview.Node.current(self.__tree)
        remove.empty_directories(node.path)
        self.synchronize_tree(node)

    def do_remove_empty_files(self):
        "Remove all empty files from selected directory."
        self.begin_rm()
        # Remove empty files from the current path.
        node = treeview.Node.current(self.__tree)
        remove.empty_files(node.path)
        # Return the Progressbar back to normal.
        self.begin_rm_update()
        self.end_rm()

    ########################################################################

    # Help update Progressbar in removal process.

    def begin_rm(self):
        "Start a long-running removal operation."
        self.operations_enabled = False
        self.__progress.configure(mode='indeterminate', maximum=100)
        self.__progress.start()

    def begin_rm_update(self, nodes=0):
        "Move to determinate mode of updating the Viewtree."
        self.__progress.stop()
        self.__progress.configure(mode='determinate', maximum=nodes)

    def end_rm(self):
        "Finish removal process by enabling operations."
        self.operations_enabled = True

    enable_operations = end_rm  # Create alias for command.

    ########################################################################

    # Update the Viewtree nodes after creating a SizeTree object.

    def synchronize_tree(self, node):
        "Find the current directory state and update the tree."
        # Build a new SizeTree to find the result.
        tree = discover.SizeTree(node.path)
        self.begin_rm_update(tree.total_nodes)
        # Record the difference and patch the Viewtree.
        diff = tree.total_size - node.total_size
        self.patch_tree(node, tree)
        # Fix all parent nodes with the correct size.
        self.update_parents(node.parent, diff)
        self.end_rm()

    def build_tree(self, node, tree, update_node=True):
        "Build the Treeview while updating the Progressbar."
        self.validate_search()
        if update_node:
            self.sync_nodes(node, tree)
        self.add_children(node, tree)

    def sync_nodes(self, node, tree):
        "Update attributes on node and refresh GUI."
        # Copy the information on the node.
        node.total_size = tree.total_size
        node.file_size = tree.file_size
        node.path = tree.path
        # Update the Progressbar and GUI.
        self.__progress.step()

################################################################################
# Directory Pruner 3/widgets.py
################################################################################

#! /usr/bin/env python

"""Module for thread-safe GUI widget library.

The _ThreadSafe base class is provides a foundation for the other widgets.
Support for more widgets can be easily added by adding more definitions."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '21 February 2011'
__version__ = '$Revision: 1 $'

################################################################################

import operator
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk
from . import scheduler

################################################################################

class _ThreadSafe:

    "Create a thread-safe GUI class for safe cross-threaded calls."

    ROOT = tkinter.Tk

    def __init__(self, master=None, *args, **keywords):
        "Initialize a thread-safe wrapper around a GUI base class."
        if master is None:
            if self.BASE is not self.ROOT:
                raise ValueError('Widget must have a master!')
            # Use Affinity() if it does not break.
            self.__job = scheduler.AffinityLoop()
            self.__schedule(self.__initialize, *args, **keywords)
        else:
            self.master = master
            self.__job = master.__job
            self.__schedule(self.__initialize, master, *args, **keywords)

    def __initialize(self, *args, **keywords):
        "Delegate instance creation to later time if necessary."
        self.__obj = self.BASE(*args, **keywords)

    ########################################################################

    # Provide a framework for delaying method execution when needed.

    def __schedule(self, *args, **keywords):
        "Schedule execution of a method till later if necessary."
        return self.__job.run(self.__run, *args, **keywords)

    @classmethod
    def __run(cls, func, *args, **keywords):
        "Execute the function after converting the arguments."
        args = tuple(cls.unwrap(i) for i in args)
        keywords = dict((k, cls.unwrap(v)) for k, v in keywords.items())
        return func(*args, **keywords)

    @staticmethod
    def unwrap(obj):
        "Unpack inner objects wrapped by _ThreadSafe instances."
        return obj.__obj if isinstance(obj, _ThreadSafe) else obj

    ########################################################################

    # Allow access to and manipulation of wrapped instance's settings.

    def __getitem__(self, key):
        "Get a configuration option from the underlying object."
        return self.__schedule(operator.getitem, self, key)

    def __setitem__(self, key, value):
        "Set a configuration option on the underlying object."
        return self.__schedule(operator.setitem, self, key, value)

    ########################################################################

    # Create attribute proxies for methods and allow their execution.
    
    def __getattr__(self, name):
        "Create a requested attribute and return cached result."
        attr = self.__Attr(self.__callback, (name,))
        setattr(self, name, attr)
        return attr

    def __callback(self, path, *args, **keywords):
        "Schedule execution of named method from attribute proxy."
        return self.__schedule(self.__method, path, *args, **keywords)

    def __method(self, path, *args, **keywords):
        "Extract a method and run it with the provided arguments."
        method = self.__obj
        for name in path:
            method = getattr(method, name)
        return method(*args, **keywords)

    ########################################################################

    class __Attr:

        "Save an attribute's name and wait for execution."

        __slots__ = '__callback', '__path'

        def __init__(self, callback, path):
            "Initialize proxy with callback and method path."
            self.__callback = callback
            self.__path = path

        def __call__(self, *args, **keywords):
            "Run a known method with the given arguments."
            return self.__callback(self.__path, *args, **keywords)

        def __getattr__(self, name):
            "Generate a proxy object for a sub-attribute."
            if name in {'__func__', '__name__'}:
                # Hack for the "tkinter.__init__.Misc._register" method.
                raise AttributeError('This is not a real method!')
            return self.__class__(self.__callback, self.__path + (name,))

################################################################################

# Provide thread-safe classes to be used from tkinter.

class Tk(_ThreadSafe): BASE = tkinter.Tk
class Frame(_ThreadSafe): BASE = tkinter.ttk.Frame
class Button(_ThreadSafe): BASE = tkinter.ttk.Button
class Entry(_ThreadSafe): BASE = tkinter.ttk.Entry
class Progressbar(_ThreadSafe): BASE = tkinter.ttk.Progressbar
class Treeview(_ThreadSafe): BASE = tkinter.ttk.Treeview
class Scrollbar(_ThreadSafe): BASE = tkinter.ttk.Scrollbar
class Sizegrip(_ThreadSafe): BASE = tkinter.ttk.Sizegrip
class Menu(_ThreadSafe): BASE = tkinter.Menu
class Directory(_ThreadSafe): BASE = tkinter.filedialog.Directory
class Message(_ThreadSafe): BASE = tkinter.messagebox.Message


    def patch_tree(self, node, tree):
        "Patch differences between node and tree."
        node.total_size = tree.total_size
        node.file_size = tree.file_size
        self.patch_children(node, tree)
        self.add_children(node, tree)

    def add_children(self, node, tree):
        "Build and traverse all child nodes."
        for child in tree.children:
            subnode = node.append(child.name)
            self.build_tree(subnode, child)

    def patch_children(self, node, tree):
        "Patch Viewtree based on children of SizeTree."
        for subnode in node.children:
            child = tree.pop_child(subnode.name)
            if child is None:
                # Directory is gone.
                subnode.delete()
            else:
                # Dig down further in tree.
                self.__progress.step()
                self.patch_tree(subnode, child)

    @staticmethod
    def update_parents(node, diff):
        "Add in difference to node and parents."
        while not node.root:
            node.total_size += diff
            node = node.parent

################################################################################

# TrimDir must already exist.
from . import treeview
