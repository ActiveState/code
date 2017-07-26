mHelpText = '''
# ----------------------------------------------
# Name: x
## D20H-53 Wrapper for DoM.py, DoCommand.py and pb.py
#
# Author: Philip S. Rist
# Date: 10/31/2010
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

# Extract command from menu, Windows registry or primary file using DoM,py,
# pb.py or DoCommand.py.  Expand the command and execute it.  Use within 
# console window to expand commands as a DOS expander macro.  All matches
# are case insensitive.
#
# Examples:
#     x {DoEdit} do.py   - Execute DoEdit command associated with .py extension
#     x open do.py       - Execute open command in the current section in the current menu file
#     x #!Open do.py     - Execute #!Open command at the head of the do.py file
#
# Syntax:
#
#          x <key> <file path> [ <arguments> ... ]
#
#  <key> -
#     <menu path>'<section>'<key> - Extract command <key> from section <section> of menu <menu path>
#     <menu path>'<section>'?     - List commands in section <section> of menu <menu path>
#     <menu path>'*'<key>         - Extract first matching command in menu <menu path> ignoring sections
#     <menu path>'*'?             - List all commands in menu <menu path>
#     <section>'<key>             - Extract command <command key> from section <section> of default menu
#     <section>'?                 - List commands in section <section> in default menu
#     *'<key>                     - Extract first matching command in default menu file ignoring sections
#     *'?                         - List commands in all sections of default menu
#     <key>                       - Extract command <key> from default section of default menu
#     ?                           - List commands in default section of default menu
#
#     <search path>'#!<key>       - Extract command <key> from file <search path>
#     <search path>'#!?           - List available commands in <search path>
#     #!?                         - List available commands in primary file <file path>
#     #!<command key>             - Extract command <key> from the primary file <file path>
#
#     <ext>'{<key>}               - Extract command <key> from registry for extension <ext>
#     {<key>}                     - Extract command <command key> from registry tree for 
#                                   file type of <file path>
#
#     <menu path>   = See MENUPATH below.  Use '_' instead of spaces
#     <search path> = See SEARCHPATH below.  Use '_' instead of spaces
#     <section>     = '*' to scan all sections, first acceptable command
#                     will be used.  Incomplete sections willmatch first section
#                     name beginning with <section>  Use '_' instead of spaces
#     <command key> = '?' will list all available commands in selected section or 
#                     sections.  Incomplete keys will match first beginning with <key>
#                     Use '_' instead of spaces
#
# Environment variables:
#
#   SEARCHPATH - path to file containing command templates.  When not defined the 
#                file <file path> is used.   May contain macros as in
#                {o}\menus.ini;c:\bin\menus.ini
#   MENUPATH   - path to menu file containing command template.  When not defined 
#                the file <file path> is used.  May contain macros as in
#                {o}\menus.ini;c:\bin\menus.ini
#   SECTION    - default section in menu file.  When not defined 'dos' is used.
#                'i' is reserved for internal commands, only 'help' currently
#                'his' is reserved for command history, not implemented yet.
#                May contain macros such ae '{e} tools'
#   INTERNAL   - path to menu file to be used for internal commands.  Only
#                section 'int' is used.  When not defined only commands defined
#                in x.py are available.  Only 'help' currently.   May contain macros as in
#                {o}\menus.ini;c:\bin\menus.ini
#   FILEPATH   - path to primary file
#
'''

import sys, os, getopt
import DoM                                # Recipe: 577453
import pb                                 # Recipe: 577454
import Do                                 # Recipe: 577439
import Do2                                # Recipe: 577440
import DoCommand                          # Recipe: 577441

if __name__ == '__main__':
    (mOptions, mArgs) = getopt.getopt(sys.argv[1:], 'd:e:m:s:v')
    mDefaultSection = 'tools'             # Change as needed
    mExtension = mDefaultExtension = '.txt'

#   ---- Check verbosity
    mVerbose = False
    for (mKey, mValue) in mOptions:
        if mKey == '-v':
            mVerbose = True
#   ---- Scan options list
    mSep = "'"   # anything except :./\"

#   ---- Get defaults from environment
    try:
        mSearchPath = os.environ['SEARCHPATH']
        if mVerbose:
            print 'x.py Default search path', mSearchPath
    except:
        mSearchPath = ''

    try:
        mMenuPath = os.environ['MENUPATH']
        if mVerbose:
            print 'x.py Default menu path', mMenuPath
    except:
        mMenuPath = ''

    try:
        mInternalPath = os.environ['INTERNAL']
        if mVerbose:
            print 'x.py Default internal path', mInternalPath
    except:
        mInternalPath = ''

    try:
        mSection = os.environ['SECTION']
        if mVerbose:
            print 'x.py Default section', mSection
    except:
        mSection = mDefaultSection
    if mSection == '':
        mSection = mDefaultSection

#   ---- Primary file path    
    if len(mArgs) > 1:
        mFilePath = os.path.abspath(mArgs[1])
        mArgs[1] = ''
    else:
        try:
            mFilePath = os.environ['FILEPATH']
            if mVerbose:
                print 'x.py File path', mFilePath
        except:
            mFilePath = ''          # <-- something else should go here

        
    mVerbose = False
    mHelp = False

#   ---- Scan options
    for (mKey, mValue) in mOptions:
        if mKey == '-d':                 # Set current directory
            if mValue.find('{') >= 0:
                mValue = Do2.ExpandArg(mValue, mFilePath, '')
            os.chdir(mValue)
            
        elif mKey == '-e':               # Set environment variable
            DoM.setenviron(mValue, mFilePath)

        elif mKey == '-m':
            mMenuPath = os.path.abspath(mValue)

        elif mKey == '-s':
            mSection = mValue

        elif mKey == '-v':
            mVerbose = True

    
    if len(mArgs) <= 0:
        mKey = '?'
        
    else:

#       ---- Command key
        mArgs[0] = mArgs[0].replace('_', ' ')
        mKey = mArgs[0]
        if mKey.find(mSep) >= 0:
            mFields = mKey.split(mSep)
            
            mLen = len(mFields)
            if mLen > 2:
                 mMenuPath = mFields[-3]

            if mLen > 1:
                if mFields[-1].startswith('#!'):
                    mSearchPath = mFields[-2]
                    mSection = ''
                elif mFields[-1][0] == '{':
                    mExtension = mFields[-2]
                    mSection = ''
                        
                elif mFields[-2] != '':  
                    mSection = mFields[-2]
                    
                else:
                    mPos = mFilePath.rfind('.')
                    if mPos >= 0:
                        mSection = mFilePath[lPos+1:]
                    else:
                        mSection = 'txt'
            mKey = mFields[-1]  
            mArgs[0] = mKey

        if mSection.find('{'):
            mSection = Do.Expand(mSection, mFilePath)

#   ---- Extract command from registry
#        Remove this and import if this is going to far  
#        Can not list commands from registry
    if mKey[0] == '{':
        if mExtension == mDefaultExtension:         # No extension specified
            lPos = mFilePath.rfind('.')
            if lPos > 0:
                mExtension = mFilePath[lPos:]     # Contains extension with '.'
            else:
                mExtension = mDefaultExtension      
        if len(mArgs) > 2:
            mArgs = mArgs[2:]
        else:
            mArgs = []

        print mFilePath, mKey[1:-1], mExtension, mArgs
        DoCommand.DoCommand(mFilePath, mKey[1:-1], mExtension, mArgs, mVerbose)

#   ---- Extract command from file
#        Remove this and import if this is going to far  
    elif mKey.startswith('#!'):
        mTemp = [ mFilePath ]
        for lArg in mArgs:
            mTemp.append(lArg)
        mArgs = mTemp

        if mSearchPath == '':
            mSearchPath = mFilePath
        if mSearchPath.find('{') >= 0:
            mSearchPath = Do2.ExpandArg(mSearchPath, mFilePath, '')
            if mSearchPath[0] == '"':
                mSearchPath = mSearchPath[1:-1]
        mSearchPath = os.path.abspath(mSearchPath)

        if mFilePath == '':
            mFilePath = mSearchPath

        if mFilePath == '':
            print 'x.py No primary file available'
        else:
            pb.submitnow(mArgs, mFilePath, mSearchPath, 20, mKey == '#!?', pVerbose=mVerbose, pWidth=15)

#   ---- Internal commands
    elif mSection == 'i':
        if mVerbose:
            print 'x.py File:   ', mFilePath
            print 'x.py Menu:   ', mMenuPath
            print 'x.py Section:', mSection
            print 'x.py Command:', mKey
        if 'help'.startswith(mKey.lower()):
            print mHelpText
        elif mInternalPath != '':
            if mInternalPath.find('{') >= 0:
                mInternalPath = Do2.ExpandArg(mInternalPath, mFilePath, '')
                if mInternalPath[0] == '"':
                    mInternalPath = mInternalPath[1:-1]
            mInternalPath = os.path.abspath(mInternalPath)
            DoM.submitnow(mArgs, mFilePath, mInternalPath, 'int', mVerbose)        
        else:
            print 'x.py Currently no internal command', mKey

#   ---- Extract command from menu
    else:  
        if mMenuPath == '':
            mMenuPath = mFilePath
        else:
            if mMenuPath.find('{') >= 0:
                mMenuPath = Do2.ExpandArg(mMenuPath, mFilePath, '')
                if mMenuPath[0] == '"':
                    mMenuPath = mMenuPath[1:-1]
            mMenuPath = os.path.abspath(mMenuPath)
        
        if mVerbose:
            print 'x.py File:   ', mFilePath
            print 'x.py Menu:   ', mMenuPath
            print 'x.py Section:', mSection
            print 'x.py Command:', mKey
           
        if mKey.lower() == '?':
            DoM.FindCommand('?', mFilePath, mMenuPath, mSection, True)
        else:
            DoM.submitnow(mArgs, mFilePath, mMenuPath, mSection, mVerbose)
