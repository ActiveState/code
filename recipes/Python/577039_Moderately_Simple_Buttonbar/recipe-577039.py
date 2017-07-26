'''
;#template` {-path} {-menu} {-s1} {-s2} {-s3}
;#option`-path`Path to controlling file or template`F`c:\source\python\projects\menu\buttonbar.py`
;#option`-menu`Path to menu file`F`c:\source\python\projects\menu\test.ini`
;#option`-s1`First section`X`info`
;#option`-s2`Second section`X`help`
;#option`-s3`Third section`X`data`
;#end

'''
# ----------------------------------------------
# Name: ButtonBarV2
# Description:
## D20E-119 Popup button bar using Qeditor style menus.ini file (ExPopen)
#
# Author: Philip S. Rist
# Date: 12/20/2009
# Copyright 2009 by St. Thomas Software
# ----------------------------------------------
# This program is freeware.  It may be used
# for any moral purpose.  You use it at your
# own risk.  St. Thomas Software makes no
# guarantees to its fitness to do anything.
#
# If you feel you must pay for it. Please
# send one million dollars to
#
#     The International Rescue Committee
#     122 East 42nd Street
#     New York, N.Y.   10168-1289
#
# Ok, we are in a recession.  So, make it a half
# million.

#
# Example of .reg file entry
#     [HKEY_CLASSES_ROOT\textfile\Shell\TextTools]
#     @="T&ext Tools
#     "EditFlags"=hex:01,00,00,00
#     [HKEY_CLASSES_ROOT\textfile\Shell\TextTools\Command]
#     @="c:\\sys\\python25\\python.exe   c:\\bin\\ButtonBarV2.py   \"%1\"  \"c:\\bin\\Text Tools.ini\"   tools     "
#
#
#     %1 is replaced by the selected file.  It is used to replace {a}, {b}, {n}, {f}, {p} etc. during command expansion.  
#     This string is used only for command expansion and for display at the top of the dialog.  If no expansion
#     is performed any string can be used and displayed.  This parameter can also be a file path template (ie. *.py) in 
#     which case a file list will be provided from which files can be selected.
#
#     The second parameter is the name of the initialization file shown below.  Each line contains a prompt displayed
#     on a button and a command separated by a comma.  Macros are replaced before execution.
#
#     The remaining parameters the sections to be used to make the button bar.  The order in the initialization file
#     is maintained.
#

# Example initialization file
#     [Text Tools 08/15/08]
#     Open,c:\source\TextFiles\qeditor.exe              "{a}"
#     Print,c:\windows\nodepad.exe                      /P "{a}"
#     Edit,c:\windows\system32\wscript.exe              c:\bin\editit.vbs "{a}"
#     Save,C:\Windows\system32\wscript.exe              c:\bin\Util.vbs  /S  "{a}"
#     Has been Saved,C:\Windows\system32\wscript.exe    c:\bin\Util.vbs  /K  "{a}"
#     Restore,C:\Windows\system32\wscript.exe           c:\bin\Util.vbs  /R  "{a}"
#     [Convert]
#     Convert to PDF,c:\sys\python25\python.exe         c:\sys\tools\pyText2PDF.py   "{a}" "{b}.pdf"
#     [Info]
#     Win Diff,"c:\sys\DevStudio\VC\Bin\Windiff.exe"    "{a}"   "c:\_backup\{f}"
#     [Tools]
#     Directory ,c:\sys\Tcl\bin\wish84.exe              c:\bin\mymenu.tcl  "c:\bin\Directory.ini"  "{p}"
#     Directory Popup,c:\sys\Tcl\bin\wish84.exe         c:\bin\RegMenu.tcl "{p}" Directory
#     [Help]
#     Help,c:\Windows\system32\Wscript.exe               c:\bin\Notes.vbs "c:\bin\Text Tools.ini"
#     [Exit]

import Tkinter
import subprocess

from Tkconstants import *
import sys
import os, os.path, glob
import tkMessageBox

import _winreg as reg


mCmds = {}
TopLevel = None

def GetExtensionInfo(pExtension):
    lHandle = reg.OpenKey(reg.HKEY_CLASSES_ROOT, pExtension)
    lSubKeys, lValueCount, lModified = reg.QueryInfoKey(lHandle)
    lValues = {}
    for lCount in range(0, lValueCount):
        lName, lValue, lType = reg.EnumValue(lHandle, lCount)
        if lName == '':
            lName = "File Type"
        lValues[lName] =lValue
        
    lKey = lValues['File Type']
    lDescription = reg.QueryValue(reg.HKEY_CLASSES_ROOT, lKey)
    lValues['Description'] = lDescription

    lKey += '\\Shell'
    lDefault = reg.QueryValue(reg.HKEY_CLASSES_ROOT, lKey)
    lValues['Default'] = lDefault    
    
    return lValues


def GetCommand(pFileType, pCommandName):
    lKey = pFileType + '\\Shell\\' + pCommandName + '\\Command'
    print lKey
    lCommand= reg.QueryValue(reg.HKEY_CLASSES_ROOT, lKey)
    print lCommand
    return lCommand

def Expand(pCommand, pFilePath):
    'Replace {?} macros'
    lEndPos = pFilePath.rfind("\\")
    lPath = pFilePath[0:lEndPos]
    lFileName = pFilePath[lEndPos+1:]
    lEndPos = lFileName.rfind(".")
    lName = lFileName[:lEndPos]
    lFilePart = lPath + "\\" + lName
    lExtension = lFileName[lEndPos:]
#
    lTempFolder    = "c:\\temp"                  # {t} <----- Change as needed
    lInstallFolder = "c:\\bin"                   # {i}
    lBackupFolder  = "c:\\_Backup"               # {u}
    lSourceFolder  = "c:\\source"                # {o}
    lSystemFolder  = "c:\\sys"                   # {y}
    lWindowsFolder = "c:\\windows\\system32"     # {w}
    lArchiveFolder = "j:\\_Backup"               # {k}
    lLibraryFolder = "c:\\Library"               # {l}
    lProgramFolder = "c:\\Program Files"         # {g}

    lCommand = pCommand
    lPos = lCommand.rfind("{a}")
    if lPos > 0:
        lCommand = lCommand.replace("{a}",pFilePath)
    lPos = lCommand.rfind("{b}")
    if lPos > 0:
        lCommand = lCommand.replace("{b}",lFilePart)
    lPos = lCommand.rfind("{p}")
    if lPos > 0:
        lCommand = lCommand.replace("{p}",lPath)
    lPos = lCommand.rfind("{f}")
    if lPos > 0:
        lCommand = lCommand.replace("{f}",lFileName)                           
    lPos = lCommand.rfind("{n}")
    if lPos > 0:
        lCommand = lCommand.replace("{n}",lName)                           
    lPos = lCommand.rfind("{e}")
    if lPos > 0:
        lCommand = lCommand.replace("{e}",lExtension)
         
    lPos = lCommand.rfind("%1")
    if lPos > 0:
        lCommand = lCommand.replace("%1",pFileName)

    lPos = lCommand.rfind("{t}")
    if lPos > 0:
        lCommand = lCommand.replace("{t}",lTempFolder)
    lPos = lCommand.rfind("{i}")
    if lPos > 0:
        lCommand = lCommand.replace("{i}",lInstallFolder)
    lPos = lCommand.rfind("{u}")
    if lPos > 0:
        lCommand = lCommand.replace("{u}",lBackupFolder)
    lPos = lCommand.rfind("{o}")
    if lPos > 0:
        lCommand = lCommand.replace("{o}",lSourceFolder)
    lPos = lCommand.rfind("{y}")
    if lPos > 0:
        lCommand = lCommand.replace("{y}",lSystemFolder)
    lPos = lCommand.rfind("{w}")
    if lPos > 0:
        lCommand = lCommand.replace("{w}",lWindowsFolder)
    lPos = lCommand.rfind("{k}")
    if lPos > 0:
        lCommand = lCommand.replace("{k}",lArchiveFolder)
    lPos = lCommand.rfind("{l}")
    if lPos > 0:
        lCommand = lCommand.replace("{l}",lLibraryFolder)
    lPos = lCommand.rfind("{g}")
    if lPos > 0:
        lCommand = lCommand.replace("{g}",lProgramFolder)

                                                     # This macro is a little flakey, you may want to remove it
                                                     # in which case you will not need _winreg, GetExtensionInfo or GetCommand
    lPos = lCommand.find("{")                        # case insensitive command extraction from registry
    if lPos >= 0:                                    # {xx} where xx is the command name
                                                     # ie. print, open etc.
        lQuote = False                               # can occur only at the beginning of the command line
        lEndPos = lCommand.find("}")
        if lEndPos > lPos:
            lKey = lCommand[lPos+1:lEndPos]
            lPos = pFilePath.rfind('.')
            lExt = pFilePath[lPos:]
            lValues = GetExtensionInfo(lExt.lower())
            print lValues
            try:
                lCommand = GetCommand(lValues['File Type'], lKey)
            except Exception, e:
                tkMessageBox.showinfo('Command Extraction Error',lKey + ' not available for ' + lExt + ':' + str(e))

    lPos = lCommand.rfind("%1")
    if lPos >= 0:
        lCommand = lCommand.replace("%1", pFilePath)
    lPos = lCommand.rfind("%*")
    if lPos >= 0:
        lCommand = lCommand.replace("%*", "")


    return lCommand
                             

def Build(pMenuName, pFileName, pLabelList, pFileNames):
    'Build window and event handlers'
#    
    lFile = open(pMenuName,'r')
    lFileText = lFile.readlines()
    lFile.close

    pFileName = pFileName.center(60)
    TopLabel = Tkinter.Label(frame, text=pFileName, bg="#FF0000")
    TopLabel.pack(side=TOP, fill=X)
    lKeep = False

    def jumpfirst(pEvent, pFileNames=pFileNames, pLabel=TopLabel):
        'Event handler for First file button'
        lPos = 0
        pLabel.config(bg="#FF0000")
        PrevButton.config(state=DISABLED)
        NextButton.config(state=NORMAL)
        lFileName = pFileNames[lPos].center(60)
        pLabel.config(text = lFileName)

    def jumplast(pEvent, pFileNames=pFileNames, pLabel=TopLabel):
        'Event handler for First file button'
        lPos = len(pFileNames)-1
        pLabel.config(bg="#00FFFF")
        NextButton.config(state=DISABLED)
        PrevButton.config(state=NORMAL)
        lFileName = pFileNames[lPos].center(60)
        pLabel.config(text = lFileName)

    def jumpnext(pEvent, pFileNames=pFileNames, pLabel=TopLabel):
        'Event handler for next file button'
        lFileName = pLabel.cget("text").strip()
        lPos = pFileNames.index(lFileName)
        lPos += 1
        if lPos >= len(pFileNames):
            lPos -= 1
            pLabel.config(bg="#00FFFF")
            NextButton.config(state=DISABLED)
        else:
            pLabel.config(bg="#FF8800")
        PrevButton.config(state=NORMAL)
        lFileName = pFileNames[lPos].center(60)
        pLabel.config(text = lFileName)

    def jumpprevious(pEvent, pFileNames=pFileNames, pLabel=TopLabel):
        'Event handler for previous file button'
        lFileName = pLabel.cget("text").strip()
        lPos = pFileNames.index(lFileName) - 1
        if lPos <= 0 :
            lPos = 0
            pLabel.config(bg="#FF0000")
            PrevButton.config(state=DISABLED)
        else:
            pLabel.config(bg="#FF8800")
        NextButton.config(state=NORMAL)
        lFileName = pFileNames[lPos].center(60)
        pLabel.config(text=lFileName)

    def OKed(pEvent, pLabel=TopLabel, pFileNames=pFileNames):
        'Update file selection'
        global mFileList, mMessage
        lPos = mFileList.curselection()
        if len(lPos) > 0:
            lText = mFileList.get(lPos[0])
        else:
            lText = ''
        lPos = pFileNames.index(lText)
        if lPos == 0:
            pLabel.config(bg="#FF0000")
            PrevButton.config(state=DISABLED)
            NextButton.config(state=NORMAL)
        elif lPos == len(pFileNames)-1:
            pLabel.config(bg="#00FFFF")
            NextButton.config(state=DISABLED)
            PrevButton.config(state=NORMAL)
        else:
            NextButton.config(state=NORMAL)
            PrevButton.config(state=NORMAL)        
            pLabel.config(bg="#FF8800")
        pLabel.config(text=lText)
        mMessage.config(text=lText)            

    def canceled(pEvent, pLabel=TopLabel):
        'Destroy file selection window'
        global TopLevel
        TopLevel.destroy()
        TopLevel = None

    def selectone(pEvent, pLabel=TopLabel, pFileNames=pFileNames):
        '''
        Build menu from menu file
        The menu file may contain commands to set the current directory and to
        set specified environment variables.  This is done while the file is
        being read.  They are not dependent on the selected button.  The last 
        command encountered will be active.
    
        set environment variable name to value
            ;#set`name=value
        set current directory to path
            ;#cd`path
        '''
        global mFileList, mMessage, TopLevel
        
        if TopLevel == None:
            TopLevel = Tkinter.Toplevel(width=60)
            lCurrentPath = pLabel.cget("text").strip()
            
            lFrame = Tkinter.Frame(TopLevel)
            lFrame.pack(side=TOP, fill=BOTH, expand=1)
            
            lScrollBar = Tkinter.Scrollbar(lFrame, orient=VERTICAL )
            lScrollBar.pack(side=RIGHT, fill=Y)
    
            mFileList = Tkinter.Listbox(lFrame, yscrollcommand=lScrollBar.set)
            mFileList.pack(side=LEFT, fill=BOTH, expand=1)
            mFileList.bind("<Double-Button-1>", OKed)
    
            lScrollBar.config(command=mFileList.yview)
            
            lFrame = Tkinter.Frame(TopLevel)
            lFrame.pack(side=TOP, fill=X)
            lCancel = Tkinter.Button(lFrame, text='Cancel', bg="#FF0000")
            lCancel.pack(side=LEFT)
            lCancel.bind("<Button-1>", canceled) 
            
            lOK = Tkinter.Button(lFrame, text='Apply', bg="#00FF00")
            lOK.pack(side=RIGHT)
            lOK.bind("<Button-1>", OKed) 
            
            mMessage = Tkinter.Label(lFrame, text='-----')
            mMessage.pack(side=LEFT, fill=X, expand=1)
            lPos = 0
            lCurrent = -1
            for lFilePath in pFileNames:
                mFileList.insert(END, lFilePath)
                if lCurrentPath == lFilePath:
                    mFileList.selection_set(END)
                    mMessage.config(text=lCurrentPath)
                    lCurrent = lPos
                    mFileList.see(lCurrent)
                lPos += 1

    def submitnow(pEvent, pLabel=TopLabel):
        'Expand and execute command'
        lPrompt = pEvent.widget.cget("text")
        lFilePath = pLabel.cget("text").strip()
        lCommand = mCmds[lPrompt]
        lCommand = Expand(lCommand, lFilePath)
        
        lCommand = '"' + lCommand + '"'
        lProcess = subprocess.Popen(lCommand, shell=True)

    def showit(pEvent, pLabel=TopLabel):
        'Expand and display command'
        lPrompt = pEvent.widget.cget("text")
        lFilePath = pLabel.cget("text").strip()
        lCommand = mCmds[lPrompt]
        lCommand = Expand(lCommand, lFilePath)
        tkMessageBox.showinfo('Expanded command:',lPrompt + " = " + lCommand)

    if len(pFileNames) > 1:
        lFrame = Tkinter.Frame(frame)
        lFrame.pack(side=TOP, fill=X)

        SelectButton = Tkinter.Button(lFrame, text="*")
        SelectButton.pack(side=LEFT, fill=X, expand=1)
        SelectButton.bind("<Button-1>", selectone) 
        
        FirstButton = Tkinter.Button(lFrame, text="|<-")
        FirstButton.pack(side=LEFT, fill=X, expand=1)
        FirstButton.bind("<Button-1>", jumpfirst) 
      
        NextButton = Tkinter.Button(lFrame, text="->")
        NextButton.pack(side=LEFT, fill=X, expand=1)
        NextButton.bind("<Button-1>", jumpnext) 
      
        PrevButton = Tkinter.Button(lFrame, text="<-")
        PrevButton.pack(side=LEFT, fill=X, expand=1)
        PrevButton.bind("<Button-1>", jumpprevious) 

        LastButton = Tkinter.Button(lFrame, text="->|")
        LastButton.pack(side=LEFT, fill=X, expand=1)
        LastButton.bind("<Button-1>", jumplast) 
      
    for lText in lFileText:
        if len(lText) > 1:
            if lText[0] != "[":
                if lText[0] == "-":
                    pass
                    #label= Tkinter.Label(frame,text=lText[:-1])
                    #label.pack(side=TOP, fill=X)
                elif lText.startswith(";#"):        # commands begin with ;#
                    lPos = lText.find("`")          # command fields are separated by `
                    if lPos > 0:
                        lCh = lText[2]
                        if lCh == 's':              # set environment variable
                            lEqPos = lText.find("=")
                            if lEqPos > lPos:
                                lKey = lText[lPos+1:lEqPos].strip()
                                lValue = lText[lEqPos+1:].strip()
                                os.environ[lKey] = lValue
                        elif lCh == 'c':            # set working directory
                            if lPos > 0 and lPos < len(lText):
                                os.chdir(lText[lPos+1:].strip())
                        else:                       # ignore
                            pass 

                elif lText[0] == ';':
                    pass
                elif lKeep == False:
                    pass
                else:
                    lPos = lText.find(",")
                    if lPos > 0:
                       lPrompt = lText[:lPos]
                       lCommand = lText[lPos+1:]
                       
                       mCmds[lPrompt] = lCommand
                       button = Tkinter.Button(frame,text=lPrompt)
                       button.pack(side=TOP,fill=X)
                       button.bind("<Button-1>", submitnow) ### (1)
                       button.bind("<Button-3>", showit)

            else:
                label = lText[1:-2].lower()
                if (label[0] < 'a') or (label[0] > 'z'):
                    label = label[1:]
                if pLabelList == [] or label in pLabelList:
                    lKeep = True
                    label = Tkinter.Label(frame,text=lText[1:-2], bg="yellow")
                    label.pack(side=TOP, fill=X)
                else:
                    lKeep = False
    return TopLabel

#sys.argv.append('c:\\source\\python\\projects\\execution\\first test.ini')    # <- Controlling file
#sys.argv.append('c:\\source\\python\\projects\\execution\\*.py')             # <- Controlling file
#sys.argv.append('c:\\source\\python\\projects\\execution\\first test.ini')    # <- Menu file
#sys.argv.append('test')                                                       # <- Sections
#sys.argv.append('copy')

tk = Tkinter.Tk()                
if len(sys.argv) > 1:
    mFileName = mFileArg = sys.argv[1]          # First argument is absolute path to file to be processed or a
                                                # path template ( c:\bin\*.py ).  If a path template is used
                                                # The buttonbar will contain controls to select files from a
                                                # list of matching files.
    mFileName = mFileName.replace("/","\\")
    lPos = mFileName.rfind("\\")
    if lPos > 0:                                # Path to file, file will be controlling file
        mFileArg = mFileName
        lFileFolder = mFileName[0:lPos+1]
        mFileName = mFileName[lPos+1:]
    elif lPos == 0:
        lFileFolder = "c:\\"
        mFileName =  mFileName[1:]
        mFileArg = lFileFolder + mFileName
    else:
        lFileFolder = os.getcwd() + "\\"
        mFileArg = lFileFolder + mFileName
        
    if len(sys.argv) > 2:                        # Second argument is path to initialization file used to
        mMenuName = sys.argv[2]                  # generate button bar
    else:
        mMenuName = "c:\\bin\\Tools Menu.ini"    # <---- Default menu file - Change as necessary
        
    if len(sys.argv) > 3:
        mLabelList = sys.argv[3:]
    else:
        mLabelList = ["references" ]             # <---- Default section - Change as necessary
    mLabelList = [x.lower() for x in mLabelList]
    
    if mFileName.find("*") >= 0 or  mFileName.find("?") >= 0 or  mFileName.find("[") >= 0:  
        lFileNames = glob.glob(mFileArg)
        if len(lFileNames) > 0:
            mFileArg = lFileNames[0]
        else:
            tkMessageBox.showinfo('File selection error:',"No files matched '%s' in folder '%s'." % (mFileName, lFileFolder) )
            mFileArg = ''
            lFileNames = [ '' ]
    else:
        lFileNames = [ mFileArg ]   
    frame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
    frame.pack(fill=BOTH,expand=1)
    mTopLabel = Build(mMenuName, mFileArg, mLabelList, lFileNames)
    label = Tkinter.Label(frame,text="", bg="yellow")
    label.pack(side=TOP, fill=X)
    button = Tkinter.Button(frame,text='Exit',command=frame.quit)
    button.pack(side=TOP,fill=X)
    tk.mainloop()
                
else:
    tkMessageBox.showinfo('Syntax Error','File name required')
    
