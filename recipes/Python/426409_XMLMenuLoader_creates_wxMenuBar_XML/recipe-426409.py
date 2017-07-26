"""
XMLMenuLoader: Class to handle loading a wxMenuBar with menu items
defined in XML

author:   Tom Jenkins <tjenkins@devis.com>
          based on code by Bjorn Pettersen <BPettersen@NAREX.com>

          20041010: Egor Zindy <ezindy@gmail.com> Code now uses pulldom, supports
          submenus and checkable items.

          #*COULDDO*# Add new XML definitions (menu images, greyed menus...)

          #*TODO*: refactor load into base class that handles loading the menu
          in another way so we can have ListMenuLoader, StreamMenuLoader, etc...
 
usage:
    self.menubar=wx.MenuBar()
    loader = XMLMenuLoader(MenuBar = self.menubar, controller=self)
    loader.load("menu.xml")
    self.SetMenuBar(self.menubar)
"""

import wx
from xml.dom import pulldom
  
class XMLMenuLoader:
    
    def __init__(self, MenuBar = None, controller = None):
        """Load the menubar with the menu items stored in XML format in
           the instance"s filename property
           wxMenuBar -> the root menubar of the frame; if given will become
           the instances new menubar property
           controller -> the class instance that will receive any callbacks
           stored in the menu items" callback attribute
        """
        self.MenuBar=MenuBar
        self.controller=controller

    def load(self,filename="menu.xml"):
        events = pulldom.parse(filename)
        self.parse(events)

    def loadString(self,xml_string):
        events = pulldom.parseString(xml_string)
        self.parse(events)

    def parse(self,events):
        #menu_list is used as a stack: the last element
        #is the parent menu to which items are appended.

        menu_list=[]
        menu_list.append(self.MenuBar)

        for (event,node) in events:
            if event=="START_ELEMENT" and node.nodeName=="menu":
                menu = wx.Menu()
                parent_menu=menu_list[-1]
                menu_name=node.getAttribute("name").replace("_", "&")

                if len(menu_list)==1:
                    parent_menu.Append(menu, menu_name)
                else:
                    parent_menu.AppendMenu(-1,menu_name,menu)

                menu_list.append(menu)

            elif event=="END_ELEMENT" and node.nodeName=="menu":
                #Encountered the end of a menu definition.
                #Remove the wx.menu from the stack.
                menu_list.pop(-1)

            elif event=="START_ELEMENT" and node.nodeName=="separator":
                #separator definition
                menu=menu_list[-1]
                menu.AppendSeparator()

            elif event=="START_ELEMENT" and node.nodeName=="menuitem":
                #the current menu
                menu=menu_list[-1]

                #checking all the attributes.

                #the menuitem name
                name=node.getAttribute("name").replace("_", "&")

                #if id is not defined, check for one available
                if node.hasAttribute("id"):
                    id=int(node.getAttribute("id"))
                else:
                    id = wx.NewId()

                #menuitem info attribute
                if node.hasAttribute("info"):
                    info=node.getAttribute("info")
                else:
                    info=""

                #callback
                if self.controller and node.hasAttribute("callback"):
                    callback=node.getAttribute("callback")
                    handler = getattr(self.controller, callback, None)
                    if handler:
                        wx.EVT_MENU(self.controller, id, handler)

                #checkable menu?
                if node.hasAttribute("chk"):
                    chk=int(node.getAttribute("chk"))
                    menu.AppendCheckItem(id,name,info)
                    menu.Check(id,chk)
                else:
                    menu.Append(id,name,info)

#----------------------------------------------------------------------
class MyFrame(wx.Frame):

    def __init__(self, parent, id, title,
        pos, size, style = wx.DEFAULT_FRAME_STYLE ):
                
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.CreateMyMenuBar()
        self.CreateStatusBar(1)

    def CreateMyMenuBar(self):
        self.mainmenu=wx.MenuBar()
        loader = XMLMenuLoader(MenuBar = self.mainmenu, controller=self)
        loader.loadString(xml_string)
        self.SetMenuBar(self.mainmenu)

    def OnChoice(self, event):
        id=event.GetId()
        menu_item=self.mainmenu.FindItemById(id)
        self.SetStatusText("item name: %s" % menu_item.GetLabel())


    def OnOptions(self, event):
        id=event.GetId()
        menu_item=self.mainmenu.FindItemById(id)
        is_checked=menu_item.IsChecked()

        if id==15000:
            my_str="apple"
        elif id==15001:
            my_str="pear"
        elif id==15002:
            my_str="orange"

        self.SetStatusText("item: %s | checked: %d" % (my_str,is_checked))

    def OnCloseWindow(self, event):
        self.Destroy()

def main(argv=None):
    app = wx.PySimpleApp()
    f = MyFrame(None, -1, "XMLMenuLoader: XML menu creation", wx.Point(20,20), wx.Size(400,300) )
    f.Show()
    app.MainLoop()

#----------------------------------------------------------------------
if __name__ == "__main__":

    global xml_string
    xml_string="""
    <menubar>
        <menu name='_File'>
            <menuitem name='_New' callback='OnChoice'/>
            <menuitem name='_Open...' callback='OnChoice'/>
            <menu name='_Export to'>
                <menuitem name='Jpeg...' callback='OnChoice'/>
                <menuitem name='Png...' callback='OnChoice'/>
            </menu>
            <separator/>
            <menuitem name='E_xit' callback='OnCloseWindow'/>
        </menu>
        <menu name='_Edit'>
            <menuitem name='Undo' callback='OnChoice'/>
            <menuitem name='Redo' callback='OnChoice'/>
        </menu>
        <menu name='_Checkable'>
            <menuitem id='15000' name='Item 1' callback='OnOptions' chk='1'/>
            <menuitem id='15001' name='Item 2' callback='OnOptions' chk='0'/>
            <menuitem id='15002' name='Item 3' callback='OnOptions' chk='0'/>
        </menu>
        <menu name='_Help'>
            <menuitem name='About...' info='Read more about it' callback='OnAbout'/>
        </menu>
    </menubar>"""
    
    main()
    
