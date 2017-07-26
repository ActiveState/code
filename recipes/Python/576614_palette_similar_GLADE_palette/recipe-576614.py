import gtk
import xml.dom.minidom as minidom

class PaletteBox:
    class PaletteBoxItem:
        def __init__(self,num,icon,tooltip,size):
            self.num=num
            self.icon=icon
            self.tooltip=tooltip
            self.Item=gtk.RadioToolButton()
            self.Item.set_size_request(size,size)
        
    def __init__(self,title,items_size = 40):
        if items_size > 64 : items_size = 64
        if items_size < 16 : items_size = 16
        self.rowcount=-1
        self.item=[]
        self.items_size = items_size
        self.button = gtk.Button()
        self.button.set_focus_on_click(False)
        self.button.connect("clicked",self.hide_show_box)
        self.btnbox=gtk.HBox()
        self.btnlabel=gtk.Label("  " + title )
        self.btnarrow=gtk.Arrow(gtk.ARROW_DOWN,gtk.SHADOW_OUT)
        self.btnarrowx = gtk.ARROW_DOWN
        self.btnbox.pack_start(self.btnarrow,0,0)
        self.btnbox.pack_start(self.btnlabel,0,0)
        self.button.add(self.btnbox)
        self.hbl = gtk.HBox()
        self.itemsbox = gtk.Fixed()
        self.itemsbox.set_size_request(items_size, -1)
        self.itemsbox.connect("size-allocate",self.redraw_itemsbox)
        self.hbl.pack_start(self.itemsbox,1,1)
        self.box=gtk.VBox()
        self.box.pack_start(self.button,0,0)
        self.box.pack_start(self.hbl,1,1)
        
    def hide_show_box(self,widget):
        if self.btnarrowx == gtk.ARROW_DOWN:
            self.btnarrow.set(gtk.ARROW_RIGHT,gtk.SHADOW_OUT)
            self.hbl.set_property("visible",False)
            self.btnarrowx=gtk.ARROW_RIGHT
        elif self.btnarrowx == gtk.ARROW_RIGHT:
            self.btnarrow.set(gtk.ARROW_DOWN,gtk.SHADOW_OUT)
            self.hbl.set_property("visible",True)
            self.btnarrowx=gtk.ARROW_DOWN
            
    def set_title(self,title):
        try:
            self.button.set_label(title)
        except:
            print "PaletteBox.set_title(" + str(title) + ") is not string."
        
    def add_item(self,icon,tooltip,group=None):
        index = len(self.item)
        self.item.append(self.PaletteBoxItem(index,icon,tooltip,self.items_size))
        if(len(self.item) > 1):
            self.item[index].Item.set_group(self.item[0].Item)
        else:
            self.item[index].Item.set_group(group)
        self.item[index].Item.set_label(tooltip)
        self.itemsbox.add(self.item[index].Item)
        self.redraw_itemsbox(self,self.itemsbox)
    def redraw_itemsbox(self,widget,event = 0):
        width = self.itemsbox.get_allocation()[2]
        rowcount = width / self.items_size
        if(self.rowcount != rowcount):
            if rowcount<1 : rowcount = self.items_size
            colcount = len(self.item) / rowcount
            extra = len(self.item) % rowcount
            itemcounter = 0
            for i in range(colcount):
                for j in range(rowcount):
                    self.itemsbox.move(self.item[itemcounter].Item , j * self.items_size , i * self.items_size)
                    itemcounter += 1
            for j in range(extra):
                self.itemsbox.move(self.item[itemcounter].Item , j * self.items_size , colcount * self.items_size)
                itemcounter += 1
            self.rowcount = rowcount
class MakePaletteByXML:
    
    def __init__(self, xmlpath, parent = gtk.VBox()):
        try:
            self.parent = parent
            x=minidom.parse(xmlpath)
            for group in x.getElementsByTagName("group"):
                isnewgroup = True
                for box in group.getElementsByTagName("box"):
                    if (box.getAttribute("title")) : title = box.getAttribute("title")
                    else : title = "unknown"
                    mypalette = PaletteBox(title)
                    self.parent.pack_start(mypalette.box, 0)
                    for item in box.getElementsByTagName("item"):
                        icon = item.getAttribute("iconpath")
                        tooltip = item.getAttribute("tooltip")
                        if (isnewgroup) :
                            isnewgroup = False
                            mypalette.add_item(icon, tooltip, None)
                            itemgroup = mypalette.item[0].Item
                        else:
                            mypalette.add_item(icon, tooltip, itemgroup)
        except :
            print "on read a xml file occured a error ."
            print "please view a xml file and repir the xml file structure..."
w = gtk.Window()
w.set_size_request(500,500)
w.connect("destroy",gtk.main_quit)
p = gtk.HPaned()
group=pb1=PaletteBox("First Test")
pb1.add_item("1", "A")
pb1.add_item("2", "B")
pb1.add_item("3", "C")
pb1.add_item("4", "D")
pb1.add_item("5", "E")
pb1.add_item("6", "F")
pb1.add_item("7", "G")
pb1.add_item("8", "H")
pb1.add_item("9", "I")
pb1.add_item("10", "J")
pb2=PaletteBox("Last Test")
pb2.add_item("1", "A",pb1.item[0].Item)
pb2.add_item("2", "B",pb1.item[0].Item)
pb2.add_item("3", "C",pb1.item[0].Item)
pb2.add_item("4", "D",pb1.item[0].Item)
pb2.add_item("5", "E",pb1.item[0].Item)
pb2.add_item("6", "F",pb1.item[0].Item)
pb2.add_item("7", "G",pb1.item[0].Item)
pb2.add_item("8", "H",pb1.item[0].Item)
pb2.add_item("9", "I",pb1.item[0].Item)
pb2.add_item("10", "J",pb1.item[0].Item)
vbb=gtk.VBox()
vbb.pack_start(pb1.box,0)
vbb.pack_start(pb2.box,0)
p.pack1(vbb,0,0)
v=gtk.VBox()
v.add(p)
l=gtk.Layout()
p.pack2(l)
w.add(v)
w.show_all()
gtk.main()
