import sys, os
import wx
from win32com.client import Dispatch


def parse_data(data, output):
    # this is where you do the processing
    pass

if __name__ == "__main__":
    app = wx.App()
    #app.MainLoop()    # strangely enough this line is isn't needed. But creating the app is...

    args = sys.argv[1:]
    if len(args) < 1:
        # no arguments? then show dialog
        dlg = wx.FileDialog(None, "Choose a file", os.getcwd(), "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            filename = path
            dlg.Destroy()
        else:
            dlg.Destroy()
            sys.exit(1)
    else:
        # use command line arguments if they were given
        filename = args[0]

    if len(args) > 1:
        ofilename = args[1]
    else:
        # automagically choose an output filename
        ofilename = filename+".csv"


    # open and read the input
    file = open(filename, "r")
    data = file.readlines()
    file.close()
    # open the output file
    output = open(ofilename, "w")
    # do the real work
    parse_data(data, output)
    # close the output
    output.close()

    # do some excel formatting on the output
    xlapp = Dispatch("Excel.Application")
    xlapp.Visible = 1
    xlapp.Workbooks.Open(ofilename)
    sheet = xlapp.ActiveSheet
    # set the widths
    sheet.Range(sheet.Cells(1, 1), sheet.Cells(1, 100)).EntireColumn.AutoFit()
