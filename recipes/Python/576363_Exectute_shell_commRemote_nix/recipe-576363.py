import telnetlib
import sys

class RemoteShellCommand:
    def __init__(self, HostIP , UserName , Password  , OutputFileName = ''):
        # Set inner info
        self.info = {}
        
        ## prompt dict
        self.info['EndList'] = ["\n"]

        ## time out
        self.info['TimeOut'] = 30

        ## connection info
        self.info['HostIP'] = HostIP
        self.info['UserName'] = UserName
        self.info['Password'] = Password

        # init connection
        self.telnet_con = None
        self.read_eoc = False
        self.result_buf = ''

        # init output
        self.outputter = None
        if OutputFileName :
            self.outputter = open( OutputFileName , 'wb' )
        else:
            self.outputter = sys.stdout



    def __del__( self ):
        if self.telnet_con :
            self.telnet_con.close()
            self.telnet_con = None

        if (  self.outputter != sys.stdout ) and ( not self.outputter ) :
            self.close()
            self.outputter = None

    def Login( self ):
        if ( not self.info['HostIP'] ) or self.telnet_con :
            raise

        # init connection
        self.telnet_con = telnetlib.Telnet()
        self.telnet_con.open( self.info['HostIP'] )

        # login
        self.telnet_con.read_until ( 'login: ' ,  self.info['TimeOut'] )
        self.telnet_con.write( self.info['UserName'] + "\n" )
        self.telnet_con.read_until ( 'Password: ' ,  self.info['TimeOut'] )
        self.telnet_con.write( self.info['Password'] + "\n" )
        self.read_eoc = False

    def Logout( self ):
        if self.telnet_con :
            self.telnet_con.close()
            self.telnet_con = None

        if (  self.outputter != sys.stdout ) and ( not self.outputter ) :
            self.close()
            self.outputter = None


    def AddPrompt( self , content ):
        if content :
            self.info['EndList'].insert( 0 , content )
        else:
            raise


    def SendCmd( self , cmd , IsHasResult = True ):
        # clear the result buffer of command
        self.ReadBuffer()
        
        # send command
        self.result_buf = ''
        self.read_eoc = False
        self.telnet_con.write( cmd + "\n" )

        # collection the result
        if IsHasResult :
            self.ReadBuffer()

    def SendInterActiveCmd( self , cmd , InteractiveList , IsHasResult = True ):
        # check valid connection
        if not self.telnet_con :
            raise


        # clear the result buffer of command
        self.ReadBuffer()

        # send command
        self.result_buf = ''
        self.read_eoc = False
        self.telnet_con.write( cmd + "\n" )
        
        # Send Interactive command
        for each in InteractiveList :
            self.telnet_con.read_until( each[0] , self.info['TimeOut'] )
            self.telnet_con.write( each[1] + "\n" )

        # read command result
        if IsHasResult :
            self.ReadBuffer()

    def ReadBuffer( self ) :
        if self.read_eoc :
            return

        self.result_buf = ''

        matchIndex , matchObj , self.result_buf = self.telnet_con.expect( self.info['EndList'] , self.info['TimeOut'] )
        self.outputter.write( self.result_buf )

        while matchIndex == len(self.info['EndList']) - 1 :
            matchIndex , matchObj , self.result_buf = self.telnet_con.expect( self.info['EndList'] , self.info['TimeOut'] )
            self.outputter.write( self.result_buf )

        self.read_eoc = True
