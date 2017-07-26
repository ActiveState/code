# ----------------------------------------------
# Name: Do2
# Description: Expand and execute command
## D20H-35 Expand and execute command
#
# Author: Philip S. Rist
# Date: 10/24/2010
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
#[HKEY_CLASSES_ROOT\*\Shell\Do2Bkup]
#@="Backup (Do2)"
#"EditFlags"=hex:01,00,00,00
#[HKEY_CLASSES_ROOT\*\Shell\Do2Bkup\Command]
#@="c:\\sys\\python25\\pythonw.exe c:\\bin\\do2.py \"%1\" c:\\Windows\\system32\\cmd.exe /K copy \"{a}\" \"{u}\\{2}\\{f}\"      "
#
#[HKEY_CLASSES_ROOT\*\Shell\Do2Edit]
#@="Edit (Do2)"
#"EditFlags"=hex:01,00,00,00
#[HKEY_CLASSES_ROOT\*\Shell\Do2Edit\Command]
#@="c:\\sys\\python25\\pythonw.exe c:\\bin\\do2.py \"%1\" c:\\Source\\{2}\\qeditor.exe  \"{a}\"     "
#


import sys, getopt, os
import Do
import subprocess

def ParentSearch(pFilePath, pDefaultPath, pJoin='\\'):
    '''
    Scan parent list for file selecting lowest level matching file
    '''
    lParts = pFilePath.split(pJoin)
    lCount = len(lParts) - 1
    lPath = ''
    while lCount > 0:
        lPath = pJoin.join(lParts[0:lCount]) + pJoin + lParts[-1]
        if os.path.exists(lPath):
            break
        lCount -= 1
    else:
        lPath = pDefaultPath
    return lPath

def ExpandArg(pArg, pFilePath, pDefaultPath, pLeft='{', pSep=';', pQuote='"', 
                              pPref='{<-}', pJoin='\\'):
    '''
    Expand single command line argument
    '''
#                    Expand argument   
    if pArg.find(pLeft) >= 0:
        lArg = Do.Expand(pArg, pFilePath)
    else:
        lArg = pArg

#                    If starts with {<-} and single path scan parent folders for
#                    first matching file.  Each folder above specified path will
#                    be checked until file is found.
    if lArg.startswith(pPref) and lArg.find(pSep) < 0:
        lArg = os.path.abspath(lArg[2:])
        print 'Parent Search 1'
        lArg = ParentSearch(lArg, pDefaultPath, pJoin=pJoin)

#                    If multiple paths separated by pSep(';') select first valid path
    lFound = ''
    if lArg.find(pSep) >= 0:
        lPaths = lArg.split(pSep)
        for lPath in lPaths:
            if lPath.startswith(pPref):
                lPath = os.path.abspath(lPath[4:])
                lPath = ParentSearch(lPath, pDefaultPath, pJoin=pJoin)    # 01/19/11
            if lPath == '':                                               #
                continue                                                  #
            lPath = os.path.abspath(lPath)
            if os.path.exists(lPath):
                lFound = lPath
                break
        else:
            lFound = os.path.abspath(pDefaultPath)
    else:
        lFound = lArg
    
#                    If argument contains space enclose it within quotes
    lFound = lFound.strip()
    if lFound.find(' ') > 0 and lFound[0] != pQuote:
        lFound = pQuote + lFound + pQuote
    return lFound

def submitnow(pCommand):
    '''
    Submit command
    '''
    lCommand = '"' + pCommand + '"'
    #print '\n\nSubmitting:', lCommand
    subprocess.Popen(lCommand, shell=True)



#sys.argv.extend( [ '-d', '{o}\\new', 'c:\\source\\python\\new\\do.py', 'c:\\bin\\echop.bat', 
#       '{a}', '{p}\\test\\{f}', '{<-}\\{p}\\menus.ini', '{t}\\{xx}.bkp',
#       '{i}\\{-1}', '   {u}\\{-2}', '{.}\\{-3}   ', '"{g}\\{2}\\test.{e}"', 
#       '{0}\\{3}\\{n}.{e}.txt'    ])

if __name__ == '__main__':
    (mOptions, mArgs) = getopt.getopt(sys.argv[1:], 'd:e:')
    
    mFilePath = mArgs[0]

    mDefaultPath = ''
    for (mKey, mValue) in mOptions:
        if mKey == '-d':
            if mValue.find('}'):
                mValue = ExpandArg(mValue, mFilePath, '')
            if mValue != '':
                os.chdir(mValue)
            
        elif mKey == '-e':
            setenviron(mValue, mFilePath)

        elif mKey == '-p':
            mValue = ExpandArg(mValue, mFilePath, '')
            if mValue != '':
                mDefaultPath = mValue

    mCommand = ''
    mCount = 0
    for mArg in mArgs[1:]:
        mText = ExpandArg(mArg, mFilePath, mDefaultPath) + ' '
        #print '%5d: %-24s * %-30s ---> %s' % (mCount, mArgs[mCount+1], mFilePath, mText)
        mCommand += mText
        mCount += 1

    if len(mCommand) > 0:                
        submitnow(mCommand)
    

    
