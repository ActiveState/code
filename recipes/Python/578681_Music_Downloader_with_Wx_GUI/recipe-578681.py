import wx
from wxPython.wx import *
import sys
import threading
import urllib, urllib2
import cookielib
from bs4 import BeautifulSoup as BS
import  cStringIO


class Get_file():
    
    def get_url(self, query):
        site1 = urllib.urlopen('http://www.youtube.com/results?search_query=%s'%query)
        html = site1.read()
        soup = BS(html)

        links = soup.findAll('a')
        vidlinks = [link.get('href') for link in links if link.get('href') is not None]
        vlink = [ i for i in vidlinks if '/watch?v=' in i][0]
        
        img_link = soup.findAll('img',{'alt':'Thumbnail', 'width':'185'})[0].get('src')
        img_url =  'http:%s' %img_link

        imagethread = threading.Thread(target=lambda:urllib.urlretrieve(img_url, 'Files\image.jpg'))
        imagethread.start()
        
        return vlink

    def get_file(self, url, quality):

        self.cookieJar = cookielib.LWPCookieJar()

        self.opener = urllib2.build_opener(
            
            urllib2.HTTPCookieProcessor(self.cookieJar),
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0))
            
        self.opener.addheaders = [('User-agent', "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36")]


        forms = {"youtubeURL": url,
                 'quality':quality
                 
                 }
                
        data = urllib.urlencode(forms)
        req = urllib2.Request('http://www.convertmemp3.com/',data)
        res = self.opener.open(req)

        self.convhtml = res.read()
        
    def download_file(self, html, name):
        
        try:
            soup = BS(html)
            links = soup.findAll('a')
            dllink = [link.get('href') for link in links][7]
            
            dlpage = urllib.urlopen("http://www.convertmemp3.com%s"%(dllink)).read()
            soup = BS(dlpage)
            download = [lnk.get('href') for lnk in soup.findAll('a')][7]
            urllib.urlretrieve("http://www.convertmemp3.com%s"%(download),"%s.mp3"%name)
            
        except urllib2.HTTPError, error:
            log.Error('Cant download file')
            
class GUI(wx.Frame):
    def __init__(self, parent, id, title):

        with open('Files\dir.txt','r') as dirtxt:
            self.new_path = dirtxt.read()
            
        wx.Frame.__init__(self, parent, id, title, size=(500, 500))

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_PREFERENCES,'Change Download Directory', 'Change Dl Dir')
        fitem2 = fileMenu.Append(wx.ID_HELP,'Information/Help', 'Info')
        fitem3 = fileMenu.Append(wx.ID_EXIT,'Exit', 'Quit application')
        menubar.Append(fileMenu, '&Options')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.get_Dir, fitem)
        self.Bind(wx.EVT_MENU, self.Info, fitem2)
        self.Bind(wx.EVT_MENU, self.Exit, fitem3)
        

        self.retreive_range = 10
        self.convert_range = 10
        self.download_range = 10

        self.timer1 = wx.Timer(self, 1)
        self.timer2 = wx.Timer(self, 1)
        self.timer3 = wx.Timer(self, 1)
        
        self.count = 0
        self.count2 = 0
        self.count3 = 0
        
        self.getfile = Get_file()

        self.Bind(wx.EVT_TIMER, self.OnTimer1, self.timer1)
        
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('#000000')

        
        mfont = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Impact')
        sfont = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Impact')

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self.panel, label='Song Title and Artist')
        st1.SetFont(mfont)
        st1.SetForegroundColour('#FFFFFF')
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        self.tc = wx.TextCtrl(self.panel, 1, '')
        self.tc.SetFont(sfont)
        hbox1.Add(self.tc, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        namelbl = wx.StaticText(self.panel, label='Filename (optional)  ')
        namelbl.SetForegroundColour("#FFFFFF")
        hbox2.Add(namelbl,flag=wx.LEFT)
        self.nametc = wx.TextCtrl(self.panel)
        hbox2.Add(self.nametc)
        
        self.rb1 = wx.RadioButton(self.panel, label='', 
            style=wx.RB_GROUP)
        rb1text = wx.StaticText(self.panel, label='   High Quality (Slower) ')
        self.rb2 = wx.RadioButton(self.panel, label='')
        rb2text = wx.StaticText(self.panel, label='   Medium Quality ')
        
        hbox2.Add(rb1text)
        hbox2.Add(self.rb1)
        hbox2.Add(rb2text)
        hbox2.Add(self.rb2)
        
        rb1text.SetForegroundColour('#FFFFFF')
        rb2text.SetForegroundColour('#FFFFFF')
        
        vbox.Add(hbox2, flag=wx.LEFT|wx.TOP, border=8)
        
        vbox.Add((-1, 10))

        con = wx.Button(self.panel, label='Convert!', size=(200,25))
        self.Bind(wx.EVT_BUTTON, self.retrieve, con)
        
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        con.SetFont(mfont)
        hbox3.Add(con)
        vbox.Add(hbox3, flag=wx.CENTER|wx.TOP, border=8)
        
        vbox.Add((-1, 10))

        lbox1 = wx.BoxSizer(wx.HORIZONTAL)
        sline1 = wx.StaticLine(self.panel)
        lbox1.Add(sline1, proportion = 1)
        vbox.Add(lbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        vbox.Add((-1, 10))
        
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.gauge = wx.Gauge(self.panel, range=10, size=(300, 25))
        self.text = wx.StaticText(self.panel, label='Ready!')
        self.text.SetForegroundColour('#FFFFFF')
        self.text.SetFont(mfont)
        hbox4.Add(self.text, wx.ALIGN_RIGHT)
        hbox4.Add(self.gauge, wx.ALIGN_LEFT)
        vbox.Add(hbox4, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=15)
        
        vbox.Add((-1, 10))

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.dltext = wx.StaticText(self.panel, label='')
        self.dltext.SetFont(mfont)
        self.dltext.SetForegroundColour('#FFFFFF')

        hbox5.Add(self.dltext,wx.CENTER)

        vbox.Add(hbox5, flag=wx.CENTER|wx.TOP, border=10)

        vbox.Add((-1, 10))
        
        self.panel.SetSizer(vbox)

        self.Show()
        self.Centre()
        
    def Error(self, dialog):
        wx.MessageBox(dialog , 'Info', 
            wx.OK | wx.ICON_INFORMATION)
        
    def get_Dir(self, e):
        dialog = wxDirDialog ( None, message = 'Pick a directory.', style = wxDD_NEW_DIR_BUTTON )

        if dialog.ShowModal() == wxID_OK:
            self.new_path = dialog.GetPath()
            with open('Files\dir.txt','w') as dirtxt:
                dirtxt.write(self.new_path + '\\')
                
        dialog.Destroy()

    def retrieve(self, e):
        self.timer1.Start(100)
        self.text.SetLabel('Retrieving URL...')
        self.query = self.tc.GetValue()
        self.vidurl = self.getfile.get_url(self.query)
        
    def convert(self):
        self.Bind(wx.EVT_TIMER, self.OnTimer2, self.timer2)
        self.dltext.SetLabel(self.query)
        self.panel.Layout()
        imageFile = 'Files\image.jpg'
        
        data = open(imageFile, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        # convert to a bitmap
        bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        # show the bitmap, (5, 5) are upper left corner coordinates
        thumb = wx.StaticBitmap(self, -1, bmp, (90,255))
        
        self.Hide()
        self.Show()
        
        self.text.SetLabel('Converting...')
        if self.rb1.GetValue() == True:
            self.timer2.Start(1000)
            worker1 = threading.Thread(target=lambda: self.getfile.get_file('http://www.youtube.com/%s'%self.vidurl, '320'))
            worker1.start()
            
        elif self.rb2.GetValue() == True:
            self.timer2.Start(600)
            worker1 = threading.Thread(target=lambda: self.getfile.get_file('http://www.youtube.com/%s'%self.vidurl, '128'))
            worker1.start()
        
    def download(self):
        self.Bind(wx.EVT_TIMER, self.OnTimer3, self.timer3)
        self.timer3.Start(1600)
        self.text.SetLabel('Downloading...')
        self.filename = self.nametc.GetValue()
        file_name = self.new_path + self.filename
        try:
            worker2 = threading.Thread(target=lambda: self.getfile.download_file(self.getfile.convhtml, file_name  ))
            worker2.start()
        except:
            self.Error("Error on conversion! Please retry")
            self.reset()
        
        
    def OnTimer1(self, e):
        self.count = self.count + 1
        self.gauge.SetValue(self.count)
        
        if self.count == self.retreive_range:
            self.timer1.Stop()
            self.text.SetLabel('Url Retreived!')
            self.convert()
            
    def OnTimer2(self, e):
        if self.rb1.GetValue() == True:
            self.count2 = self.count2 + 0.5
            self.gauge.SetValue(self.count2)
            
        elif self.rb2.GetValue() == True:
            self.count2 = self.count2 + 1
            self.gauge.SetValue(self.count2)
        
        if self.count2 == self.convert_range:
            self.timer2.Stop()
            self.text.SetLabel('Converted!')
            self.download()
            
    def OnTimer3(self, e):
        self.count3 = self.count3 + 0.5
        self.gauge.SetValue(self.count3)
        
        
        if self.count3 == self.download_range:
            self.timer3.Stop()
            self.text.SetLabel('Downloaded!')
            self.gauge.SetValue(0)
            self.reset()
            
    def reset(self):
        self.Bind(wx.EVT_TIMER, self.OnTimer1, self.timer1)
        self.text.SetLabel('Done!')
        self.count = 0
        self.count2 = 0
        self.count3 = 0
        self.nametc.Clear()
        self.tc.Clear()
        self.timer1 = wx.Timer(self, 1)
        self.timer2 = wx.Timer(self, 1)
        self.timer3 = wx.Timer(self, 1)

    def Info(self, e):
        log = InfoDialog(None,-1,'Information')

    def Exit(self, event):
        self.Close()

class InfoDialog(wx.Frame):
    def __init__(self, parent, id, title):

        wx.Frame.__init__(self, parent, id, title, size=(400, 250))


        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour('#000000')

        text = """\n \t \t \t    E-Z Music Downloader v1.0 \n \n Type in the song you want to downloading the the first box like so: "Song name by Artist" make sure you have both the artist and the song name in the query, in the second box type in what you want to name the Mp3. Next select High quality or Medium quality. High quality creates a larger file, therefore takes longer to convert. The status bar will show the actions the program is doing, once the status bar says done you can download another. To change the directory in which the song downloads, go to options in the menu bar and select "ChangeDownloadDirectory". \n \n \t \t  Thanks for chosing E-Z Musick Downloader! \n \n \t   (Songs converted using http://www.convertmemp3.com )"""
        
        txt = wx.StaticText(panel, label=text)
        txt.SetForegroundColour('#FFFFFF')
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(txt, 1, wx.EXPAND|wx.ALIGN_CENTER, 5)

        panel.SetSizer(sizer)

        self.Show()
        self.Centre()

    def Exit(self, e):
        self.Close()
        
app = wx.App()
log = GUI(None,-1,'Music Downloader')
app.MainLoop()
