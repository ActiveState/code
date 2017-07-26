# CASpy - Python implementation of DVB Simulcrypt CAS
# Currently, only implement EMM Generator (EMMG)
# Implementing DVB-Simulcrypt message :

import binascii
import socket
import ctypes
from time import sleep
import math

# Utility functions, to allow for serialization of the ctypes.Structure classes
def serialize(ctypesObj):
    """
    FAQ: How do I copy bytes to Python from a ctypes.Structure?
    """
    return buffer(ctypesObj)[:]

def deserialize(ctypesObj, inputBytes):
    """
    FAQ: How do I copy bytes to a ctypes.Structure from Python?
    """
    fit = min(len(inputBytes), ctypes.sizeof(ctypesObj))
    ctypes.memmove(ctypes.addressof(ctypesObj), inputBytes, fit)

INPUT_BUFFER_LENGTH     = 1024                                                  # Units : [Bytes]. Input buffer size of received TCP messages
SEND_EMM_PERIOD_TIME    = 50e-3                                                 # Units : [Number of Seconds] / [IP packet]
SEND_EMM_FREQUENCY      = 1.0 / SEND_EMM_PERIOD_TIME                            # Units : [Number of IP Packets] / [Sec]
BYTE_TO_BIT_SCALE       = 8
KBPS_TO_BPS_SCALE       = 1000.0
BPS_TO_KBPS_SCALE       = 0.001
#EMM_DUMMY_DATA = binascii.unhexlify('01B040FFFFC7000009160500E03213012014030078001403007C0014030FFF4009040602E0C109040D01E1F409110500E0AB130120140300E800140300E8107A38F9E2')


# ****************************************************
# DVB Simulcrypt messages semantic 
# ****************************************************
simulcrypt_protocol_version         = 0x02                                      

# Parameters type value according to Simulcrypt standard, 6.22 Table 5 - Parameters : 
client_id_type                      = 0x0001                                    
client_id_length                    = 4                                    

section_TSpkt_flag_type             = 0x0002                                    
section_TSpkt_flag_length           = 1

data_channel_id_type                = 0x0003                                    
data_channel_id_length              = 2

data_stream_id_type                 = 0x0004                                    
data_stream_id_length               = 2

datagram_type                       = 0x0005                                    # Parameter length : Variable

bandwidth_type                      = 0x0006                                    # Units: kbit/s 
bandwidth_length                    = 2 

data_type_type                      = 0x0007                                    
data_type_length                    = 1

data_id_type                        = 0x0008                                    
data_id_length                      = 2

error_status_type                   = 0x7000                                    # See clause 6.2.6
error_status_length                 = 2

# According to 6.4, 6.5 - Messages :                 
Channel_setup_message_Type          = 0x0011
Channel_test_message_Type           = 0x0012                
Channel_status_message_Type         = 0x0013
Channel_close_message_Type          = 0x0014
Channel_error_message_Type          = 0x0015
Stream_setup_message_Type           = 0x0111
Stream_test_message_Type            = 0x0112
Stream_status_message_Type          = 0x0113
Stream_close_request_message_Type   = 0x0114
Stream_close_response_message_Type  = 0x0115
Stream_error_message_Type           = 0x0116
Stream_BW_request_message_Type      = 0x0117
Stream_BW_allocation_message_Type   = 0x0118
Data_provision_messageType          = 0x0211


# ****************************************************
#        SIMULCRYPT TLV CLASS
# ****************************************************
class CMessageHeader (ctypes.BigEndianStructure):
    """
    message_header
    """
    _pack_      = 1
    
    _length_    = 5
    
    _fields_    = [("protocol_version",    ctypes.c_ubyte),
                   ("message_type",        ctypes.c_ushort),
                   ("message_length",      ctypes.c_ushort)]

class CTypeLength (ctypes.BigEndianStructure):
    """
    Type Length, of the TLV struct
    """
    _pack_      = 1
    
    _length_    = 4
    
    _fields_    = [("param_type",        ctypes.c_ushort),
                   ("param_length",      ctypes.c_ushort)]
    
class CByteParam (ctypes.BigEndianStructure):
    """
    One byte unsigned parameter
    """
    _pack_      = 1
    
    _length_    = 5
    
    _fields_    = [("param_type",        ctypes.c_ushort),
                   ("param_length",      ctypes.c_ushort),
                   ("param_value",       ctypes.c_ubyte)]

class CShortParam (ctypes.BigEndianStructure):
    """
    Two byte unsigned parameter
    """
    _pack_      = 1
    
    _length_    = 6
    
    _fields_    = [("param_type",        ctypes.c_ushort),
                   ("param_length",      ctypes.c_ushort),
                   ("param_value",       ctypes.c_ushort)]

class CLongParam (ctypes.BigEndianStructure):
    """
    Four byte unsigned parameter
    """
    _pack_      = 1
    
    _length_    = 8
        
    _fields_ = [("param_type",        ctypes.c_ushort),
                ("param_length",      ctypes.c_ushort),
                ("param_value",       ctypes.c_ulong)]


# ****************************************************
#        EMMG CLASS
# ****************************************************
class CEMMG:
    """
    Template for EMMG Simulator
    """
    def __init__(   self, 
                    client_id,                      # #1 
                    section_TSpkt_flag,             # #2
                    data_channel_id,                # #3
                    data_stream_id,                 # #4
                    bandwidth,                      # #5                        # Unit : Kbps
                    data_id,                        # #6
                    data_type,                      # #7
                    inputFile):                     # #8
        """
        These 7 parameters (excluding the actual data) form a single EMM stream. 
        One channel, One stream, One data id . 
        """
        # #1 
        self.client_id          = CLongParam(client_id_type,
                                             client_id_length,
                                             client_id)
        # #2                                               
        self.section_TSpkt_flag = CByteParam(section_TSpkt_flag_type,
                                             section_TSpkt_flag_length,
                                             section_TSpkt_flag)
        # #3                
        self.data_channel_id    = CShortParam(data_channel_id_type,
                                              data_channel_id_length,
                                              data_channel_id)
        # #4        
        self.data_stream_id     = CShortParam(data_stream_id_type,
                                              data_stream_id_length,
                                              data_stream_id)

        # #6        
        self.data_id            = CShortParam(data_id_type,
                                              data_id_length,
                                              data_id)
        # #7        
        self.data_type          = CByteParam(data_type_type,
                                             data_type_length,
                                             data_type)
        
        
        #8             
        #Initialize members                           
        self.Section                = 0
        self.IpEmmSectionPerCycle   = 0        
        self.IpEmmSection           = 0
        self.IpEmmSectionLen        = 0                                                
        self.dataTypeLength         = 0
        self._buildIpEmm_(inputFile, bandwidth)
         
        #5
        #Initialize members
        self.minimumBPS     = 0
        self.ReqBWfromMux   = 0
        self.requestBW      = 0  
        self._buildReqBWfromMux_()
               
        # DEBUG PRINTS        
        print 'Section file \"%s\" length %d, will be sent at %d mSec per cycle ' % (inputFile, len(self.Section), SEND_EMM_PERIOD_TIME * KBPS_TO_BPS_SCALE)
        print 'Minimum bitrate for this section (one section per cycle) : %.3f Kbps ' % (self.minimumBPS * BPS_TO_KBPS_SCALE)
        print 'User requested bandwidth %d Kbps, which is %d sections per cycle, %.3f Kbps ' % (bandwidth, self.IpEmmSectionPerCycle, (self.minimumBPS * self.IpEmmSectionPerCycle * BPS_TO_KBPS_SCALE))
        print 'Actual Requested Bandwidth from Multiplexer will be %d Kbps (%d sections per cycle)' % (self.ReqBWfromMux, (self.IpEmmSectionPerCycle + 1))

    def _buildIpEmm_ (self, inputFile, bandwidth):
        """
        Build data segment sent to TCP each SEND_EMM_PERIOD_TIME seconds
        EMMG sends EMMs every fixed cycle time : SEND_EMM_PERIOD_TIME
        Hence, the actual bitrate is determined by the number of sections being sent each time.
        Calculation of the number of EMM sections each cycle is done in EmmSecPerCycle  
        """
        fd                          = open(inputFile, 'rb')   
        self.Section                = fd.read()
        fd.close()                
        self.IpEmmSectionPerCycle   = self._calcNumberSectionsPerCycle_(bandwidth, len(self.Section))        
        self.IpEmmSection           = self.Section * self.IpEmmSectionPerCycle
        self.IpEmmSectionLen        = len(self.IpEmmSection)                                                
        self.dataTypeLength         = CTypeLength (datagram_type,
                                                   self.IpEmmSectionLen)  

    def _buildReqBWfromMux_ (self):
        """
        Build requested BW from Multiplexer
        """
        self.minimumBPS     = SEND_EMM_FREQUENCY * len(self.Section) * BYTE_TO_BIT_SCALE
        self.ReqBWfromMux   = int( self.minimumBPS * (self.IpEmmSectionPerCycle + 1) * BPS_TO_KBPS_SCALE )                  
        self.requestBW      = CShortParam(bandwidth_type,
                                          bandwidth_length,
                                          self.ReqBWfromMux)
        
    def _calcNumberSectionsPerCycle_ (self, requiredBW, sectionLength):
        """
        Calculate the number of sections needed to be transmitted each cycle of SEND_EMM_PERIOD_TIME seconds,
        given requiredBW in Kbps
        """
        SectionPerCycle = ((requiredBW * KBPS_TO_BPS_SCALE) * SEND_EMM_PERIOD_TIME) / (sectionLength * BYTE_TO_BIT_SCALE)                                   
        SectionPerCycle = int (math.ceil(SectionPerCycle))                      # Round up and cast to int the number of EMM sections being transmitted per cycle
        
        return SectionPerCycle

    def updateIpEmm (self, inputFile, requiredBW):
        """
        Update IP Emm length according to new requiredBW and new file.
        This method DOES NOT negotiate with Mux new BW Threshold, if requiredBW exceeds present threshold
        """
        self._buildIpEmm_(inputFile, requiredBW)
        
    def prepare_channel_setup_Msg (self):
        """
        Prepares and packs the emm_channel_setup message 
        """

        msgBody     =   serialize(self.client_id)           +   \
                        serialize(self.data_channel_id)     +   \
                        serialize(self.section_TSpkt_flag)


        
        msgHeader   =   serialize(CMessageHeader (simulcrypt_protocol_version,  # DVB simulcrypt protocol : 0x02
                                                  Channel_setup_message_Type,                 
                                                  len(msgBody)))                # Calculate total message length
                                          
        totalMsg    = msgHeader + msgBody
        
        return totalMsg 

    def prepare_stream_setup_Msg (self):
        """
        Prepares and packs the emm_stream_setup message 
        """

        msgBody     =   serialize(self.client_id)           +   \
                        serialize(self.data_channel_id)     +   \
                        serialize(self.data_stream_id)      +   \
                        serialize(self.data_id)             +   \
                        serialize(self.data_type)                                
        
        msgHeader   =   serialize(CMessageHeader (simulcrypt_protocol_version,  # DVB simulcrypt protocol : 0x02
                                                  Stream_setup_message_Type,                 
                                                  len(msgBody)))                # Calculate total message length
                                          
        totalMsg    = msgHeader + msgBody
        
        return totalMsg 
    
    def prepare_stream_BW_request_Msg (self):
        """
        Prepares and packs the stream bandwidth request message 
        """

        msgBody     =   serialize(self.client_id)           +   \
                        serialize(self.data_channel_id)     +   \
                        serialize(self.data_stream_id)      +   \
                        serialize(self.requestBW)                               
        
        msgHeader   =   serialize(CMessageHeader (simulcrypt_protocol_version,  # DVB simulcrypt protocol : 0x02
                                                  Stream_BW_request_message_Type,                 
                                                  len(msgBody)))                # Calculate total message length
                                          
        totalMsg    = msgHeader + msgBody
        
        return totalMsg 

    def prepare_Provision_Data_Msg (self):
        """
        Prepares and packs the Provision Data message 
        """

        msgBody     =   serialize(self.client_id)           +   \
                        serialize(self.data_channel_id)     +   \
                        serialize(self.data_stream_id)      +   \
                        serialize(self.data_id)             +   \
                        serialize(self.dataTypeLength)      +   \
                        self.IpEmmSection                                               
        
        msgHeader   =   serialize(CMessageHeader (simulcrypt_protocol_version,  # DVB simulcrypt protocol : 0x02
                                                  Data_provision_messageType,                 
                                                  len(msgBody)))                # Calculate total message length
                                          
        totalMsg    =   msgHeader + msgBody
        
        return totalMsg 

    def receiveMessage(self, strMsg):
        """
        Parse buffer received from mux
        """
        header      = CMessageHeader(0,0,0)
        paramTL     = CTypeLength   (0,0)                                       # Parameter Type-Length values (from the trio TYPE-LENGTH-VALUE) 
        longParam   = CLongParam    (0,0,0)
        shortParam  = CShortParam   (0,0,0)
        byteParam   = CByteParam    (0,0,0)

        JUSTIFY_LEN = 25
                        
        # Parse header       
        
        deserialize (header, strMsg)
        
        if header.message_type      == Channel_setup_message_Type           :
            print "Message type Channel_setup_message "
            
        elif header.message_type    == Channel_test_message_Type            :
            print "Message type Channel_test_message "  

        elif header.message_type    == Channel_status_message_Type          :
            print "Message type Channel_status_message "  

        elif header.message_type    == Channel_close_message_Type           :
            print "Message type Channel_close_message "  

        elif header.message_type    == Channel_error_message_Type           :
            print "Message type Channel_error_message "  

        elif header.message_type    == Stream_setup_message_Type            :
            print "Message type Stream_setup_message "

        elif header.message_type    == Stream_test_message_Type            :
            print "Message type Stream_test_message "

        elif header.message_type    == Stream_status_message_Type           :
            print "Message type Stream_status_message "

        elif header.message_type    == Stream_close_request_message_Type    :
            print "Message type Stream_close_request_message "
        
        elif header.message_type    == Stream_close_response_message_Type   :
            print "Message type Stream_close_response_message "
                
        elif header.message_type    == Stream_error_message_Type            :
            print "Message type Stream_error_message "        
        
        elif header.message_type    == Stream_BW_request_message_Type       :
            print "Message type Stream_BW_request_message "

        elif header.message_type    == Stream_BW_allocation_message_Type    :
            print "Message type Stream_BW_allocation_message "
                    
        elif header.message_type    == Data_provision_messageType           :
            print "Message type Data_provision_message "
        
        print   "Message Length   : ".ljust(JUSTIFY_LEN), header.message_length                        
               
        
        # Parse message body. Iterate on TLV structures        
        strMsg = strMsg[CMessageHeader._length_ : ]
                
        while len(strMsg) > 0 :
            
            deserialize(paramTL, strMsg)
            
            if paramTL.param_type == client_id_type :
                deserialize (longParam, strMsg)
                print "Client id : ".ljust(JUSTIFY_LEN), "0x%X" % longParam.param_value                
                strMsg = strMsg [CLongParam._length_ : ]
                
            elif paramTL.param_type == section_TSpkt_flag_type :
                deserialize (byteParam, strMsg)
                print "section TSpkt flag : ".ljust(JUSTIFY_LEN), byteParam.param_value                
                strMsg = strMsg [CByteParam._length_ : ]                                                 
        
            elif paramTL.param_type == data_channel_id_type :
                deserialize (shortParam, strMsg)
                print "data channel id : ".ljust(JUSTIFY_LEN), shortParam.param_value                
                strMsg = strMsg [CShortParam._length_ : ]                                                 
                
            elif paramTL.param_type == data_stream_id_type :
                deserialize (shortParam, strMsg)
                print "data stream id : ".ljust(JUSTIFY_LEN), shortParam.param_value                
                strMsg = strMsg [CShortParam._length_ : ]                                                 
                
            elif paramTL.param_type == bandwidth_type :
                deserialize (shortParam, strMsg)
                print "bandwidth : ".ljust(JUSTIFY_LEN), shortParam.param_value                
                strMsg = strMsg [CShortParam._length_ : ]        

            elif paramTL.param_type == data_type_type :
                deserialize (byteParam, strMsg)
                print "data type : ".ljust(JUSTIFY_LEN), byteParam.param_value                
                strMsg = strMsg [CByteParam._length_ : ]        

            elif paramTL.param_type == data_id_type :
                deserialize (shortParam, strMsg)
                print "data id : ".ljust(JUSTIFY_LEN), shortParam.param_value                
                strMsg = strMsg [CShortParam._length_ : ]        

            elif paramTL.param_type == error_status_type :
                deserialize (shortParam, strMsg)
                print "error status : ".ljust(JUSTIFY_LEN), shortParam.param_value                
                strMsg = strMsg [CShortParam._length_ : ]        


        
        
if __name__ == '__main__':
                   
    EMM_INPUT_FILE = r'D:\EmmgSimulator\section'  
                     
    #--- Prepare EMMG
    EMMG1 = CEMMG ( client_id           = 0x00099999, 
                    section_TSpkt_flag  = 0x0,
                    data_channel_id     = 0x1,
                    data_stream_id      = 0x32,
                    bandwidth           = 20,                                 # Units : Kbps. bandwidth request
                    data_id             = 0x1,
                    data_type           = 0x1,
                    inputFile           = EMM_INPUT_FILE)  

    #--- Connect to Mux EMM TCP SERVER
    muxEmmSocket    = socket.socket()   
    host            = '10.40.2.195'
    port            = 20000
    muxEmmSocket.connect ((host, port))
    
    print
    print " CHANNEL SETUP" 
    print " *************"
    #--- Send Channel Setup Message
    sendMsg = EMMG1.prepare_channel_setup_Msg()        
    muxEmmSocket.send(sendMsg);
    
    #--- Get Channel Status Message
    muxEmmMsg = muxEmmSocket.recv(INPUT_BUFFER_LENGTH)    
    EMMG1.receiveMessage(muxEmmMsg)

    print
    print " STREAM SETUP" 
    print " ************"
    #--- Send Stream Setup Message
    sendMsg = EMMG1.prepare_stream_setup_Msg()        
    muxEmmSocket.send(sendMsg);
    
    #--- Get Stream Status Message
    muxEmmMsg = muxEmmSocket.recv(INPUT_BUFFER_LENGTH)    
    EMMG1.receiveMessage(muxEmmMsg)    

    print
    print " Stream BW Allocation" 
    print " ********************"
    #--- Send stream BW request Message
    sendMsg = EMMG1.prepare_stream_BW_request_Msg()        
    muxEmmSocket.send(sendMsg);
    
    #--- Get Stream BW allocation Message
    muxEmmMsg = muxEmmSocket.recv(INPUT_BUFFER_LENGTH)    
    EMMG1.receiveMessage(muxEmmMsg)    

    print
    print " Send provision Data" 
    print " *******************"
    #--- Send stream BW request Message
    sendMsg = EMMG1.prepare_Provision_Data_Msg()        
    
    counter = 0
        
    while True :
        
        # Send TCP message with the required EMM
        muxEmmSocket.send(sendMsg);
        counter += 1
            
        # Change EMM bitrate 
        if counter == 400:                                                      
            EMMG1.updateIpEmm(EMM_INPUT_FILE, 60)
            sendMsg = EMMG1.prepare_Provision_Data_Msg()
        # Change EMM bitrate 
        elif counter == 800:                                                      
            EMMG1.updateIpEmm(EMM_INPUT_FILE, 150)
            sendMsg = EMMG1.prepare_Provision_Data_Msg()
        # Change EMM bitrate 
        elif counter == 1200:                                                      
            EMMG1.updateIpEmm(EMM_INPUT_FILE, 20)
            sendMsg = EMMG1.prepare_Provision_Data_Msg()        
        
        # Wait for SEND_EMM_PERIOD_TIME before sending again    
        sleep (SEND_EMM_PERIOD_TIME)                        
        
        # Print statistics
        if counter == 8000:
            break
        elif (counter % 80) == 0 :
            print "Sent " , counter, " packets."    
            print "Message length : %d" % len(sendMsg)
               

 
    
    
