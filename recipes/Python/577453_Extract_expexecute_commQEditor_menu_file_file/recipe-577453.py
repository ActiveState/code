mHelpText = '''
# ----------------------------------------------
# Name: DoM
# Description: Expand and execute command from menu
## D20H-53 Expand and execute command
#
# Author: Philip S. Rist
# Date: 10/26/2010
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

# DoM.py -
# The specified command in the specified section in the specified menu file will
# be expanded with Do.py and executed.

# Usage examples:
#
#[HKEY_CLASSES_ROOT\*\Shell\Rundom]
#@="Run"
#"EditFlags"=hex:01,00,00,00
#[HKEY_CLASSES_ROOT\*\Shell\Rundom\Command]
#@="c:\\sys\\python25\\pythonw.exe c:\\bin\\dom.py -m c:\bin\menus.ini \"%1\" project open     "
#

# Syntax:
#        dom.py [ options ] <file path> <section> <command key>
#
# Options:
#        -d <path>         - set current working directory
#        -e <name>=<value> - set environment variable
#        -h                - display this text, everything else is ignored
#        -l                - list available commands, everything else is ignored
#        -m <menu path>    - set path to menu file
#                 default: '{o}\menus.ini;{i}\menus.ini'   <- can be changed
#        -v                - run in verbose mode

# Sample menu file

[DOS]
Open,c:\source\TextFiles\qeditor.exe                 "{a}"
; Open file
Print,c:\windows\nodepad.exe                        /P "{a}"
; Print file
Edit,c:\windows\system32\wscript.exe                 c:\bin\editit.vbs "{a}"
; Edit file with Notetab
Save,C:\Windows\system32\wscript.exe                 c:\bin\Util.vbs  /S  "{a}"
Has Been Ssved,C:\Windows\system32\wscript.exe                  c:\bin\Util.vbs  /K  "{a}"
UnTabify,c:\sys\python25\python.exe                  c:\sys\python25\tools\scripts\untabify.py     "{a}"
U2M,c:\bin\u2m.bat                                  "{a}"
Echo,c:\bin\messagebox.exe                          "{a}"
Dir,c:\windows\system32\cmd.exe   /C                dir "{p}\*.{e}"
'''

import sys
import os
import getopt
import Do              # Recipe: 577439
import Do2             # Recipe: 577440

import subprocess

def FindCommand(pKey, pFilePath, pSearchPath, pSection, pList=False, pVerbose=False):
    '''
    Find command keyword and extract containing line
    pKey         -- String identifying line to use as command template
    pFilePath    -- File to use in macro expansion
    pSearchPath  -- File to scan for command 
    pSection     -- Section containing command
    pList        -- 
    '''
    if pVerbose:
        print 'DoM.py FindCommand:', pKey, pFilePath, pSearchPath, pSection
    
    if not os.path.exists(pSearchPath):
        lCommand = ''
        print 'DoM.py Could not find menu file', pSearchPath
    else:
        lSection = pSection.lower()
        lKey = pKey.lower()

#       ---- Load menu file
        lFile = open(pSearchPath, 'r')
        lText = lFile.readlines()
        lFile.close()
        if len(lText) < 1:
            print 'DoM.py Menu', pSearchPath, 'read failed'

        lFound = False
        lCommand = ''
        lCount = 0
        if pList:
            print 'DoM.py Available commands in', pSearchPath

#       ---- Scan menu file
        for lLine in lText:
            lLine = lLine.lstrip()
            if len(lLine) < 1:
                continue

#           ---- Start of section
            if lLine[0] == '[':
                lCount = 0
                lPos = lLine.find(']')
                if lPos > 0:
                    lFoundSection = lLine[1:lPos].lower()
                else:
                    lFoundSection = ''
                    
#               ---- Check for conditions, conditions are ignored                    
                if lFoundSection[0] == '/':
                    lPos2 = lFoundSection.rfind('/')
                    if lPos2 >= 0:
                        lFoundSection = lFoundSection[lPos2+1:]
                elif lFoundSection[0] == '!':
                    lPos2 = lFoundSection.rfind('!')
                    if lPos2 >= 0:
                        lFoundSection = lFoundSection[lPos2+1:]
                #if lSection != lFoundSection and lSection != '*':
                if not lFoundSection.startswith(lSection) and lSection != '*':
                    if pVerbose:
                        print 'DoM.py not found', lSection, 'in', lFoundSection
                    if lFound == True:
                        break
                    continue
                elif lSection != '*' and lFound == True:
                    break
                else:
                    if pVerbose:
                        print 'DoM.py found', lSection, 'in', lFoundSection
                    if pList:
                        print 'DoM.py Section:', lFoundSection
                    lFound = True

#           ---- Comments
            elif lLine[0] == ';':
                if lFound and pList:
                    print 'DoM.py        ', lLine,

#           ---- Command lines and label lines
            else:
                if not lFound:
                    continue
                if lLine[0] == '-':
                    continue
                lPos = lLine.find(',')
                if lPos > 0:
                    lMatch = lLine[0:lPos].lower()
                else:
                    continue
                    
#               ---- Check for conditions, conditions are ignored                    
                if lMatch[0] == '/':
                    lPos2 = lMatch.rfind('/')
                    if lPos2 >= 0:
                        lMatch = lMatch[lPos2+1:]
                elif lMatch[0] == '!':
                    lPos2 = lMatch.rfind('!')
                    if lPos2 >= 0:
                        lMatch = lMatch[lPos2+1:]
                
                lCount += 1
                if pList:
                    if lPos > 0:
                        lLineText = lLine[lPos+1:]
                    print "DoM.py %5d: %-20s| %s" % (lCount, lMatch, lLineText),

#               ---- Check for matching command
                #if lKey == lMatch:                   # must match command key
                if lMatch.startswith(lKey):           # command key starts with key
                    lCommand = lLine[lPos+1:]
                    if pVerbose:
                        print 'DoM.py found command', lKey, 'in', lMatch, 'for', lCommand
                    break
        else:
            print 'DoM.py no command found in', pSearchPath, pSection
                    
    return lCommand[0:-1]


def Expand(pArgs, pFilePath, pSearchPath, pSection, pSep='!!', pList=False, pVerbose=False):
    '''
    Extract command from file and replace all macros
    pArgs        -- Args passed to program except file path and section name
    pFilePath    -- File to use in macro expansion
    pSearchPath  -- File to scan for command '
    pCount       -- Number of lines at the start of the file to scan
    pSep         -- String used to identify end of command
    pHelp        -- True to display available commands
    '''
#   ---- Find command    
    lCommand = FindCommand(pArgs[0], pFilePath,  pSearchPath, pSection, pList=pList, pVerbose=pVerbose)
    
#   ---- Expand and insert/append any passed arguments       
#        Arguments on original pb.py command line will replace {} from left to right
#        otherwise they will be appended to the end of the command 
    lStart = 1
    if len(lCommand) > 0:
        if len(pArgs) > lStart:
            for lArg in pArgs[lStart:]:
                if lArg.find('{') >= 0:
                    lArg = Do2.ExpandArg(lArg, pFilePath, '')
                if len(lArg) > 0:
                    try:
                        lTest = os.path.abspath(lArg)
                        if os.path.exists(lTest):
                            if lTest.find(" ") > 0:
                                lTest = '"' + lTest + '"'
                            lArg = lTest
                    except:
                        pass
                lPos = lCommand.find('{}')
                if lPos >= 0:
                    lCommand = lCommand[0:lPos] + lArg + lCommand[lPos+2:]
                else:
                    lCommand += ' ' + lArg
    
#   ---- Prevent unwanted arguments appended to command                    
    lPos = lCommand.rfind(pSep)
    if lPos > 0:
        lCommand = lCommand[0:lPos]
    
#   ---- Expand all remaining macros
    if lCommand.find('{') >= 0:
        lCommand = Do.Expand(lCommand, pFilePath)
        
    return lCommand
 
def submitnow(pArgs, pFilePath, pSearchPath, pSection, pVerbose, pList=False):
    'Expand and submit command'
    if pVerbose:
        print 'DoM.py File path:', pFilePath
        print 'DoM.py Menu path:', pSearchPath
        print 'DoM.py Section:  ', pSection
        print 'DoM.py Arguments:', pArgs

    lCommand = Expand(pArgs, pFilePath, pSearchPath, pSection, pList=pList, pVerbose=pVerbose)
#   ---- Any macro not expanded will be assumed to be an environment variable
#        If %...% had been used it would have been replaced when pb.py was run    
    lCommand = lCommand.replace('{}',' ')    #<-- may want to do something else
    lCommand = lCommand.replace('{', '%')    # try to replace with environment variable
    lCommand = lCommand.replace('}', '%')
    if len(lCommand) == 0:
        print 'DoM.py Expansion failed'
    else:
        lCommand = '"' + lCommand + '"'
        if pVerbose:
            print 'DoM.py Submitting: ', lCommand
        subprocess.Popen(lCommand, shell=True)

def setenviron(pValue, pFileName):
    'Set environment variable'
    lParts = pValue.split('=')
    if len(lParts) > 1:
        lKey = lParts[0]
        lValue = lParts[1]
        if lValue.find('{') >= 0:
            lValue = Do2.ExpandArg(lValue, pFileName, '')
        os.environ[lKey] = lValue
    else:
        os.environ[pValue] = ''

if __name__ == '__main__':
    (mOptions, mArgs) = getopt.getopt(sys.argv[1:], 'd:e:hlm:v')
    mVerbose = False
    mHelp = False
    mList = False
    mSearchPath = '{o}\menus.ini;{i}\menus.ini'
    
    for (mKey, mValue) in mOptions:
        if mKey == '-d':                 # Set current directory
            if mValue.find('{') >= 0:
                if len(mArgs) > 2:
                    mFilePath = os.path.abspath(mArgs[0])
                    mValue = Do.ExpandArg(mValue, mFilePath)
                else:
                    print 'DoM.py No primary file, could not set directory'
                    break
            else:
                os.chdir(mValue)
            
        elif mKey == '-e':               # Set environment variable
            setenviron(mValue, mFilePath)

        elif mKey == '-h':
            print mHelpText
            mHelp = True

        elif mKey == '-l':
            mList = True

        elif mKey == '-m':               #
            mSearchPath = mValue

        elif mKey == '-v':
            mVerbose = True
                
    if len(mArgs) > 2:
        mFilePath = os.path.abspath(mArgs[0])
        

        mSection = mArgs[1]
        if mSection.find('{'):
            mSection = Do.Expand(mSection, mFilePath)

        mKey = mArgs[2]
        if mKey.find('{'):
            mArgs[2] = Do.Expand(mKey, mFilePath)
        mArgs[2] = mArgs[2].replace('_', ' ')

                
        if mSearchPath.find('{') >= 0:
            mSearchPath = Do2.ExpandArg(mSearchPath, mFilePath, '')
            if mSearchPath[0] == '"':
                mSearchPath = mSearchPath[1:-1]
        mSearchPath = os.path.abspath(mSearchPath)

        if mHelp:
            print 'DoM.py Default menu:   ', mSearchPath
            print 'DoM.py Default section:', mSection
        elif mList:
            Expand('???', mFilePath, mSearchPath, mSection, mVerbose, mList)
        else:
            submitnow(mArgs[2:], mFilePath, mSearchPath, mSection, mVerbose)
            
    elif mHelp == False:
        print 'DoM.pyCommand and/or file path missing'
    

    
