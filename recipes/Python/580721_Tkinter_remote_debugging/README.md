## Tkinter remote debugging  
Originally published: 2016-11-20 19:02:16  
Last updated: 2017-01-24 20:23:45  
Author: Miguel Martínez López  
  
This trick requires rpyc.

You can install rpyc typing:

>   pip install rpyc

Run the code below and in another interpreter write:


    import rpyc
    c = rpyc.classic.connect("localhost")
    c.execute("from Tkinter import Label; label=Label(app, text='a label')")
    c.execute("label.pack()")
    app = c.eval("app")
    app.responsive_button.invoke()