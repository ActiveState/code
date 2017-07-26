## Testing Tkinter or Selenium for Tkinter  
Originally published: 2017-01-24 13:06:11  
Last updated: 2017-01-24 20:34:52  
Author: Miguel Martínez López  
  
This code is a little variation of my other trick:

https://code.activestate.com/recipes/580721-tkinter-remote-debugging

It makes more easy to create tests for Tkinter.

Install rpyc:
>    pip install rpyc

Save the code below to a file named for example tkinter_selenium.py.

This is the usage:
>    python tkinter_selenium.py [-h] [-p PORT] filename

where filename is the path to main file of Tkinter application, and port is an optional port number for the remote interpreter. Otherwise it uses default port.


Then in another python interpreter you can interact with the application. For example, write:

    import rpyc
    c = rpyc.classic.connect("localhost")
    c.execute("""
    from Tkinter import Button, Toplevel
    import tkMessageBox 

    responsive_button = Button(Toplevel(), text="It's responsive", command = lambda:tkMessageBox.showinfo("alert window", "It's responsive!"))

    responsive_button.pack()
    """)

    responsive_button = c.eval("responsive_button")
    responsive_button.invoke()

(This example only works for Python 2. For python 3 use "tkinter" instead of "Tkinter" and so on)

Use port keyword argument to *"repyc.classic.connect"* if you want a different port number than default port. For example:

    import rpyc
    c = rpyc.classic.connect("localhost", port=8000)

For the selection of tkinter widgets, I have this other trick:

https://code.activestate.com/recipes/580738-tkinter-selectors

Using this remote debugging utility and selectors makes easy to test tkinter applications similar to selenium.

This utility could be used not only for Tkinter applications. It could be used also for wxpython, pygtk and pyqt applications.

NOTE: Interact with remote application using python of same version. If the application is running using a Python 2 interpreter, use a python 2 interpreter for remote interaction. Similarly use a python 3 interpreter for remote interaction with a python 3 application.