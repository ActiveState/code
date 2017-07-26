#-----------------------------------------------------------------------------
# Name:        BackUp.py
# Purpose:     Performes the backup of all private and checked out files in all
#              local clearcase views for windows.
#
# Author:      Luigi Poderico
#              poderico_l@yahoo.com
#              www.poderico.it
#
# Created:     2004/21/04
#-----------------------------------------------------------------------------
#!/usr/bin/env python
#Boa:PyApp:main

modules ={}

import popen2
import string
import shutil
import os
import os.path

"""
This script performes the backup of all private and checked out files in all
local clearcase views for windows.

Using with clearcase, is common to have on some clearcase server the vobs
and streams, and on own workstation a client clearcase with some local views.


Working on these views, happens very often that at end of working day some files
remain private or checked out. Supposing that the server clearcase is well-backed
up, these files are not safe.

Running this script properly, for example at user log-out or at 2:0 a.m. or other
policy, also local private and checked out files are copied in a secure place.

All error during backup will sent to administrator with an e-mail.


To configure this script, please edit:
1. the function BuildDestinationPath();
2. the methods BackUp.__NotifyByEmail(), BackUp.__SkipRubish().


Note. This script was test on windows 2k and xp.
"""



#-------------------------------------------------------------------------------

def mkdirs(aPathName):
    if os.path.exists(aPathName):
        return
    
    (myHead, myTail) = os.path.split(aPathName)
    mkdirs(myHead)
    os.mkdir(aPathName)
    return

def removedirs(aPath):
    for root, dirs, files in os.walk(aPath, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    return

#-------------------------------------------------------------------------------

class BackUp:

    theMessagesError = ''
   
    def __StartViews(self, aListOfView):
        """
        Start all the view listed in <aListOfView>.
        """
        
        for myViewName in aListOfView:
            myClearCaseCommand = 'cleartool endview ' + myViewName
            os.popen2(myClearCaseCommand)
            
            myClearCaseCommand = 'cleartool startview ' + myViewName
            os.popen2(myClearCaseCommand)
            
            """
            (mystdIn, myStdOut) = popen2.popen2(myClearCaseCommand)
            for myLine in mystdIn:
                # Consume di output
                pass
            """
            
        return
    
    def __GetLocalViews(self):
        """
        Return a list with all local view.
        """

        import socket
        
        myClearCaseCommand = 'cleartool lsview'
        myHostName = string.lower(socket.gethostname())
        
        myListLocalView = []

        (mystdIn, myStdOut) = popen2.popen2(myClearCaseCommand)
        for myLine in mystdIn:
            myLowerLine = string.lower(myLine)
            myStartHostName = string.find(myLowerLine, myHostName)
            
            if myStartHostName != -1:
                myLocalView = myLine[2:myStartHostName-2]
                myListLocalView.append(string.strip(myLocalView))
                
        self.__StartViews(myListLocalView)
                
        return myListLocalView
        
        return
    
    def __PrivateFile(self, aLocalView):
        """
        Return a list with all private and cheked out files in <aLocalView>
        view.
        """
        
        myClearCaseCommand = 'cleartool lsprivate -tag ' + aLocalView
        myPrivateFileList = []
        
        (mystdIn, myStdOut) = popen2.popen2(myClearCaseCommand)
        for myLine in mystdIn:
            myFilter = '[checkedout]'
            myLine = string.rstrip(string.lstrip(myLine))
            if myLine[-len(myFilter):] == myFilter:
                myLine = string.rstrip(string.lstrip(myLine[:-len(myFilter)]))
                
            myPrivateFileList.append(myLine)

        return myPrivateFileList
    
    def __MirrorPath(self, aLocalView, aDestinationPath, aFilePath):
        assert(string.count(aFilePath, aLocalView) != -1)
                
        myStartCommonSubpath = string.find(aFilePath, aLocalView)
        myStartCommonSubpath += len(aLocalView)
        
        myMirrorPath = aDestinationPath + aFilePath[myStartCommonSubpath:]
        myMirrorPath = os.path.dirname(myMirrorPath)
        myMirrorPath = os.path.normpath(myMirrorPath)
        
        return myMirrorPath
    
    def __SkipRubish(self, aFilePathList):
        """
        Edit this method to select the private file that will not be backed up.
        """
        
        myFilteredList = []
        
        for myFilePath in aFilePathList:
            myLowerFilePath = string.lower(string.strip(myFilePath))
            
            if myLowerFilePath[-4:]=='.obj':
                continue
            
            if myLowerFilePath[-5:]=='.class':
                continue
            
            if myLowerFilePath[-1:]=='~':
                continue
            
            myFilteredList.append(myFilePath)
        
        return myFilteredList
        
    def __DoBackupOf(self, aLocalView, aDestinationPath):
        """
        Performe the backup of private and checked out file in <aLocalView>
        view to path pointed by <aDestinationPath>.
        """
        
        aDestinationPath = os.path.normpath(aDestinationPath)
                
        # Select my private files
        myPrivateFiles = self.__PrivateFile(aLocalView)
        
        myPrivateFiles = self.__SkipRubish(myPrivateFiles)
        
        # Remove ancient files
        removedirs(aDestinationPath)
        
        # Copy files
        for myPrivateFile in myPrivateFiles:
            myDestinationPath = self.__MirrorPath(aLocalView, aDestinationPath, myPrivateFile)
            if not os.path.exists(myDestinationPath):
                mkdirs(myDestinationPath)
                
            print myPrivateFile
            try:
                if os.path.isfile(myPrivateFile):
                    shutil.copy(myPrivateFile, myDestinationPath)
                
            except Exception, e:
                self.theMessagesError += str(e) + '\n'
                pass
        
        return
    
    def Run(self, aDestinationPath):
        """
        Performe the backup of private and checked out file in all local
        view to path pointed by <aDestinationPath>.
        """
        try:
            myLocalViews = self.__GetLocalViews()
            
            for myLocalView in myLocalViews:
                print "Working on ", myLocalView
                self.__DoBackupOf(myLocalView, aDestinationPath)
        except Exception, e:
            self.theMessagesError += str(e)
        
        if (self.theMessagesError!=''):
            self.__NotifyByEmail(self.theMessagesError)
        return
    
    
    def __NotifyByEmail(self, aMessagesError):
        import smtplib
        import socket
        
        myHostName = socket.gethostname()
        server = smtplib.SMTP('myMailServer')
        server.sendmail('backupcc@' + myHostName, ['poderico_l@yahoo.com'], aMessagesError)
        server.quit()
        return
    
#-------------------------------------------------------------------------------
 
def BuildDestinationPath():
    """
    Edit this functions to build an appropriate backup destination directory.
    In this example, the backup will be stored into the server 'serverBackUp'
    at directory /home3/windowsClientBackup/<username>/<weekDay>.
    """
    import getpass
    import datetime
    
    myToday = datetime.date.today()
    myWeekDay = '%d' % myToday.isoweekday() 
    myBaseDestination = '//serverBackUp/home3/windowsClientBackup/'
    myBaseDestination += getpass.getuser() + '/' + myWeekDay 
    return myBaseDestination

def main():
    
    myDestinationPath = BuildDestinationPath()
    myBackUp = BackUp()
    myBackUp.Run(myDestinationPath)
    pass

if __name__ == '__main__':
    main()
