class logpyl:
    """The logpyl class implements basic logging functionality for Python programs.

    A logpyl log consists of three files.  The log file contains the events logged
    to a logpyl object.  The metadata file contains information about the log, such
    as creation date, modification date, and name.  The checksum file contains an MD5
    hash created from the log and metadata files, and is used to check the integrity
    of log files."""

    def __init__(self,path='logs',name='NewLog',debug='off'):
        "Initialize or open logs as log objects are instantiated."
        import sys        
        import os.path
        self.events = []    # list of events written to this log
        self.debug = debug  # flag to activate/deactive debugging messages

        # First try the metadata file
        self.metadatafile = name + '.lmd'
        self.mdf = path + '/' + self.metadatafile
        mfn = os.path.isfile(self.mdf)
        if ( mfn ):
            if ( debug == 'on' ):
                print 'DEBUG: Metadata file',self.metadatafile,'exists.'
            # Since the file exists, get the metadata
            mfn = open(self.mdf,'r')
            self.name = mfn.readline().strip()
            self.path = mfn.readline().strip()
            self.logfile = mfn.readline().strip()
            self.metadatafile = mfn.readline().strip()
            self.checksumfile = mfn.readline().strip()
            self.created = mfn.readline().strip()
            self.modified = mfn.readline().strip()
            mfn.close()
            self.ldf = path + '/' + self.logfile
            self.cdf = path + '/' + self.checksumfile            
        else:
            if ( debug == 'on' ):
                print 'DEBUG: Metadata file',metadatafile,'does not exist.'
            self.name = name
            self.path = path
            self.metadatafile = name + '.lmd'
            self.logfile = name + '.log'
            self.checksumfile = name + '.md5'
            import time
            self.created = time.asctime(time.localtime(time.time()))
            self.mdf = path + '/' + self.metadatafile
            self.ldf = path + '/' + self.logfile
            self.cdf = path + '/' + self.checksumfile            
        
        # Then try the log file
        lfn = os.path.isfile(self.ldf)
        if ( lfn ):
            if ( debug == 'on' ):
                print 'DEBUG: Log file',self.logfile,'exists.'
            lfn = open(self.ldf,'r')
            for line in lfn.readlines():
                self.events.append(line.strip())
            lfn.close()
        else:
            if ( debug == 'on' ):
                print 'DEBUG: Log file',self.logfile,'does not exist.'

        # Finally, try the checksum file
        cfn = os.path.isfile(self.cdf)
        if ( cfn ):
            if ( debug == 'on' ):
                print 'DEBUG: Checksum file',self.checksumfile,'exists.'            
            cfn = open(self.cdf, 'r')
            self.md5 = cfn.read().strip()
            if ( debug == 'on' ):
                print 'DEBUG: MD5 checksum',self.md5,'read from',self.checksumfile
            cfn.close()
        else:
            if ( debug == 'on' ):
                print 'DEBUG: Checksum file',self.checksumfile,'does not exist.'
            pass

        # Once we have read the metadata, verify the integrity of the logfiles.
        self.verify()
            
    def add(self, eventclass="note", message="Your message here"):
        "Compose a log entry from the elements passed to add() and append it to the list of events."
        import time
        event = self.datetime() + ' ' + eventclass + ' ' + message
        if ( self.debug == "on" ):
            print 'DEBUG: Adding', event, 'to log', self.name
        self.modified = time.asctime(time.localtime(time.time()))            
        self.events.append(event)
        return

    def close(self):
        "Close the log by writing all log and metadata to the proper files.  Also update the checksum file."
        import sys
        import os
        "Write the current version of the log to a file and free the variables used by the log."
        if ( self.debug == 'on' ):            
            print "DEBUG: Closing log", self.name
        # If self.path does not exist, create the directory for the logfiles.
        if ( not os.path.exists(self.path ) ):
            if ( self.debug == 'on' ):
                print 'DEBUG: Directory ',self.path,' does not exist.  I am creating it now.'
            try:                
                os.makedirs(self.path)
                if ( self.debug == 'on' ):
                    print 'DEBUG: Created log file directory',self.path
            except OSERROR:
                print 'ERROR: Could not create log file directory',self.path                
        # Make sure that the metadata file is opened (created) and written.
        import time
        mfn = open(self.mdf, 'w+')
        mfn.write(self.name+'\n')
        mfn.write(self.path+'\n')
        mfn.write(self.logfile+'\n')
        mfn.write(self.metadatafile+'\n')        
        mfn.write(self.checksumfile+'\n')
        mfn.write(self.created+'\n')
        if ( not hasattr(self,'modified') ):
            mfn.write(self.created+'\n')
        else:
            mfn.write(self.modified+'\n')
        mfn.close()

        # Make sure that the log entries are written.
        lfn = open(self.ldf, 'w+')
        for event in self.events:
            lfn.write(event+'\n')
        lfn.close()

        # Create the MD5 checksum from the log file and metadata file
        import md5
        checksum = md5.new()
        mfn = open(self.mdf, 'r')
        for line in mfn.readlines():
            checksum.update(line)
        mfn.close()
        lfn = open(self.ldf, 'r')
        for line in lfn.readlines():
            checksum.update(line)
        lfn.close()
        cs = checksum.hexdigest()        
        if ( self.debug == 'on' ):
            print 'DEBUG: The MD5 digest of the metadata and log files is',cs
        
        # Make sure that the checksum file is opened (created) and written to.
        cfn = open(self.cdf,'w+')        
        cfn.write(cs+'\n')
        cfn.close()

    def datetime(self):
        "Generate the date/time stamp used in our log entries"
        import time
        datestamp = time.asctime(time.localtime(time.time()))
        return datestamp

    def info(self):
        print 'Info about log', self.name, ':'
        print '\tName:', self.name
        print '\tPath:', self.path
        print '\tLog file:', self.logfile
        print '\tMetadata file:', self.metadatafile
        print '\tChecksum file:', self.checksumfile
        if ( hasattr(self,'md5') ):
            print '\t\tMD5 Checksum:',self.md5
        print '\tNo. of entries:', len(self.events)
        if ( hasattr(self,'created') ):
            print '\tCreated:',self.created
        if ( hasattr(self,'modified') ) :
            print '\tModified:',self.modified                

    def printlog(self):
        print '\nPrinting log', self.name
        for event in self.events:
            print event
        print '\n'   

    def verify(self):
        "Compute the MD5 checksum for this log to see if the logfiles have been corrupted."
        # If there is no self.md5, no checksum exists for this log yet...
        if ( not hasattr(self,'md5') ):
            print 'WARNING: No MD5 checksum was found for log',self.name
            print 'WARNING: Log',self.name,'may be newly created, or it may be corrupt!'
            return
        
        # Otherwise, create the MD5 checksum from the log file and metadata file for verification
        import md5
        checksum = md5.new()
        mfn = open(self.mdf, 'r')
        for line in mfn.readlines():
            checksum.update(line)
        mfn.close()
        lfn = open(self.ldf, 'r')
        for line in lfn.readlines():
            checksum.update(line)
        lfn.close()
        cs = checksum.hexdigest()
        if ( self.debug == 'on' ):
            print 'DEBUG: The MD5 digest of the metadata and log files is',cs   
        if ( self.md5 == cs ):
            if ( self.debug == 'on' ):
                print 'DEBUG: The calculated MD5 checksum',cs,'matches the stored MD5 checksum',self.md5
        else:
            if ( self.debug == 'on' ):
                print 'DEBUG: The calculated MD5 checksum',cs,'does not match the stored MD5 checksum',self.md5                
            print 'ERROR: The MD5 checksum for log',self.name,'is inconsistent!'
            print 'ERROR: Log',self.name,'may be corrupt!'                

if __name__ == '__main__':

    # create a new log or open an existing log with debugging turned on
    # (disable debugging messages by passing 'off' as the third parm to logpyl())
    mylog = logpyl('logs','testlog','on')
    # add a couple of events to the log
    mylog.add("spam","Spam is US$1.95 per can.")
    mylog.add("eggs","Eggs are US$0.89 per dozen.")
    # print some summary information about the log
    mylog.info()
    # print the log entries
    mylog.printlog()
    # close the log
    mylog.close()
