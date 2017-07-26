#! /usr/bin/env python
import tkinter.ttk
import tkinter.messagebox
import tkinter.font
import idlelib.textView

import datetime
import getpass
import os
import string
import random
import colorsys
import urllib.parse
import webbrowser
import pickle
import traceback
import sys
import contextlib
import io

################################################################################

class Color:

    HTML = dict(reversed(color.split(' ')) for color in '''\
#F0F8FF AliceBlue
#FAEBD7 AntiqueWhite
#00FFFF Aqua
#7FFFD4 Aquamarine
#F0FFFF Azure
#F5F5DC Beige
#FFE4C4 Bisque
#000000 Black
#FFEBCD BlanchedAlmond
#0000FF Blue
#8A2BE2 BlueViolet
#A52A2A Brown
#DEB887 BurlyWood
#5F9EA0 CadetBlue
#7FFF00 Chartreuse
#D2691E Chocolate
#FF7F50 Coral
#6495ED CornflowerBlue
#FFF8DC Cornsilk
#DC143C Crimson
#00FFFF Cyan
#00008B DarkBlue
#008B8B DarkCyan
#B8860B DarkGoldenRod
#A9A9A9 DarkGray
#A9A9A9 DarkGrey
#006400 DarkGreen
#BDB76B DarkKhaki
#8B008B DarkMagenta
#556B2F DarkOliveGreen
#FF8C00 Darkorange
#9932CC DarkOrchid
#8B0000 DarkRed
#E9967A DarkSalmon
#8FBC8F DarkSeaGreen
#483D8B DarkSlateBlue
#2F4F4F DarkSlateGray
#2F4F4F DarkSlateGrey
#00CED1 DarkTurquoise
#9400D3 DarkViolet
#FF1493 DeepPink
#00BFFF DeepSkyBlue
#696969 DimGray
#696969 DimGrey
#1E90FF DodgerBlue
#B22222 FireBrick
#FFFAF0 FloralWhite
#228B22 ForestGreen
#FF00FF Fuchsia
#DCDCDC Gainsboro
#F8F8FF GhostWhite
#FFD700 Gold
#DAA520 GoldenRod
#808080 Gray
#808080 Grey
#008000 Green
#ADFF2F GreenYellow
#F0FFF0 HoneyDew
#FF69B4 HotPink
#CD5C5C IndianRed
#4B0082 Indigo
#FFFFF0 Ivory
#F0E68C Khaki
#E6E6FA Lavender
#FFF0F5 LavenderBlush
#7CFC00 LawnGreen
#FFFACD LemonChiffon
#ADD8E6 LightBlue
#F08080 LightCoral
#E0FFFF LightCyan
#FAFAD2 LightGoldenRodYellow
#D3D3D3 LightGray
#D3D3D3 LightGrey
#90EE90 LightGreen
#FFB6C1 LightPink
#FFA07A LightSalmon
#20B2AA LightSeaGreen
#87CEFA LightSkyBlue
#778899 LightSlateGray
#778899 LightSlateGrey
#B0C4DE LightSteelBlue
#FFFFE0 LightYellow
#00FF00 Lime
#32CD32 LimeGreen
#FAF0E6 Linen
#FF00FF Magenta
#800000 Maroon
#66CDAA MediumAquaMarine
#0000CD MediumBlue
#BA55D3 MediumOrchid
#9370D8 MediumPurple
#3CB371 MediumSeaGreen
#7B68EE MediumSlateBlue
#00FA9A MediumSpringGreen
#48D1CC MediumTurquoise
#C71585 MediumVioletRed
#191970 MidnightBlue
#F5FFFA MintCream
#FFE4E1 MistyRose
#FFE4B5 Moccasin
#FFDEAD NavajoWhite
#000080 Navy
#FDF5E6 OldLace
#808000 Olive
#6B8E23 OliveDrab
#FFA500 Orange
#FF4500 OrangeRed
#DA70D6 Orchid
#EEE8AA PaleGoldenRod
#98FB98 PaleGreen
#AFEEEE PaleTurquoise
#D87093 PaleVioletRed
#FFEFD5 PapayaWhip
#FFDAB9 PeachPuff
#CD853F Peru
#FFC0CB Pink
#DDA0DD Plum
#B0E0E6 PowderBlue
#800080 Purple
#FF0000 Red
#BC8F8F RosyBrown
#4169E1 RoyalBlue
#8B4513 SaddleBrown
#FA8072 Salmon
#F4A460 SandyBrown
#2E8B57 SeaGreen
#FFF5EE SeaShell
#A0522D Sienna
#C0C0C0 Silver
#87CEEB SkyBlue
#6A5ACD SlateBlue
#708090 SlateGray
#708090 SlateGrey
#FFFAFA Snow
#00FF7F SpringGreen
#4682B4 SteelBlue
#D2B48C Tan
#008080 Teal
#D8BFD8 Thistle
#FF6347 Tomato
#40E0D0 Turquoise
#EE82EE Violet
#F5DEB3 Wheat
#FFFFFF White
#F5F5F5 WhiteSmoke
#FFFF00 Yellow
#9ACD32 YellowGreen'''.split('\n'))

    @property
    def best_name(self):
        diffs = []
        for name in self.HTML.keys():
            diffs.append((name, self.diff(getattr(self, name))))
        error = min(diffs, key=lambda pair: pair[1])[1]
        return tuple(pair[0] for pair in diffs if pair[1] == error)

    ########################################################################

    @classmethod
    def hsv(cls, hue, saturation, value):
        assert 0 <= hue <= 1 and 0 <= saturation <= 1 and 0 <= value <= 1
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        return cls(round(r * 0xFF), round(g * 0xFF), round(b * 0xFF))

    @classmethod
    def parse(cls, string):
        assert len(string) == 7 and string[0] == '#'
        return cls(int(string[1:3], 16),
                   int(string[3:5], 16),
                   int(string[5:7], 16))

    ########################################################################

    def __init__(self, red, green, blue):
        self.__rgb = bytes((red, green, blue))

    def __str__(self):
        return '#{:02X}{:02X}{:02X}'.format(*self.__rgb)

    def __repr__(self):
        return '{}({}, {}, {})'.format(self.__class__.__name__, *self.__rgb)

    def __hash__(self):
        return hash(self.__rgb)

    def __eq__(self, other):
        return self.__rgb == other.__rgb

    ########################################################################

    @property
    def red(self):
        return self.__rgb[0]

    @property
    def green(self):
        return self.__rgb[1]

    @property
    def blue(self):
        return self.__rgb[2]

    r, g, b = red, green, blue

    def set_red(self, value):
        return self.__class__(value, self.g, self.b)

    def set_green(self, value):
        return self.__class__(self.r, value, self.b)

    def set_blue(self, value):
        return self.__class__(self.r, self.g, value)

    def add_red(self, value):
        return self.__class__(self.r + value & 0xFF, self.g, self.b)

    def add_green(self, value):
        return self.__class__(self.r, self.g + value & 0xFF, self.b)

    def add_blue(self, value):
        return self.__class__(self.r, self.g, self.b + value & 0xFF)

    ########################################################################

    @property
    def hue(self):
        return colorsys.rgb_to_hsv(self.__rgb[0] / 0xFF,
                                   self.__rgb[1] / 0xFF,
                                   self.__rgb[2] / 0xFF)[0]

    @property
    def saturation(self):
        return colorsys.rgb_to_hsv(self.__rgb[0] / 0xFF,
                                   self.__rgb[1] / 0xFF,
                                   self.__rgb[2] / 0xFF)[1]

    @property
    def value(self):
        return colorsys.rgb_to_hsv(self.__rgb[0] / 0xFF,
                                   self.__rgb[1] / 0xFF,
                                   self.__rgb[2] / 0xFF)[2]

    h, s, v = hue, saturation, value

    def set_hue(self, value):
        return self.hsv(value, self.s, self.v)

    def set_saturation(self, value):
        return self.hsv(self.h, value, self.v)

    def set_value(self, value):
        return self.hsv(self.h, self.s, value)

    def add_hue(self, value):
        return self.hsv(self.__mod(self.h + value), self.s, self.v)

    def add_saturation(self, value):
        return self.hsv(self.h, self.__mod(self.s + value), self.v)

    def add_value(self, value):
        return self.hsv(self.h, self.s, self.__mod(self.v + value))

    ########################################################################

    def invert(self):
        return self.__class__(0xFF - self.r, 0xFF - self.g, 0xFF - self.b)

    def rotate(self, value):
        return self.__class__(self.r + value & 0xFF,
                              self.g + value & 0xFF,
                              self.b + value & 0xFF)

    def diff(self, other):
        r = (self.r - other.r) ** 2
        g = (self.g - other.g) ** 2
        b = (self.b - other.b) ** 2
        return r + g + b

    def mix(self, bias, other):
        assert 0 <= bias <= 1
        alpha = 1 - bias
        return self.__class__(round(self.r * alpha + other.r * bias),
                              round(self.g * alpha + other.g * bias),
                              round(self.b * alpha + other.b * bias))

    @staticmethod
    def get(bias, *colors):
        assert 0 <= bias <= 1
        ranges = len(colors) - 1
        assert ranges > 0
        length = 1 / ranges
        index = int(bias / length)
        if index == ranges:
            return colors[-1]
        first, second = colors[index:index+2]
        return first.mix(bias % length / length, second)

    ########################################################################

    @staticmethod
    def __mod(value):
        div, mod = divmod(value, 1.0)
        if div > 0.0 and not mod:
            return 1.0
        return mod

for key, value in Color.HTML.items():
    setattr(Color, key, Color.parse(value))

################################################################################

class ColorOptions(tkinter.Toplevel):

    LABEL = dict(width=9, anchor=tkinter.CENTER)
    SCALE = dict(orient=tkinter.HORIZONTAL, length=256, from_=0.0, to=1.0)
    VALUE = dict(text='0.0', width=5, relief=tkinter.GROOVE)
    BYTE = dict(text='00', width=3, relief=tkinter.GROOVE,
                anchor=tkinter.CENTER)
    PADDING = dict(padx=2, pady=2)

    ########################################################################

    OPEN = False

    @classmethod
    def open_window(cls, root, color):
        # Only open if not already open and return selection.
        if not cls.OPEN:
            cls.OPEN = True
            window = cls(root, color)
            window.mainloop()
            return window.color
        return ''

    ########################################################################

    def __init__(self, master, color):
        super().__init__(master)
        self.transient(master)
        self.geometry('+{}+{}'.format(master.winfo_rootx(),
                                      master.winfo_rooty()))
        # Build all the widgets that will in the window.
        self.create_interface()
        # Populate the widgets with the correct settings.
        self.load_widget_settings(color)
        # Override the closing of this window to keep track of its state.
        self.protocol('WM_DELETE_WINDOW', self.ask_destroy)
        # Prepare the window for general display.
        self.title('Colors')
        self.resizable(False, False)
        # Create a message box to warn about closing.
        options = dict(title='Warning?', icon=tkinter.messagebox.QUESTION,
                       type=tkinter.messagebox.YESNO, message='''\
Are you sure you want to close?
You will lose all your changes.''')
        self.__cancel_warning = tkinter.messagebox.Message(self, **options)

    def load_widget_settings(self, color):
        # Set the colors.
        color = Color.parse(color)
        self.update_hsv(color.h, color.s, color.v)
        self.hsv_updated(color)

    @property
    def color(self):
        # Return the color of the canvas.
        return self.__color

    def ask_destroy(self):
        # Only close if user wants to lose settings.
        if self.__cancel_warning.show() == tkinter.messagebox.YES:
            self.destroy()
        else:
            self.focus_set()

    def destroy(self):
        # Destroy this window and unset the OPEN flag.
        super().destroy()
        self.quit()
        self.__class__.OPEN = False

    def create_interface(self):
        # Create all the widgets.
        self.rgb_scales = self.create_rgb_scales()
        self.hsv_scales = self.create_hsv_scales()
        self.color_area = self.create_color_area()
        self.input_buttons = self.create_buttons()
        # Place them on the grid.
        self.rgb_scales.grid(row=0, column=0)
        self.hsv_scales.grid(row=1, column=0)
        self.color_area.grid(row=2, column=0, sticky=tkinter.EW)
        self.input_buttons.grid(row=3, column=0, sticky=tkinter.EW)

    def create_rgb_scales(self):
        rgb_scales = tkinter.ttk.Labelframe(self, text='RGB Scales')
        # Create the inner widget.
        self.r_label = tkinter.ttk.Label(rgb_scales, text='Red', **self.LABEL)
        self.g_label = tkinter.ttk.Label(rgb_scales, text='Green', **self.LABEL)
        self.b_label = tkinter.ttk.Label(rgb_scales, text='Blue', **self.LABEL)
        self.r_scale = tkinter.ttk.Scale(rgb_scales, command=self.rgb_updated,
                                         **self.SCALE)
        self.g_scale = tkinter.ttk.Scale(rgb_scales, command=self.rgb_updated,
                                         **self.SCALE)
        self.b_scale = tkinter.ttk.Scale(rgb_scales, command=self.rgb_updated,
                                         **self.SCALE)
        self.r_value = tkinter.ttk.Label(rgb_scales, **self.VALUE)
        self.g_value = tkinter.ttk.Label(rgb_scales, **self.VALUE)
        self.b_value = tkinter.ttk.Label(rgb_scales, **self.VALUE)
        self.r_byte = tkinter.ttk.Label(rgb_scales, **self.BYTE)
        self.g_byte = tkinter.ttk.Label(rgb_scales, **self.BYTE)
        self.b_byte = tkinter.ttk.Label(rgb_scales, **self.BYTE)
        # Place widgets on grid.
        self.r_label.grid(row=0, column=0, **self.PADDING)
        self.g_label.grid(row=1, column=0, **self.PADDING)
        self.b_label.grid(row=2, column=0, **self.PADDING)
        self.r_scale.grid(row=0, column=1, **self.PADDING)
        self.g_scale.grid(row=1, column=1, **self.PADDING)
        self.b_scale.grid(row=2, column=1, **self.PADDING)
        self.r_value.grid(row=0, column=2, **self.PADDING)
        self.g_value.grid(row=1, column=2, **self.PADDING)
        self.b_value.grid(row=2, column=2, **self.PADDING)
        self.r_byte.grid(row=0, column=3, **self.PADDING)
        self.g_byte.grid(row=1, column=3, **self.PADDING)
        self.b_byte.grid(row=2, column=3, **self.PADDING)
        # Return the label frame.
        return rgb_scales

    def create_hsv_scales(self):
        hsv_scales = tkinter.ttk.Labelframe(self, text='HSV Scales')
        # Create the inner widget.
        self.h_label = tkinter.ttk.Label(hsv_scales, text='Hue', **self.LABEL)
        self.s_label = tkinter.ttk.Label(hsv_scales, text='Saturation',
                                         **self.LABEL)
        self.v_label = tkinter.ttk.Label(hsv_scales, text='Value', **self.LABEL)
        self.h_scale = tkinter.ttk.Scale(hsv_scales, command=self.hsv_updated,
                                         **self.SCALE)
        self.s_scale = tkinter.ttk.Scale(hsv_scales, command=self.hsv_updated,
                                         **self.SCALE)
        self.v_scale = tkinter.ttk.Scale(hsv_scales, command=self.hsv_updated,
                                         **self.SCALE)
        self.h_value = tkinter.ttk.Label(hsv_scales, **self.VALUE)
        self.s_value = tkinter.ttk.Label(hsv_scales, **self.VALUE)
        self.v_value = tkinter.ttk.Label(hsv_scales, **self.VALUE)
        self.h_byte = tkinter.ttk.Label(hsv_scales, **self.BYTE)
        self.s_byte = tkinter.ttk.Label(hsv_scales, **self.BYTE)
        self.v_byte = tkinter.ttk.Label(hsv_scales, **self.BYTE)
        # Place widgets on grid.
        self.h_label.grid(row=0, column=0, **self.PADDING)
        self.s_label.grid(row=1, column=0, **self.PADDING)
        self.v_label.grid(row=2, column=0, **self.PADDING)
        self.h_scale.grid(row=0, column=1, **self.PADDING)
        self.s_scale.grid(row=1, column=1, **self.PADDING)
        self.v_scale.grid(row=2, column=1, **self.PADDING)
        self.h_value.grid(row=0, column=2, **self.PADDING)
        self.s_value.grid(row=1, column=2, **self.PADDING)
        self.v_value.grid(row=2, column=2, **self.PADDING)
        self.h_byte.grid(row=0, column=3, **self.PADDING)
        self.s_byte.grid(row=1, column=3, **self.PADDING)
        self.v_byte.grid(row=2, column=3, **self.PADDING)
        # Return the label frame.
        return hsv_scales

    def create_color_area(self):
        # Create a display area set to black to begin with.
        color_area = tkinter.ttk.Labelframe(self, text='Color Sample')
        self.canvas = tkinter.Canvas(color_area, height=70,
                                     background='#000000')
        self.canvas.grid(row=0, column=0)
        return color_area

    def create_buttons(self):
        # Create a frame for the buttons.
        input_buttons = tkinter.ttk.Frame(self)
        # Create the buttons.
        self.empty_space = tkinter.ttk.Label(input_buttons, width=38)
        self.okay_button = tkinter.ttk.Button(input_buttons, text='Accept',
                                              command=self.accept)
        self.cancel_button = tkinter.ttk.Button(input_buttons, text='Cancel',
                                                command=self.cancel)
        # Place them on the grid.
        self.empty_space.grid(row=0, column=0, sticky=tkinter.EW)
        self.okay_button.grid(row=0, column=1, sticky=tkinter.EW)
        self.cancel_button.grid(row=0, column=2, sticky=tkinter.EW)
        # Return the containing frame.
        return input_buttons

    def accept(self):
        # Close the window and allow color to be returned.
        self.destroy()

    def cancel(self):
        # Cancel the color before closing window.
        self.__color = ''
        self.destroy()

    def rgb_updated(self, value):
        # Update the interface after RBG change.
        r = self.r_scale['value']
        g = self.g_scale['value']
        b = self.b_scale['value']
        self.update_rgb(r, g, b)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        self.update_hsv(h, s, v)
        self.update_color_area()

    def hsv_updated(self, value):
        # Update the interface after HSV change.
        h = self.h_scale['value']
        s = self.s_scale['value']
        v = self.v_scale['value']
        self.update_hsv(h, s, v)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        self.update_rgb(r, g, b)
        self.update_color_area()

    def update_rgb(self, r, g, b):
        # Update RGB values to those given.
        self.r_scale['value'] = r
        self.g_scale['value'] = g
        self.b_scale['value'] = b
        self.r_value['text'] = str(r)[:5]
        self.g_value['text'] = str(g)[:5]
        self.b_value['text'] = str(b)[:5]
        self.r_byte['text'] = '{:02X}'.format(round(r * 255))
        self.g_byte['text'] = '{:02X}'.format(round(g * 255))
        self.b_byte['text'] = '{:02X}'.format(round(b * 255))
        
    def update_hsv(self, h, s, v):
        # Update HSV values to those given.
        self.h_scale['value'] = h
        self.s_scale['value'] = s
        self.v_scale['value'] = v
        self.h_value['text'] = str(h)[:5]
        self.s_value['text'] = str(s)[:5]
        self.v_value['text'] = str(v)[:5]
        self.h_byte['text'] = '{:02X}'.format(round(h * 255))
        self.s_byte['text'] = '{:02X}'.format(round(s * 255))
        self.v_byte['text'] = '{:02X}'.format(round(v * 255))

    def update_color_area(self):
        # Change the color of preview area based on RGB.
        color = '#{}{}{}'.format(self.r_byte['text'],
                                 self.g_byte['text'],
                                 self.b_byte['text'])
        self.canvas['background'] = color
        self.__color = color

################################################################################

class AboutFSM(tkinter.Toplevel):

    NEW_FEATURES = '''\
What's New in FSM 2.5?
=========================

- Timestamps are still encoded in GMT but are automatically converted
  to local time when displayed. Program will not need to be restarted
  if daylight savings time changes while program is running.

- Errors will be recorded to the "FSM Settings" folder if any occur
  during execution. Once the program closes, the file will be created
  with a record of your name, the time, and a stack trace taken from
  the exceptions.

- Links are automatically created to files referenced in relative to
  the program's root folder. If FSM is running on Windows, clicking
  on those links will open the file. See General Help for more info.


What's New in FSM 2.4?
=========================

- Pressing F1 now brings up an "About FSM" box that allows access to
  various documentation regarding the program.

- Menus have been slightly modified in how they come up and close
  down. Fewer errors should be generated in the background when
  closing dialogs that own open child windows (though some may exist).


What's New in FSM 2.3?
=========================

- Pressing F2 allows access to user-settable options in the program.
  Reasonable defaults are provided, and the settings can easily be
  reset by deleting the settings file in the settings folder.

- Clicking on buttons brings up a custom color picker. The only way to
  set the color is by clicking on the "Okay" button at the bottom.

- Ten settings are supplied, but some do not take effect until restart
  while others only apply to new messages. To get the most current
  view according to the settings, the program must be restarted.


What's New in FSM 2.2?
=========================

- Wispering and reverse wispering is now possible. Writing "@[name]"
  before a message should allow only the intended recipient to view
  the message.

- Reverse wispering is accomplished by placing a "!" mark before the
  wispered message ("!@[name] message"). The person named should not
  receive the message.


What's New in FSM 2.1?
=========================

- Links are automatically recognized now when entered into messages.
  Clicking on them should open them up in your default browser.


What's New in FSM 2.0?
=========================

- Entire program was written from scratch. FSM 1 has been canceled
  and is not able to work with the new I/O system. Major version
  changes will probably continue based on changes to the I/O system
  that would not be compatible with older designs.'''

    GENERAL_HELP = '''\
Automatic Links
=========================

If FSM detects a special attribute of the text as described in the
following sections, it will create a "link" that highlights and
possibly reformats that text. Clicking on links is system dependent.

URL - If the text appears to be a URL, it will be highlighted and
      changed into a link that can be clicked on. Clicking on the link
      should try opening the URL in the system's default browser. As
      of right now, only HTTP, HTTPS, and FTP links can be recognized.

PATH - If the text has been formatted to reference a file relative to
       the program's root folder, then a link will be created will the
       file's name highlighted. If the OS is Windows, clicking on that
       link will open that file as though it have been double-clicked.

       Note: the syntax of the command is <path>. As an easy example:
       Has anyone checked out <Stephen Chappell\My Files.txt> yet?


Function Keys
=========================

F1 - Opens "About FSM" and displays a menu to open various bodies of
     documentation. You may browse the history of changes to this
     program, find out different features and how to use this program,
     and find a list of things yet to be accomplished in FSM.

F2 - Brings up a list of options that can be set to change the
     operation of FSM. Colors can be set by clicking on the buttons
     and using the color picker to select a new color. Some options do
     not take effect until restarting the program and cannot be
     changed by others. Options are saved to disk on program exit.


Writing Messages
=========================

Normal Wispering - If you want to write a message to one person, then
     you have the option of wispering to that person. Messages are
     always displayed will the origin's name in brackets beside it. To
     wisper to someone, write "@[name] message" where "name" is the
     person's name and the message follows special wisper syntax.

Reversed Wispering - When you want to send a message to everyone
     except someone in particular, you can reverse wisper by adding a
     "!" to the front of your wispered message. The full syntax for
     the command is "!@[name] message" and is simple to remember since
     "!" and "@" are right beside each other on the keyboard.


Effects of Settings
=========================

Message Settings - Different colors may be selected for highlighting
     messenger names. By default, normal text messages show up light
     blue, wispered text messages show up light red, and reverse
     wispers show up light green. Only names are actually colorized.

Timestamp Settings - If you want to see when a message was written,
     you can turn on timestamps. You have the ability of toggling if
     they are displayed along with the background and foreground color
     of the text.

Hyperlink Settings - When the program identifies possible links to web
     sites, they are changed into clickable text to open up the link
     in your default browser. You may change whether or not links are
     underlines along with the color they show up in.

Display Settings - Normally, only the past day's worth of messages are
     shown when the FSM opens. You can change this in the options to
     be up to ten days. You may also test your ability to read text
     that has been modified to test if spelling is as important as
     your English teachers says it is. You might be surprised.'''

    FUTURE_PLANS = '''\
There are no future plans for FSM at this time.'''

    ########################################################################

    STYLE = dict(padx=5, pady=5, sticky=tkinter.EW)

    OPEN = False

    @classmethod
    def open_window(cls, root):
        # Only open window if not already open.
        if not cls.OPEN:
            cls.OPEN = True
            window = cls(root)
            window.mainloop()
            cls.OPEN = False

    ########################################################################

    def __init__(self, master):
        super().__init__(master)
        self.geometry('+{}+{}'.format(master.winfo_rootx(),
                                      master.winfo_rooty()))
        self.transient(master)
        self.protocol('WM_DELETE_WINDOW', self.close)
        # Create the interface for this window.
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        self.title('About FSM')
        # Create a header for the buttons.
        self.font = tkinter.font.Font(self, family='arial', size=24,
                                      weight=tkinter.font.NORMAL)
        self.name = tkinter.ttk.Label(self, text=self.master.title(), width=20,
                                      font=self.font, anchor=tkinter.CENTER)
        self.name.grid(column=0, row=0, columnspan=3)
        # Separate head from the options.
        self.divide = tkinter.Frame(self, borderwidth=1, height=2,
                                    relief=tkinter.SUNKEN, bg='#777')
        self.divide.grid(column=0, row=1, columnspan=3, **self.STYLE)
        # Create buttons to open various informational dialogs.
        # ============
        # New Features
        # General Help
        # Future Plans
        self.new_features = \
            tkinter.ttk.Button(self, text='New Features',
                command=lambda: idlelib.textView.TextViewer(self.master,
                    'New Features', self.NEW_FEATURES))
        self.general_help = \
            tkinter.ttk.Button(self, text='General Help',
                command=lambda: idlelib.textView.TextViewer(self.master,
                    'General Help', self.GENERAL_HELP))
        self.future_plans = \
            tkinter.ttk.Button(self, text='Future Plans',
                command=lambda: idlelib.textView.TextViewer(self.master,
                    'Future Plans', self.FUTURE_PLANS))
        # Place the button on the window.
        self.new_features.grid(column=0, row=2, **self.STYLE)
        self.general_help.grid(column=1, row=2, **self.STYLE)
        self.future_plans.grid(column=2, row=2, **self.STYLE)

    def close(self):
        # Cancel execution of this widnow.
        self.destroy()
        self.quit()        

################################################################################

class SettingsDialog(tkinter.Toplevel):

    FRAME = dict(sticky=tkinter.EW, padx=4, pady=2)
    LABEL = dict(width=19)
    BUTTON = dict(width=5)
    BUTTON_GRID = dict(padx=1, pady=1)

    MIN_CUTOFF = 1
    MAX_CUTOFF = 240

    ########################################################################

    OPEN = False

    @classmethod
    def open_window(cls, root):
        # Only open settings if not open.
        if not cls.OPEN:
            cls.OPEN = True
            window = cls(root)
            window.mainloop()

    ########################################################################

    def __init__(self, master):
        super().__init__(master)
        self.geometry('+{}+{}'.format(master.winfo_rootx(),
                                      master.winfo_rooty()))
        self.transient(master)
        # Build all the widgets that will be in the window.
        self.create_interface()
        # Populate the widgets with the correct settings.
        self.load_widget_settings()
        # Override the closing of this window to keep track of its state.
        self.protocol('WM_DELETE_WINDOW', self.ask_destroy)
        # Prepare the window for general display.
        self.title('Settings')
        self.resizable(False, False)
        # Create a message box to warn about closing.
        options = dict(title='Warning?', icon=tkinter.messagebox.QUESTION,
                       type=tkinter.messagebox.YESNO, message='''\
Are you sure you want to close?
You will lose all your changes.''')
        self.__cancel_warning = tkinter.messagebox.Message(self, **options)

    def ask_destroy(self):
        # Only close if user wants to lose settings.
        if self.__cancel_warning.show() == tkinter.messagebox.YES:
            self.destroy()
        else:
            self.focus_set()

    def destroy(self):
        # Destroy this window and unset the OPEN flag.
        super().destroy()
        self.quit()
        self.__class__.OPEN = False

    def create_interface(self):
        # Create label frames for the different settings.
        self.message_settings()
        self.timestamp_settings()
        self.hyperlink_settings()
        self.display_settings()
        # Create buttons for accepting or cancelling changes.
        self.create_ok_cancel()

    def bind_color_button(self, button):
        # Setup a command for changing the color.
        button['command'] = lambda: self.get_new_color(button)

    def message_settings(self):
        # Create frame for widgets.
        m = self.message = tkinter.ttk.Labelframe(self, text='Message Settings')
        # Create the widgets.
        m.normal_label = tkinter.ttk.Label(m, text='Normal Text:', **self.LABEL)
        m.wisper_label = tkinter.ttk.Label(m, text='Wisper Text:', **self.LABEL)
        m.reverse_label = tkinter.ttk.Label(m, text='Reversed Text:',
                                            **self.LABEL)
        m.normal_button = tkinter.Button(m, **self.BUTTON)
        m.wisper_button = tkinter.Button(m, **self.BUTTON)
        m.reverse_button = tkinter.Button(m, **self.BUTTON)
        # Position the widgets.
        m.normal_label.grid(row=0, column=0)
        m.wisper_label.grid(row=1, column=0)
        m.reverse_label.grid(row=2, column=0)
        m.normal_button.grid(row=0, column=1, **self.BUTTON_GRID)
        m.wisper_button.grid(row=1, column=1, **self.BUTTON_GRID)
        m.reverse_button.grid(row=2, column=1, **self.BUTTON_GRID)
        # Configure the buttons.
        self.bind_color_button(m.normal_button)
        self.bind_color_button(m.wisper_button)
        self.bind_color_button(m.reverse_button)
        # Position the frame.
        m.grid(row=0, column=0, **self.FRAME)

    def timestamp_settings(self):
        # Create frame for widgets.
        t = self.timestamp = tkinter.ttk.Labelframe(self,
                                                    text='Timestamp Settings')
        # Create the widgets.
        t.show_string = tkinter.StringVar(t)
        t.show_checkbutton = tkinter.ttk.Checkbutton(t, text='Show Timestamp',
                                                     variable=t.show_string,
                                                     onvalue='True',
                                                     offvalue='False')
        t.background_label = tkinter.ttk.Label(t, text='Background Color:',
                                               **self.LABEL)
        t.foreground_label = tkinter.ttk.Label(t, text='Foreground Color:',
                                               **self.LABEL)
        t.background_button = tkinter.Button(t, **self.BUTTON)
        t.foreground_button = tkinter.Button(t, **self.BUTTON)
        # Position the widets.
        t.show_checkbutton.grid(row=0, column=0, columnspan=2)
        t.background_label.grid(row=1, column=0)
        t.foreground_label.grid(row=2, column=0)
        t.background_button.grid(row=1, column=1, **self.BUTTON_GRID)
        t.foreground_button.grid(row=2, column=1, **self.BUTTON_GRID)
        # Configure the buttons.
        self.bind_color_button(t.background_button)
        self.bind_color_button(t.foreground_button)
        # Position the frame.
        t.grid(row=1, column=0, **self.FRAME)

    def hyperlink_settings(self):
        # Create frame for widgets.
        h = self.hyperlink = tkinter.ttk.Labelframe(self,
                                                    text='Hyperlink Settings')
        # Create the widgets.
        h.underline_string = tkinter.StringVar(h)
        h.underline_checkbutton = \
            tkinter.ttk.Checkbutton(h, text='Underline Link',
                                    variable=h.underline_string,
                                    onvalue='True', offvalue='False')
        h.foreground_label = tkinter.ttk.Label(h, text='Foreground Color:',
                                               **self.LABEL)
        h.foreground_button = tkinter.Button(h, **self.BUTTON)
        # Position the widgets.
        h.underline_checkbutton.grid(row=0, column=0, columnspan=2)
        h.foreground_label.grid(row=1, column=0)
        h.foreground_button.grid(row=1, column=1, **self.BUTTON_GRID)
        # Configure the button.
        self.bind_color_button(h.foreground_button)
        # Position the frame.
        h.grid(row=2, column=0, **self.FRAME)

    def display_settings(self):
        # Create frame for widgets.
        d = self.display = tkinter.ttk.Labelframe(self, text='Display Settings')
        # Create the widgets.
        d.cutoff_label = tkinter.ttk.Label(d, text='Text Cutoff (hours):',
                                           **self.LABEL)
        d.cutoff_string = tkinter.StringVar(d)
        d.cutoff_spinbox = tkinter.Spinbox(d, from_=self.MIN_CUTOFF,
                                           to=self.MAX_CUTOFF,
                                           textvariable=d.cutoff_string,
                                           **self.BUTTON)
        d.confuse_string = tkinter.StringVar(d)
        d.confuse_checkbutton = tkinter.ttk.\
                                Checkbutton(d, text='Scramble Text',
                                            variable=d.confuse_string,
                                            onvalue='True', offvalue='False')
        # Position the widgets.
        d.cutoff_label.grid(row=0, column=0)
        d.cutoff_spinbox.grid(row=0, column=1)
        d.confuse_checkbutton.grid(row=1, column=0, columnspan=2)
        # Position the frame.
        d.grid(row=3, column=0, **self.FRAME)

    def create_ok_cancel(self):
        # Create frame for widgets.
        b = self.buttons = tkinter.ttk.Frame(self)
        # Create the widgets.
        b.accept = tkinter.ttk.Button(b, text='Accept', command=self.accept)
        b.label = tkinter.ttk.Label(b, width=3)
        b.cancel = tkinter.ttk.Button(b, text='Cancel', command=self.cancel)
        # Position the widgets.
        b.accept.grid(row=0, column=0)
        b.label.grid(row=0, column=1)
        b.cancel.grid(row=0, column=2)
        # Position the frame.
        b.grid(row=4, column=0, **self.FRAME)

    def accept(self):
        # Close window after changing settings.
        self.save_widget_settings()
        self.destroy()

    def cancel(self):
        # Close the window without changing anything.
        self.destroy()

    def save_widget_settings(self):
        # Save settings by their catagories.
        self.save_message_settings()
        self.save_timestamp_settings()
        self.save_hyperlink_settings()
        self.save_display_settings()

    def load_widget_settings(self):
        # Have the widgets display the correct information.
        self.load_message_settings()
        self.load_timestamp_settings()
        self.load_hyperlink_settings()
        self.load_display_settings()

    def load_message_settings(self):
        # Set the color for the name background.
        self.message.normal_button['background'] = SETTINGS.normal_message
        self.message.wisper_button['background'] = SETTINGS.wisper_message
        self.message.reverse_button['background'] = SETTINGS.reverse_wisper

    def save_message_settings(self):
        # Copy current settings back out to global settings.
        SETTINGS.normal_message = Color.parse(self.message.normal_button['bg'])
        SETTINGS.wisper_message = Color.parse(self.message.wisper_button['bg'])
        SETTINGS.reverse_wisper = Color.parse(self.message.reverse_button['bg'])

    def load_timestamp_settings(self):
        # Get timstamp settings and load them in the GUI.
        boolean = ('False', 'True')[SETTINGS.show_timestamp]
        self.timestamp.show_string.set(boolean)
        self.timestamp.background_button['bg'] = SETTINGS.time_background
        self.timestamp.foreground_button['bg'] = SETTINGS.time_foreground

    def save_timestamp_settings(self):
        # Take timestamp options and save in global settings.
        SETTINGS.show_timestamp = self.timestamp.show_string.get() == 'True'
        SETTINGS.time_background = \
            Color.parse(self.timestamp.background_button['bg'])
        SETTINGS.time_foreground = \
            Color.parse(self.timestamp.foreground_button['bg'])

    def load_hyperlink_settings(self):
        # Update the GUI according to the hyperlink settings.
        boolean = ('False', 'True')[SETTINGS.link_underline]
        self.hyperlink.underline_string.set(boolean)
        self.hyperlink.foreground_button['bg'] = SETTINGS.link_foreground

    def save_hyperlink_settings(self):
        # Save the hyperlink settings in the global settings object.
        SETTINGS.link_underline = \
            self.hyperlink.underline_string.get() == 'True'
        SETTINGS.link_foreground = \
            Color.parse(self.hyperlink.foreground_button['bg'])

    def load_display_settings(self):
        # Load the display settings into the GUI.
        self.display.cutoff_string.set(SETTINGS.message_cutoff)
        boolean = ('False', 'True')[SETTINGS.message_confuser]
        self.display.confuse_string.set(boolean)

    def save_display_settings(self):
        # Save user's setting for display for use in program.
        try:
            cutoff = int(self.display.cutoff_string.get())
        except ValueError:
            pass
        else:
            if self.MIN_CUTOFF <= cutoff <= self.MAX_CUTOFF:
                SETTINGS.message_cutoff = cutoff
        SETTINGS.message_confuser = self.display.confuse_string.get() == 'True'

    def get_new_color(self, button):
        # Try changing the color of the button.
        color = ColorOptions.open_window(self.master, button['background'])
        if color:
            button['background'] = color
        self.focus_force()

################################################################################

class Settings:

    FILENAME = 'settings.pickle'
    SLOTS = {'_Settings__path', '_Settings__data'}
    DEFAULT = {'normal_message': Color.LightSteelBlue,
               'wisper_message': Color.LightSteelBlue.set_hue(0),
               'reverse_wisper': Color.LightSteelBlue.set_hue(1 / 3),
               'show_timestamp': False,
               'time_background': Color.Black,
               'time_foreground': Color.White,
               'link_foreground': Color.Blue,
               'link_underline': True,
               'message_cutoff': 24,
               'message_confuser': False}
    
    def __init__(self, path):
        # Save the path and load settings from file.
        self.__path = path
        new, self.__data = self.get_settings()
        # If these the settings did not exist, create and save them.
        if new:
            self.save_settings()

    def get_settings(self):
        # Try opening and loading the settings from file.
        filename = os.path.join(self.__path, self.FILENAME)
        try:
            with open(filename, 'rb') as file:
                settings = pickle.load(file)
            # Test the pickle and check each setting inside it.
            assert isinstance(settings, dict)
            key_list = list(self.DEFAULT)
            for key in settings:
                assert isinstance(key, str)
                assert key in self.DEFAULT
                key_list.remove(key)
            # Add new settings as needed (when new ones are created).
            for key in key_list:
                settings[key] = self.DEFAULT[key]
            # Return old settings, or on error, the default settings.
            return False, settings
        except (IOError, pickle.UnpicklingError, AssertionError):
            return True, self.DEFAULT

    def save_settings(self):
        # Make the directory if it does not exist or check its type.
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        elif os.path.isfile(self.__path):
            raise IOError('Directory cannot be created!')
        # Pickle and save the settings in the specified path (filename).
        filename = os.path.join(self.__path, self.FILENAME)
        with open(filename, 'wb') as file:
            pickle.dump(self.__data, file, pickle.HIGHEST_PROTOCOL)

    def __getattr__(self, name):        # Get an attribute.
        # If the name is an instance variable, return it.
        if name in self.SLOTS:
            return vars(self)[name]
        # Otherwise, get it from the settings stored in __data.
        return self.__data[name]

    def __setattr__(self, name, value): # Set an attribute.
        # If the name is an instance variable, go ahead and set it.
        if name in self.SLOTS:
            vars(self)[name] = value
        else:
            # Otherwise, store the setting in the __data attribute.
            self.__data[name] = value

################################################################################

random = random.SystemRandom().sample
string = string.digits + string.ascii_uppercase
# For version 3, use all ASCII letter (uppercase and lowercase).

uuid = lambda: ''.join(random(string, len(string)))

################################################################################

class DirectoryMonitor:

    def __init__(self, path):
        # Save directory path and file monitors (by path).
        self.__path = path
        self.__files = {}

    def update(self, callback):
        # Discover any files are new to the path.
        for name in os.listdir(self.__path):
            if self.valid_name(name) and name not in self.__files:
                path_name = os.path.join(self.__path, name)
                self.__files[name] = FileMonitor(path_name)
        errors = set()
        # Try updating each file monitor with reference to callback.
        for name, monitor in self.__files.items():
            try:
                monitor.update(callback)
            except OSError:
                errors.add(name)
        # Remove any problem files from the list.
        for name in errors:
            del self.__files[name]

    @staticmethod
    def valid_name(name):
        # There should be 36 characters in a valid name.
        if len(name) != len(string):
            return False
        # Every single character should be there (from the template).
        expected_characters = set(string)
        in_both = set(name) & expected_characters
        return in_both == expected_characters
        

################################################################################

class FileMonitor:

    def __init__(self, path):
        # Track mondification is a file and present position within file.
        self.__path = path
        self.__modified = 0
        self.__position = 0

    def update(self, callback):
        # Find out if the file has been modified.
        modified = os.path.getmtime(self.__path)
        if modified != self.__modified:
            # Remember the present time (we are getting an update).
            self.__modified = modified
            with open(self.__path, 'r') as file:
                # Go to present location, read to EOF, and remember position.
                file.seek(self.__position)
                try:
                    text = file.read()
                except UnicodeError:
                    print('Please report problem with:', repr(self.__path))
                    traceback.print_exc()
                    print('-' * 80)
                self.__position = file.tell()
            # Execute callback with file ID and new text update.
            callback(self.__path, text)

################################################################################

class Aggregator:

    def __init__(self):
        # Keep track of message streams.
        self.__streams = {}

    def update(self, path, text):
        # Create a new MessageStream if the path is not recognized.
        if path not in self.__streams:
            self.__streams[path] = MessageStream()
        # Split text on NULL and check that there is nothing following.
        parts = text.split('\0')
        if parts[-1]:
            raise IOError('Text is not properly terminated!')
        # Update stream with all message parts except the last empty one.
        self.__streams[path].update(parts[:-1])

    def get_messages(self):
        all_messages = []
        # Get all new messages waiting in the streams.
        for stream in self.__streams.values():
            all_messages.extend(stream.get_messages())
        # Return them sorted by the timestamps.
        return sorted(all_messages, key=lambda message: message.time)

################################################################################

class MessageStream:

    def __init__(self):
        # Save name, buffered tail, and any waiting messages.
        self.__name = None
        self.__buffer = None
        self.__waiting = []

    def update(self, parts):
        # If there is no name, assume the first part is the name.
        if self.__name is None:
            self.__name = parts.pop(0)
        # If something is in the buffer, add it to front of parts and clear.
        if self.__buffer is not None:
            parts.insert(0, self.__buffer)
            self.__buffer = None
        # If the parts length is odd, save tail in the buffer.
        if len(parts) & 1:
            self.__buffer = parts.pop()
        # Append new, waiting messages to the list.
        for index in range(0, len(parts), 2):
            self.__waiting.append(Message(self.__name, *parts[index:index+2]))

    def get_messages(self):
        # Return the messages and clear the list.
        messages = self.__waiting
        self.__waiting = []
        return messages

################################################################################

class Message:

    def __init__(self, name, timestamp, text):
        self.name = name
        try:
            # Try to parse the timestamp.
            self.time = datetime.datetime.strptime(timestamp,
                                                   '%Y-%m-%dT%H:%M:%SZ')
            self.text = text.strip()
        except ValueError:
            # The messages appear corrupt.
            self.time = datetime.datetime.utcnow()
            self.text = '[STREAM IS CORRUPT]'
        # Assume this is a normal message (for name color).
        self.tag = 'name'

################################################################################

class MessageWriter:

    def __init__(self, path, name):
        # Check the name, save it, and set a couple other variables.
        assert '\0' not in name, 'Name may not have null characters!'
        self.__name = name
        self.__primed = False
        self.__path = os.path.join(path, self.__find(path))

    def __find(self, path):
        # For each file in the directory ...
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            if os.path.isfile(full_path):
                # Check the first 256 bytes for a name.
                with open(full_path, 'r') as file:
                    data = file.read(256).split('\0', 1)[0]
                # If (your) name was found, file exists.
                if data == self.__name:
                    self.__primed = True
                    return name
        # A new file will need to be created with a unique identifier.
        return uuid()

    def write(self, text):
        # Check the message for invalid characters and try priming the file.
        assert '\0' not in text, 'Text may not have null characters!'
        self.prime()
        # Save the message as (timestamp, null, text, null) in the file.
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        with open(self.__path, 'a') as file:
            file.write(timestamp + '\0' + text + '\0')

    def prime(self):
        if not self.__primed:
            # Write name to file followed by a null.
            with open(self.__path, 'w') as file:
                file.write(self.__name + '\0')
            self.__primed = True
                
################################################################################

# This code provides error logging facilities.

def main():
    # Figure out where files should be stored.
    public_path = os.path.join('Message Storage', 'V2.5')
    private_path = os.path.join('..', 'FSM Settings')
    # Execute the main class (static) function of FSM.
    with capture_stderr() as stderr:
        FSM.main(public_path, private_path)
    # Cleanup stderr and save and errors to file.
    record(stderr, private_path, 'errorlog.pickle')

@contextlib.contextmanager
def capture_stderr():
    # Provide a context manager that captures standard error.
    orig_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        yield sys.stderr
    finally:
        sys.stderr = orig_stderr

def record(stream, path, filename):
    # Find out if there were any errors during execution.
    errors = stream.getvalue()
    if errors:
        # Save them to a pickled file with a timestamp.
        with open(os.path.join(path, filename), 'ab', 0) as file:
            problem = getpass.getuser(), datetime.datetime.utcnow(), errors
            pickle.dump(problem, file)

################################################################################

class FSM(tkinter.ttk.Frame):

    @classmethod
    def main(cls, log_path, settings_path):
        # Create a global settings object for the application.
        global SETTINGS
        SETTINGS = Settings(settings_path)
        # Create the root GUI object.
        tkinter.NoDefaultRoot()
        root = tkinter.Tk()
        # Bind an event handler for closing the program.
        def on_close():
             SETTINGS.save_settings()
             root.destroy()
             root.quit()
        root.protocol('WM_DELETE_WINDOW', on_close)
        # Set the window title and minimum size for the window.
        name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        root.title(name)
        root.minsize(320, 240)  # QVGA
        # Create, position, and setup FSM widget for resizing.
        view = cls(root, log_path)
        view.grid(row=0, column=0, sticky=tkinter.NSEW)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        # Bind buttons to access the application's menus.
        root.bind_all('<F2>', lambda event: SettingsDialog.open_window(root))
        root.bind_all('<F1>', lambda event: AboutFSM.open_window(root))
        # Start the application's event loop.
        root.mainloop()

    def __init__(self, master, log_path, **kw):
        super().__init__(master, **kw)
        self.configure_widgets()
        # Save username and prepare for program I/O.
        self.__username = getpass.getuser()
        self.__writer = MessageWriter(log_path, self.__username)
        self.__monitor = DirectoryMonitor(log_path)
        self.__messages = Aggregator()
        # Start looking for updates to the files.
        self.after_idle(self.update)

    def configure_widgets(self):
        # Create widgets.
        self.__text = tkinter.Text(self, state=tkinter.DISABLED,
                                   wrap=tkinter.WORD, cursor='arrow')
        self.__scroll = tkinter.ttk.Scrollbar(self, orient=tkinter.VERTICAL,
                                              command=self.__text.yview)
        self.__entry = tkinter.ttk.Entry(self, cursor='xterm')
        # Alter their settings.
        self.__text.configure(yscrollcommand=self.__scroll.set)
        self.__text.tag_configure('name', background=SETTINGS.normal_message)
        self.__text.tag_configure('high', background=SETTINGS.wisper_message)
        self.__text.tag_configure('mess', background=SETTINGS.reverse_wisper)
        self.__text.tag_configure('time', background=SETTINGS.time_background,
                                  foreground=SETTINGS.time_foreground)
        # Configure settings for hyperlinks.
        self.__text.tag_configure('dynamic_link',
                                  foreground=SETTINGS.link_foreground,
                                  underline=SETTINGS.link_underline)
        self.__text.tag_bind('dynamic_link', '<Enter>',
                      lambda event: self.__text.configure(cursor='hand2'))
        self.__text.tag_bind('dynamic_link', '<Leave>',
                      lambda event: self.__text.configure(cursor='arrow'))
        # Configure settings for static links.
        self.__text.tag_configure('static_link',
                                  foreground=SETTINGS.link_foreground,
                                  underline=SETTINGS.link_underline)
        # Place everything on the grid.
        self.__text.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.__scroll.grid(row=0, column=1, sticky=tkinter.NS)
        self.__entry.grid(row=1, column=0, columnspan=2, sticky=tkinter.EW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Setup box for typing.
        self.__entry.bind('<Control-Key-a>', self.select_all)
        self.__entry.bind('<Control-Key-/>', lambda event: 'break')
        self.__entry.bind('<Return>', self.send_message)
        self.__entry.focus_set()
        # Save first status and link counts.
        self.__first_line = True
        self.__url_id = 0
        self.__path_id = 0

    def select_all(self, event):
        # Select everything in the widget.
        event.widget.selection_range(0, tkinter.END)
        return 'break'

    def send_message(self, event):
        # Cut everything from the entry and write to file.
        text = self.__entry.get()
        self.__entry.delete(0, tkinter.END)
        self.__writer.write(text)

    def update(self):
        # Update the directory monitor once a second.
        self.after(1000, self.update)
        self.__monitor.update(self.__messages.update)
        # For each message, show those less than a day old.
        utcnow = datetime.datetime.utcnow()
        for message in self.__messages.get_messages():
            hours = (utcnow - message.time).total_seconds() / 3600
            if hours < SETTINGS.message_cutoff and self.allowed(message):
                self.display(message)

    def allowed(self, message):
        # If there is no text, it is not allowed.
        if not message.text:
            return False
        # Extract some information about the text.
        dest, text, reverse = self.get_wisper(message.text)
        # If there is no destination, it is allowed.
        if dest is None:
            return True
        # Change the message's color.
        message.tag = 'mess' if reverse else 'high'
        if self.__username == message.name:
            # ... unless the source really wants to ignore himself.
            if reverse:
                return False
            # Reformat the text and allow message.
            form = '![{}] {}' if reverse else '-> [{}] {}'
            message.text = form.format(dest, text)
            return True
        # If this is not a reversed whisper ...
        if not reverse:
            # It is only allowed for the destination.
            if dest == self.__username:
                message.text = text
                return True
            return False
        # Otherwise, it is not allowed to anyone else.
        if dest != self.__username:
            message.text = '![{}] {}'.format(dest, text)
            return True
        return False

    def get_wisper(self, message):
        # Note to self: start wispers as "@[" and reversals as "!["
        # next time you implement this system for version 3 of FSM.
        reverse, cleaned = False, message
        # If the messages starts with a '!', it should be cleaned.
        if message[0] == '!':
            reverse, cleaned = True, message[1:]
        # If the message starts with the proper prefix ...
        if cleaned[:2] == '@[':
            try:
                # Find the "end of name" marker.
                index = cleaned.index(']')
            except ValueError:
                pass    # Not wispered.
            else:
                # Return name, cleaned text, and reversal flag.
                dest = cleaned[2:index]
                text = cleaned[index+1:].strip()
                return dest, text, reverse
        # It was not wispered.
        return None, message, False

    def display(self, message):
        # Enable changes and take first line into account.
        self.__text['state'] = tkinter.NORMAL
        if self.__first_line:
            self.__first_line = False
        else:
            self.__text.insert(tkinter.END, '\n')
        # Show the timestamp if requested.
        if SETTINGS.show_timestamp:
            diff = datetime.datetime.now() - datetime.datetime.utcnow()
            time = message.time + diff
            # Display string that has been corrected for local time zone.
            self.__text.insert(tkinter.END, time.strftime('%I:%M %p'), 'time')
            self.__text.insert(tkinter.END, ' ')
        # Show the name with the proper color (message.tag).
        self.__text.insert(tkinter.END, '[' + message.name + ']', message.tag)
        # Add text with formatting, scroll to botton, and disable changes.
        self.add_text_with_URLs(' ' + message.text)
        self.__text.see(tkinter.END)
        self.__text['state'] = tkinter.DISABLED

    def add_text_with_URLs(self, message):
        url_list = self.find_urls(message)
        # Split on each URL, prefix, and create URL.
        for url in url_list:
            head, message = message.split(url, 1)
            self.add_text_with_PATHs(head)
            self.create_url(url)
        # Display whatever may be left.
        self.add_text_with_PATHs(message)

    def add_text_with_PATHs(self, message):
        path_list = self.find_paths(message)
        # Split on each path markup and create path links.
        for markup, path, name in path_list:
            head, message = message.split(markup, 1)
            self.add_plain_text(head)
            self.create_path(path, name)
        # Finish displaying any trailing text.
        self.add_plain_text(message)

    def create_url(self, url):
        # Create a new, incremented URL tag for text.
        self.__url_id += 1
        tag = 'url' + str(self.__url_id)
        # Insert the text and bind a command to open a webbrowser.
        self.__text.insert(tkinter.END, url, ('dynamic_link', tag))
        self.__text.tag_bind(tag, '<1>', lambda event: webbrowser.open(url))

    def create_path(self, path, name):
        # If the user is running Windows ...
        if hasattr(os, 'startfile'):
            # Create a new tag for the path.
            self.__path_id += 1
            tag = 'path' + str(self.__path_id)
            # Add the text and create an opening command.
            self.__text.insert(tkinter.END, name, ('dynamic_link', tag))
            self.__text.tag_bind(tag, '<1>', lambda event: os.startfile(path))
        else:
            # Insert a link that does not do anything.
            self.__text.insert(tkinter.END, name, 'static_link')

    def add_plain_text(self, message):
        # Confuse text if needed before adding text to display.
        if SETTINGS.message_confuser:
            message = confuse(message)
        self.__text.insert(tkinter.END, message)

    def find_paths(self, message):
        # Track found paths and current search positions.
        paths = []
        index_a = index_b = 0
        # While we are still searching the message's end ...
        while index_a > -1 and index_b > -1:
            index_a = message.find('<', index_b)
            # If the less than symbol has been found ...
            if index_a > -1:
                index_b = message.find('>', index_a)
                # If the greater than symbol has been found ...
                if index_b > -1:
                    path_markup = message[index_a:index_b+1]
                    # Add path to list if it exists.
                    self.test_and_add_path(path_markup, paths)
        return paths

    def test_and_add_path(self, markup, paths):
        # Extract the path and create an "absolute" path.
        pulled = markup[1:-1].strip()
        program = os.path.dirname(sys.argv[0])
        absolute = os.path.join(program, pulled)
        # Turn the path into a normal path and test for existence.
        normal = os.path.normpath(absolute)
        if os.path.exists(normal):
            # Record the markup, normal path, and filename.
            base = os.path.basename(normal)
            file = os.path.splitext(base)[0]
            paths.append((markup, normal, file))

    def find_urls(self, message):
        urls = []
        # Split text on whitespace.
        for text in message.split():
            result = urllib.parse.urlparse(text)
            # It is a URL if the protocol is correct and there is a location.
            if result.scheme in {'http', 'https', 'ftp'} and result.netloc:
                urls.append(text)
        # Return the list of found URLs.
        return urls

################################################################################

def confuse(text):
    # Collect all the words in a buffer after processing.
    buffer = []
    for data in words(text):
        if isinstance(data, str):
            buffer.append(data)             # Normal Text
        elif len(data) < 4:
            buffer.append(''.join(data))    # Short Text
        else:
            buffer.append(scramble(data))   # Confused Text
    # Return the processed string.
    return ''.join(buffer)

def words(string):
    # Prepare to process a string.
    data = str(string)
    if data:
        # Collect words and non-words and determine starting state.
        buffer = ''
        mode = 'A' <= data[0] <= 'Z' or 'a' <= data[0] <= 'z'
        for character in data:
            # Add characters to buffer until a mode change.
            if mode == ('A' <= character <= 'Z' or 'a' <= character <= 'z'):
                buffer += character
            else:
                # Yield a data type indicating what has been found.
                yield tuple(buffer) if mode else buffer
                buffer = character
                mode = not mode
        # Yield any remaining data in the buffer.
        yield tuple(buffer) if mode else buffer
    else:
        yield data

def scramble(data):
    # Get the first letter and scramble the middle letters.
    array = [data[0]]
    array.extend(random(data[1:-1], len(data) - 2))
    # Append the last letter and return the final string.
    array.append(data[-1])
    return ''.join(array)

################################################################################

if __name__ == '__main__':
    main()
