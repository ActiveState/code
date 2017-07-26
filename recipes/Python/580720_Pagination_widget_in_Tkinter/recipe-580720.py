# Author: Miguel Martinez Lopez
# Version: 0.8

try:
    import Tkinter as tk
    import ttk

    import tkFont
    from Tkconstants import *
except ImportError:
    import tkinter as tk
    import tkinter.ttk as ttk

    from tkinter import font as tkFont
    from tkinter.constants import *

# Python 2 and 3 compatibility
try:
    xrange
except NameError:
    xrange = range

# Page label states
NOT_SELECTED = 0
SELECTED = 1

NORMAL_STATE = 0
ACTIVE_STATE = 1


def config_style(label, style, is_selected, is_active):
    label.config(**style[is_selected, is_active])

class Page_Label(tk.Label, object):
    def __init__(self, master, page_number, style, on_click, is_selected, is_active, is_displayed=True):
        tk.Label.__init__(self, master, width=0, text=page_number)

        if is_selected:
            current_style = style[SELECTED, NORMAL_STATE]
        else:
            current_style = style[NOT_SELECTED, NORMAL_STATE]
        
        self.config(**current_style)
        
        self._style = style
        self.bind("<1>", lambda event: on_click(self))
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        self._page_number = page_number
        
        self.is_selected = is_selected
        self.is_active = is_active
        
        self.is_displayed = is_displayed
        
    @property
    def page_number(self):
        return self._page_number

    @page_number.setter
    def page_number(self, number):
        self._page_number = number
        self.config(text=str(number))

    def _on_enter(self, event):
        if self.is_selected:
            self.change_state(SELECTED, ACTIVE_STATE)
        else:
            self.change_state(NOT_SELECTED, ACTIVE_STATE)

    def _on_leave(self, event):
        if self.is_selected:
            self.change_state(SELECTED, NORMAL_STATE)
        else:
            self.change_state(NOT_SELECTED, NORMAL_STATE)

    def change_state(self, is_selected, is_active):
        self.is_selected = is_selected
        self.is_active = is_active

        config_style(self, self._style, is_selected, is_active)

class Page_Control(tk.Frame):
        
    def _navigation_control(self, pagination, style, control_name, text):
        onclick_control = getattr(pagination, "%s_page"%control_name)
        
        label = tk.Label(self, text=text, width=0)
        
        config_style(label, style, NOT_SELECTED, NORMAL_STATE)

        label.bind("<1>", lambda event: onclick_control())
        
        label.bind("<Enter>", lambda event, label=label: config_style(label, style, NOT_SELECTED, ACTIVE_STATE))
        label.bind("<Leave>", lambda event, label=label: config_style(label, style, NOT_SELECTED, NORMAL_STATE))

        return label

    
class Left_Control(Page_Control):
    def __init__(self, pagination, style, first_button, prev_button, spacing):
        Page_Control.__init__(self, pagination)

        if first_button is None:
            if prev_button is not None:
                self._previous_label = self._navigation_control(pagination, style, "prev", prev_button)
                self._previous_label.pack(side=LEFT)
        else:
            self._first_label = self._navigation_control(pagination, style, "first", first_button)
            self._first_label.pack(side=LEFT)

            if prev_button is not None:
                self._previous_label = self._navigation_control(pagination, style, "prev", prev_button)
                self._previous_label.pack(side=LEFT, padx=(spacing,0))


class Right_Control(Page_Control):
    def __init__(self, pagination, style, last_button, next_button, spacing):
        Page_Control.__init__(self, pagination)
        if last_button is None:
            if prev_button is not None:               
                self._next_label = self._navigation_control(pagination, style, "next", next_button)               
                self._next_label.pack(side=RIGHT)
        else:
            self._last_label = self._navigation_control(pagination, style, "last", last_button)
            self._last_label.pack(side=RIGHT)

            if next_button is not None:
                self._next_label = self._navigation_control(pagination, style, "next", next_button)
                self._next_label.pack(side=RIGHT, padx=(0, spacing))

class Pagination(tk.Frame):

    def __init__(self, master, displayed_pages, total_pages, background=None, current_page=None, start_page=1, prev_button= "Prev", next_button="Next", first_button="First", last_button="Last", hide_controls_at_edge=False, command =None, pagination_style=None):
        if pagination_style is None:
            raise Exception("No pagination style defined")
        
        self._start_page = start_page
        self._end_page = min(total_pages, start_page + displayed_pages - 1)

        if current_page is None:
            current_page = start_page
        else:
            if not self._start_page <= current_page <= self._end_page:
                raise ValueError("Not valid selected page")

        tk.Frame.__init__(self, master, background=background)

        self._command = command
        
        self._hide_controls_at_edge = hide_controls_at_edge

        self._list_of_page_labels = []

        self._total_pages = total_pages        
        self._displayed_pages = displayed_pages

        self._left_controls = None
        self._right_controls = None

        self._current_page = current_page
        
        self._label_spacing = pagination_style.get("button_spacing", 0)

        self._style_config = style_config = {}

        for selected_state in (NOT_SELECTED, SELECTED):
            for active_state in (NORMAL_STATE, ACTIVE_STATE):
                style_config[selected_state, active_state] = self._create_configuration_of_state(pagination_style, selected_state, active_state)

        self._render_pagination(current_page, prev_button, next_button, first_button, last_button, displayed_pages, self._start_page, self._end_page, self._label_spacing, hide_controls_at_edge)

    def _render_pagination(self, current_page, prev_button, next_button, first_button, last_button, displayed_pages, start_page, end_page, spacing, hide_controls_at_edge):
        if prev_button is not None or first_button is not None:
            self._left_controls = Left_Control(self, self._style_config, first_button, prev_button, spacing)

            if hide_controls_at_edge and start_page == 1:
                self._left_controls.is_displayed = False
            else:
                self._left_controls.pack(side=LEFT, padx=(0, self._label_spacing))        
                self._left_controls.is_displayed = True

        self._page_frame = tk.Frame(self)
        self._page_frame.pack(side=LEFT)

        for page_number in range(start_page, start_page + displayed_pages):
            is_selected = page_number == self._current_page

            if page_number <= end_page:
                page_label = Page_Label(self._page_frame, page_number, self._style_config, self._on_click_page, is_selected, False, is_displayed=True)

                if page_number == start_page:
                    page_label.pack(side=LEFT)
                else:
                    page_label.pack(side=LEFT, padx=(self._label_spacing, 0))
            else:
                page_label = Page_Label(self._page_frame, page_number, self._style_config, self._on_click_page, is_selected, False, is_displayed=False)
    
            self._list_of_page_labels.append(page_label)
        if next_button is not None or last_button is not None:
            self._right_controls = Right_Control(self, self._style_config, last_button, next_button, spacing)

            if hide_controls_at_edge and end_page == total_pages:
                self._right_controls.is_displayed = False
            else:
                self._right_controls.pack(side=LEFT, padx=(self._label_spacing, 0))
                self._right_controls.is_displayed = True

    def _update_labels(self):

        if self._hide_controls_at_edge:
            if self._left_controls is not None:
                if self._start_page == 1:
                    if self._left_controls.is_displayed:
                        self._left_controls.is_displayed = False
                        self._left_controls.pack_forget()
                else:
                    if not self._left_controls.is_displayed:
                        self._left_controls.is_displayed = True
                        self._left_controls.pack(side=LEFT, padx=(0, self._label_spacing), before=self._page_frame)

            if self._right_controls is not None:
                if self._end_page == self._total_pages:
                    if self._right_controls.is_displayed:
                        self._right_controls.is_displayed = False
                        self._right_controls.pack_forget()
                else:                
                    if not self._right_controls.is_displayed:
                        self._right_controls.is_displayed = True
                        self._right_controls.pack(side=LEFT, padx=(self._label_spacing, 0), after=self._page_frame)

        for i, page_number in enumerate(range(self._start_page, self._end_page+1)):
            page_label = self._list_of_page_labels[i]
            page_label.page_number = page_number
            
            if self._current_page == page_number:
                if not page_label.is_selected:
                    page_label.change_state(SELECTED, NORMAL_STATE)
            else:
                if page_label.is_selected:
                    page_label.change_state(NOT_SELECTED, NORMAL_STATE)

            if not page_label.is_displayed:
                page_label.is_displayed = True
                if i == 0:
                    page_label.pack(side=LEFT)
                else:
                    page_label.pack_configure(side=LEFT, padx=(self._label_spacing, 0))
                    

        for i in range(self._end_page-self._start_page+1, self._displayed_pages):
            page_label = self._list_of_page_labels[i]
            
            if page_label.is_displayed:
                page_label.pack_forget()
                page_label.is_displayed = False

    def _create_configuration_of_state(self, pagination_style, selected_state, active_state):
        config = {}

        if "font" in pagination_style:
            config["font"] = pagination_style["font"]

        if "font_family" in pagination_style:
            font_family = pagination_style["font_family"]
        else:
            font_family = None

        if "font_size" in pagination_style:
            font_size = pagination_style["font_size"]
        else:
            font_size = None

        if "font_weight" in pagination_style:
            font_weight = pagination_style["font_weight"]
        else:
            font_weight = None

        if "button_padx" in pagination_style:
            config["padx"] = pagination_style["button_padx"]

        if "button_pady" in pagination_style:
            config["pady"] = pagination_style["button_pady"]

        if selected_state == SELECTED:
            state_style = pagination_style["selected_button"]
        else:
            state_style = pagination_style["normal_button"]
        
        if active_state == ACTIVE_STATE:
            if "activebackground" in state_style:
                config["background"] = state_style["activebackground"]
            if "activeforeground" in state_style:
                config["foreground"] = state_style["activeforeground"]
        else:
            if "background" in state_style:
                config["background"] = state_style["background"]
            if "foreground" in state_style:
                config["foreground"] = state_style["foreground"]

        if "padx" in state_style:
            config["padx"] = state_style["padx"]

        if "pady" in state_style:
            config["pady"] = state_style["pady"]

        if "font" in state_style:
            config["font"] = state_style["font"]
        else:
            font_family = state_style.get("font_family", font_family)
            font_size = state_style.get("font_size", font_size)
            font_weight = state_style.get("font_weight", font_weight)
            
            kw = {}
            if font_family is not None:
                kw["family"] = font_family

            if font_size is not None:
                kw["size"] = font_size
                
            if font_weight is not None:
                kw["weight"] = font_weight
            
            config["font"] = tkFont.Font(**kw)

        return config

    def select_page(self, page_number, start_page=None):
        self._current_page = page_number
        if start_page is None:
            if page_number < self._start_page:
                self._start_page = page_number
                self._end_page = self._start_page + self._displayed_pages - 1
        else:
            end_page = start_page + self._displayed_pages - 1

            if not start_page <= page_number <= end_page:
                raise ValueError("Page number not visible")
                
            self._start_page = start_page
            self._end_page = end_page
            
        self._update_labels()

    def prev_page(self):
        if self._current_page == 1: return

        if self._current_page == self._start_page:
            self._start_page -= 1
            self._end_page -= 1

        self._current_page -= 1
        
        if self._command is not None:
            self._command(self._current_page)

        self._update_labels()

    def next_page(self):
        if self._current_page == self._total_pages: return

        if self._current_page == self._end_page:
            self._start_page += 1
            self._end_page += 1

        self._current_page += 1
        
        if self._command is not None:
            self._command(self._current_page)

        self._update_labels()
        
    def first_page(self):
        if self._current_page == 1: return

        self._start_page = 1
        self._end_page = min(self._total_pages, self._displayed_pages)
        
        self._current_page = 1
        
        if self._command is not None:
            self._command(self._current_page)
        
        self._update_labels()

    def last_page(self):
        if self._current_page == self._total_pages: return

        self._end_page = self._total_pages
        self._start_page = max(self._end_page- self._displayed_pages + 1, 1)

        self._current_page = self._total_pages
        
        if self._command is not None:
            self._command(self._current_page)

        self._update_labels()

    @property
    def current_page(self):
        return self._current_page
    
    page = current_page

    @property
    def total_pages(self):
        return self._total_pages
        
    @total_pages.setter
    def total_pages(self, num):
        self._total_pages = num

        _end_page = self._end_page
        self._start_page = max(min(self._total_pages - self._displayed_pages+1, self._start_page), 1)
        self._end_page = min(self._start_page + self._displayed_pages -1 , self._total_pages)

        if _end_page == self._end_page:
            return
        elif _end_page < self._end_page:
            for page_number in range(_end_page+1, self._end_page +1):
                i = page_number - self._start_page
                page_label = self._list_of_page_labels[i]
                page_label.page_number = page_number

                if i == 0:
                    page_label.pack(side=LEFT)
                else:
                    page_label.pack_configure(side=LEFT, padx=(self._label_spacing, 0))
                    
                page_label.is_displayed = True
        else:
            for i in range(self._end_page - _end_page):
                page_label = self._list_of_page_labels[i]

                page_label.pack_forget()
                page_label.is_displayed = False

    def _on_click_page(self, new_page):
        if new_page.page_number == self._current_page:
            return

        old_page = self._list_of_page_labels[self._current_page - self._start_page]
        old_page.change_state(NOT_SELECTED, NORMAL_STATE)

        new_page.change_state(SELECTED, ACTIVE_STATE)
        
        self._current_page = new_page.page_number

        if self._command is not None:
            self._command(self._current_page)

    def update(self, total_pages, current_page, start_page=1):
        end_page = min(total_pages, start_page + self._displayed_pages - 1)

        if not start_page <= current_page <= end_page:
                raise ValueError("Not valid selected page")

        self._start_page = start_page
        self._end_page = end_page
        
        self._total_pages = total_pages
        self._current_page = current_page

        self._update_labels()
    
pagination_style1 = {
    "button_spacing": 3,
    "button_padx":12,
    "button_pady": 6,
    "normal_button": {
        "font": ("Verdana", 10),
        "foreground": "#337ab7", 
        "activeforeground":"#23527c",
        "background": "white",
        "activebackground": "#eee"
    }, 
    "selected_button": {
        "font":("Verdana", 10, "bold"),
        "foreground":"#fff",
        "activeforeground":"#fff", 
        "background":"#337ab7", 
        "activebackground":"#337ab7"
    }
}

pagination_style2 = {
    "button_spacing": 3,
    "button_padx":12,
    "button_pady":6,
    "normal_button": {
        "font": ("Verdana", 10),
        "foreground": "black", 
        "activeforeground":"black",
        "background": "white", 
        "activebackground": "#ccc"
    }, 
    "selected_button": {
        "font":("Verdana", 10, "bold"),
        "foreground":"white",
        "activeforeground":"#fff", 
        "background":"#f44336", 
        "activebackground":"#f44336"
    }
}

pagination_style3 = {
    "button_spacing": 3,
    "button_padx":12,
    "button_pady":6,
    "normal_button": {
        "font": ("Verdana", 10),
        "foreground": "#717171", 
        "activeforeground":"#717171",
        "background": "#e9e9e9", 
        "activebackground": "#fefefe"
    }, 
    "selected_button": {
        "font":("Verdana", 10, "bold"),
        "foreground":"#f0f0f0",
        "activeforeground":"#f0f0f0", 
        "background":"#616161", 
        "activebackground":"#616161"
    }
}

pagination_style4 = {
    "button_spacing": 3,
    "button_padx":12,
    "button_pady":6,
    "normal_button": {
        "font": ("Verdana", 10),
        "foreground": "#feffff", 
        "activeforeground":"#feffff",
        "background": "#3e4347", 
        "activebackground": "#3d4f5d"
    }, 
    "selected_button": {
        "font":("Verdana", 10, "bold"),
        "foreground":"#feffff",
        "activeforeground":"#feffff", 
        "background":"#2f3237", 
        "activebackground":"#2f3237"
    }
}

pagination_style5 = {
    "button_spacing": 3,
    "button_padx":12,
    "button_pady":6,
    "normal_button": {
        "font": ("Verdana", 10),
        "foreground": "#2E4057", 
        "activeforeground":"#2E4057",
        "background": "white", 
        "activebackground": "white"
    }, 
    "selected_button": {
        "font":("Verdana", 10, "bold"),
        "foreground":"white",
        "activeforeground":"white", 
        "background":"#64a281", 
        "activebackground":"#64a281"
    }
}

if __name__ == "__main__":
    
    try:
        from Tkinter import Tk
        from tkMessageBox import showinfo
    except ImportError:
        from tkinter import Tk
        from tkinter.messagebox import showinfo
        
    root = Tk()

    page = tk.Frame()
    page.pack()

    def print_page(page_number):
        print("page number %s"%page_number)

    row = tk.Frame(page)
    row.pack(padx=10, pady=4, fill=X)

    tk.Label(row, text="Pagination").pack(anchor=W)
    
    pagination = Pagination(row, 5, 100, command=print_page, pagination_style=pagination_style1)
    pagination.pack(pady=10, anchor=W)

    pagination = Pagination(row, 5, 100, command=print_page, pagination_style=pagination_style2)
    pagination.pack(pady=10, anchor=W)

    pagination = Pagination(row, 5, 50, command=print_page,  pagination_style=pagination_style3)
    pagination.pack(pady=10, anchor=W)

    pagination = Pagination(row, 5, 100, command=print_page, pagination_style=pagination_style4)
    pagination.pack(pady=10, anchor=W)

    pagination = Pagination(row, 5, 100, command=print_page, pagination_style=pagination_style5)
    pagination.pack(pady=10, anchor=W)
    
    
    root.mainloop()
