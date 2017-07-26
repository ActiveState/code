import tkinter.ttk
import colorsys

class ColorStudy(tkinter.ttk.Frame):

    LABEL = dict(width=9, anchor=tkinter.CENTER)
    SCALE = dict(orient=tkinter.HORIZONTAL, length=256, from_=0.0, to=1.0)
    VALUE = dict(text='0.0', width=5, relief=tkinter.GROOVE)
    BYTE = dict(text='00', width=3, relief=tkinter.GROOVE,
                anchor=tkinter.CENTER)
    PADDING = dict(padx=2, pady=2)

    @classmethod
    def main(cls):
        tkinter.NoDefaultRoot()
        root = tkinter.Tk()
        root.title('Color Study')
        root.resizable(False, False)
        view = cls(root)
        view.grid(row=0, column=0)
        root.mainloop()

    def __init__(self, master):
        super().__init__(master)
        # Create all the widgets.
        self.rgb_scales = self.create_rgb_scales()
        self.hsv_scales = self.create_hsv_scales()
        self.color_area = self.create_color_area()
        # Place them on the grid.
        self.rgb_scales.grid(row=0, column=0)
        self.hsv_scales.grid(row=1, column=0)
        self.color_area.grid(row=2, column=0, sticky=tkinter.EW)

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
        color_area = tkinter.ttk.Labelframe(self, text='Color Sample')
        self.canvas = tkinter.Canvas(color_area, height=70,
                                     background='#000000')
        self.canvas.grid(row=0, column=0)
        return color_area

    def rgb_updated(self, value):
        r = self.r_scale['value']
        g = self.g_scale['value']
        b = self.b_scale['value']
        self.update_rgb(r, g, b)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        self.update_hsv(h, s, v)
        self.update_color_area()

    def hsv_updated(self, value):
        h = self.h_scale['value']
        s = self.s_scale['value']
        v = self.v_scale['value']
        self.update_hsv(h, s, v)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        self.update_rgb(r, g, b)
        self.update_color_area()

    def update_rgb(self, r, g, b):
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
        color = '#{}{}{}'.format(self.r_byte['text'],
                                 self.g_byte['text'],
                                 self.b_byte['text'])
        self.canvas['background'] = color

if __name__ == '__main__':
    ColorStudy.main()
