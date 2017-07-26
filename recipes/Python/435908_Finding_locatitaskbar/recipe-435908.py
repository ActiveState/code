import wx

def getTaskbarPos():
    d_w, d_h = wx.DisplaySize()
    c_x, c_y, c_w, c_h = wx.ClientDisplayRect()
                        
    l = [(c_y, "top"), (d_h - c_y - c_h, "bottom"), (c_x, "left"), (d_w - c_x - c_w, "right")]
    def sorter(a,b):
        if a[0]<b[0] : return 1
        if a[0]>b[0] : return -1
        return 0
    l.sort(sorter)
    return l[0][1]
