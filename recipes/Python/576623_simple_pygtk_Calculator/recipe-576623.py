import pygtk,math,string

pygtk.require('2.0')

import gtk

class mainwin():

    def __init__(self): #This function autorun at assign object to class >> "win=mainwin()"

        self.mwin=gtk.Window()

        self.mwin.set_size_request(300,270)

        self.mwin.set_resizable(False)

        self.mwin.set_title('Calculator')

        #=============== Create menu bar and popups ===============

        self.menus=(

        ("/_Calculator",None,None,0,"<Branch>"),

        ("/Calculator/_CE","<Control>C",self.ce,0,"<StockItem>",gtk.STOCK_CANCEL),

        ("/Calculator/C_lear","<Control>L",self.clear,0,"<StockItem>",gtk.STOCK_CLEAR),

        ("/Calculator/_Bksp","<Backspace>",self.bksp,0,"<StockItem>",gtk.STOCK_GO_BACK ),

        ("/Calculator/sep1",None,None,0,"<Separator>"),

        ("/Calculator/_Quit","<Control>Q",gtk.main_quit,0,"<StockItem>",gtk.STOCK_QUIT),

        )

        #======== Create map of buttons and clicked event =========

        ButtonsProp=(

        (("Bksp",self.bksp)       ,("Clear",self.clear)    ,("CE",self.ce)),

        (("7",self.calc_numbers)  ,("8",self.calc_numbers) ,("  9  ",self.calc_numbers) ,(" / " ,self.calc_operators),("sqrt",self.sqrt)),

        (("4" ,self.calc_numbers) ,("5",self.calc_numbers) ,("  6  ",self.calc_numbers) ,(" * ",self.calc_operators) ,("%" ,self.percent)),

        (("1",self.calc_numbers)  ,("2" ,self.calc_numbers),("  3  " ,self.calc_numbers),(" - ",self.calc_operators) ,("1/x",self.one_div_x)),

        (("0",self.calc_numbers)  ,("+/-",self.change_sign),(" . ",self.dot)            ,(" + " ,self.calc_operators),("=",self.do_equal))

        )

        #================ Create entry and buttons ================

        self.accelg=gtk.AccelGroup()

        itemfac=gtk.ItemFactory(gtk.MenuBar,"<main>")

        itemfac.create_items(self.menus)

        self.mwin.add_accel_group(self.accelg)

        self.itemfac=itemfac

        self.menubar=itemfac.get_widget("<main>")

        self.vb1=gtk.VBox(0,0)

        self.vb1.pack_start(self.menubar,0,0,0)

        self.mwin.add(self.vb1)

        self.mtext=gtk.Entry()

        self.mtext.set_text("0")

        self.mtext.set_editable(False)

        self.hb1=gtk.HBox()

        self.hb1.pack_start(self.mtext,1,1,4)

        self.vb1.pack_start(self.hb1,0,0,3)

        self.mtable=gtk.Table(4,3)

        self.mtable.set_row_spacings(3)

        self.mtable.set_col_spacings(3)

        x=y=0

        for i in ButtonsProp:

            for j in i:

                btn=gtk.Button(j[0])

                btn.connect("clicked",j[1])

                self.mtable.attach(btn,x,x+1,y,y+1)

                x+=1

                print  j[0] ,"   ",

            x=0

            y+=1

            print ""

        self.hb2=gtk.HBox()

        self.hb2.pack_start(self.mtable,1,1,4)

        self.vb1.pack_start(self.hb2,1,1,2)

        #============= set flags =============

        self.zero=True

        self.equal=False

        self.oldnum=0

        self.operator=""

        # {  The End  }

    def do_equal(self,widget):

        if self.oldnum != 0:

            if not self.equal: self.currentnum=string.atof(self.mtext.get_text())

            if self.operator==" / ":

                if self.currentnum==0: return 1

                self.mtext.set_text(str(self.oldnum/self.currentnum));self.oldnum=string.atof(self.mtext.get_text())

            elif self.operator==" * ":

                self.mtext.set_text(str(self.oldnum*self.currentnum));self.oldnum=string.atof(self.mtext.get_text())

            elif self.operator==" - ":

                self.mtext.set_text(str(self.oldnum-self.currentnum));self.oldnum=string.atof(self.mtext.get_text())

            elif self.operator==" + ":

                self.mtext.set_text(str(self.oldnum+self.currentnum));self.oldnum=string.atof(self.mtext.get_text())

        self.clear_dot_zero()

        self.equal=True

    def calc_numbers(self,widget):

        if self.zero==True :

            self.mtext.set_text("")

            self.zero=False

        if self.mtext.get_text()=="0": self.mtext.set_text("")

        self.mtext.set_text(self.mtext.get_text()+ str(string.atoi( widget.get_label())))

    def calc_operators(self,widget):

    	self.oldnum=string.atof(self.mtext.get_text())

        self.operator=widget.get_label()

        self.zero=True

        self.equal=False

    def change_sign(self,widget):

        self.mtext.set_text(str(string.atof(self.mtext.get_text())* -1))

        self.clear_dot_zero()

    def dot(self,widget):
        if self.zero==True :

            self.oldnum=string.atof(self.mtext.get_text())

            self.mtext.set_text("0")

            self.zero=False

        if string.find(self.mtext.get_text(),".")<=0:

            self.mtext.set_text(self.mtext.get_text()+".")

            self.zero=False

    def sqrt(self,widget):

        self.mtext.set_text(str(math.sqrt(string.atof(self.mtext.get_text()))))

        self.clear_dot_zero()

        self.zero=True

    def percent(self,widget):

        if (self.oldnum != 0)and(string.atof(self.mtext.get_text()) != 0):

            self.mtext.set_text(str(string.atof(self.mtext.get_text())*(self.oldnum*0.01)))

            self.clear_dot_zero()

    def one_div_x(self,widget):

        if string.atof(self.mtext.get_text()) != 0:

            self.mtext.set_text(str(1/string.atof(self.mtext.get_text())))

            self.clear_dot_zero()

            self.zero=True

    def bksp(self,widget,e=0):

        self.mtext.set_text(self.mtext.get_text()[0:-1])

        if self.mtext.get_text()=="":

            self.mtext.set_text("0")

            self.zero=True

    def clear(self,widget,e=0):

        self.mtext.set_text("0")

        self.zero=True

    def ce(self,widget,e=0):

        self.mtext.set_text("0")

        self.operator=""

        self.oldnum=0

        self.zero=True

    def clear_dot_zero(self):

        if self.mtext.get_text()[-2:]==".0":

            self.mtext.set_text(self.mtext.get_text()[0:-2])

    def main(self):

        self.mwin.connect("destroy",gtk.main_quit)

        self.mwin.show_all()

        gtk.main()

if __name__=='__main__':

    win=mainwin()

    win.main()
