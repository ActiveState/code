# ----------------------------------------------
# Name: Do
# Description: Expand and execute command
## D20H-23 Do command from Windows registry
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


from _winreg import *
import sys, os, os.path, getopt
import subprocess
import Do

def SubmitNow(pCommand):
    'Execute command'
    lCommand = '"' + pCommand + '"'
    #lCommand = 'c:\\bin\\messagebox.exe   ' + lCommand
    subprocess.Popen(lCommand, shell=True)

def GetExtensionInfo(pExtension):
    'Extract data saved in registry for specific extension'
    lHandle = OpenKey(HKEY_CLASSES_ROOT, pExtension)
    lSubKeys, lValueCount, lModified = QueryInfoKey(lHandle)
    lValues = {}
    for lCount in range(0, lValueCount):
        lName, lValue, lType = EnumValue(lHandle, lCount)
        if lName == '':
            lName = "File Type"
        lValues[lName] =lValue
        
    lKey = lValues['File Type']
    lDescription = QueryValue(HKEY_CLASSES_ROOT, lKey)
    lValues['Description'] = lDescription

    lKey += '\\Shell'
    lDefault = QueryValue(HKEY_CLASSES_ROOT, lKey)
    lValues['Default'] = lDefault    
    return lValues


def GetCommand(pFileType, pKey):
    'Retrieve text for selected command'
    lAbort = False
    try:
        lKey =  pFileType + "\\Shell\\" + pKey + "\\Command"
        lText = QueryValue(HKEY_CLASSES_ROOT, lKey)
    except:
        lText = ''
        lAbort = True
    return (lAbort, lText)


def BuildCommand(pExpandFile, pKey, pExtension, pArgs, pVerbose=False):
    '''
    The extension from pExpandFile is used to select the command associated with
    the command named in pKey for the file type associated with the given extension.

    pExpandFile - File to be processed
    pKey        - Command name
    pExtension  - Extension used to select command text
    pArgs       - Passed arguments

    Note: c:\messagebox.exe displays its command line in a popup window.
    '''
    if pVerbose:      # not currently used for anything
        lValues = GetExtensionInfo(pExtension)
    else:
        lValues = {}
    if len(pArgs) > 1:
        pArgs = pArgs[1:]
    else:
        pArgs = []
    lExpandFile = pExpandFile
    lKey = pKey
    lAbort = False
    
    lText = ''
    if len(lKey) > 0 and len(lExpandFile) > 0:
        lPos = lExpandFile.rfind('.')
        if lPos > 0:
            if pExtension == '':
                lExtension = lExpandFile[lPos:]
            else:
                lExtension = pExtension
            lFileType = QueryValue(HKEY_CLASSES_ROOT, lExtension)
            if len(lFileType) > 0:
                (lAbort, lText) = GetCommand(lFileType, lKey)
                if lAbort:
                    (lAbort, lText) = GetCommand('*', lKey)
            else:
                lAbort = True
                pass
        else:
            lAbort = True
            pass
    else:
        lAbort = True
        pass
        
    lArgs = ''
    if len(pArgs) > 0:
        lArgs = ' '.join(pArgs)
    if not lAbort:
        if lText.find("%") >= 0:
            lText = lText.replace("%1", str(lExpandFile))
            for lCount in range(0,len(pArgs)):
                lString = '%' + str(lCount+2)
                lText = lText.replace(lString, pArgs[lCount])
                lText = lText.replace("%*", lArgs)
        else:
            lText += " " + lExpandFile + " "+ lArgs
            
        if lText.find('{') >= 0:
            lText = Do.Expand(lText, lExpandFile)

    else:
        lText = ''
    return lText

def DoCommand(pExpandFile, pKey, pExtension, pArgs, pVerbose=False):
    lCommand = BuildCommand(pExpandFile, pKey, pExtension, pArgs, pVerbose)
    if len(lCommand) > 0:
        SubmitNow(lCommand)
    else:                              # requires a program that will display passed arguments
#        SubmitNow("c:\\bin\\messagebox.exe DoCommand: Execution aborted for " + pKey + 
#                          " on file " + pExpandFile )
        print 'Command not generated'

# DoCommand is designed to be executed from another program such as QEditor or Crimson Editor 
# which allow the user to define external commands.
#
# from QEditor:
#     Display References,c:\sys\python25\pythonw.exe  c:\bin\DoCommand.py  "{a}" RefList
#
#     This command will execute the RefList command associated with what ever file is being edited 
#     passing that file.  Most useful with a program such as Crimson Editor which provide for only
#     a limited number of user defined commands.

#sys.argv.extend(['-x', '.txt', 'c:\\source\\python\\Projects\\Program Execution\\docommand.py', 
#                'Open', 'First', '{p}' ])
#     uses Open command for .txt files to open Python source file

if __name__ == '__main__':
    lSys = len(sys.argv)
    if lSys > 1:
        (mOptions, mArgs) = getopt.getopt(sys.argv[1:], 'd:e:vx:')
        
        mFileName = mExpandFile = mArgs[0]  # 1st Path to file
        
        if len(mArgs) > 1:                  # 2nd command name
            mCommand = mArgs[1]             # 3rd on command arguments
            mArgs = mArgs[1:]
        else:
            mCommand = "Open"
        
        lPos = mExpandFile.rfind('.')
        if lPos >= 0:
            mExtension = mExpandFile[lPos:]
        else:
            mExtension = ''

        mVerbose = False
        
        for (mKey, mValue) in mOptions:  
            if mKey == '-d':                 # Set current directory
                if mValue.find('}'):
                    mValue = Do.Expand(mValue, mFileName)
                os.chdir(mValue)
                
            elif mKey == '-e':               # Set environment variable
                setenviron(mValue, mFileName)

            elif mKey == '-v':               # Run in verbose mode
                mVervose = True
                
            elif mKey == '-x':               # override extension where command
                mExtension = mValue          # is extracted

        if mExtension == '':
            mExtension = 'txt'
                    
        DoCommand(mExpandFile, mCommand, mExtension, mArgs, pVerbose=mVerbose)
    else:
        #SubmitNow("c:\\bin\\messagebox.exe DoCommand.py requires a file name and a command name")
        print "DoCommand.py requires a file name and a command name"
