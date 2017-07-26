# author: Miguel Martinez Lopez

try:
    from Tkinter import Tk, Frame, BitmapImage, Label
    from Tkconstants import *
except ImportError:
    from tkinter import Tk, Frame, BitmapImage, Label
    from tkinter.constants import *

import base64

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


class Chord(Frame):
    RIGHT_ARROW_ICON = 'I2RlZmluZSBpbWFnZV93aWR0aCAxNwojZGVmaW5lIGltYWdlX2hlaWdodCAxNwpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLAoweDYwLDB4MDAsMHgwMCwweGUwLDB4MDAsMHgwMCwweGUwLDB4MDMsMHgwMCwweGUwLDB4MGYsMHgwMCwweGUwLDB4MDMsMHgwMCwKMHhlMCwweDAxLDB4MDAsMHg2MCwweDAwLDB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLDB4MDAsCjB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwCn07'
    DOWN_ARROW_ICON = 'I2RlZmluZSBpbWFnZV93aWR0aCAxNwojZGVmaW5lIGltYWdlX2hlaWdodCAxNwpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLAoweDAwLDB4MDAsMHgwMCwweGUwLDB4MGYsMHgwMCwweGUwLDB4MGYsMHgwMCwweGMwLDB4MDcsMHgwMCwweGMwLDB4MDMsMHgwMCwKMHg4MCwweDAzLDB4MDAsMHgwMCwweDAxLDB4MDAsMHgwMCwweDAxLDB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLDB4MDAsCjB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwCn07'

    def __init__(self, master, title, width, body_background="white", background="#f0f0f0", foreground="#333333", selected_background="#1ba1e2", selected_foreground="white", active_foreground="#0067cb", cursor="hand1"):
        Frame.__init__(self, master, background="white")
        self._title = title

        self._background = background
        self._foreground = foreground
        self._active_foreground = active_foreground
        self._selected_foreground = selected_foreground
        self._selected_background = selected_background

        self._cursor = cursor
        
        self._right_arrow_icon = BitmapImage(data=base64.b64decode(Chord.RIGHT_ARROW_ICON))
        self._down_arrow_icon = BitmapImage(data=base64.b64decode(Chord.DOWN_ARROW_ICON))
        
        self._caption = Frame(self, width =width, background=background, padx=2)
        self._caption.pack(fill=X, pady=(0,2))
        self._caption.pack_propagate(False)

        self._icon_label = Label(self._caption, image=self._right_arrow_icon, background=background)
        self._icon_label.pack(side=LEFT)

        self._title_label = Label(self._caption, text=title, bg = background, fg=foreground)
        self._title_label.pack(side=LEFT, padx=4, fill=X)

        self._caption.configure(height= self._title_label.winfo_reqheight())

        self.body = Frame(self, background=body_background)
        self._body_height = None

        self._is_opened = False
        self._is_animating = False

        self._caption.bind('<Button-1>', self._on_click)
        self._title_label.bind('<Button-1>', self._on_click)
        self._icon_label.bind('<Button-1>', self._on_click)

        self._caption.bind('<Enter>', self._on_enter)
        self._caption.bind('<Leave>', self._on_leave)
    
    @property
    def title(self):
        return self._title
        
    @title.setter
    def title(self, text):
        self._title = text
        self._title_label.configure(text=text)

    def _on_enter(self, event):
        if not self._is_opened:
            self._down_arrow_icon.configure(foreground=self._active_foreground)
            self._right_arrow_icon.configure(foreground=self._active_foreground)

        self.config(cursor=self._cursor)

    def _on_leave(self, event):
        if not self._is_opened:
            self._down_arrow_icon.configure(foreground=self._foreground)
            self._right_arrow_icon.configure(foreground=self._foreground)
        
        self.config(cursor="arrow")

    def _on_click(self, event):
        if self._is_animating: return

        self.toggle()

    def open(self):
        if self._is_animating: return

        if not self._is_opened: self._open()

    def _open(self):        
        self.body.pack()
        self.body.pack_propagate(False)
        
        self._icon_label.configure(image=self._down_arrow_icon, background = self._selected_background)
        self._title_label.configure(foreground= self._selected_foreground, background = self._selected_background)
        self._caption.configure(background = self._selected_background)
        
        self._down_arrow_icon.configure(foreground=self._selected_foreground)

        if self._body_height is None:
            self._body_height= self.body.winfo_reqheight()

        end_value = self._body_height

        self.body.configure(width=self.winfo_width())
        self._is_opened = True
        self._is_animating = True

        animation = Animation(
            self,
            ticks=16,
            interval_time=0.01,
            start_value=0, 
            end_value=end_value,
            config_function=lambda height: self.body.configure(height=int(height)), 
            callback=self._on_finnish_animation)

        animation.start_animation()
        
    def _on_finnish_animation(self):
        self._is_animating = False
        
        if not self._is_opened:
            self.body.pack_forget()

    def close(self):
        if self._is_animating:
            return

        if self._is_opened: self._close()
    
    def _close(self):
        self._icon_label.configure(image=self._right_arrow_icon, background = self._background)
        self._title_label.configure(foreground= self._foreground, background = self._background)
        self._caption.configure(background = self._background)
        
        self._right_arrow_icon.configure(foreground=self._foreground)

        start_value = self.body.winfo_height()

        self._is_opened = False
        self._is_animating = True

        animation = Animation(
            self,
            ticks=16,
            interval_time=0.01,
            start_value=start_value, 
            end_value=0,
            config_function=lambda height: self.body.configure(height=int(height)), 
            callback=self._on_finnish_animation)

        animation.start_animation()
        
    def toggle(self):
        if self._is_opened:
            self._close()
        else:
            self._open()

class Accordion(Frame):

    def __init__(self, parent, width, **kwargs):
        Frame.__init__(self, **kwargs)

        self._width = width
        self._list_of_chords = []

    def create_chord(self, title, background="white"):
        chord = Chord(self, title=title, body_background=background, width=self._width)
        self._list_of_chords.append(chord)

        if len(self._list_of_chords) == 1:
            chord.pack(fill=X)
        else:
            chord.pack(fill=X, pady=(1,0))

        return chord
            
if __name__ == '__main__':
    try:
        from Tkinter import Entry, Button, Text
    except ImportError:
        from tkinter import Entry, Button, Text

    root = Tk()
    root.geometry("400x300")

    root.configure(background="white")
    

    # create the Accordion
    accordion = Accordion(root, width=200)
    accordion.pack(pady=10)

    first_chord = accordion.create_chord('First Chord')
    Label(first_chord.body, text='hello world', bg='white').pack()

    # second chord
    second_chord = accordion.create_chord('Second Chord')
    Entry(second_chord.body).pack()
    Button(second_chord.body, text='Button').pack()

    # third chord
    third_chord = accordion.create_chord(title='Third Chord')
    Text(third_chord.body).pack()

    root.mainloop()
