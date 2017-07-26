'''
;#template` {-path} {-menu} {-s1} {-s2} {-s3}
;#option`-path`Path to controlling file`F`c:\source\python\projects\menu\buttonbar.py`
;#option`-menu`Path to menu file`F`c:\source\python\projects\menu\test.ini`
;#option`-s1`First section`X`info`
;#option`-s2`Second section`X`help`
;#option`-s3`Third section`X`data`
;#end

'''
# ----------------------------------------------
# Name: ButtonBarV1
# Description:
## D20E-119 Popup button bar using Qeditor style menus.ini file, selects sections to use (ExPopen)
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
#     @="c:\\sys\\python25\\python.exe   c:\\bin\\ButtonBarV1.py   \"%1\"  \"c:\\bin\\Text Tools.ini\"   tools  \"text tools\"   "
#

#
#     %1 is replaced by the selected file.  It is used to replace {a}, {b}, {n}, {f}, {p} etc. during command expansion.  
#     This string is used only for command expansion and for display at the top of the dialog.  If no expansion
#     is performed any string can be used and displayed.
#
#     The second parameter is the name of the initialization file shown below.  Each line contains a prompt displayed
#     on a button and a command separated by a comma.  Macros are replaced before execution.
#
#     The remaining parameters the sections to be used to make the button bar.  The order in the initialization file
#     is maintained.
#

# Example initialization file (Text Tools.ini)
#     [Text Tools]
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

import sys
import os
import Tkinter
from Tkconstants import *
import tkMessageBox
import subprocess

mCmds = {}

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
    lTempFolder    = "c:\\temp"                  # {t} <------------- Change these as necessary
    lInstallFolder = "c:\\bin"                   # {i}
    lBackupFolder  = "c:\\_Backup"               # {u}
    lSourceFolder  = "c:\\source"                # {c}
    lSystemFolder  = "c:\\sys"                   # {y}
    lWindowsFolder = "c:\\windows\\system32"     # {w}
    lArchiveFolder = "j:\\_Backup"               # {v}
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
    return lCommand
                             


def showit(pEvent):
    'View expansion of selected command'
    pPrompt = pEvent.widget.cget("text")
    pCommand = mCmds[pPrompt]
    tkMessageBox.showinfo('Expanded Command:',pPrompt + " = " + pCommand)

def submitnow(pEvent):
    'Execute selected command'
    pPrompt = pEvent.widget.cget("text")
    pCommand = mCmds[pPrompt]

    #               synchronous
    #f = os.popen(pCommand,"r")
    #print f.read()
    #f.close()

    #               synchronous
    #os.system(pCommand)

    pCommand = '"' + pCommand + '"'
    lCmd = subprocess.Popen(pCommand, shell=True)

def Build(pMenuName, pFileName, pLabelList):
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
#
    lFile = open(pMenuName,'r')
    lFileText = lFile.readlines()
    lFile.close

    label = Tkinter.Label(frame, text=pFileName)
    label.pack(side=TOP, fill=X)
    lKeep = False
   
    for lText in lFileText:
        if len(lText) > 1:
            if lText[0] != "[":
                if lText[0] == "-":
                    pass
                    #label= Tkinter.Label(frame,text=lText[:-1])
                    #label.pack(side=TOP, fill=X)
                elif lText.startswith(";#"):        # <---- Special commands start with ;#
                    lPos = lText.find("`")          # <---- Fields are separated by `
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
                elif lText[0] == ";":
                    pass
                elif lKeep == False:
                    pass
                else:
                    lPos = lText.find(",")
                    if lPos > 0:
                        lPrompt = lText[:lPos]
                        lCommand = lText[lPos+1:]

                        lCommand = Expand(lCommand, pFileName)
                        
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

tk = Tkinter.Tk()                
if len(sys.argv) > 1:
    mFileName = sys.argv[1]                      # First argument is absolute path to file to be processed 
    mFileName = mFileName.replace("/","\\")
    if len(sys.argv) > 2:                        # Second argument is absolute path to initialization file used to
        mMenuName = sys.argv[2]                  # generate button bar
    else:
        mMenuName = "c:\\bin\\Tools Menu.ini"    # <------- Default menu - Change this
    if len(sys.argv) > 3:
        mLabelList = sys.argv[3:]
    else:
        mLabelList = [ "references" ]            # <------- Default section - Change this
    mLabelList = [x.lower() for x in mLabelList]
        
    frame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
    frame.pack(fill=BOTH,expand=1)
    
    Build(mMenuName, mFileName, mLabelList)
    
    label = Tkinter.Label(frame,text="", bg="yellow")
    label.pack(side=TOP, fill=X)
    button = Tkinter.Button(frame,text='Exit',command=frame.quit)
    button.pack(side=TOP,fill=X)
    tk.mainloop()

else:
    tkMessageBox.showinfo('Syntax Error','File name required')
    
tk.destroy()
    
    
