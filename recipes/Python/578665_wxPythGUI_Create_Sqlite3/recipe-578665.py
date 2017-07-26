#!/usr/bin/env python

#-----------------------------------------------------------------------
# developer : toufic zaarour , Byblos-Lebanon

# for any suggestions or improvements, my gmail is : touficmc@gmail.com
#-----------------------------------------------------------------------

import wx
import wx.grid
import gettext
import os
import sqlite3
import datetime

cwd = os.path.abspath(os.curdir)

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.frame_1_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(1, _("Create sqlite3 DataBase"), "", wx.ITEM_NORMAL)
        self.frame_1_menubar.Append(wxglade_tmp_menu,_("DataBase Configuration"))
        
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(2, _("Message"), "", wx.ITEM_NORMAL)
        self.frame_1_menubar.Append(wxglade_tmp_menu,_("About"))

        self.SetMenuBar(self.frame_1_menubar)
        self.__set_properties()
        self.__do_layout()
        self.Bind(wx.EVT_MENU, self.open_dialog, id=1)
        self.Bind(wx.EVT_MENU,self.open_dialog1,id =2)


    def __set_properties(self):
        self.SetTitle(_("Sqlite3 Creator"))
        self.SetSize((555, 444))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer_1)
        self.Layout()

    def open_dialog(self, event):
        MyDialog1(self).Show()

    def open_dialog1(self,event):
        wx.MessageBox("This App is made for you and for all developpers who use sqlite3 and want to create fast databases and data tables\n\nEnjoy...!")


class MyDialog1(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_27 = wx.StaticText(self, -1, _(" Create Your Data Tables :"))
        self.label_25 = wx.StaticText(self, -1, _(" File/Data/Table"))
        self.txtFileName = wx.TextCtrl(self, -1, "")
        self.txtDataName = wx.TextCtrl(self, -1, "")
        self.txtDataTable = wx.TextCtrl(self, -1, "")
        self.grid_1 = wx.grid.Grid(self, -1, size=(1, 1))
        self.bnt_add = wx.Button(self, -1, _("Add Column"))
        self.bnt_remove = wx.Button(self, -1, _("Remove Column"))
        self.bnt_create = wx.Button(self, -1, _("Create DataBase"))
        self.bnt_reset = wx.Button(self, -1, _("Reset Grid"))
        self.txtDataFileOutput = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.cl_add_col, self.bnt_add)
        self.Bind(wx.EVT_BUTTON, self.clk_remove_col, self.bnt_remove)
        self.Bind(wx.EVT_BUTTON, self.clk_Create_db, self.bnt_create)
        self.Bind(wx.EVT_BUTTON, self.clk_reset_grid, self.bnt_reset)


    def __set_properties(self):
        self.SetTitle(_("DataBase Creator"))
        self.SetSize((555, 444))
        self.txtFileName.SetMinSize((100, 27))
        self.txtDataName.SetMinSize((100, 27))
        self.txtDataTable.SetMinSize((100, 27))
        self.grid_1.CreateGrid(1, 2)
        self.grid_1.SetColLabelValue(0, _("Name"))
        self.grid_1.SetColSize(0, 200)
        self.grid_1.SetColLabelValue(1, _("Type"))
        self.grid_1.SetColSize(1,200)
        self.bnt_add.SetMinSize((200, 29))
        self.bnt_remove.SetMinSize((200, 29))
        self.bnt_create.SetMinSize((200, 29))
        self.bnt_reset.SetMinSize((200, 29))
        self.txtDataFileOutput.SetMinSize((400, 30))

    def __do_layout(self):
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_10 = wx.GridSizer(2, 2, 0, 0)
        grid_sizer_8 = wx.GridSizer(1, 4, 0, 0)
        sizer_7.Add(self.label_27, 0, 0, 0)
        grid_sizer_8.Add(self.label_25, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_8.Add(self.txtFileName, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_8.Add(self.txtDataName, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_8.Add(self.txtDataTable, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_7.Add(grid_sizer_8, 1, wx.EXPAND, 0)
        sizer_7.Add(self.grid_1, 1, wx.EXPAND, 0)
        grid_sizer_10.Add(self.bnt_add, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_10.Add(self.bnt_remove, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_10.Add(self.bnt_create, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_10.Add(self.bnt_reset, 0, 0, 0)
        sizer_7.Add(grid_sizer_10, 1, wx.EXPAND, 0)
        sizer_7.Add(self.txtDataFileOutput, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_7)
        self.Layout()

    def cl_add_col(self, event):
        self.grid_1.AppendRows(1)
        event.Skip()

    def clk_remove_col(self, event):
        try:
            lst = self.grid_1.GetSelectedRows()[0]
            self.grid_1.DeleteRows(lst,1)
            event.Skip()
        except IndexError:
            wx.MessageBox("You Did Not Select Any Row To Delete")

    def clk_Create_db(self, event):
        try:
            DataColumnsList=[]
            DataTypeList=[]
            DataString=[]
            DataTableName=str(self.txtDataTable.Value)
            ConnectionString=cwd + "/"+(self.txtFileName.Value + "/" + self.txtDataName.Value + ".db")
            RowNum = self.grid_1.GetNumberRows()

            for i in range(0,RowNum):
                DataColumnsList.append(str(self.grid_1.GetCellValue(i,0)))
                DataTypeList.append(str(self.grid_1.GetCellValue(i,1)))
            
            for i in range(len(DataColumnsList)):
                DataString.append(DataColumnsList[i]+ " " + DataTypeList[i])
            
            elem= ",".join(DataString)
            CreateQuery = ("""CREATE TABLE """ + DataTableName + """(%s)"""%elem)

            if not os.path.isfile("CreationLog.txt"):
                f=open("CreationLog.txt","w")
            
            with open("CreationLog.txt","r+") as NewLog:
                OldLog=NewLog.read()
                NewLog.seek(0)
                NewLog.write(OldLog + "\nCreated on "+str(datetime.date.isoformat(datetime.datetime.now())) + " in '"+ ConnectionString + "' ,Used Query : "+ CreateQuery+"\n")
                
                
            if not os.path.exists(self.txtFileName.Value):
                os.makedirs(self.txtFileName.Value)
            else:
                wx.MessageBox("The Folder Already Exists, but you can add to it data tables!")
            
            cnn = sqlite3.connect(ConnectionString)
            cursor=cnn.cursor()
            cursor.execute(CreateQuery)
            cnn.commit
            cnn.close()
            
            self.txtDataFileOutput.Value=("A Data File Named "+self.txtDataName.Value+".db Was Created in "+ self.txtFileName.Value)
        
        except OSError:
            wx.MessageBox("The Grid Is Empty!")
        event.Skip()

    def clk_reset_grid(self, event):
        r=self.grid_1.GetNumberRows()
        
        for i in range(0,r):
            self.grid_1.DeleteRows(1,i)
        
        for c in range(0,2):
            self.grid_1.SetCellValue(0,c,"")
        
        self.txtFileName.Value=""
        self.txtDataName.Value=""
        self.txtDataTable.Value=""
        self.txtDataFileOutput.Value=""
        event.Skip()

if __name__ == "__main__":
    gettext.install("app")
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, wx.ID_ANY, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
