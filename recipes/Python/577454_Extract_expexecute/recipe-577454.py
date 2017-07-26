#!Test c:\bin\messagebox.exe Display for {a} %xyz% {} {xyz} {} and {p}
##              #!Test2 c:\bin\messagebox.exe Display for {a} and {} with {} and {p}
#!Edit {o}\qeditor.exe {a}   !!
#       Run the #!Inst command
#! c:\bin\qeditor.exe   "{a}"        !!
#!py  c:\bin\messagebox.exe    "{a}" is a python program
#!Inst c:\windows\system32\cmd.exe /C copy "{a}" "{i}\{f}"     !!
#!BadI c:\windows\system32\cmd.exe /C copy "{a}" "{i}\{f}"     
#!Run  c:\sys\python27\pythonw.exe "{a}" list of arguments
##  #!OKI c:\windows\system32\cmd.exe /C copy "{a}" "{t}\{f}"     !!
#!pynew c:\bin\messagebox.exe Display for {a} new
#!oldpy c:\bin\messagebox.exe Display for "{a}" old

mHelpText = '''
# ----------------------------------------------
# Name: pb
# Description: Expand and execute command from file
## D20H-57 Expand and execute command
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

# pb.py -
# Scan file for specified #! keyword then expand and execute command following on line.
# See above for examples.  Scanned lines must be at the beginning of the file with no
# blank or shorx t lines preceeding them.
#
# Usage examples:
#
#[HKEY_CLASSES_ROOT\*\Shell\Runpb]
#@="Run"
#"EditFlags"=hex:01,00,00,00
#[HKEY_CLASSES_ROOT\*\Shell\Runpb\Command]
#@="c:\\sys\\python25\\pythonw.exe c:\\bin\\pb.py \"%1\" #!run     "
#
# Syntax:
#    pb.py [ Options ] <File path> #!<Key> [ <Optional parameter> ... ] 
#
# Options:
#
#    -c <Count>           - Set last line to search for #! default 10
#                           A too short line will also abort scan
#    -d <Directory path>  - Set current directory         
#    -e <Name>=<Value>    - Set environment variable
#    -h                   - Display this text
#    -s <File to search>  - Set name of file containing command, defaults to
#                           primary file named in <File path>
#    -v                   - Run in verbose mode
#    -w <Count>           - Set last column in line to search for #! default 15
#    -x                   - Do not run, list expanded command
'''

import sys
import os
import getopt
import Do              # Recipe: 577439
import Do2             # Recipe: 577440

import subprocess

def FindCommand(pKey, pFilePath, pSearchPath, pCount=10, pDefault='#!', pList=False, pWidth=10, pVerbose=False):
    '''
    Find command keyword and extract containing line
    pKey         -- String identifying line to use as command template
    pFilePath    -- File to use in macro expansion
    pSearchPath  -- File to scan for command '
    pCount       -- Number of lines at the start of the file to scan
    pDefault     -- Prefix for keys, from UNIX #!
    pList        -- True to display available commands
    pWidth       -- Number of columns at start of line in which key must appear
    '''
    lShortest = 6         # A line shorter than this will abort scan
    
    if not os.path.exists(pSearchPath):
        lCommand = ''
        print 'pb.py Could not find search file', pSearchPath
        
    else:
#       ---- Check allowed key values    
        if pKey == '' or pKey == pDefault:          #   #!
            lKey = pDefault 
        elif pKey.find('{') >= 0:                   #   #!{e}
            lKey = pDefault + Do.Expand(pKey, pFilePath)
            if not lKey.startswith(pDefault):
                lKey = pDefault + lKey
        elif pKey.startswith(pDefault):             #   #!text
            lKey = pKey
        else:
            lKey = pDefault + pKey                  #   text
            lKey = lKey.lower()
#        lKey += ' '                                #   Full key only

#       ---- read maximum scan lines
        lFile = open(pSearchPath, 'r')
        lText = lFile.readlines(pCount)
        lText = lText[0:pCount]                     #???
        lFile.close()
        
        lCommand = ''

#       ---- list available commands
        if pList:
            lText = [x for x in lText if x.find(pDefault) >= 0 ]
            lText = [x for x in lText if x.find(pDefault) < pWidth ]
            print 'Available Commands in', pSearchPath
            for (lCount, lLine) in enumerate(lText):
                lLine = lLine.strip()
                print "%5d: %s" % (lCount, lLine)

#       ---- Scan for selected command
#            Since comments in some languages do not start with first character of key,
#            the key need not appear at start of line but must appear within first pWidth
#            columns to allow for skipping lines with key that are not to be matched
        else:   
            lCount = 0     
            for lLine in lText:
                if len(lLine.strip()) < lShortest:              # blank or short line will stop scan
                    break
                lLine = lLine.lower()
                lPos = lLine.find(lKey.lower()) 
                if pVerbose:
                    lCount += 1
                    print "pb.py %5d: %s" % (lCount, lLine),
                    if lPos >= 0:
                        lAt = lPos + 13
                        print ' ' * lAt + '^'                
                if  lPos >= 0 and lPos < pWidth:  
#                   ---- Full key only                
#                    lCommand = lLine[lPos+len(lKey):]           
#                   ---- Partial keys allowed                     
                    lCommand = lLine[lPos+len(lKey):]          
                    if lCommand[0] == ' ':                 # matched full key
                        lCommand = lCommand.lstrip()
                    else:
                        lPos = lCommand.find(' ')          # matched partial key
                        lCommand = lCommand[lPos:].lstrip()
                        
                    break
    return lCommand[0:-1]


def Expand(pArgs, pFilePath, pSearchPath, pCount, pSep='!!', pDefault='#!', pList=False, pWidth=15, pVerbose=False):
    '''
    Extract command from file and replace all macros
    pArgs        -- Args passed to program except file path
                    #!key and any arguments
    pFilePath    -- File to use in macro expansion
    pSearchPath  -- File to scan for command '
    pCount       -- Number of lines at the start of the file to scan
    pSep         -- String used to identify end of command, extra arguments will not be appended
    pList        -- True to display available commands
    pWidth       -- Number of columns to scan for #!
    '''
#   ---- Find command  
    if len(pArgs[1]) == 0:
        lKey = pDefault 
        lStart = 1
    elif pArgs[1].startswith(pDefault):
        lKey = pArgs[1]
        lStart = 2
    else:
        lKey = pDefault
        lStart = 1
            
    lCommand = FindCommand(lKey, pFilePath, pSearchPath, pCount, pDefault=pDefault, pList=pList, pWidth=pWidth, pVerbose=pVerbose)
    
    if lCommand == '':
        print 'pb.py Command', lKey, 'not found'
   
#   ---- Expand and insert/append any passed arguments   
#        Arguments on original pb.py command line will replace {} from left to right
#        otherwise they will be appended to the end of the command 
    if len(lCommand) > 0:
        if len(pArgs) > lStart:
            for lArg in pArgs[lStart:]:
                if lArg.find('{') >= 0:
                    lArg = Do2.ExpandArg(lArg, pFilePath, '')
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
 
def submitnow(pArgs, pFilePath, pSearchPath, pCount, pList=False, pExtract=False, pVerbose=False, pWidth=15):
    'Expand and submit command'
    if pVerbose:
        print 'pb.py File path:  ', pFilePath
        print 'pb.py Search path:', pSearchPath
        print 'pb.py Arguments:  ', pArgs
   
    lCommand = Expand(pArgs, pFilePath, pSearchPath, pCount, pList=pList, pWidth=pWidth, pVerbose=pVerbose)
#   ---- Any macro not expanded will be assumed to be an environment variable
#        If %...% had been used it would have been replaced when pb.py was run    
    lCommand = lCommand.replace('{}',' ')    # <-- may want to do something else
    lCommand = lCommand.replace('{', '%')
    lCommand = lCommand.replace('}', '%')

#   ---- Complete execution
    if pList:                      # List only
        pass
    elif len(lCommand) == 0:       # Expansion failed
        print 'pb.py Expansion failed'
    elif pExtract:                 # Expand command only
        print lCommand
    else:                          # Submit command
        lCommand = '"' + lCommand + '"'
        if pVerbose:
            print 'pb.py Submitting: ', lCommand
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

#sys.argv.extend(   [ 'c:\\source\\python\\projects\\program execution\\pb.py', '#!Inst', 'A', '{p}'  ] )
#sys.argv.extend(   [ 'c:\\source\\python\\projects\\program execution\\pb.py', '#!BadI', 'A', '{p}'  ] )
#sys.argv.extend(   [ 'c:\\source\\python\\projects\\program execution\\pb.py', '#!OKI',  'A', '{p}'  ] )
#sys.argv.extend(   [ 'c:\\source\\python\\projects\\program execution\\pb.py', '#!Edit', 'A', '{p}'  ] )

if __name__ == '__main__':
    (mOptions, mArgs) = getopt.getopt(sys.argv[1:], 'c:d:e:hls:vx')
    if len(mArgs) > 1:

#       ---- Set defaults
        mFilePath = os.path.abspath(mArgs[0])
        mArgs[1] = mArgs[1].replace('_', ' ')
        mSearchPath = mFilePath
        mCount = 10
        mList = False
        mExtract = False
        mVerbose = False
        mWidth = 15
        mHelp = False

#       ---- Scan option list
        for (mKey, mValue) in mOptions:
            if mKey == '-d':                 # Set current directory
                if mValue.find('{') >= 0:
                    mValue = Do.Expand(mValue, mFilePath)
                os.chdir(mValue)
                
            elif mKey == '-e':               # Set environment variable
                setenviron(mValue, mFilePath)

            elif mKey == '-c':               # Set last line to search for #!
                try:
                    mCount = int(mValue)
                except Exception, e:
                    mCount = 10
                    
            elif mKey == '-s':               # Set search path
                mSearchPath = mValue
                if mValue.find('{') >= 0:
                    mSearchPath = Do2.ExpandArg(mSearchPath, mFilePath, '')
                    if mSearchPath[0] == '"':
                        mSearchPath = mSearchPath[1:-1]
                mSearchPath = os.path.abspath(mSearchPath)

            elif mKey == '-h':               # Display help only
                mHelp = True
                
            elif mKey == '-l':               # Display available commands
                mList = True

            elif mKey == '-x':               # List expanded command only
                mExtract = True

            elif mKey == '-v':               # Run in verbose mode
                mVerbose = True

            elif mKey == '-w':               # Set last column in file to search for #!
                try:
                    mWidth = int(mValue)
                except Exception, e:
                    mWidth = 10

        if mHelp:
            print mHelpText
            print 'pb.py Search file:', mSearchPath
            print 'pb.py Width:      ', mWidth
            print 'pb.py Lines:      ', mCount
            mList = True
        else:
            submitnow(mArgs, mFilePath, mSearchPath, mCount, mList, mExtract, mVerbose, mWidth)
    else:
        print 'pb.py Command and/or file path missing'
    

    
