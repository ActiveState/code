#! /usr/bin/env python3

"""Module providing GUI capability to prune any directory.

The code presented in this module is for the purposes of: (1) ascertaining
the space taken up by a directory, its files, its sub-directories, and its
sub-files; (2) allowing for the removal of the sub-files, sub-directories,
files, and directory found in the first purpose; (3) giving the user a GUI
to accomplish said purposes in a convenient way that is easily accessible."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '4 June 2012'
__version__ = 4, 2, 0

################################################################################

# Import several custom libraries.
from affinity import slots
from threadbox import MetaBox
from safetkinter import *

# Import other needed modules.
import _thread
import base64
import logging
import math
import os
import sys
import traceback
import zlib

################################################################################

ICON = b'eJxjYGAEQgEBBiApwZDBzMAgxsDAoAHEQCEGBQaIOAwkQDE2UOSkiUM\
Gp/rlyd740Ugzf8/uXROxAaA4VvVAqcfYAFCcoHqge4hR/+btWwgCqoez8aj//fs\
XWiAARfCrhyCg+XA2HvV/YACoHs4mRj0ywKWe1PD//p+B4QMOmqGeMAYAAY/2nw=='

################################################################################

# Allow starting threads that can be debugged.

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

class TrimDirView(Frame):

    "Widget for examining size of directory with optional deletion."

    WARN = True # Should warnings be made for permanent operations?
    MENU = True # Should the (destructive) context menu be enabled?
    SIZE = True # Should directory sizes be patched for less words?

    # Give names to columns.
    CLMS = 'total_size', 'file_size', 'path'
    TREE = '#0'

    ########################################################################

    # Allow direct execution of TrimDirView widget.

    @classmethod
    def main(cls):
        "Create an application containing a single TrimDirView widget."
        root = cls.create_application_root()
        cls.attach_window_icon(root, ICON)
        view = cls.setup_class_instance(root)
        root.mainloop()

    @staticmethod
    def create_application_root():
        "Create and configure the main application window."
        root = Tk()
        root.minsize(430, 215)
        root.title('Directory Pruner')
        root.option_add('*tearOff', tkinter.FALSE)
        return root

    @staticmethod
    def attach_window_icon(root, icon):
        "Generate and use the icon in the window's corner."
        with open('tree.ico', 'wb') as file:
            file.write(zlib.decompress(base64.b64decode(ICON)))
        root.iconbitmap('tree.ico')
        os.remove('tree.ico')

    @classmethod
    def setup_class_instance(cls, root):
        "Build TrimDirView instance that expects resizing."
        instance = cls(root)
        instance.grid(row=0, column=0, sticky=tkinter.NSEW)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        return instance

    ########################################################################

    # Initialize the TrimDirView object.

    def __init__(self, master=None, **kw):
        "Initialize the TrimDirView instance and configure for operation."
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
        while not isinstance(widget, Tk):
            widget = widget.master
        self.__tk = widget

    def create_widgets(self):
        "Create all the widgets that will be placed in this frame."
        self.__label = Button(self, text='Path:', command=self.choose)
        self.__path = Entry(self, cursor='xterm')
        self.__run = Button(self, text='Search', command=self.search)
        self.__cancel = Button(self, text='Cancel', command=self.stop_search)
        self.__progress = Progressbar(self, orient=tkinter.HORIZONTAL)
        self.__tree = Treeview(self, columns=self.CLMS,
                               selectmode=tkinter.BROWSE)
        self.__scroll_1 = Scrollbar(self, orient=tkinter.VERTICAL,
                                    command=self.__tree.yview)
        self.__scroll_2 = Scrollbar(self, orient=tkinter.HORIZONTAL,
                                    command=self.__tree.xview)
        self.__grip = Sizegrip(self)

    def create_supports(self):
        "Create all GUI elements not placed directly in this frame."
        self.__menu = Menu(self)
        self.create_directory_browser()
        self.create_error_message()
        self.create_warning_message()

    def create_directory_browser(self):
        "Find root of file system and create directory browser."
        head, tail = os.getcwd(), True
        while tail:
            head, tail = os.path.split(head)
        self.__dialog = Directory(self, initialdir=head)

    def create_error_message(self):
        "Create error message when trying to search bad path."
        options = {'title': 'Path Error',
                   'icon': tkinter.messagebox.ERROR,
                   'type': tkinter.messagebox.OK,
                   'message': 'Directory does not exist.'}
        self.__error = Message(self, **options)

    def create_warning_message(self):
        "Create warning message for permanent operations."
        options = {'title': 'Important Warning',
                   'icon': tkinter.messagebox.QUESTION,
                   'type': tkinter.messagebox.YESNO,
                   'message': '''\
You cannot undo these operations.
Are you sure you want to do this?'''}
        self.__warn = Message(self, **options)

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
        if TrimDirView.SIZE:
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
        start_thread(self.search_thread)

    @MetaBox.thread
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
                indicate_error(self.__tk, self.__error, self.enable_operations)

    @MetaBox.thread
    def __search(self, path):
        "Execute the search procedure and display in Treeview."
        self.__run.grid_remove()
        self.__cancel.grid()
        children = self.start_search()
        try:
            tree = SizeTree(path, self.validate_search)
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
        children = Apply(TreeviewNode(self.__tree).children)
        children.detach()
        self.__progress.configure(mode='indeterminate', maximum=100)
        self.__progress.start()
        return children

    @MetaBox.thread
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

    @MetaBox.thread
    def finish_search(self, children, tree):
        "Delete old children, update Progressbar, and update Treeview."
        children.delete()
        self.__progress.stop()
        self.__progress.configure(mode='determinate',
                                  maximum=tree.total_nodes+1)
        node = TreeviewNode(self.__tree).append(tree.name)
        try:
            self.build_tree(node, tree)
        except StopIteration:
            pass

    ########################################################################

    # Handle Treeview column sorting events initiated by user.

    def sort_name(self):
        "Sort children of selected node by name."
        TreeviewNode.current(self.__tree).sort_name()

    def sort_total_size(self):
        "Sort children of selected node by total size."
        TreeviewNode.current(self.__tree).sort_total_size()

    def sort_file_size(self):
        "Sort children of selected node by file size."
        TreeviewNode.current(self.__tree).sort_file_size()

    def sort_path(self):
        "Sort children of selected node by path."
        TreeviewNode.current(self.__tree).sort_path()

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
        path = TreeviewNode.current(self.__tree).path
        self.__path.delete(0, tkinter.END)
        self.__path.insert(0, path)
        self.search()

    def rm_dir(self):
        "Remove the currently selected directory."
        if self.commit_permanent_operation:
            start_thread(self.do_remove_directory)

    def rm_files(self):
        "Remove the files in the currently selected directory."
        if self.commit_permanent_operation:
            start_thread(self.do_remove_files)

    def rm_subdirs(self):
        "Remove the sub-directories of the currently selected directory."
        if self.commit_permanent_operation:
            start_thread(self.do_remove_subdirectories)

    def rm_subfiles(self):
        "Remove the sub-files of the currently selected directory."
        if self.commit_permanent_operation:
            start_thread(self.do_remove_subfiles)

    def rm_empty_dirs(self):
        "Recursively remove empty directories from selected directory."
        if self.commit_permanent_operation:
            start_thread(self.do_remove_empty_dirs)

    def rm_empty_files(self):
        "Recursively remove empty files from selected directory."
        if self.commit_permanent_operation:
            start_thread(self.do_remove_empty_files)

    @property
    def commit_permanent_operation(self):
        "Check if warning should be issued before committing operation."
        return not self.WARN or self.__warn.show() == tkinter.messagebox.YES

    def open_dir(self):
        "Open up the current directory (only available on Windows)."
        os.startfile(TreeviewNode.current(self.__tree).path)

    ########################################################################

    # Execute actions requested by context menu.

    @MetaBox.thread
    def do_remove_directory(self):
        "Remove a directory and all of its sub-directories."
        self.begin_rm()
        # Get the current Treeview node and delete it.
        node = TreeviewNode.current(self.__tree)
        directory_size, path = node.total_size, node.path
        position, parent = node.position, node.delete(True)
        # Delete the entire directory at path.
        remove_directory_files(path, True, True)
        if os.path.isdir(path):
            # Add the directory back to the Treeview.
            tree = SizeTree(path)
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
        node = TreeviewNode.current(self.__tree)
        total_size = remove_files(node.path)
        # Update current and parent nodes if the size changed.
        if node.file_size != total_size:
            diff = total_size - node.file_size
            node.file_size = total_size
            node.total_size += diff
            self.update_parents(node.parent, diff)

    @MetaBox.thread
    def do_remove_subdirectories(self):
        "Remove all subdirectories in the directory."
        self.begin_rm()
        # Remove all the children nodes in Viewtree.
        node = TreeviewNode.current(self.__tree)
        for child in node.children:
            child.delete()
        # Delete all of the subdirectories and their files.
        remove_directory_files(node.path, True)
        # Find out what subdirectories could not be deteled.
        tree = SizeTree(node.path)
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

    @MetaBox.thread
    def do_remove_subfiles(self):
        "Remove all subfiles while keeping subdirectories in place."
        self.begin_rm()
        node = TreeviewNode.current(self.__tree)
        remove_directory_files(node.path)
        self.synchronize_tree(node)

    @MetaBox.thread
    def do_remove_empty_dirs(self):
        "Remove all empty directories from selected directory."
        self.begin_rm()
        node = TreeviewNode.current(self.__tree)
        remove_empty_directories(node.path)
        self.synchronize_tree(node)

    @MetaBox.thread
    def do_remove_empty_files(self):
        "Remove all empty files from selected directory."
        self.begin_rm()
        # Remove empty files from the current path.
        node = TreeviewNode.current(self.__tree)
        remove_empty_files(node.path)
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

    @MetaBox.thread
    def synchronize_tree(self, node):
        "Find the current directory state and update the tree."
        # Build a new SizeTree to find the result.
        tree = SizeTree(node.path)
        self.begin_rm_update(tree.total_nodes)
        # Record the difference and patch the Viewtree.
        diff = tree.total_size - node.total_size
        self.patch_tree(node, tree)
        # Fix all parent nodes with the correct size.
        self.update_parents(node.parent, diff)
        self.end_rm()

    @MetaBox.thread
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

    @MetaBox.thread
    def patch_tree(self, node, tree):
        "Patch differences between node and tree."
        node.total_size = tree.total_size
        node.file_size = tree.file_size
        self.patch_children(node, tree)
        self.add_children(node, tree)

    @MetaBox.thread
    def add_children(self, node, tree):
        "Build and traverse all child nodes."
        for child in tree.children:
            subnode = node.append(child.name)
            self.build_tree(subnode, child)

    @MetaBox.thread
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

# Show an error when searching paths that do not exist.

def indicate_error(root, alternative, callback, force=False):
    "Prepare to shake the application's root window."
    if force:
        tkinter._tkinter.setbusywaitinterval(20)
    elif tkinter._tkinter.getbusywaitinterval() != 20:
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

# Help in removing directories and files with these functions.

def remove_directory_files(path, remove_directory=False, remove_path=False):
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

def remove_files(path):
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

def remove_empty_directories(path, remove_root=False, recursive=True):
    "Remove all empty directories while respecting the flags."
    if recursive:
        for name in os.listdir(path):
            try:
                remove_empty_directories(os.path.join(path, name), True)
            except OSError:
                pass
    if remove_root:
        os.rmdir(path)

def remove_empty_files(path, recursive=True):
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

class TreeviewNode:

    "Interface to allow easier interaction with Treeview instance."

    @classmethod
    def current(cls, tree):
        "Take a tree view and return its currently selected node."
        node = tree.selection()
        return cls(tree, node[0] if node else node)

    ########################################################################

    # Standard Treeview Operations

    slots('tree, node')

    def __init__(self, tree, node=''):
        "Initialize the TreeviewNode object (root if node not given)."
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
        if TrimDirView.SIZE:
            self.__tree.nodes[node] = dict()
        return TreeviewNode(self.__tree, node)

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
            if TrimDirView.SIZE:
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
        return TreeviewNode(self.__tree, self.__tree.parent(self.__node))

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
        "Return whether or not this node is currently open."
        value = self.__tree.item(self.__node, 'open')
        return bool(value) and value.string == 'true'

    @property
    def children(self):
        "Yield back each child of this node."
        for child in self.__tree.get_children(self.__node):
            yield TreeviewNode(self.__tree, child)

    ########################################################################

    # Custom Treeview Properties
    # (specific for application)

    @property
    def name(self):
        "Return the name of this node (tree column)."
        return self.__tree.item(self.__node, 'text')

    # PATCH: Custom Size
    if TrimDirView.SIZE:
        # Shortened Byte Size
        def __get_total_size(self):
            return self.__tree.nodes[self.__node][TrimDirView.CLMS[0]]

        def __set_total_size(self, value):
            self.__tree.nodes[self.__node][TrimDirView.CLMS[0]] = value
            self.__tree.set(self.__node, TrimDirView.CLMS[0], abbr(value))

        def __get_file_size(self):
            return self.__tree.nodes[self.__node][TrimDirView.CLMS[1]]

        def __set_file_size(self, value):
            self.__tree.nodes[self.__node][TrimDirView.CLMS[1]] = value
            self.__tree.set(self.__node, TrimDirView.CLMS[1], abbr(value))
    else:
        # Complete Byte Size
        def __get_total_size(self):
            return parse(self.__tree.set(self.__node, TrimDirView.CLMS[0]))

        def __set_total_size(self, value):
            self.__tree.set(self.__node, TrimDirView.CLMS[0], convert(value))

        def __get_file_size(self):
            return parse(self.__tree.set(self.__node, TrimDirView.CLMS[1]))

        def __set_file_size(self, value):
            self.__tree.set(self.__node, TrimDirView.CLMS[1], convert(value))
    #========================================================================

    def __get_path(self):
        return self.__tree.set(self.__node, TrimDirView.CLMS[2])

    def __set_path(self, value):
        self.__tree.set(self.__node, TrimDirView.CLMS[2], value)

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
    level = int(math.log(number, 1 << 10))
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

# Execute main method if ran directly.

if __name__ == '__main__':
    TrimDirView.main()
