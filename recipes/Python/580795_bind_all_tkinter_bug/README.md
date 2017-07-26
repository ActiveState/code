## bind all tkinter "bug"  
Originally published: 2017-05-02 22:40:54  
Last updated: 2017-05-05 20:33:31  
Author: Miguel Martínez López  
  
This recipes tries to solve the problem of bind_all and unbind_all for tkinter.

When a callback is registered using bind_all method and later it's unregistered using unbind_all, all the callbacks are deleted for the "all" tag event. This makes difficult to register and unregister only one callback at a time. This recipes tries to solve this problem.

Observe the difference between the code below and the recipe. With the code below, when the user clicks nothing happens. But with my recipe it's possible to bind and unbind specific callbacks.

    try:
        from Tkinter import Tk, Frame
    except ImportError:
        from tkinter import Tk, Frame
        
    root = Tk()
    f = Frame(root, width= 300, height=300)
    f.pack()

    def callback1(event):
        print("callback1")
        
    def callback2(event):
        print("callback2")

    def callback3(event):
        print("callback3")
        
    root.bind_all("<1>", callback1, add="+")
    f.bind_all("<1>", callback2, add="+")
    f.bind_all("<1>", callback3, add="+")

    f.unbind_all("<1>")

    root.mainloop()
