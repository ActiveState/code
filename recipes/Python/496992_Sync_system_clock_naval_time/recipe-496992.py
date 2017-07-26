#!/usr/bin/python
#
# File:   nts_sync.py
# Author: Jason Letbetter
# Date:   8/24/2006
#
# This software gets the date from a naval time server and updates the system
# clock for posix OS supporting the "date" command.  It also requires an
# internet connection.
#
# WARNING: It will not work if your system clock is already off by more than
# 1 month.
#
# TIP: Use kcron to schedule this script on a periodic basis.
#
# Example:
# jason@gummybear:~$ nts_sync.py
# Before update: Sat Aug 26 08:48:41 CDT 2006
# Updating to: Sat Aug 26 13:48:41 UTC 2006
# After update: Sat Aug 26 08:48:41 CDT 2006
#



import sys, os, re, urllib2



def main(argv):
    # Print current date
    sys.stdout.write('Before update: ')
    sys.stdout.flush()
    os.system('date')
    # Update date from naval server
    date = GetDate()
    sys.stdout.write('Updating to: ')
    sys.stdout.flush()
    os.system('sudo date -u %s' % date)
    # Print updated date
    sys.stdout.write('After update: ')
    sys.stdout.flush()
    os.system('date')

    

def GetLocalYear(svrMo):
    # Use the local machine's year b/c naval server doesn't have it
    i,o = os.popen4('date')	
    date = o.read()
    yr = int(date[-5:-1],10)
    # TRICKY: We have to be careful around January 1st
    svrMo = int(svrMo)
    locMo = int(monthMap[date[4:7]])
    # Assume local machine is slow and its near Jan 1st
    if svrMo == 1 and locMo == 12:
        yr+=1
    # Assume local machine is fast and its near Jan 1st
    elif svrMo == 12 and locMo == 1:
        yr-=1
    return str(yr)

        
    
def GetDate():
    # Read date from naval time server (tax payers only ;^)
    url = urllib2.urlopen('http://tycho.usno.navy.mil/cgi-bin/timer.pl')
    text = url.read()    
    # Parse text to get UTC date strings
    regx = r'([a-z,A-Z,]+)\.\s+(\d+)\,\s+(\d+):(\d+):(\d+)\s+UTC'
    mo, da, hr, mi, se = re.search(regx, text).groups()
    # Compute month number from abbreviation
    mo = monthMap[mo]
    # Get the year from our local clock
    yr = GetLocalYear(mo)
    # Return the proper date format
    return mo+da+hr+mi+yr+'.'+se



monthMap = {
    'Jan':  '01', 'Feb':  '02', 'Mar':  '03', 'Apr':  '04',
    'May':  '05', 'Jun':  '06', 'Jul':  '07', 'Aug':  '08',
    'Sep':  '09', 'Oct':  '10', 'Nov':  '11', 'Dec':  '12'
    }
        
        
        
if __name__ == '__main__':
    main(sys.argv[1:])
