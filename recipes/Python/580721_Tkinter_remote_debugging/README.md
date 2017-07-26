## Tkinter remote debugging

Originally published: 2016-11-20 19:02:16
Last updated: 2017-01-24 20:23:45
Author: Miguel Martínez López

This trick requires rpyc.\n\nYou can install rpyc typing:\n\n>   pip install rpyc\n\nRun the code below and in another interpreter write:\n\n\n    import rpyc\n    c = rpyc.classic.connect("localhost")\n    c.execute("from Tkinter import Label; label=Label(app, text='a label')")\n    c.execute("label.pack()")\n    app = c.eval("app")\n    app.responsive_button.invoke()