"""
DateTimeSyncer with Daylight Savings Time adjustment

Synchronizes computer's current date and time with Daylight Savings adjustment
directly without depending on operating system or Python's time.localtime().

This allows programmers to update Daylight Savings Time rules without
depending on external updates to OS or Python.

Double-clicking  this module will synchronize your computer's date and time on a Windows machine.  

Jack Trainor 2008
"""
import socket
import struct
import os
import sys
import time
import calendar

# ==============================================================================
# Constants
# ==============================================================================
SNTP_SERVER = "usno.pa-x.dec.com"  # substitute other servers as desired
SNTP_PORT = 123

TIME_1970 = 2208988800L 

MINUTE_SECONDS = 60
HOUR_SECONDS = 60 * MINUTE_SECONDS
DAY_SECONDS = 24 * HOUR_SECONDS
WEEK_SECONDS = 7 * DAY_SECONDS

JAN = 1
FEB = 2
MAR = 3
APR = 4
MAY = 5
JUN = 6
JUL = 7
AUG = 8
SEP = 9
OCT = 10
NOV = 11
DEC = 12

MON = 0
TUE = 1
WED = 2
THU = 3
FRI = 4
SAT = 5
SUN = 6

UNIVERSAL = "Universal"
EASTERN = "Eastern"
CENTRAL = "Central"
MOUNTAIN = "Mountain"
PACIFIC = "Pacific"

TIME_ZONE_OFFSETS_TO_UTC = { 
    UNIVERSAL: 0, 
    EASTERN: 5 * HOUR_SECONDS, 
    CENTRAL: 6 * HOUR_SECONDS, 
    MOUNTAIN: 7 * HOUR_SECONDS, 
    PACIFIC: 8 * HOUR_SECONDS 
    }

# ==============================================================================
# Time utilities
# ==============================================================================
def secs_to_tuple(secs):
    """ Convert seconds to time tuple in UTC. """
    return time.gmtime(secs)
    
def tuple_to_secs(tuple):
    """ Convert time tuple to UTC seconds. """
    return calendar.timegm(tuple)

def fill_in_tuple(tuple):
    """ Ensure that all tuple fields are filled in as completely as possible. """
    secs = tuple_to_secs(tuple)
    out_tuple = secs_to_tuple(secs)
    return out_tuple

def local_tuple_to_utc_secs(time_tuple, timezone=UNIVERSAL, is_dst=False):
    """ Convert time tuple with timezone and DST info to UTC seconds. """
    """ NOTE: It's up to caller that is_dst flag makes sense. """
    time_tuple = fill_in_tuple(time_tuple)
    secs = tuple_to_secs(time_tuple)
    secs += TIME_ZONE_OFFSETS_TO_UTC[timezone]
    if is_dst:
        secs -= HOUR_SECONDS
    return secs

def local_tuple_to_utc_tuple(time_tuple, timezone=UNIVERSAL, is_dst=False):
    """ Convert time tuple with timezone and DST info to UTC tuple. """
    """ NOTE: It's up to caller that is_dst flag makes sense. """
    utc_secs = local_tuple_to_utc_secs(time_tuple, timezone, is_dst)
    utc_tuple = secs_to_tuple(utc_secs)
    return secs

def utc_tuple_to_local_secs(utc_tuple, output_timezone=UNIVERSAL, is_dst=False):
    """ Convert UTC time tuple to seconds according to timezone and is_dst. """
    """ NOTE: It's up to caller that is_dst flag makes sense. """
    utc_tuple = fill_in_tuple(utc_tuple)
    secs = tuple_to_secs(utc_tuple)
    secs -= TIME_ZONE_OFFSETS_TO_UTC[timezone]
    if is_dst:
        secs += HOUR_SECONDS
    return secs

def utc_tuple_to_local_tuple(utc_tuple, output_timezone=UNIVERSAL, is_dst=False):
    """ Convert UTC time tuple to tuple in terms of timezone and is_dst. """
    """ NOTE: It's up to caller that is_dst flag makes sense. """
    local_secs = utc_tuple_to_local_secs(utc_tuple, output_timezone, is_dst)
    return secs_to_tuple(local_secs)            

def debug_secs(secs):
    return "%d: %s" % (secs, time.asctime(secs_to_tuple(secs)))

def debug_tuple(tuple):
    return "%s: %s" % (tuple, time.asctime(tuple))


# ==============================================================================
# Daylight Savings Time functions
# ==============================================================================
def calc_DST_utc_secs(start_tuple, timezone=UNIVERSAL, is_dst=False, weekday=SUN):
    """ Calculate DST transition in UTC seconds. DST can be specified as the 
    first weekday (usually Sunday) after a date and time in a local time zone. """
    start_tuple = fill_in_tuple(start_tuple)
    utc_secs = local_tuple_to_utc_secs(start_tuple, timezone, is_dst)
    utc_tuple = secs_to_tuple(utc_secs)
    
    # Walk to first day on or after start day that corresponds to weekday.
    # Compensate in case weekday changes in conversion to UTC.
    weekday = ((weekday + utc_tuple[6] - start_tuple[6]) % 7)
    while True:
        if utc_tuple[6] == weekday:
            break
        utc_secs += DAY_SECONDS
        utc_tuple = secs_to_tuple(utc_secs)
    return utc_secs

def calc_DST_start_utc_secs(year, timezone):
    """ Calculates start of US Daylight Savings Time for year and timezone. """
    if year <= 2006:
        return calc_DST_utc_secs((year, APR, 1, 2, 0, 0, 0, 0, 0), timezone)
    else:
        return calc_DST_utc_secs((year, MAR, 8, 2, 0, 0, 0, 0, 0), timezone)
        
def calc_DST_end_utc_secs(year, timezone):
    """ Calculates end of US Daylight Savings Time for year and timezone. """
    if year <= 2006:
        return calc_DST_utc_secs((year, OCT, 25, 2, 0, 0, 0, 0, 0), timezone, True)
    else:
        return calc_DST_utc_secs((year, NOV, 1, 2, 0, 0, 0, 0, 0), timezone, True)


# ==============================================================================
# get_current_SNTP_time
# ==============================================================================
def get_current_SNTP_time(sntp_server=SNTP_SERVER):
    """ Acquires current time in UTC secs from SNTP server. """
    """ Thanks to Simon Foster's "Simple (very) SNTP client" recipe:
    http://code.activestate.com/recipes/117211/ """
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = '\x1b' + 47 * '\0'
        client.sendto(data, (sntp_server, SNTP_PORT))
        data, address = client.recvfrom(1024)
        if data:
            utc_secs = struct.unpack('!12I', data)[10]
            utc_secs -= TIME_1970
            return utc_secs
    except Exception, e:
        print "get_current_SNTP_time failed:", sntp_server
    return None
    
    
# ==============================================================================
# OS_set_datetime
# ==============================================================================
def Windows_set_datetime(dt):
    """ Uses DateTime instance to set OS date and time for Windows computer. """
    print "date %d/%d/%d" % (dt.month(), dt.date(), dt.year())
    print "time %d:%d:%d" % (dt.hour(), dt.minutes(), dt.seconds())
    os.system("date %d/%d/%d" % (dt.month(), dt.date(), dt.year()))
    os.system("time %d:%d:%d" % (dt.hour(), dt.minutes(), dt.seconds()))
    
def Linux_set_datetime(dt):
    """ Uses DateTime instance to set OS date and time for Linux computer. """
    """ NOTE: untested, presumes root privileges """
    os.system("date %d%d%d%d%d" % (dt.month(), dt.date(), dt.hour(), dt.seconds(),dt.year()))
    os.system("hwclock --utc --systohc")


# ==============================================================================
# class DateTime
# ==============================================================================
class DateTime(object):
    """ DateTime provides simple conversion of a time in UTC seconds to a
    time tuple expressed in another time zone including compensation for
    Daylight Savings Time. 
    
    * All calculations are based on __utc_secs.
    * __output_tuple is recalculated each time _utc_secs or _output_timezone changes.
    * isdst tuple field is ignored.
    * tuple fields are accessed by index for compatibility with older Pythons.
    * tuple fields are wrapped by DateTime field methods. 
    """
    def __init__(self, utc_secs=0, output_timezone=UNIVERSAL):
        self.__utc_secs = 0
        self.__output_tuple = None
        self.set_by_utc_secs(utc_secs, output_timezone)
        
    def set_by_utc_secs(self, utc_secs, output_timezone=UNIVERSAL):
        self.__utc_secs = utc_secs
        self.set_output_timezone(output_timezone)
        return self

    def set_output_timezone(self, output_timezone):
        self.__output_timezone = output_timezone
        self.calc_output_tuple()
        return self

    def calc_output_tuple(self):
        utc_secs = self.__utc_secs
        utc_tuple = secs_to_tuple(utc_secs)
        year = utc_tuple[0]
        self.is_dst = False
        timezone = self.__output_timezone
        output_secs = utc_secs - TIME_ZONE_OFFSETS_TO_UTC[timezone]
        if timezone != UNIVERSAL:
            dst_start = calc_DST_start_utc_secs(year, timezone)
            dst_end = calc_DST_end_utc_secs(year, timezone)
            if (utc_secs >= dst_start and utc_secs <= dst_end):
                output_secs += HOUR_SECONDS
                self.is_dst = True
        self.__output_tuple = secs_to_tuple(output_secs)
        self.db_output = time.asctime(self.__output_tuple)
        return self

    def set_utc_secs(self, utc_secs):
        self.__utc_secs = utc_secs
        self.__timezone = UNIVERSAL
        self.__output_tuple = secs_to_tuple(utc_secs)
        return self
        
    def offset_secs(self, secs):
        self.__utc_secs += secs
        self.__output_tuple()
        return self
        
    def output_tuple(self):
        return self.__output_tuple
    
    def utc_secs(self):
        return self.__utc_secs
    
    def year(self):
        return self.__output_tuple[0]
    
    def month(self):
        return self.__output_tuple[1]
    
    def date(self):
        return self.__output_tuple[2]
    
    def hour(self):
        return self.__output_tuple[3]
    
    def minutes(self):
        return self.__output_tuple[4]
    
    def seconds(self):
        return self.__output_tuple[5]
    
    def weekday(self):
        return self.__output_tuple[6]
    
    def yearday(self):
        return self.__output_tuple[6]
    
# ==============================================================================
# class DateTimeSyncer
# ==============================================================================
class DateTimeSyncer(object):
    """ DateTimeSyncer acquires current time from an SNTP servers, converts
    that time to a DateTime instance adjusted to Daylight Savings time
    of specified timezone. 
    
    Example: DateTimeSyncer(PACIFIC).execute() 
    """
    def __init__(self, timezone, sntp_server=SNTP_SERVER):
        self.sntp_server = sntp_server
        self.timezone = timezone
    
    def execute(self, set_date_time_func=Windows_set_datetime, pause=False):
        """ Perform time synchronization. """
        """ For other non-Windows platforms, write corresponding function 
        set_date_time_func and pass it in. """
        utc_secs = get_current_SNTP_time(self.sntp_server)
        if utc_secs:
            dt = DateTime(utc_secs, self.timezone)
            set_date_time_func(dt)
            print "DateTimeSyncer succesful."
        else:
            print "DateTimeSyncer failed."
        if pause:
            raw_input("Press a key...")
            
def test():
    ds_start_minus1_dt = DateTime(calc_DST_start_utc_secs(2008, PACIFIC)-1, PACIFIC)
    print "DST start-1s:", debug_tuple(ds_start_minus1_dt.output_tuple())   
    ds_start_dt = DateTime(calc_DST_start_utc_secs(2008, PACIFIC), PACIFIC)
    print "DST start:", debug_tuple(ds_start_dt.output_tuple())
    ds_start_plus_dt = DateTime(calc_DST_start_utc_secs(2008, PACIFIC)+1, PACIFIC)
    print "DST start+1s:", debug_tuple(ds_start_plus_dt.output_tuple())
    print
    ds_end_minus1_dt = DateTime(calc_DST_end_utc_secs(2008, PACIFIC)-1, PACIFIC)
    print "DST end-1s:", debug_tuple(ds_end_minus1_dt.output_tuple())
    ds_end_dt = DateTime(calc_DST_end_utc_secs(2008, PACIFIC), PACIFIC)
    print "DST end:", debug_tuple(ds_end_dt.output_tuple())
    ds_end_plus_dt = DateTime(calc_DST_end_utc_secs(2008, PACIFIC)+1, PACIFIC)
    print "DST end+1s:", debug_tuple(ds_end_plus_dt.output_tuple())
    print
    
if __name__ == '__main__': 
    #test()
    DateTimeSyncer(PACIFIC).execute() 
