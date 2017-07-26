"""I am P1.

The latest public version of me may be found at:
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/543267/index_txt

I will download all of the recipes from the Python Cookbook using
the URL http://aspn.activestate.com/ASPN/Cookbook/Python?query_start=????
and store them into the drive and directory you specify.

I extract the file names using the recipe number and the HTML <a></a> string;
replacing special characters with an underscore.  I also clean up the filename.

There are a few commands that I recognize:
   Help or ? - shows the list of commands
   Recipes   - shows lists of recipe numbers as they are downloaded
   Files     - shows lists of file names and their CRC64 hashes
   Stats     - shows processing statistics for this run
   Compile   - compiles everything in the selected download directory
   Time      - shows timing information for this process
   Find      - shows the number of recipes that have recipe numbers
               greater than the recipe number you enter, used for planning,
               this does not download the recipes.
   Print     - route output to the specified networked printer
   You may combine them with interleaving spaces;  Help will stop the process.

You will be asked for information such as:

If you so choose, enter the drive and the full path name, with trailing backslash where
    the downloaded folders and files will end up. -- J:\Python\Doc\Cookbook\ is the default

If you so choose, enter a number of a recipe where I should start downloading
    (if negative, I'll start retreiving from the recipe last used.) -- 0 is the default
    -1 looks for the number in ...\largest_number.txt
    99999999 will skip the Cookbook download and proceed to the other download sections

If you so choose, enter a command (Help, Stats, Time, Recipes, Files, ?, Compile, Find, Print)
    -- 'Stats Time Print' are the defaults

If you have chosen the command 'Print', enter the printer's network path
    (\\\\servername\printername) -- no default

If you so choose, enter the URL (hyperlink,) with trailing backslash, to a website 
    to download all files from that website that match the .suffix you specify in the .py box

If you so choose, click Download all .??? files from the ENTIRE World Wide Web -- .py is the default

If you so choose, click Enter the Download Contest -- no default
    Before doing this you must have modified the P1 source code on only the one line so noted,
    so that the Google search string will find the most .py files anywhere on the World Wide Web.
    Find that line on line #375 of this source code, or search for 'CONTEST CONTEST'.

If you have clicked the 'Enter the Download Contest' button:
    Enter your Name or u$3rN4m3.
    Enter your e-mail address.
    Enter your SMTP server name.
        To find this in MS Outlook 2003:
        1)  On the Menu Bar, click on Tools, then
        2)  click on E-mail Accounts..., then
        3)  select "View or change existing e-mail accounts'; then click next, then
        4)  select "Microsoft Exchange Server"; then click Change...; then
        5)  select the text inside the box labeled "Microsoft Exchange Server"; then
        6)  press ctrl-c (to copy this selected text); then click cancel
        7)  back at 'your.smtp.server.name'; select it and press ctrl-v

Click either Quit or Continue.  Quit will halt the process.  Continue will proceed with the process.

CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST 
Each month the winner of the contest will have their information
logged here, possibly shown in the next version of the printed Cookbook
+-------------------------------------------------------------------------------------------+
|MMM/Year Name             E-mail Address                   Duration       # of Files       |
|Jan/2008 pee one          p1p1p1p1p1p1p1p1p1p1p1@gmail.com 00:40:23       2,047            |
|         searchFor = '.py+intitle:index.of'                                                |
|Feb/2008                                                                                   |
|Mar/2008                                                                                   |
|Apr/2008                                                                                   |
|May/2008                                                                                   |
|Jun/2008                                                                                   |
|Jul/2008                                                                                   |
|Aug/2008                                                                                   |
|Sep/2008                                                                                   |
|Oct/2008                                                                                   |
|Nov/2008                                                                                   |
|Dec/2008                                                                                   |
|Jan/2009                                                                                   |
|Feb/2009                                                                                   |
|Mar/2009                                                                                   |
|Apr/2009                                                                                   |
|May/2009                                                                                   |
|Jun/2009                                                                                   |
|Jul/2009                                                                                   |
|Aug/2009                                                                                   |
|Sep/2009                                                                                   |
|Oct/2009                                                                                   |
|Nov/2009                                                                                   |
|Dec/2009                                                                                   |
+-------------------------------------------------------------------------------------------+
I am P1.
"""
#J:\Python\Doc\Cookbook\
try:
    import re,urllib,urllib2,os,sys,Tkinter,string,readline
except ImportError:
    raise ImportError, "This program requires Python 2.4 or later."

from Tkinter import *

#Initialize counters
fls = rem = skipped = recipe_count = largest_number = nooffolders = nooffiles = time2Quit = skipCookbook = 0

# CRC64 is borrowed from _259177_CRC64_Calculate_the_cyclic_redundancy_check.py
POLY64REVh = 0xd8000000L
CRCTableh = [0] * 256
CRCTablel = [0] * 256
isInitialized = False

def CRC64(aString):
    global isInitialized
    crcl = 0
    crch = 0
    if (isInitialized is not True):
        isInitialized = True
        for i in xrange(256):
            partl = i
            parth = 0L
            for j in xrange(8):
                rflag = partl & 1L
                partl >>= 1L
                if (parth & 1):
                    partl |= (1L << 31L)
                parth >>= 1L
                if rflag:
                    parth ^= POLY64REVh
            CRCTableh[i] = parth;
            CRCTablel[i] = partl;

    for item in aString:
        shr = 0L
        shr = (crch & 0xFF) << 24
        temp1h = crch >> 8L
        temp1l = (crcl >> 8L) | shr
        tableindex = (crcl ^ ord(item)) & 0xFF

        crch = temp1h ^ CRCTableh[tableindex]
        crcl = temp1l ^ CRCTablel[tableindex]
    return (crch, crcl)

def CRC64digest(aString):
    return "%08X%08X" % (CRC64(aString))

def printP1():
    p = ''.join("""oolcay itay""")
    print p
    if printFound != -1:
        pp.write(p)
        pp.flush()
        pp.close()
    sys.exit()

def help():
    p = __doc__
    print p
    if printFound != -1:
        pp.write(p)
        pp.flush()
        pp.close()
    sys.exit()

class App:
    def __init__(self, master):
        #Define the outer frame
        frame = Frame(master)
        frame.grid()

        #Define a label(0,0) asking for the name of the storage directory
        self.label1 = Label(frame, wraplength=500, justify=LEFT, text="Enter the drive and the full path name, with trailing backslash where the downloaded files will end up. -- J:\Python\Doc\Cookbook\ is the default -->", font=("Verdana", 12))
        self.label1.grid(row=0, column=0, sticky=W)

        #Define an entry(0,1) accepting the name of the storage directory
        self.entry1 = Entry(frame, fg="blue", font=("Verdana", 12), relief=RAISED, width=25)
        self.entry1.grid(row=0, column=1, sticky=W)
        self.entry1.insert(0, 'J:\\Python\\Doc\\Cookbook\\')

        #Define a label(1,0) asking for the starting recipe number
        self.label2 = Label(frame, wraplength=500, justify=LEFT, text="Enter a number of a recipe where I should start downloading (if negative, gets recipe last used.) -- 0 is the default; -1 looks for the number in <specified drive and path>\largest_number.txt-->", font=("Verdana", 12))
        self.label2.grid(row=1, column=0, sticky=W)

        #Define an entry(1,1) accepting the starting recipe number
        self.entry2 = Entry(frame, fg="blue", font=("Verdana", 12), relief=RAISED, width=25)
        self.entry2.grid(row=1, column=1, sticky=W)
        self.entry2.insert(0, '0')

        #Define a label(2,0) asking for a command list
        self.label3 = Label(frame, wraplength=500, justify=LEFT, text="Enter a command (Help, ?, Stats, Time, Recipes, Files, Compile, Find, Print, Multiple commands may be separated by spaces.) 'Stats Time Print' is the default -->", font=("Verdana", 12))
        self.label3.grid(row=2, column=0, sticky=W)

        #Define an entry(2,1) accepting the command list
        self.entry3 = Entry(frame, fg="blue", font=("Verdana", 12), relief=RAISED, width=25)
        self.entry3.grid(row=2, column=1, sticky=W)
        self.entry3.insert(0, 'Stats Time Print')

        #Define a lable(3,0) asking for the printer's network path
        self.label4 = Label(frame, wraplength=500, justify=LEFT, text="Enter the printer's network path (Ignore this if you did not specify 'Print' as a command) (\\\\servername\printername) -- no default -->", font=("Verdana", 12))
        self.label4.grid(row=3, column=0, sticky=W)

        #Define an entry(3,1) accepting the printer's network path
        self.entry4 = Entry(frame, fg="blue", font=("Verdana", 12), relief=RAISED, width=25)
        self.entry4.grid(row=3, column=1, sticky=W)
        self.entry4.insert(0, '\\\\servername\\printername')

        #Define a lable(4,0) asking for the URL to search
        self.label5 = Label(frame, wraplength=500, justify=LEFT, text="Enter the URL of the website to search for files.  (http://www.koders.com/zeitgeist/python/)\n(Specify what kind of filetype in the .py box.)\n-- no default -->", font=("Verdana", 12))
        self.label5.grid(row=4, column=0, sticky=W)

        #Define an entry(4,1) accepting the URL to search
        self.entry5 = Entry(frame, fg="blue", font=("Verdana", 12), relief=RAISED, width=25)
        self.entry5.grid(row=4, column=1, sticky=W)
        self.entry5.insert(0, ' ')


        #Define a lable(5,0) asking to search the WWW
        self.label6 = Label(frame, wraplength=500, justify=LEFT, text="Check if you want to search the entire WWW for <anything><.supplied suffix> files -->", font=("Verdana", 12))
        self.label6.grid(row=5, column=0, sticky=W)

        #Define a checkbutton(5,1) accepting whether to search the WWW
        self.var1 = IntVar()
        self.textvar1 = StringVar()
        self.textvar1.set('Click to Search ENTIRE WWW')
        self.checkbutton1 = Checkbutton(frame, textvariable=self.textvar1, command=self.changeText, font=("Verdana", 12), foreground='blue', selectcolor='red', variable=self.var1, borderwidth=3, indicatoron=FALSE)
        self.checkbutton1.grid(row=5, column=1, sticky=W)

        #Define an entry(5,2) accepting the files' suffix (.py)
        self.entry7 = Entry(frame, fg="blue", font=("Verdana", 12), relief=RAISED, width=5, borderwidth=3)
        self.entry7.grid(row=5, column=2, sticky=W, padx=3)
        self.entry7.insert(0, '.py')


        #Define a label(6,0) asking to enter the contest
        self.label8 = Label(frame, wraplength=500, justify=LEFT, text="Check if you want to enter the contest to find the most .py files on the World Wide Web -->", font=("Verdana", 12))
        self.label8.grid(row=6, column=0, sticky=W)

        #Define a checkbutton(6,1) accepting whether to enter the contest
        self.var2 = IntVar()
        self.textvar2 = StringVar()
        self.textvar2.set('Click to Enter Contest')
        self.checkbutton2 = Checkbutton(frame, textvariable=self.textvar2, command=self.contestText, font=("Verdana", 12), foreground='blue', selectcolor='red', variable=self.var2, borderwidth=3, indicatoron=FALSE)
        self.checkbutton2.grid(row=6, column=1, sticky=W)

        #Define a label(7,0) asking for their name
        self.textvar3 = StringVar()
        self.textvar3.set(' ')
        self.label9 = Label(frame, wraplength=500, justify=LEFT, textvariable=self.textvar3, font=("Verdana", 12))
        self.label9.grid(row=7, column=0, sticky=W)
        
        #Define an entry(7,1) accepting their name
        self.entry9 = Entry(frame, fg="blue", font=("Verdana", 12), relief=RAISED, width=25)
        self.entry9.grid(row=7, column=1, sticky=W)
        self.entry9.insert(0, 'Your name or u$3rN4m3')

        #Define a label(8,0) asking for their email address
        self.textvar4 = StringVar()
        self.textvar4.set(' ')
        self.label10 = Label(frame, wraplength=500, justify=LEFT, textvariable=self.textvar4, font=("Verdana", 12))
        self.label10.grid(row=8, column=0, sticky=W)

        #Define an entry(8,1) accepting their email address
        self.entry10 = Entry(frame, fg="blue", font=("Verdana", 12), relief=RAISED, width=25)
        self.entry10.grid(row=8, column=1, sticky=W)
        self.entry10.insert(0, 'youremailname<at>youremail<dot>com')
        
        #Define a label(9,0) asking for their SMTP server name
        self.textvar5 = StringVar()
        self.textvar5.set(' ')
        self.label11 = Label(frame, wraplength=500, justify=LEFT, textvariable=self.textvar5, font=("Verdana", 12))
        self.label11.grid(row=9, column=0, sticky=W)
        
        #Define an entry(9,1) accepting their SMTP server name
        self.entry11 = Entry(frame, fg="blue", font=("Verdana", 12), relief=RAISED, width=25)
        self.entry11.grid(row=9, column=1, sticky=W)
        self.entry11.insert(0, 'your.smtp.server.name')
                
        #Define an entry(7,1) accepting their name
        self.labelb9b = Entry(frame, fg="blue", font=("Verdana", 12), relief=FLAT, width=25)
        self.labelb9b.grid(row=7, column=1, sticky=W)
        self.labelb9b.insert(0, ' ')

        #Define an entry(8,1) accepting their email address
        self.labelb10b = Entry(frame, fg="blue", font=("Verdana", 12), relief=FLAT, width=25)
        self.labelb10b.grid(row=8, column=1, sticky=W)
        self.labelb10b.insert(0, ' ')

        #Define an entry(9,1) accepting their SMTP server name
        self.labelb11b = Entry(frame, fg="blue", font=("Verdana", 12), relief=FLAT, width=25)
        self.labelb11b.grid(row=9, column=1, sticky=W)
        self.labelb11b.insert(0, ' ')


        import tkFont
        #Define a Verdana font
        Verdana = tkFont.Font(family="Verdana", size=12, weight=tkFont.BOLD)

        #Define a button to continue
        self.button1 = Button(frame, text='CONTINUE', fg='green', font=Verdana, width=20, command=self.say)
        self.button1.grid(row=10, column=0, columnspan=1)

        #Define a button to quit
        self.button2 = Button(frame, text='QUIT', fg='red', font=Verdana, width=20, command=self.quit)
        self.button2.grid(row=10, column=1, columnspan=1)

    def quit(self):
        #Chop down the tree and pull out the roots
        global time2Quit
        time2Quit = 1
        root.destroy()

    def say(self):
        #Define a command list to set the variables from the contents of the entry boxes
        global fileInName, greaterThan, commandPrompt, printPath, searchURL, fileSuffix
        fileInName    = app.entry1.get()
        greaterThan   = app.entry2.get()
        commandPrompt = app.entry3.get()
        printPath     = app.entry4.get()
        searchURL     = app.entry5.get()
        fileSuffix    = app.entry7.get()
        root.destroy()

    def changeText(self):
        #Define a command list to set the searchWWW button text
        global searchWWW
        searchWWW = app.var1.get()
        if app.var1.get() == 0:
            app.textvar1.set('Search Disabled')
        else:
            app.textvar1.set('Search ENTIRE WWW')

    def contestText(self):
        """Define a command list to:
           1) set contestWWW from the contents of the entry box
           2) set the contestWWW button text
           3) turn on and off the labels and entry boxes of the name, email address, and smtp server name """
        global contestWWW, fromname, fromaddr, smtpServer
        contestWWW = app.var2.get()
        fromname   = app.entry9.get()
        fromaddr   = app.entry10.get()
        smtpServer = app.entry11.get()
        if app.var2.get() == 0:
            app.textvar2.set("No, thanks")
            #Hide self.lable7, self.entry7, self.lable8, and self.entry8
            app.textvar3.set(" ")
            app.textvar4.set(" ")
            app.textvar5.set(" ")
            app.entry9.lower()
            app.entry10.lower()
            app.entry11.lower()
            app.labelb9b.lift()
            app.labelb10b.lift()
            app.labelb11b.lift()
        else:
            app.textvar2.set("YES, CONTEST ENTERED!!")
            #Unhide self.lable7, self.entry7, self.lable8, and self.entry8
            app.textvar3.set("Enter your full name or your u$3rN4m3, will be entered in the comments log and possibly in the printed Cookbook) -- no default -->")
            app.textvar4.set("Enter your email address (youremailname<at>youremail<dot>com) -- no default -->")
            app.textvar5.set("Enter your SMTP server name (your.smtp.server.name) -- no default -->")
            app.entry9.lift()
            app.entry10.lift()
            app.entry11.lift()
            app.labelb9b.lower()
            app.labelb10b.lower()
            app.labelb11b.lower()
#Start the Google search
def getGoogle():
    global searchFor
    re_links = re.compile(r'<h2 class=r><a href="(.+?)"',re.IGNORECASE|re.DOTALL)
    #CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST
    #If you are entering the contest this is the one line of code you are allowed to modify (change only what is between the single quotes):
    searchFor = 'py+intitle:index.of'
    #original line of code:  searchFor = 'py+intitle:index.of'
    #CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST CONTEST 
    p = 'Google: Searching on google...'
    print p
    if printFound != -1:
        pp.write(p)
    links = {}
    currentPage = 0
    while True:
        p = "Google: Querying page %d (%d links found so far)" % (currentPage/100+1, len(links))
        print p
        if printFound != -1:
            pp.write(p)
        address = "http://www.google.com/search?q=%s&num=100&hl=en&start=%d" % (urllib.quote_plus(searchFor),currentPage)
        p = address
        print p
        if printFound != -1:
            pp.write(p)
        request = urllib2.Request(address, None, {'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'} )
        urlfile = urllib2.urlopen(request)
        #page = urlfile.read(200000)
        page = urlfile.read()
        p = 'page:', page
        print p
        if printFound != -1:
            pp.write(p)
        urlfile.close()
        for url in re_links.findall(page):
            links[url] = 0
        if "</div>Next</a></table></div></div><center>" in page: # Is there a "Next" link for next page of results ?
            currentPage += 100  # Yes, go to next page of results.
        else:
            break   # No, break out of the while True loop.
    p = "Google: Found %d links." % len(links)
    print p
    if printFound != -1:
        pp.write(p)
    return sorted(links.keys())

#Get files found on the returned Google page
def getFile(path, site, dir):
    global s, files, nooffiles, folder
    url = site + dir
    try:
        f = urllib.urlopen(url)
    except:
        p = 'Bad URL open: ' + url
        print p
        if printFound != -1:
            pp.write(p)
        return
    s = f.read()
    f.close()
    regexPy = re.compile('(?<=href=")[A-Za-z0-9_-]*'+fileSuffix)
    matches = regexPy.findall(s)
    for x in range(len(matches)):
        url = site + dir + matches[x]
        try:
            f = urllib.urlopen(url)
        except:
            p = 'Can not open URL: ' + url
            print p
            if printFound != -1:
                pp.write(p)
            continue
        s = f.read()
        f.close()
        if folder[-4:-1] == fileSuffix:
            try:
                os.chdir(path + folder[7:] + dir)
            except:
                p = 'Can not chdir to folder name: ' + folder
                print p
                if printFound != -1:
                    pp.write(p)
                continue
        else:
            try:
                os.chdir(path + folder[7:-1] + dir)
            except:
                p = 'Can not chdir to folder name: ' + folder
                print p
                if printFound != -1:
                    pp.write(p)
                continue   
        try:
            m = open(matches[x], 'w')
            m.write(s)
            m.close()
            p = 'Loading file: ' + matches[x]
            print p
            if printFound != -1:
                pp.write(p)  
            files += 1
            nooffiles += 1
        except:
            p = matches[x] + ' IOError: [Errno 9] Bad file descriptor'
            print p
            if printFound != -1:
                pp.write(p)

#Begin processing; request information
root = Tk()
root.tk_bisque()
root.title('P-1')
app = App(root)
root.mainloop()

#If the Quit button was pressed stop the presses (pun intended)
if time2Quit == 1:
    time2Quit = 0
    print 'Quit button pressed -- process halted'
    sys.exit()

#If help was asked for, help them
helpFound = string.find(str(commandPrompt),'Help')
if helpFound != -1:
    help()

#Shhh
POneFound = string.find(str(commandPrompt),'P-1')
if POneFound != -1:
    printP1()

#Shhh
requestFound = string.find(str(commandPrompt),'rodtsasdt llllllreport')
if requestFound != -1:
    import time
    now = time.time()
    cpus = 20476
    CP = [[1175414400000,2835],[1192176000000,2912],[1193122800000,4321],[1199433600000,6283],[2147328000000,43008],[46893711600000,2147483647]]
    for i in range(5):
        if now < CP[i][0]:break
    ts = CP[i - 1][0];
    bs = CP[i - 1][1];
    megabytes = (((ts-now) / (CP[i][0]+ts) * (CP[i][1]-bs)) + bs);
    cpus = cpus + int(largest_number % int(10000))
    p = ''.join('P-1 CUR ALLOC ' + str(cpus) + ' .... ' + str(megabytes) + ' megabytes\nHELLO GREGORY')
    print p
    if printFound != -1:
        pp.write(p)
        pp.flush()
        pp.close()
    sys.exit()

#Shhh
POneFound = string.find(str(commandPrompt),'P1')
if POneFound != -1:
    printP1()

#If help was asked for, help them
helpFound = string.find(str(commandPrompt),'?')
if helpFound != -1:
    help()

#Open the print path if necessary
printFound = string.find(str(commandPrompt),'Print')
if printFound != -1:
    try:
        #printPath = raw_input("Enter the printer's network path (\\\\servername\printername)-->")
        pp = open(printPath, 'w')
    except:
        print printPath, 'does not exist -- system shutting down\n'
        sys.exit()
        
#Format and Print the start time
timeFound = string.find(str(commandPrompt),'Time')
if timeFound != -1:
    import time
    start = time.localtime(time.time())
    year, month, day, hour, minute, second, weekday, yearday, daylight = start
    p = ''.join("Process Started " + "%02d:%02d:%02d" % (hour, minute, second) + '\n')
    print p
    if printFound != -1:
        pp.write(p)
else:
    p = ''.join("Process Started\n")
    print p
    if printFound != -1:
        pp.write(p)

#If largest_number.txt is not found create it
largestFound = 0
try:
    for root, dirs, files in os.walk(fileInName):
        for _name in files:
            if _name == 'largest_number.txt':
                #print 'largest_number.txt found in',_name
                largestFound += 1
except:
    try:
        root.destroy()
    except:
        pass
    print '\n for root, dirs, files in os.walk(fileInName): line #560 failed\n'
    sys.exit()

#Keep track of the largest Recipe number found so far
if largestFound == 0:
    largest_number = 0
    filegTName = fileInName + 'largest_number.txt'
    try:
        gT = open(filegTName, 'w')
        gT.write(str(largest_number))
        gT.flush()
        gT.close()
    except:
        print 'Open failed on file:', filegTName
        print 'If you entered the correct directory name, then make sure it has been built.'
        sys.exit()
        

#fileInName = raw_input('Enter the drive and the full path name, with trailing backslash where the downloaded files will end up-->')
if fileInName == '':
    fileInName = 'J:\\Python\\Doc\\Cookbook\\'

#greaterThan = input('Enter a number of a recipe where I should start downloading (if negative, gets number last used)-->')
if greaterThan == '':
    greaterThan = 0
if greaterThan == None:
    greaterThan = 0
greaterThan = int(greaterThan)
if greaterThan < 0:
    filegTName = fileInName + 'largest_number.txt'
    gT = open(filegTName, 'r')
    largest_number = gT.readlines()
    greaterThan = int(largest_number[0])
    largest_number = int(largest_number[0])
    gT.flush()
    gT.close()
if greaterThan == 99999999:
    skipCookbook = 1
    
#commandPrompt = raw_input('Enter a command (Help,Stats,Time, Recipes,Files,?, Compile,Find,Print)-->')
if commandPrompt == '':
    commandPrompt = 'Stats Time Print'

#Check to see if we are going to search one website
if searchURL == '' or searchURL == None or searchURL == ' ':
    pass
else:
    p = 'We are going to search for ' + searchURL + fileSuffix + ' files'
    print p
    if printFound != -1:
        pp.write(p)
    p = 'Good Connection: ' + searchURL
    print p
    if printFound != -1:
        pp.write(p)
    path = fileInName
    site = searchURL + fileSuffix
    dir  = ''
    folder = str(re.sub("[\[\`\!\%\^\&\*\(\)\+\-\=\{\}\:\;\<\>\,\?\|\'\"\]]",'_',site))
    #Build a directory(folder) for each returned "site"
    try:
        if folder[-4:-1] == fileSuffix:
            os.makedirs(path + folder[8:])
            nooffolders += 1
        else:
            os.makedirs(path + folder[8:-1])
            nooffolders += 1
    except WindowsError, e:
        if e.errno == 17:
            pass
        else:
            raise
    files = 0
    getFile(path, site, dir)
    if files == 0:
        try:
            if folder[-4:-1] == fileSuffix:
                os.removedirs(path + folder[7:])
                nooffolders -= 1
            else:
                os.removedirs(path + folder[7:-1])
                nooffolders -= 1
        except:
            p = 'Directory remove failed -- not empty ' + path+folder[7:-1]
            print p
            if printFound != -1:
                pp.write(p)    
    #For each directory found iterate and get more files from that directory
    regexDir = re.compile('(?<=href=)"[A-Za-z0-9_-]*/"')
    matches = regexDir.findall(s)
    for x in range(len(matches)):
        try:
            if folder[-4:-1] == fileSuffix:
                os.mkdir(path + folder[8:] + matches[x][1:-1])
                nooffolders += 1
            else:
                os.mkdir(path + folder[8:-1] + matches[x][1:-1])
                nooffolders += 1
        except WindowsError, e:
            if e.errno == 17:
                pass
            else:
                raise
        files = 0
        getFile(path, site, matches[x][1:-1])
        if files == 0:
            if folder[-4:-1] == fileSuffix:
                os.rmdir(path + folder[8:] + matches[x][1:-1])
                nooffolders -= 1
            else:
                os.rmdir(path + folder[8:-1] + matches[x][1:-1])
                nooffolders -= 1

#Check to see if we are going to search the ENTIRE World Wide Web for files
if app.var1.get() == 1:
    #Check to see if we are going to compete in the CONTEST
    if app.var2.get() == 1:
        fileSuffix = '.py'
    p = 'We are going to search the ENTIRE World Wide Web for ' + fileSuffix + ' files'
    print p
    if printFound != -1:
        pp.write(p)
    #Process 100 pages per search, for a total limit of 1000 URLs placed in the "sites" list
    pages = getGoogle()
    for x in range(len(pages)):
        p = 'Good Connection: ' + pages[x]
        print p
        if printFound != -1:
            pp.write(p)
        path = fileInName
        site = pages[x]
        dir  = ''
        folder = str(re.sub("[\[\`\!\%\^\&\*\(\)\+\-\=\{\}\:\;\<\>\,\?\|\'\"\]]",'_',site))
        #Build a directory(folder) for each returned "site"
        try:
            if folder[-4:-1] == fileSuffix:
                os.makedirs(path + folder[7:])
                nooffolders += 1
            else:
                os.makedirs(path + folder[7:-1])
                nooffolders += 1
        except WindowsError, e:
            if e.errno == 17:
                pass
            else:
                raise
        files = 0
        getFile(path, site, dir)
        if files == 0:
            try:
                if folder[-4:-1] == fileSuffix:
                    os.removedirs(path + folder[7:])
                    nooffolders -= 1
                else:
                    os.removedirs(path + folder[7:-1])
                    nooffolders -= 1
            except:
                p = 'Directory remove failed -- not empty ' + path+folder[7:-1]
                print p
                if printFound != -1:
                    pp.write(p)    
    #For each directory found iterate and get more files from that directory
    regexDir = re.compile('(?<=href=)"[A-Za-z0-9_-]*/"')
    matches = regexDir.findall(s)
    for x in range(len(matches)):
        try:
            if folder[-4:-1] == fileSuffix:
                os.mkdir(path + folder[7:] + matches[x][1:-1])
                nooffolders += 1
            else:
                os.mkdir(path + folder[7:-1] + matches[x][1:-1])
                nooffolders += 1
        except WindowsError, e:
            if e.errno == 17:
                pass
            else:
                raise
        files = 0
        getFile(path, site, matches[x][1:-1])
        if files == 0:
            if folder[-4:-1] == fileSuffix:
                os.rmdir(path + folder[7:] + matches[x][1:-1])
                nooffolders -= 1
            else:
                os.rmdir(path + folder[7:-1] + matches[x][1:-1])
                nooffolders -= 1
                
if skipCookbook == 0:
    #Read in a batch of recipes
    for x in range(1,2120,20):
        url = 'http://aspn.activestate.com/ASPN/Cookbook/Python?query_start=' + str(x)
        f = urllib.urlopen(url)
        s = f.read()
        f.close()
        matches = re.findall("/ASPN/Cookbook/Python/Recipe/(\d*)",s)
        # if nothing was found try again
        if matches == []:
            f = urllib.urlopen(url)
            s = f.read()
            f.close()
            matches = re.findall("/ASPN/Cookbook/Python/Recipe/(\d*)",s)
        #If command = Recipes, list each recipe
        recipesFound = string.find(str(commandPrompt),'Recipes')
        if recipesFound != -1:
            p = ''.join(str(x) + ' ' + str(greaterThan) + ' ' + str(matches) + '\n')
            print p
            if printFound != -1:
                pp.write(p)
        #Loop through batches of recipes finding matches
        xcape = 'n'
        for y in range(len(matches)):
            try:
                intMatches = int(matches[y])
            except:
                intMatches = int(0)
            try:
                if intMatches < greaterThan:
                    xcape = 'y'
                else:
                    xcape = 'n'
                    break
            except:
                xcape = 'n'
                break
        if xcape == 'y':
            skipped += 1
            continue
        #Find the recipe numbers
        pattern = '/ASPN/Cookbook/Python/Recipe/.*.(?=<)'
        name_matches = re.findall(pattern,s)
        for z in range(len(name_matches)):
            try:
                intMatches = int(matches[z])
            except:
                intMatches = int(0)
            if intMatches < greaterThan:continue
            #if Find is true then don't download the recipes, just count them
            findFound = string.find(str(commandPrompt),'Find')
            if findFound != -1:
                largest_number = int(matches[z])
                recipe_count += 1
                continue
            if recipesFound != -1:
                p = 'Loading recipe #:' + str(matches[z])
                print p
                if printFound != -1:
                    pp.write(p)
            #Add to largest_number.txt
            try:
                if int(matches[z]) > largest_number:
                    gT = open(filegTName, 'w')
                    gT.write(matches[z])
                    largest_number = int(matches[z])
                    gT.flush()
                    gT.close()
            except:
                pass
            #Make sure formatting matches 5 or 6 digits of the number and clean up the filename
            try:
                if intMatches < int(100000):
                    end = 36
                else:
                    end = 37
            except:
                end = 36
            #Change special characters to underscores
            name_matches[z] = '_' + str(re.sub("[\[\`\~\!\@\#\$\%\ \^\&\*\(\)\_\+\-\=\{\}\\\:\;\<\>\,\.\?\/\|\'\"\]]",'_',name_matches[z][end:]))
            #Strip _a from the right side of the end of the filename
            name_matches[z] = string.rstrip(name_matches[z],'_a')
            #Clean up the ending of the filename
            while '__' in name_matches[z]:
                name_matches[z] = string.replace(name_matches[z], '__', '_')
            name_matches[z] = '_' + matches[z] + name_matches[z] + fileSuffix
            name_matches[z] = string.replace(name_matches[z], '_py.py', '.py')
            name_matches[z] = string.replace(name_matches[z], '_by.py', '.py')
            name_matches[z] = string.replace(name_matches[z], 'quot_', '')
            #Download a recipe
            url = 'http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/' + str(matches[z]) + '/index_txt'
            f = urllib.urlopen(url)
            s = f.read()
            f.close()
            fileOutName = str(fileInName) + str(name_matches[z])
            fileOut = open(fileOutName, 'w')
            #Add new line characters on the right side of every line
            s = re.sub('\r*\n','\n',str(s))
            #Remove whitespace from the right side of every line and make sure there is a new line character on the end
            s = re.sub(' *\n','\n',str(s))
            #Search for alphanumerics, if found the recipe is not empty
            found = re.search('[:alnum:]',str(s))
            #Search for HTML, if found this recipe is empty
            HTMLfound = re.search('<title>ASPN : Cookbook : Python Cookbook</title>',str(s),re.S)
            #If HTML is found, throw out that recipe and report doing so
            if HTMLfound:
                fileOut.close()
                rem = rem + 1
                os.remove(fileOutName)
                p = ''.join(fileOutName  + ' html found - tossed out\n')
                print p
                if printFound != -1:
                    pp.write(p)
                continue
            #If a recipe is found, write it out, add one to the found counter
            if found:
                filesFound = string.find(str(commandPrompt),'Files')
                #If a command is Files, produce the CRC64 cyclic redundancy check, print it out and the file name
                if filesFound != -1:
                    p = ''.join(str(CRC64(s)) + ' ' + fileOutName + '\n')
                    print p
                    if printFound != -1:
                        pp.write(p)
                fileOut.write(s)
                fls = fls + 1
                fileOut.close()
            else:
                #If the file is empty skip it, add one to the removed counter
                fileOut.close()
                rem = rem +1
                p = ''.join(fileOutName + ' empty file - tossed out\n')
                print p
                if printFound != -1:
                    pp.write(p)
                os.remove(fileOutName)

#Compile everything in the specified directory
compileFound = string.find(str(commandPrompt),'Compile')
if compileFound != -1:
    import compileall
    compileall.compile_dir(fileInName, force=1)

#Format and Print the End-Of-Process Statistics
findFound = string.find(str(commandPrompt),'Find')
statsFound = string.find(str(commandPrompt),'Stats')
if statsFound != -1:
    #If just "Find"ing show different stats
    if findFound != -1:
        p = ''.join('Largest Recipe # to find:     ' + str(largest_number) + '\n')
        print p
        if printFound != -1:
            pp.write(p)
        p = ''.join('Number of Recipes found:      ' + str(recipe_count) + '\n')
        print p
        if printFound != -1:
            pp.write(p)
    else:
        #Otherwise show all of the stats
        p = ''.join('Largest Recipe # stored:      ' + str(largest_number) + '\n')
        print p
        if printFound != -1:
            pp.write(p)
    p = ''.join('Number of Recipes retreived:  ' + str(fls) + '\n')
    print p
    if printFound != -1:
        pp.write(p)
    p = ''.join('Number of Recipes removed:    ' + str(rem) + '\n')
    print p
    if printFound != -1:
        pp.write(p)
    p = ''.join('Number of Recipes skipped:    ' + str(skipped) + '\n')
    print p
    if printFound != -1:
        pp.write(p)
    p = ''.join('Number of Recipes processed:  ' + str(fls+rem+skipped) + '\n')
    print p
    if printFound != -1:
        pp.write(p)
    p = ''.join('Number of folders processed:  ' + str(nooffolders) + '\n')
    print p
    if printFound != -1:
        pp.write(p)
    p = ''.join('Number of files processed:    ' + str(nooffiles) + '\n')
    print p
    if printFound != -1:
        pp.write(p)

#Calculate the process' duration; format and print the start time, stop time, and duration
timeFound = string.find(str(commandPrompt),'Time')
if timeFound != -1:
    stop = time.localtime(time.time())
    syear, smonth, sday, shour, sminute, ssecond, sweekday, syearday, sdaylight = stop

    thour   = shour
    tminute = sminute
    tsecond = ssecond

    if tsecond < second:
        tminute = tminute - 1
        dursecond = 60 + tsecond - second
    else:
        dursecond = tsecond - second

    if tminute < minute:
        thour = thour - 1
        durminute = 60 + tminute - minute
    else:
        durminute = tminute - minute

    if thour < hour:
        xday = 1
        durhour = hour - thour
    else:
        xday = 0
        durhour = thour - hour

    if xday == 0:
        p = ''.join("Process Completed -- start: " + "%02d:%02d:%02d" % (hour, minute, second) + ' stop: ' + "%02d:%02d:%02d" % (shour, sminute, ssecond) + ' duration: ' + "%02d:%02d:%02d" % (durhour, durminute, dursecond) + '\n')
        print p
        if printFound != -1:
            pp.write(p)
            pp.flush()
            pp.close()
    else:
        p = ''.join("Process Completed -- start: " + "%02d:%02d:%02d" % (hour, minute, second) + ' stop: ' + "%02d:%02d:%02d" % (shour, sminute, ssecond) + ' duration: ' + "%02d:%02d:%02d" % (durhour, durminute, dursecond) + ' and one day\n')
        print p
        if printFound != -1:
            pp.write(p)
            pp.flush()
            pp.close()
else:
    p = ''.join("Process Completed\n")
    print p
    if printFound != -1:
        pp.write(p)
        pp.flush()
        pp.close()

#If we are competing in the CONTEST, report the results to pee one.
if app.var2.get() == 1:
    import smtplib
    toaddrs = 'p1p1p1p1p1p1p1p1p1p1p1@gmail.com'
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n" % (fromaddr, toaddrs, '.py file Contest'))
    msg = msg + '\nA Contestant has entered the .py file Contest'
    msg = msg + '\n' + fromname + ' ' + fromaddr
    msg = msg + ' duration: ' + "%02d:%02d:%02d" % (durhour, durminute, dursecond)
    msg = msg + ' # of file: ' + "%10d" % (nooffiles) + '\n'
    msg = msg + 'searchFor: ' + searchFor
    server = smtplib.SMTP(smtpServer)
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
