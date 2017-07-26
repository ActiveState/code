# Author: Miguel Martinez Lopez

try:
    from Tkinter import Frame, N, S, E, W
except ImportError:
    from tkinter import Frame, N, S, E, W

class Animation(object):
    def __init__(self, w, ticks, config_function, duration=1, interval_time=None, easing_function=None, start_value=0, end_value=1, callback=None):
        self._w = w

        self._tick = 0
        self._total_ticks = float(ticks)
        
        if easing_function is None:
            self._easing_function = lambda x: x

        self._duration = duration
        
        if interval_time:
            self._interval_time = int(interval_time * 1000)
        else:
            self._interval_time = int(duration * 1000 / self._total_ticks)
        
        self._start_value = start_value
        self._end_value = end_value
        self._interval_value = end_value - start_value
        
        self._config_function = config_function
        
        self._callback = callback

    def start_animation(self, after=0):        
        if after != 0:
            self.after(int(after*1000), self._animate)
        else:
            self._animate()
        
    def _animate(self):
        t =  self._tick / self._total_ticks

        value = self._start_value + self._interval_value * self._easing_function(t)
        self._config_function(value)
        
        self._tick += 1
        
        if self._tick <= self._total_ticks:
            self._w.after(self._interval_time, self._animate)
        else:
            if self._callback is not None:
                self._w.after(self._interval_time, self._callback)

class Stacked_Frame(Frame):
    def __init__(self, master, animate=False, animate_direction=W, **kw):
        Frame.__init__(self, master, **kw)
        self._list_of_widgets = []
        
        self._current_index = None
        self._current_widget = None
        
        self._animate = animate
        
        if animate:
            if animate_direction not in (E, W, N, S):
                raise ValueError("Invalid animate_direction value: %s"%animate_direction)

            self._animate_direction = animate_direction
        
        self._is_animating = False

    def add_widget(self, widget):
        self._list_of_widgets.append(widget)
        if self._current_index is None:
            self._current_index = 0
            self._show_widget(widget)

        index = len(self._list_of_widgets) - 1
        return index

    def remove_widget(self, widget):
        self._list_of_widgets.remove(widget)

    def insert_widget(self, index, widget):
        self._list_of_widgets.insert(index, widget)
        if self._current_index is None:
            self._current_index = 0

            self._show_widget(widget)
        
    def count(self):
        return len(self._list_of_widgets)

    def current_index(self):
        return self._current_index

    def index_of(self, widget):
        return self._list_of_widgets.index(widget)

    def set_current_index(self, index):
        if self._is_animating:
            return

        if index == self._current_index: return
        
        widget = self._list_of_widgets[index]
        self._current_index = index
        
        self._show_widget(widget)
        
    def set_current_widget(self, widget):
        if self._is_animating:
            return

        index = self._list_of_widgets.index(widget)
        self._current_index = index

        self._show_widget(widget)
        
    def widget(self, index):
        return self._list_of_widgets[index]
    
    def next(self):
        if self._current_index  == len(self._list_of_widgets) - 1:
            return
            
        if self._is_animating:
            return

        self._current_index += 1
        widget = self._list_of_widgets[self._current_index]
        
        self._show_widget(widget)

    def previous(self):
        if not self._current_index:
            return
        
        if self._is_animating:
            return

        self._current_index -= 1
        widget = self._list_of_widgets[self._current_index]
        
        self._show_widget(widget)
        
    def _show_widget(self, widget):
        if self._current_widget is None:
            self._current_widget = widget
            widget.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            if self._animate:
                old_widget = self._current_widget

                widget.place(relwidth=1, relheight=1)

                if self._animate_direction == W:
                    start_value = 0
                    end_value = self.winfo_width()

                    def config_function(position):
                        widget.place(x=position, y=0, anchor=N+E)
                        old_widget.place(x=position, y=0, anchor=N+W)

                elif self._animate_direction == E:
                    start_value = self.winfo_width()
                    end_value = 0
                    
                    def config_function(position):
                        widget.place(x=position, y=0, anchor=N+W)
                        old_widget.place(x=position, y=0, anchor=N+E)

                elif self._animate_direction == S:
                    start_value = 0
                    end_value = self.winfo_height()
                    
                    def config_function(position):
                        widget.place(x=0, y=position, anchor=S+W)
                        old_widget.place(x=0, y=position, anchor=N+W)

                elif self._animate_direction == N:
                    start_value = self.winfo_height()
                    end_value = 0

                    def config_function(position):
                        widget.place(x=0, y=position, anchor=N+W)
                        old_widget.place(x=0, y=position, anchor=S+W)

                animation = Animation(
                    self,
                    ticks=20,
                    interval_time=0.05,
                    start_value=start_value, 
                    end_value=end_value,
                    config_function=config_function, 
                    callback=lambda widget=widget: self._on_finnish_animation(widget))

                animation.start_animation()
                self._is_animating = True
            else:
                self._current_widget.place_forget()
                self._current_widget = widget
            
                widget.place(x=0, y=0, relwidth=1, relheight=1)

    def _on_finnish_animation(self, widget):
        self._current_widget.place_forget()
        self._current_widget = widget
        
        self._is_animating = False

if __name__ == "__main__":
    try:
        from Tkinter import Tk, Button, Label
    except ImportError:
        from tkinter import Tk, Button, Label
        
    root = Tk()
    stack = Stacked_Frame(root, width=300, height=400, animate=True, animate_direction=S)
    stack.pack(padx=5)
    
    frame1 = Frame(stack, background="red")
    Label(frame1, text="this is frame1").pack(expand=True)

    frame2 = Frame(stack, background="white")
    Label(frame2, text="this is frame2").pack(expand=True)
    
    frame3 = Frame(stack, background="yellow")
    Label(frame3, text="this is frame3").pack(expand=True)
    
    frame4 = Frame(stack, background="green")
    Label(frame4, text="this is frame4").pack(expand=True)

    stack.add_widget(frame1)
    stack.add_widget(frame2)
    stack.add_widget(frame3)
    stack.add_widget(frame4)
    
    row = Frame(root)
    row.pack(fill="x", pady=10, padx=5)
    Button(row, text="previous", command= lambda: stack.previous()).pack(side="left")
    Button(row, text="next", command= lambda: stack.next()).pack(side="left", padx=(8,0))

    root.mainloop()
