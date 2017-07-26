#!/usr/bin/env python
# coding: utf-8
import sys
from datetime import datetime
#easier way by Massimiliano
#import sys
#from datetime import date
#month=sys.argv[1]
#my_date=date(date.today().year,month,1)
#while my_date.month==month:
#    filename=my_date.strftime('%Y%m%d')
#    f=open(filename,'w')
#    f.write('#'+filename)
#    f.close()
#    my_date=date.fromordinal(my_date.toordinal()+1)
#
def day_month(m):
    """
    change date at the end of month
    """
    if(s=="02"):
        return 28
    elif(m=="04" or m=="06" or m=="09" or m=="11"):
        return 30
    else:
        return 31
d=datetime.now()
year=str(d.year)

numberday=day_month(sys.argv[1])
for x in range(1,numberday+1):

    if(x<10):
        num = str(x).zfill(2) #before "0"+str(x)

    else:
        num=str(x)

    filename= year + sys.argv[1] + num
    
    f = open(filename,'w')
    f.write("#"+filename)
    f.close()
