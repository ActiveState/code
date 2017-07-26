import os
import sys
import win32com.client

class daoBaseClass:
    '''
    This base class is used to read/write data from/to daoDatabase.  It
    is necessarry that makepy be run against Microsoft DAO 3.6 Object
    Library (5.0) prior to using this class.
    '''
    #
    # Completely free, no warranties.
    #
    def __init__(self, databasepath, SQL_query=None, logf=None, _trace=0, _debug=0):
        #----------------------------------------------------------------------
        # Create an attribute to hold EOF status
        #----------------------------------------------------------------------
        self.EOF=0
        self._AddNew=0
        self.path=databasepath
        self.logf=logf
        self._trace=_trace
        self._debug=_debug
        #
        # Support both MoveNext and fetchone with same method
        #
        self.fetchone=self.MoveNext
        #
        # Dispatch the DAO Engine
        #
        try:    self.daoEngine=win32com.client.Dispatch("DAO.DBEngine.36")
        except:
            emsg="Unable to dispatch DAO.DBEngine.36"
            self.abort(emsg)
            
        #----------------------------------------------------------------------
        # Try to open the database
        #----------------------------------------------------------------------
        try:     self.daoDB = self.daoEngine.OpenDatabase(self.path)
        except: 
            emsg="Unable open database file=%s" % self.path
            self.abort(emsg)

        #----------------------------------------------------------------------
        # If query is specified, open a recordset with it
        #----------------------------------------------------------------------
        if SQL_query: self.execute(SQL_query)
        return

    def __getitem__(self, key):
        #----------------------------------------------------------------------
        # Try to get the Value for the field requested from the recordset
        #----------------------------------------------------------------------
        try:    return self.daoRS.Fields(key).Value
        except:
            emsg="Field name '%s' not found in current record" % key
            if self.logf: self.logf.writelines("E", emsg)
            else:         print emsg
            return None

    def __setitem__(self, key, value):
        #----------------------------------------------------------------------
        # If I'm adding new information to a record, skip call to Edit()
        #----------------------------------------------------------------------
        if not self._AddNew: self.daoRS.Edit()
        #----------------------------------------------------------------------
        # Try to set the value for the field requested in the recordset
        #----------------------------------------------------------------------
        try:    self.daoRS.Fields(key).Value=value
        except:
            emsg="Unable to set Field name '%s' to value=%s" % (key, str(value))
            if self.logf: self.logf.writelines("E", emsg)
            else:         print emsg
        
        else:
            #----------------------------------------------------------------------
            # If I'm adding new information to a record, skip call to Update()
            #----------------------------------------------------------------------
            if not self._AddNew:  self.daoRS.Update()
            
        return

    def execute(self, SQL_query):
        '''
        This method is used to execute a SQL_query against the TimePilot
        database.
        '''
        try: self.daoRS = self.daoDB.OpenRecordset(SQL_query)
        except:
            emsg="Unable execute SQL_query=%s" % SQL_query
            if self.logf: self.logf.writelines("E", emsg)
            else:         print emsg

        self.EOF=self.daoRS.EOF            
        return
    
    def MoveNext(self):
        self.daoRS.MoveNext()
        self.EOF=self.daoRS.EOF
        return

    def AddNew(self):
        #----------------------------------------------------------------------
        # Sets a flag so that __setitem__ will know that I'm adding new
        # information not editing existing information.
        #----------------------------------------------------------------------
        self._AddNew=1
        self.daoRS.AddNew()
        return

    def Update(self):
        #----------------------------------------------------------------------
        # Resets flag so I'm no longer in AddNew mode
        #----------------------------------------------------------------------
        self._AddNew=0
        self.daoRS.Update()
        return

    def close(self):
        self.daoRS.Close()
        self.daoDB.Close()

    def abort(self, emsg):
        if self.logf: self.logf.writelines("E", emsg)
        else:         print emsg
        sys.exit(emsg)
