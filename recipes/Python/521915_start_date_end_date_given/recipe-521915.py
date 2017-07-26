#!/usr/bin/env /usr/bin/python2.4

import sys
import datetime
from time import strptime, strftime

def _getWeekDetails(_weekNo, _Year, _weekStart):
    rslt = []
    janOne = strptime('%s-01-01' % _Year, '%Y-%m-%d')
    dayOfFirstWeek = ((7-int((strftime("%u",janOne)))+ int(_weekStart)) % 7)
    if dayOfFirstWeek == 0:
        dayOfFirstWeek = 7
    dateOfFirstWeek = strptime('%s-01-%s' % (_Year, dayOfFirstWeek), '%Y-%m-%d')
    dayOne = datetime.datetime( dateOfFirstWeek.tm_year, dateOfFirstWeek.tm_mon, dateOfFirstWeek.tm_mday )
    daysToGo = 7*(int(_weekNo)-1)
    lastDay = daysToGo+6
    dayX = dayOne + datetime.timedelta(days = daysToGo)
    dayY = dayOne + datetime.timedelta(days = lastDay)
    resultDateX = strptime('%s-%s-%s' % (dayX.year, dayX.month, dayX.day), '%Y-%m-%d')
    resultDateY = strptime('%s-%s-%s' % (dayY.year, dayY.month, dayY.day), '%Y-%m-%d')
    rslt.append(resultDateX)
    rslt.append(resultDateY)
    return rslt

if __name__ == '__main__':
    passedArgs = sys.argv
    if not (passedArgs[1] == None or passedArgs[2] == None):

        #initiate start of week to Monday (sunday =1, monday =2, so on)
        startOfWeek = 2
        try :
            startOfWeek = passedArgs[3]
        except:
            startOfWeek = 2

        WeekData = _getWeekDetails(passedArgs[1], passedArgs[2], startOfWeek)
        print "Monday of Week %s: %s \n" % (passedArgs[1], strftime("%Y-%m-%d", WeekData[0]))
        print "Sunday of Week %s: %s \n" % (passedArgs[1], strftime("%Y-%m-%d", WeekData[1]))
