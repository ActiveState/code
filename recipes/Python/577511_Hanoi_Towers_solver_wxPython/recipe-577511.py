#author: A. Polino
import wx
import sys


## make sure the windows is focused than press any button, and the program will move a plate. keep  ## pressing until the problem is solved
## by default it will display 5 plates. To change this, you have to call the script with a second   ## argument, wich is the number of plates (max 10)

def gen_hanoi(stack, start=1, temp=2, goal=3):
    if stack == 2:
        yield start, temp
        yield start, goal
        yield temp, goal
    else:
        for x in gen_hanoi(stack - 1, start, goal, temp):
            yield x
        yield start, goal
        for x in gen_hanoi(stack - 1, temp, start, goal):
            yield x


class Plate(object):
    def __init__(self, x_len, x_start):
        self.x_len = x_len
        self.x_start = x_start


def create_plates(num):
    assert num <= 10
    x_start = 10
    x_len = 100
    plates = []
    for x in xrange(num):
        plates.append(Plate(x_len, x_start))
        x_len -= 10
        x_start += 5
    return plates


class HanoiWindow(wx.Window):
    def __init__(self, parent, num):
        wx.Window.__init__(self, parent, id=-1, pos = wx.Point(0, 0),
                           size=wx.DefaultSize, style=wx.SUNKEN_BORDER|
                           wx.WANTS_CHARS|wx.FULL_REPAINT_ON_RESIZE)
        self.SetBackgroundColour(wx.NamedColour('white'))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.towers = [create_plates(num), [], []]
        self.solver = gen_hanoi(num)

    def OnPaint(self, evt):
        def draw_rect(x_len, x_start, y_start):
            dc = wx.PaintDC(self)
            font = dc.GetFont()
            font.SetPointSize(15)
            dc.SetFont(font)
            size, colour = 2, wx.NamedColour('black')
            dc.SetPen(wx.Pen(colour, size, wx.SOLID))
            point = wx.Point(x_start, y_start)
            dc.DrawLines([point, point + wx.Point(x_len, 0)])
            dc.DrawLines([point - wx.Point(0, 5), point + wx.Point(x_len, 0) - wx.Point(0, 5)])
            dc.DrawLines([point, point - wx.Point(0, 5)])
            dc.DrawLines([point + wx.Point(x_len, 0), point - wx.Point(0, 5) + wx.Point(x_len, 0)])

        w, h = self.GetClientSizeTuple()
        buffer = wx.EmptyBitmap(w, h)
        dc = wx.PaintDC(self)
        font = dc.GetFont()
        font.SetPointSize(15)
        dc.SetFont(font)
        msg = 'Hanoi Towers'
        w, h = dc.GetTextExtent(msg)
        dc.DrawText(msg, 200, 20)
        size, colour = 8, wx.NamedColour('black')
        dc.SetPen(wx.Pen(colour, size, wx.SOLID))
        for num in xrange(len(self.towers)):
            y_start = 300
            tower = self.towers[num]
            num = num * 200 + 10
            point = wx.Point(num, y_start)
            dc.DrawLines([point, point + wx.Point(120, 0)]) #base
            ## plates
            for plate in tower:
                y_start -= 10
                draw_rect(plate.x_len, num + plate.x_start, y_start)

    def OnKeyUp(self, evt):
        try:
            from_, to = self.solver.next()
            self.towers[to-1].append(self.towers[from_-1].pop())
            self.Refresh()
        except StopIteration:
            wx.MessageBox('Problem Solved!', 'Problem solved', wx.OK)
                

class HanoiFrame(wx.Frame):
    def __init__(self, title, num):
        wx.Frame.__init__(self, parent=None, id=-1,
                          title=title, size=(600, 500), pos=(200, 200))
        self.Window = HanoiWindow(self, num)
        self.Bind(wx.EVT_CLOSE, self.close_frame)

    def close_frame(self, evt):
        sys.exit(0)


class HanoiApp(wx.App):
    def OnInit(self):
        if len(sys.argv) < 2:
            num = 5
        else:
            num = int(sys.argv[1])
        hano = HanoiFrame('Hanoi Towers', num)
        hano.Show(True)
        self.SetTopWindow(hano)
        return True


if __name__ == '__main__':
    fh = HanoiApp(0)
    fh.MainLoop()
