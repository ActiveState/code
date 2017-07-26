"""wxView.py - a simple view for ZODB files

TODO:
    -Support ZEO
    -Rewrite/extend to use the builtin HTTP server a la pydoc
"""
import UserDict
import UserList
import locale
import os
import os.path
import sys

import wx

import ZODB
from   ZODB import FileStorage, DB
from persistent import Persistent
from BTrees.OOBTree import OOBTree
from persistent.list import PersistentList as PList
from persistent.mapping import PersistentMapping as PMap

def close_zodb(DataBase):
    """Closes the ZODB.

    This function MUST be called at the end of each program !!!
    See open_zodb() for a description of the argument.
    """
    get_transaction().abort()
    DataBase[1].close()
    DataBase[2].close()
    DataBase[3].close()
    return True

def open_zodb(Path):
    """Open ZODB.

    Returns a tuple consisting of:(root,connection,db,storage)
    The same tuple must be passed to close_zodb() in order to close the DB.
    """
    # Connect to DB
    storage     = FileStorage.FileStorage(Path)
    db          = DB(storage)
    connection  = db.open()
    root        = connection.root()
    return (root,connection,db,storage)

def save_pos(win, cfg):
    """Save a window position to the registry"""
    (xpos, ypos) = win.GetPositionTuple()
    (width, height) = win.GetSizeTuple()
    cfg.WriteInt('xpos', xpos)
    cfg.WriteInt('ypos', ypos)
    cfg.WriteInt('width', width)
    cfg.WriteInt('height', height)

def set_pos(win, cfg):
    """Restore a window to a position from the registry"""
    xpos = cfg.ReadInt('xpos', -1)
    ypos = cfg.ReadInt('ypos', -1)
    width = cfg.ReadInt('width', -1)
    height = cfg.ReadInt('height', -1)
    win.SetDimensions(xpos, ypos, width, height)

class ZODBFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ZODBFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.window_1 = wx.SplitterWindow(self, -1,
                                          style=wx.SP_3D|wx.SP_BORDER)
        self.panel_1 = wx.Panel(self.window_1, -1)
        self.window_1_pane_1 = wx.Panel(self.window_1, -1)

        # Menu Bar
        self.mb = wx.MenuBar()
        self.SetMenuBar(self.mb)
        self.mnuFile = wx.Menu()
        self.mnuOpen = wx.MenuItem(self.mnuFile, wx.ID_OPEN, "&Open\tCtrl-O",
                                   "", wx.ITEM_NORMAL)
        self.mnuFile.AppendItem(self.mnuOpen)
        self.mnuFile.Append(wx.ID_CLOSE, "&Close", "", wx.ITEM_NORMAL)
        self.mnuFile.AppendSeparator()
        self.mnuFile.Append(wx.ID_EXIT, "E&xit", "", wx.ITEM_NORMAL)
        self.mb.Append(self.mnuFile, "&File")
        # Menu Bar end
        self.sb = self.CreateStatusBar(1, wx.ST_SIZEGRIP)
        self.db_layout_tree = wx.TreeCtrl(self.window_1_pane_1, -1,
                                          style=wx.TR_HAS_BUTTONS|
                                                wx.TR_LINES_AT_ROOT|
                                                wx.TR_DEFAULT_STYLE|
                                                wx.SUNKEN_BORDER)
        self.label_1 = wx.StaticText(self.panel_1, -1, "Data Type:")
        self.txtType = wx.StaticText(self.panel_1, -1, "txtType")
        self.txtData = wx.TextCtrl(self.panel_1, -1, "", style=wx.TE_MULTILINE)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

        self.__create_image_list()
        self.__create_file_history()
        self.__set_window_position()
        self.__set_bindings()

        self.db = None
        self.root = None

    def __create_file_history(self):
        self.file_history = wx.FileHistory()
        self.file_history.UseMenu(self.mnuFile)
        old_path = self.wxcfg.GetPath()
        self.wxcfg.SetPath('/RecentFiles')
        self.file_history.Load(self.wxcfg)
        self.wxcfg.SetPath(old_path)
        self._need_save = False

    def __create_image_list(self):
        """Setup our image list for the tree control"""
        isz = (16, 16)
        il = wx.ImageList(*isz)
        self.folder_idx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,
                                wx.ART_OTHER, isz))
        self.folder_open_idx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,
                                wx.ART_OTHER, isz))
        self.file_idx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_REPORT_VIEW,
                                wx.ART_OTHER, isz))
        self.il = il

    def __set_bindings(self):
        self.Bind(wx.EVT_CLOSE, self.onExit)
        self.Bind(wx.EVT_MENU, self.onExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.doOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.doClose, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_MENU_RANGE, self.doFileHistory, id=wx.ID_FILE1,
                  id2=wx.ID_FILE9)

        self.db_layout_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelChange)

    def __set_properties(self):
        # begin wxGlade: ZODBFrame.__set_properties
        self.SetTitle("ZODB Viewer")
        self.sb.SetStatusWidths([-1])
        # statusbar fields
        sb_fields = [""]
        for i in range(len(sb_fields)):
            self.sb.SetStatusText(sb_fields[i], i)
        self.txtType.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD, 0,
                                     "Courier New"))
        self.txtData.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, 0,
                                     "Courier New"))
        # end wxGlade

    def __set_window_position(self):
        self.wxcfg = wx.Config()
        old_path = self.wxcfg.GetPath()
        self.wxcfg.SetPath('/Window Information')
        set_pos(self, self.wxcfg)
        self.wxcfg.SetPath(old_path)

    def __do_layout(self):
        # begin wxGlade: ZODBFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_2 = wx.FlexGridSizer(2, 1, 5, 0)
        grid_sizer_3 = wx.FlexGridSizer(1, 2, 0, 5)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.db_layout_tree, 1, wx.EXPAND, 0)
        self.window_1_pane_1.SetAutoLayout(True)
        self.window_1_pane_1.SetSizer(sizer_2)
        sizer_2.Fit(self.window_1_pane_1)
        sizer_2.SetSizeHints(self.window_1_pane_1)
        grid_sizer_3.Add(self.label_1, 0, wx.FIXED_MINSIZE, 0)
        grid_sizer_3.Add(self.txtType, 0, wx.FIXED_MINSIZE, 0)
        grid_sizer_3.AddGrowableCol(1)
        grid_sizer_2.Add(grid_sizer_3, 1, wx.EXPAND, 0)
        grid_sizer_2.Add(self.txtData, 0, wx.EXPAND|wx.FIXED_MINSIZE, 0)
        self.panel_1.SetAutoLayout(True)
        self.panel_1.SetSizer(grid_sizer_2)
        grid_sizer_2.Fit(self.panel_1)
        grid_sizer_2.SetSizeHints(self.panel_1)
        grid_sizer_2.AddGrowableRow(1)
        grid_sizer_2.AddGrowableCol(0)
        self.window_1.SplitVertically(self.window_1_pane_1, self.panel_1)
        sizer_1.Add(self.window_1, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()
        # end wxGlade

    def _set_child_icons(self, c, d):
        """Set the appropriate icons for a given tree child

        c
            The child we are updating

        d
            The data associated with the child
        """
        if isinstance(d, (dict, UserDict.UserDict, OOBTree)):
            self.db_layout_tree.SetItemImage(c,
                                             self.folder_idx,
                                             wx.TreeItemIcon_Normal)
            self.db_layout_tree.SetItemImage(c,
                                             self.folder_open_idx,
                                             wx.TreeItemIcon_Expanded)
        else:
            self.db_layout_tree.SetItemImage(c, self.file_idx,
                                                 wx.TreeItemIcon_Normal)

    def createTree(self, filename):
        """Create a new tree structure for when we open a file"""
        self.doClose()

        self.db = open_zodb(filename)
        self.db_layout_tree.SetImageList(self.il)

        self.root = self.db_layout_tree.AddRoot(os.path.basename(filename))
        self.db_layout_tree.SetPyData(self.root, self.db[0])
        self.db_layout_tree.SetItemImage(self.root, self.folder_idx,
                                         wx.TreeItemIcon_Normal)
        self.db_layout_tree.SetItemImage(self.root, self.folder_open_idx,
                                         wx.TreeItemIcon_Expanded)

        db = self.db[0]
        for key in db.keys():
            child = self.db_layout_tree.AppendItem(self.root, key)
            self.db_layout_tree.SetPyData(child, db[key])
            if isinstance(db[key], dict) or isinstance(db[key], list):
                self.db_layout_tree.SetItemImage(child, self.folder_idx,
                                                 wx.TreeItemIcon_Normal)
                self.db_layout_tree.SetItemImage(child, self.folder_open_idx,
                                                 wx.TreeItemIcon_Expanded)
            else:
                self.db_layout_tree.SetItemImage(child, self.file_idx,
                                                 wx.TreeItemIcon_Normal)

        self.db_layout_tree.Expand(self.root)

    def doClose(self, *event):
        """Close the current file and clear the screen"""
        if self.db:
            close_zodb(self.db)
            self.db = None
        if self.root:
            self.db_layout_tree.DeleteAllItems()
        self.txtType.SetLabel('')
        self.txtData.Clear()

    def doFileHistory(self, event):
        """Open a file from file history"""
        file_number = event.GetId() - wx.ID_FILE1
        filename = self.file_history.GetHistoryFile(file_number)
        self.createTree(filename)

    def doOpen(self, *event):
        """Open a file from the file system"""
        # Select and open the ZODB file object.
        dlg = wx.FileDialog(self, message="Choose a file",
            defaultFile="", style=wx.OPEN | wx.CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            filename = dlg.GetPath()
            self.createTree(filename)
            self.file_history.AddFileToHistory(filename)
        dlg.Destroy()

    def onExit(self, event):
        """Exit the program"""
        self.doClose()

        old_path = self.wxcfg.GetPath()
        self.wxcfg.SetPath('/RecentFiles')
        self.file_history.Save(self.wxcfg)
        self.wxcfg.SetPath(old_path)

        old_path = self.wxcfg.GetPath()
        self.wxcfg.SetPath('/Window Information')
        save_pos(self, self.wxcfg)
        self.wxcfg.SetPath(old_path)
        self.Destroy()

    def onSelChange(self, event):
        """Select a new tree node, loading it if needed"""
        item = event.GetItem()
        data = self.db_layout_tree.GetPyData(item)
        if isinstance(data, (dict, UserDict.UserDict, OOBTree)):
            self.txtData.Clear()
            self.txtType.SetLabel(str(type(data)))
            if hasattr(data, 'wx_str'):
                self.txtData.AppendText(data.wx_str())
            if not self.db_layout_tree.ItemHasChildren(item):
                keys = data.keys()
                try:
                    keys.sort()
                except AttributeError:
                    pass
                for key in keys:
                    child = self.db_layout_tree.AppendItem(item, str(key))
                    self.db_layout_tree.SetPyData(child, data[key])
                    self._set_child_icons(child, data[key])
        elif isinstance(data, (list, UserList.UserList)):
            self.txtData.Clear()
            self.txtType.SetLabel(str(type(data)))
            for d in data:
                self.txtData.AppendText(str(type(d)) + ' --\n')
                if hasattr(d, 'wx_str'):
                    self.txtData.AppendText(d.wx_str())
                else:
                    self.txtData.AppendText(str(d))
                self.txtData.AppendText('\n')
        else:
            self.txtType.SetLabel(str(type(data)))
            fmt = '%s\n-----\n%s'
            if hasattr(data, 'wx_str'):
                self.txtData.SetValue(data.wx_str())
            else:
                self.txtData.SetValue(str(data))

# end of class ZODBFrame


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')

    wxviewdb = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frmZODB = ZODBFrame(None, -1, "")
    wxviewdb.SetTopWindow(frmZODB)
    frmZODB.Show()
    wxviewdb.MainLoop()
