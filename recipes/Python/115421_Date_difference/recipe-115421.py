# cal.py
#
# This code has been released to the Public Domain.
#
# finds the number of days between two particular dates
#
from string import *

FALSE,TRUE = range(2)

# Standard number of days for each month.
months = (31,28,31,30,31,30,31,31,30,31,30,31)

JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC = range(len(months))

def leapyear(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return TRUE
            else:
                return FALSE
        else:
            return TRUE
    else:
        return FALSE

def main():
    days=sum=0
    month = atoi(raw_input("Enter Month 1: "))
    day = atoi(raw_input("Enter Day 1: "))
    year = atoi(raw_input("Enter Year 1: "))
    emonth = atoi(raw_input("Enter Month 2: "))
    eday = atoi(raw_input("Enter Day 2: "))
    eyear = atoi(raw_input("Enter Year 2: "))

    month = month - 1
    emonth = emonth - 1

    if month == JAN:
        if leapyear(year):
            days = days + (366 - day)
        else:
            days = days + (365 - day)
    else:
        i = 0
        while i < month:
            sum = sum + months[i]
            i = i + 1
        sum = sum + day
        if leapyear(year):
            days = days + (366 - sum)
        else:
            days = days + (365 - sum)

    print "Days first year ==",days
    print "Number of years between ==",eyear - year

    i = year + 1
    while i < eyear:
        if leapyear(i):
            days = days + 366
        else:
            days = days + 365
        print "in year",i
        i = i + 1

    print "Total days not including last year ==",days

    if emonth == JAN:
        days = days + eday
    else:
        i = 0
        while i < emonth:
            days = days + months[i]
            i = i + 1
        days = days + day
        if leapyear(year) and emonth > FEB:
            days = days + 1

    print "Final total days ==",days

if __name__ == '__main__':
    main()
