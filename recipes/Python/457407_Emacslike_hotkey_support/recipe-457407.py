'''
multi_hotkey.py

A few simple methods which implement multiple hotkey support for emacs-like
hotkey sequences.

Feel free to use this code as you desire, though please cite the source.

Josiah carlson
http://come.to/josiah
'''

import wx
import time

keyMap = {}

def gen_keymap():
    keys = ("BACK", "TAB", "RETURN", "ESCAPE", "SPACE", "DELETE", "START",
        "LBUTTON", "RBUTTON", "CANCEL", "MBUTTON", "CLEAR", "PAUSE",
        "CAPITAL", "PRIOR", "NEXT", "END", "HOME", "LEFT", "UP", "RIGHT",
        "DOWN", "SELECT", "PRINT", "EXECUTE", "SNAPSHOT", "INSERT", "HELP",
        "NUMPAD0", "NUMPAD1", "NUMPAD2", "NUMPAD3", "NUMPAD4", "NUMPAD5",
        "NUMPAD6", "NUMPAD7", "NUMPAD8", "NUMPAD9", "MULTIPLY", "ADD",
        "SEPARATOR", "SUBTRACT", "DECIMAL", "DIVIDE", "F1", "F2", "F3", "F4",
        "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "F14",
        "F15", "F16", "F17", "F18", "F19", "F20", "F21", "F22", "F23", "F24",
        "NUMLOCK", "SCROLL", "PAGEUP", "PAGEDOWN", "NUMPAD_SPACE",
        "NUMPAD_TAB", "NUMPAD_ENTER", "NUMPAD_F1", "NUMPAD_F2", "NUMPAD_F3",
        "NUMPAD_F4", "NUMPAD_HOME", "NUMPAD_LEFT", "NUMPAD_UP",
        "NUMPAD_RIGHT", "NUMPAD_DOWN", "NUMPAD_PRIOR", "NUMPAD_PAGEUP",
        "NUMPAD_NEXT", "NUMPAD_PAGEDOWN", "NUMPAD_END", "NUMPAD_BEGIN",
        "NUMPAD_INSERT", "NUMPAD_DELETE", "NUMPAD_EQUAL", "NUMPAD_MULTIPLY",
        "NUMPAD_ADD", "NUMPAD_SEPARATOR", "NUMPAD_SUBTRACT", "NUMPAD_DECIMAL",
        "NUMPAD_DIVIDE")
    
    for i in keys:
        keyMap[getattr(wx, "WXK_"+i)] = i
    for i in ("SHIFT", "ALT", "CONTROL", "MENU"):
        keyMap[getattr(wx, "WXK_"+i)] = ''

def GetKeyPress(evt):
    keycode = evt.GetKeyCode()
    keyname = keyMap.get(keycode, None)
    modifiers = ""
    for mod, ch in ((evt.ControlDown(), 'Ctrl+'),
                    (evt.AltDown(),     'Alt+'),
                    (evt.ShiftDown(),   'Shift+'),
                    (evt.MetaDown(),    'Meta+')):
        if mod:
            modifiers += ch

    if keyname is None:
        if 27 < keycode < 256:
            keyname = chr(keycode)
        else:
            keyname = "(%s)unknown" % keycode
    return modifiers + keyname

def _spl(st):
    if '\t' in st:
        return st.split('\t', 1)
    return st, ''

class StatusUpdater:
    def __init__(self, frame, message):
        self.frame = frame
        self.message = message
    def __call__(self, evt):
        self.frame.SetStatusText(self.message)

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "test")
        self.CreateStatusBar()
        ctrl = self.ctrl = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE|wx.WANTS_CHARS|wx.TE_RICH2)
        ctrl.SetFocus()
        ctrl.Bind(wx.EVT_KEY_DOWN, self.KeyPressed, ctrl)
        
        self.lookup = {}
        
        menuBar = wx.MenuBar()
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.menuBar = menuBar
        
        testmenu = wx.Menu()
        self.menuAddM(menuBar, testmenu, "TestMenu", "help")
        self.menuAdd(testmenu, "testitem\tCtrl+Y\tAlt+3\tShift+B", "testdesc", StatusUpdater(self, "hello!"))
        
        print self.lookup
        
        self._reset()
        self.Show(1)
    
    def addHotkey(self, acc, fcn):
        hotkeys = self.lookup
        x = [i for i in acc.split('\t') if i]
        x = [(i, j==len(x)-1) for j,i in enumerate(x)]
        for name, last in x:
            if last:
                if name in hotkeys:
                    raise Exception("Some other hotkey shares a prefix with this hotkey: %s"%acc)
                hotkeys[name] = fcn
            else:
                if name in hotkeys:
                    if not isinstance(hotkeys[name], dict):
                        raise Exception("Some other hotkey shares a prefix with this hotkey: %s"%acc)
                else:
                    hotkeys[name] = {}
                hotkeys = hotkeys[name]

    def menuAdd(self, menu, name, desc, fcn, id=-1, kind=wx.ITEM_NORMAL):
        if id == -1:
            id = wx.NewId()
        a = wx.MenuItem(menu, id, 'TEMPORARYNAME', desc, kind)
        menu.AppendItem(a)
        wx.EVT_MENU(self, id, fcn)
        ns, acc = _spl(name)
        
        if acc:
            self.addHotkey(acc, fcn)
        
        menu.SetLabel(id, '%s\t%s'%(ns, acc.replace('\t', ' ')))
        menu.SetHelpString(id, desc)

    def menuAddM(self, parent, menu, name, help=''):
        if isinstance(parent, wx.Menu) or isinstance(parent, wx.MenuPtr):
            id = wx.NewId()
            parent.AppendMenu(id, "TEMPORARYNAME", menu, help)

            self.menuBar.SetLabel(id, name)
            self.menuBar.SetHelpString(id, help)
        else:
            parent.Append(menu, name)

    def _reset(self):
        self.sofar = ''
        self.cur = self.lookup
        self.SetStatusText('')
    
    def _add(self, key):
        self.cur = self.cur[key]
        self.sofar += ' ' + key
        self.SetStatusText(self.sofar)

    def KeyPressed(self, evt):
        key = GetKeyPress(evt)
        print key
        
        if key == 'ESCAPE':
            self._reset()
        elif key.endswith('+') and len(key) > 1 and not key.endswith('++'):
            #only modifiers
            evt.Skip()
        elif key in self.cur:
            self._add(key)
            if not isinstance(self.cur, dict):
                sc = self.cur
                self._reset()
                sc(evt)
        elif self.cur is not self.lookup:
            sf = "%s %s  <- Unknown sequence"%(self.sofar, key)
            self._reset()
            self.SetStatusText(sf)
        else:
            evt.Skip()

if __name__ == '__main__':
    gen_keymap()
    app = wx.PySimpleApp()
    frame = MainFrame()
    app.MainLoop()
