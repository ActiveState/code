# Author: Miguel Martinez Lopez

import pytweening

try:
    from Tkinter import Toplevel, PhotoImage, Frame, Button, N, S, E, W, RIGHT, BOTH, X
except ImportError:
    from tkinter import Toplevel, PhotoImage, Frame, Button, N, S, E, W, RIGHT, BOTH, X
    
SUCCESS_BACKGROUND = "#60a917"
WARNING_BACKGROUND = "#fa6800"
ALERT_BACKGROUND = "#ce352c"
INFO_BACKGROUND = "#59cde2"
    
class Notification(Toplevel):
    def __init__(self, notification_manager, builder, index, x, y, h, v, padx, pady, background=None, on_hide=None):
        Toplevel.__init__(self)
        
        self._notification_manager = notification_manager

        self.index = index
        self.on_hide = on_hide

        # Removes the native window boarder.
        self.overrideredirect(True)

        # Disables resizing of the widget.
        self.resizable(False, False)

        # Places window above all other windows in the window stack.
        self.wm_attributes("-topmost", True)

        notification_frame = Frame(self)
        notification_frame.pack(expand=True, fill=BOTH, padx=padx, pady=pady)

        top_row = Frame(notification_frame)
        top_row.pack(fill=X)
        
        if not hasattr(notification_manager, "_close_icon"):
            notification_manager._close_icon = PhotoImage(data="R0lGODlhEAAQAPeQAIsAAI0AAI4AAI8AAJIAAJUAAJQCApkAAJoAAJ4AAJkJCaAAAKYAAKcAAKcCAKcDA6cGAKgAAKsAAKsCAKwAAK0AAK8AAK4CAK8DAqUJAKULAKwLALAAALEAALIAALMAALMDALQAALUAALYAALcEALoAALsAALsCALwAAL8AALkJAL4NAL8NAKoTAKwbAbEQALMVAL0QAL0RAKsREaodHbkQELMsALg2ALk3ALs+ALE2FbgpKbA1Nbc1Nb44N8AAAMIWAMsvAMUgDMcxAKVABb9NBbVJErFYEq1iMrtoMr5kP8BKAMFLAMxKANBBANFCANJFANFEB9JKAMFcANFZANZcANpfAMJUEMZVEc5hAM5pAMluBdRsANR8AM9YOrdERMpIQs1UVMR5WNt8X8VgYMdlZcxtYtx4YNF/btp9eraNf9qXXNCCZsyLeNSLd8SSecySf82kd9qqc9uBgdyBgd+EhN6JgtSIiNuJieGHhOGLg+GKhOKamty1ste4sNO+ueenp+inp+HHrebGrefKuOPTzejWzera1O7b1vLb2/bl4vTu7fbw7ffx7vnz8f///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAJAALAAAAAAQABAAAAjUACEJHEiwYEEABniQKfNFgQCDkATQwAMokEU+PQgUFDAjjR09e/LUmUNnh8aBCcCgUeRmzBkzie6EeQBAoAAMXuA8ciRGCaJHfXzUMCAQgYooWN48anTokR8dQk4sELggBhQrU9Q8evSHiJQgLCIIfMDCSZUjhbYuQkLFCRAMAiOQGGLE0CNBcZYmaRIDLqQFGF60eTRoSxc5jwjhACFWIAgMLtgUocJFy5orL0IQRHAiQgsbRZYswbEhBIiCCH6EiJAhAwQMKU5DjHCi9gnZEHMTDAgAOw==")

        close_button = Button(top_row, image=notification_manager._close_icon, highlightthickness=0, borderwidth=0, command=self.close)
        close_button.pack(side=RIGHT, anchor=E)

        self.interior = Frame(notification_frame)
        self.interior.pack(expand=True, fill=BOTH)

        if builder:
            builder(self.interior)
        
        if background is not None:
            top_row.config(background=background)
            notification_frame.config(background=background)
            self.config(background=background)
            self.interior.config(background=background)
            close_button.config(background=background)
            
        self.place(x,y, h, v)
    
    @property
    def x(self):
        return self._offset_x
    
    @property
    def y(self):
        return self._offset_y
    
    @property
    def h(self):
        return self._h
    
    @property
    def v(self):
        return self._v

    def place(self, x, y, h, v):
        ''' The windows overall position on the screen  '''
        self.wm_geometry("{h}{x}{v}{y}".format(x=x,y=y, h=h, v=v))
        
        self._offset_x = x
        self._offset_y = y
        self._h = h
        self._v = v
    
    def start_animation(self, easing_function, ticks, duration, start_time=0):
        self._tick = 0
        self._total_ticks = float(ticks)
        self._easing_function = easing_function
        self._duration = duration
        
        self._interval_time = int(duration * 1000 / self._total_ticks)
        
        if start_time != 0:
            self.after(int(start_time*1000), self._animate)
        else:
            self._animate()
        
    def _animate(self):
        t =  self._tick / self._total_ticks
        # This changes the alpha value (How transparent the window should be). 
        # It ranges from 0.0 (completely transparent) to 1.0 (completely opaque).
        self.attributes("-alpha", self._easing_function(1-t))
        
        self._tick += 1
        
        if self._tick <= self._total_ticks:
            self.after(self._interval_time, self._animate)
        else:
            self.after(self._interval_time, self.close)

    def close(self):
        self._notification_manager.delete(self)
        
class Notification_Manager(object):
    def __init__(self, offset_x=12, offset_y=8, corner=N+E, background=None, spacing=5, ticks=15, easing_function=pytweening.linear, duration=3, start_time=3, padx=5, pady=5):
        if corner == N+W:
            self._h = "+"
            self._v = "+"
        elif corner == N+E:
            self._h = "-"
            self._v = "+"            
        elif corner == S+W:
            self._h = "+"
            self._v = "-"            
        elif corner == S+E:
            self._h = "-"
            self._v = "-"        
        else:
            raise ValueError("Not a valid corner value: %s"%corner)
        
        self._list_of_notifications = []

        self._offset_x = offset_x
        self._offset_y = offset_y
        self._padx = padx
        self._pady = pady
        self._corner = corner
        self._background = background
        self._ticks = ticks
        self._duration = duration
        self._easing_function = easing_function
        self._spacing = spacing
        self._start_time = start_time
        
    @property
    def corner(self):
        return self._corner
    
    @property
    def background(self):
        return self._background
    
    @property    
    def duration(self):
        return self._duration
    
    @property
    def spacing(self):
        return self._spacing
        
    @property
    def ticks(self):
        return self._ticks
        
    def create_notification(self, builder, start_time=None, duration=None, easing_function=None,ticks=None, background=None, padx=None, pady=None, on_hide=None):
        if ticks is None:
            ticks = self._ticks

        if builder is None:
            builder = self._builder
            
            notification.on_hide = on_hide
        
        if duration is None:
            duration = self._duration
            
        if easing_function is None:
            easing_function = self._easing_function   
            
        if background is None:
            background = self._background
            
        if padx is None:
            padx = self._padx
            
        if pady is None:
            pady = self._pady
            
        if start_time is None:
            start_time = self._start_time

        if len(self._list_of_notifications) == 0:
            x = self._offset_x
            y = self._offset_y
            
            index = 0
        else:
            last_notification = self._list_of_notifications[-1]
            last_notification.update_idletasks()

            x = self._offset_x
            y = last_notification.y + last_notification.winfo_height() + self._spacing
            
            index = len(self._list_of_notifications)

        notification = Notification(self, builder, index, x, y, self._h, self._v, padx, pady, background, on_hide)
        self._list_of_notifications.append(notification)

        notification.start_animation(easing_function=easing_function, ticks=ticks, duration=duration, start_time=start_time)
        
    def simple_notification(self, text, foreground, background, font=None, width=None, anchor=None, justify=None, wraplength=None, start_time=None, duration=None, easing_function=None,ticks=None, padx=None, pady=None, on_hide=None):
        builder = self.create_builder(text, foreground, background, font=font, width=width, anchor=anchor, justify=justify, wraplength=wraplength)
        self.create_notification(builder, background= background, start_time=start_time, duration=duration, easing_function=easing_function, ticks=ticks, padx=padx, pady=pady, on_hide=on_hide)
        
    def success(self, text, font=None, width=None, anchor=None, justify=None, wraplength=None, start_time=None, duration=None, easing_function=None,ticks=None, padx=None, pady=None, on_hide=None):
        self.simple_notification(text, "white", SUCCESS_BACKGROUND, font=font, width=width, anchor=anchor, justify=justify, wraplength=wraplength, start_time=start_time, duration=duration, easing_function=easing_function, ticks=ticks, padx=padx, pady=pady, on_hide=on_hide)
    
    def warning(self, text, font=None, width=None, anchor=None, justify=None, wraplength=None, start_time=None, duration=None, easing_function=None,ticks=None, padx=None, pady=None, on_hide=None):
        self.simple_notification(text, "white", WARNING_BACKGROUND, font=font, width=width, anchor=anchor, justify=justify, wraplength=wraplength, start_time=start_time, duration=duration, easing_function=easing_function, ticks=ticks, padx=padx, pady=pady, on_hide=on_hide)

    def alert(self, text, font=None, width=None, anchor=None, justify=None, wraplength=None, start_time=None, duration=None, easing_function=None,ticks=None, padx=None, pady=None, on_hide=None):        
        self.simple_notification(text, "white", ALERT_BACKGROUND, font=font, width=width, anchor=anchor, justify=justify, wraplength=wraplength, start_time=start_time, duration=duration, easing_function=easing_function, ticks=ticks, padx=padx, pady=pady, on_hide=on_hide)

    def info(self, text, font=None, width=None, anchor=None, justify=None, wraplength=None, start_time=None, duration=None, easing_function=None,ticks=None, padx=None, pady=None, on_hide=None):        
        self.simple_notification(text, "white", INFO_BACKGROUND, font=font, width=width, anchor=anchor, justify=justify, wraplength=wraplength, start_time=start_time, duration=duration, easing_function=easing_function, ticks=ticks, padx=padx, pady=pady, on_hide=on_hide)

    def create_builder(self, text, foreground, background, font=None, width=None, anchor=None, justify=None, wraplength=None):
        kwargs = dict(text=text, fg=foreground, background=background)
        
        if font:
            kwargs["font"] = font
        
        if anchor:
            kwargs["anchor"] = anchor
        
        if justify:
            kwargs["justify"] = justify
            
        if width:
            kwargs["width"] = width
            
        if wraplength:
            kwargs["wraplength"] = wraplength

        def builder(interior):            
            Label(interior, **kwargs).pack()

        return builder

    def delete(self, notification):
        index = notification.index
        height = notification.winfo_height()

        self._list_of_notifications.pop(index)
        notification.destroy()
        
        x = self._offset_x
        for i in range(index, len(self._list_of_notifications)):
            _notification = self._list_of_notifications[i]

            y = _notification.y - height - self._spacing
            _notification.index = i
            _notification.place(x, y, h=self._h, v=self._v)

        if notification.on_hide:
            notification.on_hide()
        
if __name__ == "__main__":
    try:
        from Tkinter import Tk, Label
    except ImportError:
        from tkinter import Tk, Label
        
    root = Tk()
    notification_manager = Notification_Manager(background="white")
    
    def create_notification(start_time, text):
        def notify():
            def builder(interior):
                Label(interior, text=text, background="white").pack()

            notification_manager.create_notification(builder=builder)

        root.after(start_time, notify)
    
    create_notification(100, "this is a label")
    create_notification(2500, "this is another label")
    create_notification(5000, "this is the third label")

    notification_manager.success("my succes message")
    notification_manager.warning("warning!")

    root.mainloop()
