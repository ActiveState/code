# This is the emulating class.
class Function:
    def __init__(self):
        # Dummy function
        self.function = lambda *args:None

        self.menu = None
        self.button = None
        self.enabled = True

    # This method causes the Function instances to be
    # callable as though they were a function
    def __call__(self, *args):
        if self.enabled:
            return self.function(*args)

    def SetFunction(self, func):
        self.function = func

    def SetMenu(self, menu):
        self.menu = menu
        self.menu.Enable(self.enabled)

    def SetButton(self, btn):
        self.button = btn
        self.button.Enable(self.enabled)

    def Enable(self, on=True):
        if self.menu:
            self.menu.Enable(on)
        if self.button:
            self.button.Enable(on)
        self.enabled = on


class FUNCTION_TABLE:
    NewFile     = Function()
    OpenFile    = Function()
    SaveFile    = Function()

    Exit        = Function()

...
    # Initializing the main wx.Frame...

    item = wx.MenuItem( menu, id, "&Open", "Open a file" )

    # Note that OpenFile will act as an event handler, but at this
    # moment, no function has actually been assigned to handle the event
    self.Bind( wx.EVT_MENU, FUNCTION_TABLE.OpenFile, id=id )
    FUNCTION_TABLE.OpenFile.SetMenu( item )

...
    # Populating a wx.Panel (or similiar object) with controls, etc...

    button = wx.Button( self, id, "Open File" )
    button.Bind( wx.EVT_BUTTON, FUNCTION_TABLE.OpenFile )
    FUNCTION_TABLE.OpenFile.SetButton( button )

    # A function is finally assigned, but nobody is any the wiser.
    # My button and my menu are still going to call the same thing.
    # They don't know anything about self.OnOpenFile, nor do they 
    # need to.  They also don't know about each other!
    FUNCTION_TABLE.OpenFile.SetFunction( self.OnOpenFile )

...
    # An event handler method of the wx.Panel...

    def OnOpenFile(event):
        ...
