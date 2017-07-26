from threading import Thread
from time import sleep
from PythonCard import model
import urllib
import re


def get_quote(symbol):
        global quote
        base_url = 'http://finance.google.com/finance?q='
        content = urllib.urlopen(base_url + symbol).read()
        m = re.search('class="pr".*?>(.*?)<', content)
        if m:
            quote = m.group(1)
        else:
            quote = 'N/A'
        return quote

def get_change(symbol):
    global change
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('class="chg".*?>(.*?)<', content)
    if m:
        change = m.group(1)
    else:
        change = 'N/A'
    return change

def get_open(symbol):
    global opens
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('".*?op".*?>(.*?)<', content)
    if m:
        opens = m.group(1)
    else:
        opens = 'N/A'
    return opens

def get_high(symbol):
    global high
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('".*?hi".*?>(.*?)<', content)
    if m:
        high = m.group(1)
    else:
        high = 'N/A'
    return high

def get_high52(symbol):
    global high52
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('".*?hi52".*?>(.*?)<', content)
    if m:
        high52 = m.group(1)
    else:
        high52 = 'N/A'
    return high52

def get_low(symbol):
    global low
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('".*?lo".*?>(.*?)<', content)
    if m:
        low = m.group(1)
    else:
        low = 'N/A'
    return low

def get_vol(symbol):
    global vol
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('".*?vo".*?>(.*?)<', content)
    if m:
        vol = m.group(1)
    else:
        vol = 'N/A'
    return vol

def get_mc(symbol):
    global mc
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('".*?mc".*?>(.*?)<', content)
    if m:
        mc = m.group(1)
    else:
        mc = 'N/A'
    return mc

def get_lo52(symbol):
    global lo52
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('".*?lo52".*?>(.*?)<', content)
    if m:
        lo52 = m.group(1)
    else:
        lo52 = 'N/A'
    return lo52

def get_pe(symbol):
    global pe
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('".*?lo52".*?>(.*?)<', content)
    if m:
        pe = m.group(1)
    else:
        pe = 'N/A'
    return pe

def get_beta(symbol):
    global beta
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('".*?beta".*?>(.*?)<', content)
    if m:
        beta = m.group(1)
    else:
        beta = 'N/A'
    return beta

def get_div(symbol):
    global div
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('".*?div".*?>(.*?)<', content)
    if m:
        div = m.group(1)
    else:
        div = 'N/A'
    return div

def get_yield(symbol):
    global yield1
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('".*?yield".*?>(.*?)<', content)
    if m:
        yield1 = m.group(1)
    else:
        yield1 = N/A
    return yield1

def get_shares(symbol):
    global shares
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('".*?shares".*?>(.*?)<', content)
    if m:
        shares = m.group(1)
    else:
        shares = N/A
    return shares

def get_own(symbol):
    global own
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()
    m = re.search('".*?own".*?>(.*?)<', content)
    if m:
        own = m.group(1)
    else:
        own = N/A
    return own

class stock(model.Background):

    def on_getQuote_mouseClick(self, event):
        global symbol
        symbol = self.components.quotese.text
        class Repeater(Thread):
                def __init__(self,interval,fun,*args,**kw):
                        Thread.__init__(self)
                        self.interval=interval
                        self.fun=fun
                        self.args=args
                        self.kw=kw
                        self.keep_going=True

                def run(self):
                       while(self.keep_going):
                            sleep(self.interval)
                            self.fun(*self.args,**self.kw)

    

        def Refresh(*a):
                get_quote(symbol)
                get_change(symbol)
                self.components.current.text = quote
                self.components.change.text = change
                
        r=Repeater(1.0, Refresh)
        r.start()
        


    def on_stockinfo_mouseClick(self, event):
        global symbol
        symbol = self.components.quotese.text
        get_open(symbol)
        get_high(symbol)
        get_high52(symbol)
        get_low(symbol)
        get_vol(symbol)
        get_mc(symbol)
        get_lo52(symbol)
        get_pe(symbol)
        get_beta(symbol)
        get_div(symbol)
        get_yield(symbol)
        get_shares(symbol)
        get_own(symbol)
        self.components.inst.text = own
        self.components.shares.text = shares
        self.components.yield1.text = yield1
        self.components.div.text = div
        self.components.beta.text = beta
        self.components.pe.text = pe
        self.components.lo52.text = lo52
        self.components.mkt.text = mc
        self.components.vol.text = vol
        self.components.opens.text = opens
        self.components.high.text = high
        self.components.hi52.text = high52
        self.components.low.text = low

    def on_save_mouseClick(self, event):
        stock1 = open('stock1.txt', 'w')
        stock1.write(self.components.stock1.text)
        stock1.close()
        stock2 = open('stock2.txt', 'w')
        stock2.write(self.components.stock2.text)
        stock2.close()
        stock3 = open('stock3.txt', 'w')
        stock3.write(self.components.stock3.text)
        stock3.close()
        stock4 = open('stock4.txt', 'w')
        stock4.write(self.components.stock4.text)
        stock4.close()

    def on_load_mouseClick(self, event):
        load1 = open('stock1.txt' , 'r').read()
        self.components.stock1.text = load1
        
        load2 = open('stock2.txt' , 'r').read()
        self.components.stock2.text = load2
        
        load3 = open('stock3.txt' , 'r').read()
        self.components.stock3.text = load3
        
        load4 = open('stock4.txt' , 'r').read()
        self.components.stock4.text = load4

    def on_update_mouseClick(self, event):
        symbol = self.components.stock1.text
        get_quote(symbol)
        self.components.change1.text = quote

        symbol = self.components.stock2.text
        get_quote(symbol)
        self.components.change2.text = quote

        symbol = self.components.stock3.text
        get_quote(symbol)
        self.components.change3.text = quote

        symbol = self.components.stock4.text
        get_quote(symbol)
        self.components.change4.text = quote
        
    def on_clear_mouseClick(self, event):
        self.components.stock1.text = ""
        self.components.stock2.text = ""
        self.components.stock3.text = ""
        self.components.stock4.text = ""
        self.components.change1.text = ""
        self.components.change2.text = ""
        self.components.change3.text = ""
        self.components.change4.text = ""

if __name__ == '__main__':
    app = model.Application(stock)
    app.MainLoop()


_______________________________________________________________________________

save following as stock.rsrc.py

{'application':{'type':'Application',
          'name':'Template',
    'backgrounds': [
    {'type':'Background',
          'name':'bgTemplate',
          'title':'Standard Template with File->Exit menu',
          'size':(711, 634),
          'style':['resizeable'],

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': [
                  {'type':'MenuItem',
                   'name':'save',
                   'label':u'Save',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit',
                   'command':'exit',
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'Button', 
    'name':'clear', 
    'position':(333, 555), 
    'label':u'Clear', 
    },

{'type':'Button', 
    'name':'save', 
    'position':(523, 444), 
    'size':(117, -1), 
    'label':u'Save', 
    },

{'type':'StaticText', 
    'name':'statictext10', 
    'position':(40, 510), 
    'font':{'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 12}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':u'Update to show price', 
    },

{'type':'Button', 
    'name':'load', 
    'position':(523, 420), 
    'size':(117, -1), 
    'label':u'Load', 
    },

{'type':'StaticText', 
    'name':'StaticText5', 
    'position':(26, 488), 
    'font':{'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 12}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':u'Or load to load previous', 
    },

{'type':'Button', 
    'name':'update', 
    'position':(522, 470), 
    'size':(120, 80), 
    'font':{'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 11}, 
    'label':u'Update', 
    },

{'type':'StaticText', 
    'name':'StaticText4', 
    'position':(31, 465), 
    'font':{'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 12}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':u'Then click save to save', 
    },

{'type':'StaticText', 
    'name':'StaticText3', 
    'position':(10, 445), 
    'font':{'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 12}, 
    'foregroundColor':(0, 0, 160, 255), 
    'text':u'Enter name of stocks to monitor', 
    },

{'type':'StaticBox', 
    'name':'StaticBox1', 
    'position':(343, 109), 
    'size':(349, 242), 
    },

{'type':'StaticLine', 
    'name':'StaticLine1', 
    'position':(2, 400), 
    'size':(697, -1), 
    'layout':'horizontal', 
    },

{'type':'StaticText', 
    'name':'StaticText2', 
    'position':(395, 414), 
    'text':u'Current Price', 
    },

{'type':'StaticText', 
    'name':'StaticText1', 
    'position':(268, 414), 
    'text':u'Name Of Stock', 
    },

{'type':'TextField', 
    'name':'change4', 
    'position':(378, 530), 
    'editable':False, 
    },

{'type':'TextField', 
    'name':'stock4', 
    'position':(258, 530), 
    },

{'type':'TextField', 
    'name':'change3', 
    'position':(378, 500), 
    'editable':False, 
    },

{'type':'TextField', 
    'name':'stock3', 
    'position':(258, 500), 
    },

{'type':'TextField', 
    'name':'change2', 
    'position':(378, 471), 
    'editable':False, 
    },

{'type':'TextField', 
    'name':'stock2', 
    'position':(258, 470), 
    },

{'type':'TextField', 
    'name':'change1', 
    'position':(378, 440), 
    'editable':False, 
    },

{'type':'TextField', 
    'name':'stock1', 
    'position':(258, 440), 
    },

{'type':'Button', 
    'name':'stockinfo', 
    'position':(170, 92), 
    'label':u'Get Info', 
    },

{'type':'HtmlWindow', 
    'name':'HtmlWindow1', 
    'position':(348, 120), 
    'size':(339, 225), 
    'backgroundColor':(255, 255, 255, 255), 
    'text':u'tickers.html', 
    },

{'type':'StaticText', 
    'name':'stockCheckversion', 
    'position':(213, 0), 
    'font':{'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 36}, 
    'foregroundColor':(255, 128, 0, 255), 
    'text':u'Stock Check V2.0', 
    },

{'type':'StaticText', 
    'name':'Changelbl', 
    'position':(14, 84), 
    'foregroundColor':(128, 0, 0, 255), 
    'text':u'Change', 
    },

{'type':'TextField', 
    'name':'change', 
    'position':(53, 74), 
    'size':(-1, 21), 
    'border':'none', 
    'editable':False, 
    'font':{'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 10}, 
    'foregroundColor':(128, 0, 0, 255), 
    },

{'type':'TextField', 
    'name':'current', 
    'position':(12, 33), 
    'size':(194, 33), 
    'border':'none', 
    'editable':False, 
    'font':{'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 24}, 
    'foregroundColor':(0, 128, 0, 255), 
    },

{'type':'StaticText', 
    'name':'Currentlbl', 
    'position':(81, 10), 
    'font':{'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 18}, 
    'foregroundColor':(0, 128, 0, 255), 
    'text':u'Current', 
    },

{'type':'StaticText', 
    'name':'wkLowlbl', 
    'position':(8, 364), 
    'text':u'52Wk Low', 
    },

{'type':'StaticText', 
    'name':'instOwnlbl', 
    'position':(183, 325), 
    'text':u'Inst. Own', 
    },

{'type':'StaticText', 
    'name':'Shareslbl', 
    'position':(186, 284), 
    'text':u'Shares', 
    },

{'type':'StaticText', 
    'name':'PElbl', 
    'position':(193, 124), 
    'text':u'P/E', 
    },

{'type':'StaticText', 
    'name':'Openlbl', 
    'position':(12, 124), 
    'text':u'Open', 
    },

{'type':'StaticText', 
    'name':'Highlbl', 
    'position':(16, 164), 
    'text':u'High', 
    },

{'type':'TextField', 
    'name':'pe', 
    'position':(260, 120), 
    'size':(81, -1), 
    'editable':False, 
    },

{'type':'TextField', 
    'name':'opens', 
    'position':(80, 120), 
    'size':(81, -1), 
    'editable':False, 
    },

{'type':'TextField', 
    'name':'high', 
    'position':(80, 160), 
    'size':(80, -1), 
    'editable':False, 
    },

{'type':'TextField', 
    'name':'inst', 
    'position':(260, 320), 
    'size':(81, -1), 
    'editable':False, 
    },

{'type':'TextField', 
    'name':'shares', 
    'position':(260, 280), 
    'size':(81, -1), 
    'editable':False, 
    },

{'type':'StaticText', 
    'name':'Yieldlbl', 
    'position':(191, 244), 
    'text':u'Yield', 
    },

{'type':'StaticText', 
    'name':'Dividendlbl', 
    'position':(183, 163), 
    'text':u'Dividend', 
    },

{'type':'TextField', 
    'name':'lo52', 
    'position':(80, 360), 
    'size':(81, -1), 
    'editable':False, 
    },

{'type':'TextField', 
    'name':'yield1', 
    'position':(260, 240), 
    'size':(81, -1), 
    'editable':False, 
    },

{'type':'TextField', 
    'name':'div', 
    'position':(260, 160), 
    'size':(81, -1), 
    'editable':False, 
    },

{'type':'StaticText', 
    'name':'Betalbl', 
    'position':(193, 204), 
    'text':u'Beta', 
    },

{'type':'TextField', 
    'name':'beta', 
    'position':(260, 200), 
    'size':(81, -1), 
    'editable':False, 
    },

{'type':'StaticText', 
    'name':'wkHighlbl', 
    'position':(6, 323), 
    'text':u'52Wk High', 
    },

{'type':'TextField', 
    'name':'hi52', 
    'position':(80, 320), 
    'size':(80, -1), 
    'editable':False, 
    },

{'type':'StaticText', 
    'name':'mktCaplbl', 
    'position':(11, 283), 
    'size':(-1, 16), 
    'text':u'Mkt Cap', 
    },

{'type':'TextField', 
    'name':'mkt', 
    'position':(80, 280), 
    'size':(80, -1), 
    'editable':False, 
    },

{'type':'StaticText', 
    'name':'Vollbl', 
    'position':(19, 244), 
    'text':u'Vol', 
    },

{'type':'StaticText', 
    'name':'Lowlbl', 
    'position':(16, 204), 
    'text':u'Low', 
    },

{'type':'TextField', 
    'name':'vol', 
    'position':(80, 240), 
    'size':(80, -1), 
    'editable':False, 
    },

{'type':'TextField', 
    'name':'low', 
    'position':(80, 200), 
    'size':(80, -1), 
    'editable':False, 
    },

{'type':'Button', 
    'name':'getQuote', 
    'position':(313, 63), 
    'label':u'Get Quote', 
    },

{'type':'TextField', 
    'name':'quotese', 
    'position':(209, 64), 
    },

] # end components
} # end background
] # end backgrounds
} }
