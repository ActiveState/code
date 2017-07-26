'''
;#template` {-path} {-menu} {-s1} {-s2} {-s3}
;#option`-path`Path to controlling file`F`c:\source\python\projects\menu\buttonbar.py`
;#option`-menu`Path to menu file`F`c:\source\python\projects\menu\test.ini`
;#option`-s1`First section`X`info`
;#option`-s2`Second section`X`help`
;#option`-s3`Third section`X`data`
;#end

'''
mHelpText = '''
# ----------------------------------------------
# Name: ButtonBarV1Ex
# Description:
## D20G-76 Popup button bar using Qeditor style menus.ini file, selects sections to use (ExPopen)
#
# Author: Philip S. Rist
# Date: 10/27/2010
# Copyright 2010 by St. Thomas Software
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
#     @="c:\\sys\\python25\\python.exe   c:\\bin\\ButtonBarV1Ex.py   \"%1\"  {p}\\menus.ini;{o}\\menus.ini;c:\\bin\\menus.ini   ide     "
#

#
#     Syntax:
#         ButtonBarV1Ex.py  [options] <file path> <menu path> <first section> [ <another section> ... ]
#
#     Options:
#
#         -b <color>        - default button background color
#         -d <directory>    - set working directory
#         -e <name>=<value> - set environment variable
#         -h                - print help text
#         -l <color>        - default label background color
#         -o                - set orientation to horizontal
#
#     The command line template extracted from the menu file may contain macros of the form '{x}' which
#     are replaced by parts of the file path or other string.  The Do.py and Do2.py modules are used.
#     %1 is replaced by the selected file path.  The file path string is also used for display 
#     at the top of the button bar.  If no expansion is performed any string can be used and displayed.
#
#     The second parameter is the name of an initialization file similar to the one shown below.  
#     Each line contains a prompt displayed on a button and a command separated by a comma.  
#     Macros are replaced before execution.
#
#     The remaining parameters name sections to be used to make the button bar.  The order in the 
#     initialization file is maintained.  Selection is case insensitive.
#
#     Do.py and Do2.py are used to expand the command line, the menu selection and each section
#     name.  The command line can also contain '{pr}' which will be replaced by the prompt
#     displayed on the button.  Also, any string enclosed in braces not a macro will be taken
#     as a command name in the registry entry for the primary files file type.
#
#     The Menu File:
#
#     The menu file follows the syntax used by the QEditor menus.ini file.  The same syntax as an .ini 
#     file except a ',' is used to separate key from value.  In this case the values are command
#     line templates usually containing one or more macro strings.
#
#     Lines beginning with ';' are comments unless followed by '#' in which case the line may contain 
#     a special command.  Command line options are also available for the same functions
#
#     ;#cd`c:\bin               - Sets the working directory to c:\bin   or '-d c:\bin'
#     ;#set`abc=def             - Sets the environment variable abc to 'def' or '-s abc=def'
#     ;#button`#00CCCC          - Sets the background of succeeding buttons to #00CCCC. or '-b #00CCCC'
#     ;#label`light blue        - Sets the background of labels created by succeeding '-' lines
#                                 to light blue.  If included before the first section the
#                                 color will also be used for section header labels   or '-l "light blue"'
#     Within sections not included in the button bar special commands are ignored.  The '`' usually
#     appears under the '~' on the keyboard.
#
#     -o option will produce a horizontal button bar
#
#     Section names and command prompts can contan a file pattern enclosed within two '/' or two '!'
#     to include the section or line if the file path matches or does not match the pattern.  Examples
#     are shown below.
#     

# Example initialization file (Text Tools.ini)

;#set`test=A Short String
;#set`use=c:\sys\python27\pythonw.exe
;#set`gain=none
;#cd`\source\tcl
;#cd`c:\source\python\Projects\Program Execution
;#label`yellow

[Test1]
;#button`#00EEEE
;#label`#00CCCC
test 1,c:\bin\messagebox.exe  {a} {b} {p} "{f}" {n} {e} {o} %test%
-Directory List
Dir,c:\windows\system32\cmd.exe /C dir "{p}\*.{e}"
DirX,c:\windows\system32\cmd.exe /C dir *.*
Dir2,c:\windows\system32\cmd.exe /C dir c:\source\Python\*.*
;#label`light gray
-Program execution
/*.exe/Run,"{a}" I am running "{a}"
/*.py/Run,c:\bin\messagebox.exe I am running a Python program "{a}"
/*.py/Run 2,%use% "{a}"
/*.exe/Run 2,"{a}" I am running "{a}"

[/*.py/Test2]
Edit T,{o}\qeditor.exe "{a}"
Dir *,%comspec% /C dir {.}\*.*
'''

import sys
import os
import getopt
import fnmatch
import Tkinter
from Tkconstants import *
import tkMessageBox
from _winreg import *
import Do                              # Recipe: 577439
from Do2 import ExpandArg              # Recipe: 577440
from DoCommand import BuildCommand     # Recipe: 577441
import subprocess

mCmds = {}

def Expand(pCommand, pFilePath, pPrompt, pSep=','):
    '''
    Expand 
    '''

#   ---- Standard macro expansion with added {pr} macro
#        Can separate arguments with ',' fo force argument by argument 
#        expansion
    if pCommand.find(pSep) >= 0:
      try:
        lArgs = pCommand.split(pSep)     
        lCommand = ''
        lDefaultPath = pFilePath
        for lArg in lArgs:
            lVal = ExpandArg(lArg, pFilePath, lDefaultPath)
            if lVal.find('{pr}') >= 0:        # insert button prompt
                lVal = lVal.replace('{pr}', pPrompt)      
            lCommand = lCommand + lVal + " "
      except Exception, e:
        print 'BBV1Ex',e
    else:
        lCommand = Do.Expand(pCommand, pFilePath)
        if lCommand.find('{pr}') >= 0:
            lCommand = lCommand.replace('{pr}', pPrompt)

#   ---- Remove {} for compatibility with DoM.py
    lCommand = lCommand.replace('{}', ' ')

#   ---- Remaining macros will be replaced by command of same name
#        in registry
    lPos = lCommand.find("{")                      
    if lPos >= 0:                                 
        lEndPos = lCommand.find("}")
        if lEndPos > lPos:
            try:
                lKey = lCommand[lPos+1:lEndPos]
                lDotPos = lKey.rfind('.')
                if lDotPos > 0:
                    lExt = lKey[lDotPos]
                    lKey = lKey[0:lDotPos]
                else:
                    lDotPos = pFilePath.rfind('.')
                    lExt = pFilePath[lDotPos:]
                lReplace = BuildCommand(pFilePath, lKey, lExt, [])
                lCommand = lCommand[0:lPos] + lReplace + lCommand[lEndPos+1:]
            except:
                pass

#   ---- replace %1 and %*
    else:
        lPos = lCommand.rfind("%1")
        if lPos >= 0:
            lCommand = lCommand.replace("%1", pFilePath)
        lPos = lCommand.rfind("%*")
        if lPos >= 0:
            lCommand = lCommand.replace("%*", "")

#   ---- Remove !! used by DoM.py
    lPos = lCommand.rfind('!!')
    if lPos > 0:
        lCommand = lCommand[0:lPos]

    return lCommand

def showit(pEvent):
    'View expansion of selected command'
    lPrompt = pEvent.widget.cget("text")
    lCommand = mCmds[lPrompt]
    lCommand = Expand(lCommand, mFileName, lPrompt)
    
    tkMessageBox.showinfo('Expanded Command:', lPrompt + " = " + lCommand)

def submitnow(pEvent):
    'Execute selected command'
    lPrompt = pEvent.widget.cget("text")
    lCommand = mCmds[lPrompt]
    lCommand = Expand(lCommand, mFileName, lPrompt)
    lCommand = '"' + lCommand + '"'
    subprocess.Popen(lCommand, shell=True)

def Commands():
    return mCmds

def Build(pFrame, pMenuName, pFileName, pLabelList, pSubmit=submitnow, pCallBack=None,
              pDefaultLabel='yellow', pDefaultButton='light blue', pSide=TOP, pFill=X):
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
    set label background color
        ;#label`color
    set button background color
        ;#button`color
    '''
#
    lPos = pFileName.rfind('\\')
    if lPos >= 0:
        lFileName = pFileName[lPos+1:].lower()
    else:
        lFileName = pFileName.lower()

    lExist = os.path.exists(pFileName)
        
    lFile = open(pMenuName,'r')
    lFileText = lFile.readlines()
    lFile.close

    lDefaultButton = lButtonColor = pDefaultButton
    lDefaultLabel = lLabelColor = pDefaultLabel
    label = Tkinter.Label(pFrame, text=pFileName, bg=lLabelColor)
    #label.pack(side=TOP, fill=X)
    label.pack(side=pSide, fill=pFill)
    lKeep = False
    lSectionCount = 0
   
    for lText in lFileText:
        if len(lText) > 1:
            if lText[0] != "[":

#               ---- Menu splitter line
                if lText[0] == "-" and lKeep:
                    if len(lText) > 1:
                        lPrompt = lText[1:-1]
                        if lPrompt.find('{') >= 0:
                            lPrompt = ExpandCmd(lPrompt, pFileName)
                                
#                   ---- Display label for - line                                
#                            can be removed without affecting remainder of program
                    if len(lPrompt) > 0 and lKeep == True:
                        label= Tkinter.Label(pFrame, text=lPrompt, bg=lLabelColor)
                        #label.pack(side=TOP, fill=X)
                        label.pack(side=pSide, fill=pFill)

#               ---- process special command
                elif lText.startswith(";#") and (lSectionCount == 0 or lKeep == True): 
                    lPos = lText.find("`")          # <---- Fields are separated by ` (below ~)
                    if lPos > 0:
                        lCh = lText[2]

#                       ---- Set environment variable
                        if lCh == 's':              # set environment variable
                            lEqPos = lText.find("=")
                            if lEqPos > lPos:
                                lKey = lText[lPos+1:lEqPos].strip()
                                lValue = lText[lEqPos+1:].strip()
                                if lValue.find('{') >= 0:
                                    lValue = ExpandCmd(lValue, pFileName)
                                os.environ[lKey] = lValue

#                       ---- Change working directory
                        elif lCh == 'c':            # set working directory
                            if lPos > 0 and lPos < len(lText):
                                lText = lText[lPos+1:].strip()
                                if lText.find('{') >= 0:
                                    lText = ExpandCmd(lText, pFileName)
                                os.chdir(lText)
                                
                        elif lCh == 'b':
                            lButtonColor = lText[lPos+1:].strip().lower()
                            if lSectionCount == 0:
                                lDefaultButton = lButtonColor

                        elif lCh == 'l':
                            lLabelColor = lText[lPos+1:].strip().lower()
                            if lSectionCount == 0:
                                lDefaultLabel = lLabelColor

                        elif pCallBack != None:
                            pCallBack(lText)
                            
                        else:                       # ignore
                            pass 

#               ---- Comment                            
                elif lText[0] == ";":
                    pass

#               ---- Menu section is being skipped
                elif lKeep == False:
                    pass

#               ---- Command template
                else:
                    lPos = lText.find(",")
                    if lPos > 0:
                        lPrompt = lText[:lPos]
                        lCommand = lText[lPos+1:]

#                       ---- Filter commands based on match with file name
#                            /*3.py/Run,c:\source\python31\pyrhonw.exe ...
#                            can be removed without affecting remainder of program
                        if lPrompt[0] == '/':
                            try:
                                (lMask, lPrompt) = lPrompt[1:].split('/')
                                if not fnmatch.fnmatch(lFileName, lMask.lower()):
                                    continue
                            except Exception, e:
                                continue
                                
#                       ---- Filter commands based on mismatch with file name
#                            !*3.py!Run,c:\source\python27\pythonw.exe ...
#                            can be removed without affecting remainder of program
                        elif lPrompt[0] == '!':
                            try:
                                (lMask, lPrompt) = lPrompt[1:].split('!')
                                if fnmatch.fnmatch(lFileName, lMask.lower()):
                                    continue
                            except Exception, e:
                                continue

#                       ---- Create toolbar button                        
                        mCmds[lPrompt] = lCommand
                        try:
                            button = Tkinter.Button(pFrame, text=lPrompt, bg=lButtonColor)
                        except:
                            button = Tkinter.Button(pFrame, text=lPrompt)
                        #button.pack(side=TOP,fill=X)
                        button.pack(side=pSide, fill=pFill)
                        button.bind("<Button-1>", pSubmit) ### (1)
                        button.bind("<Button-3>", showit)

#           ---- Section Header
            else:
                lSectionCount += 1
                lLabelColor = lDefaultLabel
                lButtonColor = lDefaultButton
                if lText.find('{') >= 0:
                    lText = ExpandCmd(label, pFileName)
                label = lText[1:-2].lower()

#               ---- Filter section based on match with file name
#                    [/*3.py/Special]
#                    can be removed without affecting remainder of program
                if label[0] == '/':
                    try:
                        (lMask, label) = label[1:].split('/')
                        if not fnmatch.fnmatch(lFileName, lMask.lower()):
                            lKeep = False
                            continue
                    except Exception, e:
                        lKeep = False
                        continue
                        
#               ---- Filter section based on mismatch with file name
#                    [!*3.py!Special]
#                    can be removed without affecting remainder of program
                elif label[0] == '!':
                    try:
                        (lMask, label) = label[1:].split('!')
                        if fnmatch.fnmatch(lFileName, lMask.lower()):
                            lKeep = False
                            continue
                    except Exception, e:
                        lKeep = False
                        continue

#               ---- label must begin with letter
                elif (label[0] < 'a') or (label[0] > 'z'):
                    label = label[1:]

#               ---- Select/Unselect section                    
                if pLabelList == [] or label in pLabelList:
                    lKeep = True
                    label = Tkinter.Label(pFrame,text=label.capitalize(), bg=lLabelColor)
                    #label.pack(side=TOP, fill=X)
                    label.pack(side=pSide, fill=pFill)
                else:
                    lKeep = False
                    
    label = Tkinter.Label(pFrame,text="", bg=lLabelColor)
    #label.pack(side=TOP, fill=X)
    label.pack(side=pSide, fill=pFill)
    button = Tkinter.Button(pFrame,text='Exit', command=pFrame.quit, bg=lButtonColor)
    #button.pack(side=TOP, fill=X)
    button.pack(side=pSide, fill=pFill)

if __name__ == '__main__':
    (mOptions, mArgs) = getopt.getopt(sys.argv[1:], 'b:d:e:hl:o')

#   ---- Set run options
    mDefaultLabel = 'light green'
    mDefaultButton = 'light blue'
    mOrient = VERTICAL
    for (mKey, mValue) in mOptions:
        if mKey == '-b':
            mDefaultButton = mValue
            
        elif mKey == '-d':                 # Set current directory
            if mValue.find('}') >= 0:
                mValue = Expand(mValue, mFileName)
            os.chdir(mValue)
            
        elif mKey == '-e':               # Set environment variable
            Do.setenviron(mValue, mFileName)

        elif mKey == '-h':
            print mHelpText
            
        elif mKey == '-l':
            mDefaultLabel = mValue
            
        elif mKey == '-o':
            mOrient = HORIZONTAL
    
    tk = Tkinter.Tk()                
    if len(mArgs) > 0:
    
        try:
            mDefaultMenu = os.environ['MENUPATH']
            if mVerbose:
                print 'BB1Ex Default menu path', mDefaultMenu
        except:
            mDefaultMenu = ''

                 
        try:
            mDefaultSection = os.environ['SECTION']
            if mVerbose:
                print 'BB1Ex Default section', mDefaultSection
        except:
            mDefaultSection = ''             # <------- Default section - Change this
        if mDefaultSection == '':
            mDefaultSection = ''
  
#       ---- First argument is absolute path to file to be processed
        mFileName = mArgs[0]                    
        mFileName = mFileName.replace("/","\\")
        
#       ---- Second argument is absolute path to initialization menu 
#                    Selected menu can depend on file path (ie. {o}\menus.ini) See do2.py
        if len(mArgs) > 1:                       
            mMenuArg = mArgs[1]                 # generate button bar
            mMenuArg += ';' + mDefaultMenu
        else:
            mMenuArg = mDefaultMenu        
    
#       ---- Prevent QEditor from performing replacement, may be removed                
        mMenuArg = mMenuArg.replace("(","{")
        mMenuArg = mMenuArg.replace(")","}")

#       ---- Expand menu name and/or select from list
        if mMenuArg.find('{') >= 0:
            mMenuName = ExpandArg(mMenuArg, mFileName, mDefaultMenu)
        elif mMenuArg.find(';') >= 0:
            for mMenu in mMenuArg.split(';'):
                if os.path.exists(mMenu):
                    mMenuName = mMenu
                    break
            else:
                mMenuName = mDefaultMenu 
        else:
            mMenuName = mMenuArg
        
    
#       ---- Remaining arguments list sections to include in menu
        if len(mArgs) > 2:
            mLabelList = []
            for lItem in mArgs[2:]:
                if lItem == '*':
                    break
                if lItem == '-':
                     lItem = mDefaultSection
                lItem = lItem.lower()
#               ---- Prevent QEditor from performing replacement, may be removed                
                lItem = lItem.replace("(","{")
                lItem = lItem.replace(")","}")
#               ---- Selected section can be dependent on file path                
                if lItem.find('{') >= 0:
                    lItem = ExpandArg(lItem, mFileName, '')
                mLabelList.append(lItem)
                
        elif mDefaultSection != '':
            mLabelList = [ mDefaultSection ]
            
        else:
            mLabelList = [ ]  
        
#       ---- Build buttonbar
        mFrame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
        mFrame.pack(fill=BOTH, expand=1)
        if mOrient == VERTICAL:
            Build(mFrame, mMenuName, mFileName, mLabelList, pDefaultLabel=mDefaultLabel, pDefaultButton=mDefaultButton, pSide=TOP, pFill=X)
        else:
            Build(mFrame, mMenuName, mFileName, mLabelList, pDefaultLabel=mDefaultLabel, pDefaultButton=mDefaultButton, pSide=LEFT, pFill=Y)

#       ---- Enter event loop
        tk.mainloop()
    else:
        tkMessageBox.showinfo('Syntax Error','File name required')
        
   
        
        
    
    
