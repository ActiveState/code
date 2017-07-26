""" logger.py
    This module is responsible for controlling the action logging for the
    application. 
"""
"""
 Author: Johan Geldenhuys

"""


##
#Imports
################################################################################
import os, time, threading

#Constants
################################################################################

""" Tuple containing the backup filename extensions"""
OLD_FILE_TUP    = ('.1bak','.2bak','.3bak','.4bak')
STR_TIME_FORMAT = '%d/%m/%Y %H:%M:%S'
CR              = '\n'
TIMESTAMP       = 'TIMESTAMP: '
SPACE           = ' '

#Classes
################################################################################
class ActionLogManager (object):

    """ Script action log storage manager class

        
    """

    ##
    #Constructor
    ############################################################################
    def __init__ (self):
        """ LogStorageManager constructor

        Initialising the LogStorageManager class

        :Parameters:
             - 
             
        :Returns:
             - None
        """
        ##
        #Private Members
        ########################################################################
        self._actionLogName  =   ('ActivityLogFile')
        self._logHandle      =   None
        self._maxEntries     =   20
        self._maxEntryCount  =   0
        self._logStr         =   None
        self._threadObject   =   None
        self._threadFlag     =   False
        
        """ check if the log file exists. If yes read the entries and update the
        entry counter."""
        if os.path.exists(self._actionLogName):
             """ The log file exists already """
             logFile = open(self._actionLogName, 'r')
             """ Read the number of entries from the log file"""
             self._maxEntryCount = len(logFile.readlines())
             print('No. of entries in Action log file:%d' %\
                              self._maxEntryCount )
             """ Close it"""
             logFile.close()
             
        """ Flag which will be usd to determine that the application is shutting down """
        self._isRunning = True         
        print('LogStorageManager Class Initialised..')
        
    ##
    #Methods
    ############################################################################
    def writeActionLog(self):
        """ This method just logs the logStr into log-action-file and increments
        the entry-count
        
        :Parameters:
            - None 
            
        :Returns:
            - None    
            
        :Raises:
            -`FileHandlingException` : Raised when the script encounters an
                                        IOError.
        """
        try:
                """ Opening the file in append mode and writing to it """
                self._logHandle = open(self._actionLogName, 'a+')
                
                self._logHandle.write(self._logStr)
                
                """ Incrementing the entry count """                
                self._maxEntryCount += 1
                
                print('The action log string written to the file')
                self._logHandle.close()
        except IOError:
                print('ActionLogFile could not be written to.')
                
    ############################################################################
    def logMessage(self, msg):
        """ This method will log the data together with time stamp.
        The eventual checking, file transfer and backup will also be done by
        this method. 

        :Parameters:
            - `msg` :   Contains the text message.

        :Returns:
            - None.

        :Raises:
            - `FileHandlingException` : Raised when file operation fails.
            
        """
        """ Getting the Time-Stamp """
        timeStr   = time.strftime(STR_TIME_FORMAT, time.localtime())
        
        string = msg
        
        self._logStr = TIMESTAMP + timeStr + SPACE + string + CR
        print self._logStr
       
        """ Calling the writeActionLog method """
        self.writeActionLog()
        
        """ Checking for Maximum entries """
        if( self._maxEntryCount >=  self._maxEntries):
            """ If the maximum entries is reached start the thread"""
            try:
                
                if self._threadFlag is not True:
                       
                    """ Creating a new thread object """
                    self._threadObject = WriteThread(self)

                    """ Starting the new thread """                
                    self._threadObject.start()
                    
                    """ Sleeping so that the thread runs """
                    time.sleep(1)
                else:
                    print('Log file already resized, Write thread active !!')
                    
            except Exception :
                printException()

    ############################################################################
    def threadRun (self):
        """run method of the thread
        
        This method will run as a separate thread which will handle the file overwrite function.
        
        :Parameters:
            - None

        :Returns:
            - None
        
        Setting the threadFlag so that any accidental duplicate spawning doesnt occur.
        """
        
        self._threadFlag = True
        print('Maximum entry count exceeded. Starting the '\
                        + 'Write thread..')
        
        
        try:
            
            try:
                """ Checks whether the files exist """                
                if(os.path.exists(self._actionLogName)):
                     
                    """ if 4th bak file exists remove it """
                    if(os.path.exists(self._actionLogName + OLD_FILE_TUP[3])):
                        os.remove(self._actionLogName + OLD_FILE_TUP[3])
                        print('Removing %s file' \
                                          %self._actionLogName + OLD_FILE_TUP[3])

                    """ Renaming the bak files to accomodate the new file """  
                    for index in range(2, -1, -1):
                        if(os.path.exists(self._actionLogName \
                                                            + OLD_FILE_TUP[index])):
                            os.rename(self._actionLogName + OLD_FILE_TUP[index],
                                      self._actionLogName + OLD_FILE_TUP[index + 1])
                    os.rename(self._actionLogName, self._actionLogName \
                                                                  + OLD_FILE_TUP[0])
            except IOError:
                printException()
                
            """ Making the entry count to 0 """                
            self._maxEntryCount = 0
        finally:
             """ Clearing the threadFlag when the thread ends """        
             self._threadFlag = False
    
    ############################################################################
    
    def stop (self):
        """ method for stopping the WriteThread
        
        :Parameters:
            - None

        :Returns:
            - None

        """
        """ Calling the stop method of the thread """
        print('Stopping ActionLogManager ..')
        if (self._threadFlag == True):
            """ Notify the Write thread that it needs to be stopped """
            self._isRunning = False    
            self._threadObject.join()
        
################################################################################
class WriteThread (threading.Thread):
    """ WriteThread class
        This class will overwrite old backup files and rename the other files in 
        separate threads.
    
    """

    ##        
    #Constructor
    ############################################################################
    def __init__ (self , caller):
        """ WriteThread constructor

        :Paramters:
            - `caller`  : Reference to the calling object
            

        :Returns:
            - None

        """
        """ Calling the constructor of the base class """
        threading.Thread.__init__ (self)
        
        self._caller = caller
        print('Initialising the WriteThread class ..')

    ############################################################################
    def run (self):
        """ run method of the WriteThread class

        :Parameters:
            - None

        :Returns:
            - None

        """
        print('Inside the run method of the WriteThread')

        """ Calling the threadRun method of the LogStorageManager class """
        self._caller.threadRun()
            
################################################################################
