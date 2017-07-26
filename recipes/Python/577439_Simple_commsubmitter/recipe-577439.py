#
 ----------------------------------------------
# Name: Do
# Description: Expand and execute command
## D20H-35 Expand and execute command
#
# Author: Philip S. Rist
# Date: 10/12/2010
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

# Usage examples:
#
#[HKEY_CLASSES_ROOT\*\Shell\DoBkup]
#@="Backup (Do)"
#"EditFlags"=hex:01,00,00,00
#[HKEY_CLASSES_ROOT\*\Shell\DoBkup\Command]
#@="c:\\sys\\python25\\pythonw.exe c:\\bin\\do.py \"%1\" 
c:\\Windows\\system32\\cmd.exe /K copy \"{a}\" \"{u}\\{2}\\{f}\"      "
#
#[HKEY_CLASSES_ROOT\*\Shell\DoEdit]
#@="Edit (Do)"
#"EditFlags"=hex:01,00,00,00
#[HKEY_CLASSES_ROOT\*\Shell\DoEdit\Command]
#@="c:\\sys\\python25\\pythonw.exe c:\\bin\\do.py \"%1\" 
{o}\\qeditor.exe  \"{a}\"     "
#


import sys
import os
import getopt

#                    Used only by the {o} option which you will
#                    probably want to remove
from _winreg import *

import subprocess

def Expand(pCommand, pFilePath, pSep='\\'):
    'Replace all {?} macros in pCommand'
#             Split file path into parts
    if len(pFilePath) > 0:
        lFilePath  = os.path.abspath(pFilePath) 
        lEndPos    = lFilePath.rfind(pSep)
        lPath      = lFilePath[0:lEndPos]
        lFileName  = lFilePath[lEndPos+1:]
        lEndPos    = lFileName.rfind(".")
        lName      = lFileName[:lEndPos]
        lFilePart  = lPath + pSep + lName
        lExtension = lFileName[lEndPos+1:]
        lPathParts = lFilePath.split(pSep)
    else:
        lFilePath = lPath=lFileName=lName=lFilePart=lExtension=""
        lPathParts = []

    lParts = pCommand.split('{')
    if len(lParts) == 1:                              # no replacements
        lCommand = pCommand
    else:                                             # scan and replace
 commands
        lCommand = lParts[0]
        for lPart in lParts[1:]:                      # for each 
replacement
            lPos = lPart.find('}')
            lCh = lPart[0].lower()
            if lPos == 1:
                lPos = 0
                if lCh   == 'a':                          # entire file 
path
                    lInsert = lFilePath
                elif lCh == 'b':                          # file path 
except extension
                    lInsert = lFilePart
                elif lCh == 'p':                          # path to 
folder containing file
                    lInsert = lPath
                elif lCh == 'f':                          # file name 
without path
                    lInsert = lFileName
                elif lCh == 'n':                          # file name 
without path or extension
                    lInsert = lName
                elif lCh == 'e':                          # extension
                    lInsert = lExtension
                elif lCh == 't':
                    lInsert = "c:\\temp"                  # temporary 
directory
                elif lCh == 'i':
                    lInsert = "c:\\bin"                   # installation
 directory
                elif lCh == 'u':
                    lInsert = "c:\\_Backup"               # backup 
directory
                elif lCh == 'o':                          # source 
directory
                                                          # I added a 
SourceDir key for each programming
                                                          # language 
extension.  This replacements is
                                                          # replaced by 
that text.
                    try:
                        lKey = OpenKey(HKEY_CLASSES_ROOT, '.' + 
lExtension)
                        lIndex = 1
                        while lIndex < 10:
                            try:
                                lValue = EnumValue(lKey, lIndex)
                                if lValue[0] == 'SourceDir':
                                    lInsert = lValue[1]
                                    break
                            except Exception ,e:
                                lInsert =  "c:\\unknown_type"
                                break
                            lIndex += 1
                        else:
                            lInsert = "c:\\unknown_type"
                    except Exception, e: 
                        lInsert = "c:\\unknown_type"                # 
{o}
                elif lCh == 'y':
                    lInsert = "c:\\sys"                   # System 
directory
                elif lCh == 'w':
                    lInsert = "c:\\windows\\system32"     # Windows 
directory
                elif lCh == 'v':
                    lInsert = "j:\\_Backup"               # Archive 
directory
                elif lCh == 'l':
                    lInsert = "c:\\Library"               # Library 
directory
                elif lCh == 'g':
                    lInsert = "c:\\Program Files"         # Program 
Files directory
                elif lCh == '.':
                    lInsert = os.getcwd()                 # Current 
directory
                elif lCh == '*':                          # System 
command
                    lInsert = 'c:\\windows\\system32\\cmd.exe'
                elif lCh == '+':                          # Python
                    lInsert = 'c:\\sys\\python25\\python.exe'
                #elif lCh == '%':
                #    try:
                #        lPos = lPart[1:].find("%")
                #        if lPos > 1:
                #            lKey = lPart[1:lPos]
                #            lInsert = os.environ[lKey]
                #            lPos += 1
                #        else:
                #            lInsert = ''
                #    except:
                #        lInsert = ''
                elif lCh == '0':                          # Drive letter
 (ie. c:\source\python\new\test.py --> c:\)
                    lInsert = lPathParts[0]
                elif lCh == '1' and len(lPathParts) > 1:  # First 
level  (ie. c:\source\python\new\test.py --> source)
                    lInsert = lPathParts[1]
                elif lCh == '2' and len(lPathParts) > 2:  # Second 
level (ie. c:\source\python\new\test.py --> python)
                    lInsert = lPathParts[2]
                elif lCh == '3' and len(lPathParts) > 3:  # Third 
level (ie. c:\source\python\new\test.py --> new)
                    lInsert = lPathParts[3]
                else:
                    lInsert = '{' + lPart
                    
            elif lCh == '-' and lPos == 2:
                lPos = 1
                lCh = lPart[1]
                if lCh == '1' and len(lPathParts) > 2:     # Last 
level (ie. c:\source\python\new\test.py --> new)
                    lInsert = lPathParts[-2]
                elif lCh == '2' and len(lPathParts) > 3:   # Next to 
last level (ie. c:\source\python\new\test.py --> python)
                    lInsert = lPathParts[-3]
                elif lCh == '3' and len(lPathParts) > 4:   # Second 
to last level (ie. c:\source\python\new\test.py --> source)
                    lInsert = lPathParts[-4]
                else:
                    lInsert = '{' + lPart[lPos+2]
            else:
                lInsert = '{' + lPart[lPos+2]

            lPart = lInsert + lPart[lPos+2:]
            lCommand += lPart
    return lCommand

def submitnow(pCommand, pFileName):
    'Expand and submit command'
    lCommand = Expand(pCommand, pFileName)
    lCommand = '"' + lCommand + '"'
    subprocess.Popen(lCommand, shell=True)

def setenviron(pValue, pFileName):
    'Set environment variable'
    lParts = pValue.split('=')
    if len(lParts) > 1:
        lKey = lParts[0]
        lValue = lParts[1]
        if lValue.find('{') >= 0:
            lValue = Expand(lValue, pFileName)
        os.environ[lKey] = lValue
    else:
        os.environ[pValue] = ''

#sys.argv.extend( [ '-d', '{o}\\new', 'c:\\source\\c\\test\\menus.ini', 
'c:\\bin\\echop.bat', '{a}', '{p}\\test\\{f}', '{b}.exe', 
'{t}\\{n}.bkp',
#                    '{i}\\{-1}', '{u}\\{-2}', '{.}\\{-3}', 
'"{g}\\{2}\\test.{e}"', '{fp}', '{0}\\{3}\\{n}.{e}.txt'    ])

#   Syntax: [Options] file-path command

if __name__ == '__main__':
    (mOptions, mArgs) = getopt.getopt(sys.argv[1:], 'd:e:')
    if len(mArgs) > 1:
        mFileName = mArgs[0]
        mCommand = ' '.join(mArgs[1:])
    
        for (mKey, mValue) in mOptions:
            if mKey == '-d':                 # Set current directory
                if mValue.find('}') >= 0:
                    mValue = Expand(mValue, mFileName)
                os.chdir(mValue)
                
            elif mKey == '-e':               # Set environment variable
                setenviron(mValue, mFileName)
                            
        submitnow(mCommand, mFileName)
    else:
        print 'Command and/or file path missing'
    

    
