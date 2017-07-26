"""
The module defines a class Date and several methods to deal with it, including conversions.

The "format" of the Date class is as follows: Each instance has three attributes,
year, month and day, all represented as integers and writable. Although no constraints are
enforced, the intended range of values is:

1 <= day <= 31 (more precisely 1 <= day <= NumberDaysMonth(month, year))
1 <= month <= 12 (1 is January and 12 is December)

It is up to the client of this class to make sure that all assignments are correct.

In making conversions with the time module (wether in seconds or in a 9-tuple) local time
is always used.

History of changes:
version 2.0.1:
 - Added docstring to the module.
 - Changed implementation of next() and previous() to take advantage of NumberDaysMonth().

version 2.0: Complete rewrite of the module.
 - Removed weekday as instance attribute of the class.
 - Added conversion to and from Julian Day number. Added NumberDaysMonth function. Added
   __sub__ and __add__. Made the class hashable.
 - Added some (still insuficient and completely ad-hoc) test code when run as __main__.
"""

__version__ = 2.01
__author__ = "G. Rodrigues"

import time

#Needed for conversion to COM dates.
import pythoncom

def IsLeapYear(year):
    """Returns 1 if year is a leap year, zero otherwise."""
    if year%4 == 0:
        if year%100 == 0:
            if year%400 == 0:
                return 1
            else:
                return 0
        else:
            return 1
    else:
        return 0

def NumberDaysYear(year):
    """Returns the number of days in the year."""
    return 365 + IsLeapYear(year)

def NumberDaysMonth(month = None, year = None):
    """Returns the number of days in the month.

    If any of the arguments is missing (month or year) the current month/year is assumed."""
    if month is None:
        m = time.localtime()[1]
    else:
        m = month

    if year is None:
        y = time.localtime()[0]
    else:
        y = year
    
    if m == 2:
        if IsLeapYear(y):
            return 29
        else:
            return 28
    elif m in (1, 3, 5, 7, 8, 10, 12):
        return 31
    else:
        return 30


class Date(object):
    """The Date class."""
    
    Weekdays = ["Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"]

    Months = ["January",
              "February",
              "March",
              "April",
              "May",
              "June",
              "July",
              "August",
              "September",
              "October",
              "November",
              "December"]

    #The slots in a Date object are constrained to allow more efficient operations.
    __slots__ = ["year", "month", "day"]

    def __init__(self, tm = None):
        """The initializer has an optional argument, time, in the time module format,
        wether as in seconds since the epoch (Unix time) wether as a tuple (time tuple).
        If it is not provided, then it returns the current date."""
        if tm is None:
            t = time.localtime()
        else:
            if isinstance(tm, int):
                t = time.localtime(tm)
            else:
                t = tm
                
        self.year, self.month, self.day = t[:3]

    def weekday(self):
        """Returns the weekday of the date.

        The format is as in the time module: Monday is 0 and sunday is 6."""
        a = (14 - self.month)//12
        y = self.year - a
        m = self.month + 12*a -2
        d = (self.day + y + y//4 - y//100 + y//400 + (31*m//12))%7
        if d:
            ret = d - 1
        else:
            ret = 6
        return ret

    def __str__(self):
        return "%s, %d-%s-%d" % (Date.Weekdays[self.weekday()],
                                 self.day,
                                 Date.Months[self.month - 1],
                                 self.year)

    def copy(self):
        """Deep copy of Date objects."""
        ret = Date()
        ret.year, ret.month, ret.day = self.year, self.month, self.day
        return ret

    #The iterator protocol. The iteration is "destructive", like in files.
    def __iter__(self):
        return self

    def next(self):
        #Last day of the month.
        if self.day == NumberDaysMonth(self.month, self.year):
            self.day = 1
            #December case.
            if self.month == 12:
                self.month = 1
                self.year += 1
            else:
                self.month += 1
        else:
            self.day += 1

    #Extended iterator protocol. One can go backwards.
    def previous(self):
        #First day of the month.
        if self.day == 1:
            #January case.
            if self.month == 1:
                self.month = 12
                self.year -= 1
            else:
                self.month -= 1
            self.day = NumberDaysMonth(self.month, self.year)
        else:
            self.day -= 1

    #Comparison methods.
    def __eq__(self, date):
        return self.year == date.year and self.month == date.month and\
               self.day == date.day

    def __lt__(self, other):
        return (self.year, self.month, self.day) < (other.year, other.month, other.dy)

    def __le__(self, other):
        return (self.year, self.month, self.day) <= (other.year, other.month, other.dy)

    #Dates can be used as keys in dictionaries.
    def __hash__(self):
        return hash((self.year, self.month, self.day))

    #Some useful methods.
    def GetYearDay(self):
        """Returns the year day of a date."""
        ret = self.day
        for month in range(1, self.month):
            ret += NumberDaysMonth(month, self.year)
        return ret

    def DaysToEndYear(self):
        """Returns the number of days until the end of the year."""
        ret = NumberDaysMonth(self.month, self.year) - self.day
        for i in range(self.month + 1, 13):
            ret += NumberDaysMonth(i, self.year)
        return ret

    def GetWeekday(self):
        """Returns the weekday of the date in string format."""
        return Date.Weekdays[self.weekday()]

    def GetMonth(self):
        """Returns the month of the date in string format."""
        return Date.Months[self.month - 1]

    def ToJDNumber(self):
        """Returns the Julian day number of a date."""
        a = (14 - self.month)//12
        y = self.year + 4800 - a
        m = self.month + 12*a - 3
        return self.day + ((153*m + 2)//5) + 365*y + y//4 - y//100 + y//400 - 32045

    #Binary operations.
    def __add__(self, n):
        """Adds a (signed) number of days to the date."""
        if isinstance(n, int):
            #Calculate julian day number and add n.
            temp = self.ToJDNumber() + n
            #Convert back to date format.
            return DateFromJDNumber(temp)
        else:
            raise TypeError, "%s is not an integer." % str(n)

    def __sub__(self, date):
        """Returns the (signed) difference of days between the dates."""
        #If it is an integer defer calculation to the __add__ method.
        if isinstance(date, int):
            return self.__add__(-date)
        elif isinstance(date, Date):
            #Case: The years are equal.
            if self.year == date.year:
                return self.GetYearDay() - date.GetYearDay()
            else:
                if self < date:
                    ret = self.DaysToEndYear() + date.GetYearDay()
                    for year in range(self.year + 1, date.year):
                        ret += NumberDaysYear(year)
                    return -ret
                else:
                    ret = date.DaysToEndYear() + self.GetYearDay()
                    for year in range(date.year + 1, self.year):
                        ret += NumberDaysYear(year)
                    return ret
        else:
            raise TypeError, "%s is neither an integer nor a Date." % str(date)

    #Adding an integer is "commutative".
    def __radd__(self, n):
        return self.__add__(n)

    #Conversion methods.
    def ToTimeTuple(self):
        """Convert a date into a time tuple (time module) corresponding to the
        same day with the midnight hour."""
        ret = [self.year, self.month, self.day]
        ret.extend([0, 0, 0])
        ret.append(self.weekday())
        ret.extend([self.GetYearDay(), 0])
        return tuple(ret)

    def ToUnixTime(self):
        """Convert a date into Unix time (seconds since the epoch) corresponding
        to the same day with the midnight hour."""
        return time.mktime(self.ToTimeTuple())

    def ToCOMTime(self):
        """Convert a date into COM format."""
        return pythoncom.MakeTime(self.ToUnixTime())


#More conversion functions.
def DateFromJDNumber(n):
    """Returns a date corresponding to the given Julian day number."""
    if not isinstance(n, int):
        raise TypeError, "%s is not an integer." % str(n)

    a = n + 32044
    b = (4*a + 3)//146097
    c = a - (146097*b)//4
    d = (4*c + 3)//1461
    e = c - (1461*d)//4
    m = (5*e + 2)//153

    ret = Date()
    ret.day = e + 1 - (153*m + 2)//5
    ret.month = m + 3 - 12*(m//10)
    ret.year = 100*b + d - 4800 + m/10
    return ret

def DateFromCOM(t):
    """Converts a COM time directly into the Date format."""
    return Date(int(t))

def strpdate(s):
    """This function reads a string in the standard date representation
    format and returns a date object."""
    ret = Date()
    temp = s.split(", ")
    temp = temp[1].split("-")
    ret.year, ret.month, ret.day = (int(temp[2]),
                                    Date.Months.index(temp[1]) + 1,
                                    int(temp[0]))
    return ret


#Some test code.
if __name__ == "__main__":
    #Print the days still left in the month.
    temp = Date()
    curr_month = temp.month
    while temp.month == curr_month:
        print temp
        temp.next()

    print "\n"

    #How many days until the end of the year?
    temp = Date()
    temp.day, temp.month = 1, 1
    curr_year = temp.year
    while temp.year == curr_year:
        print "%s is %d days away from the end of the year." % (str(temp),
                                                                temp.DaysToEndYear())
        temp += NumberDaysMonth(temp.month)

    print "\n"

    #Playing with __sub__.
    temp = Date()
    temp_list = []
    curr_year = temp.year
    while temp.year == curr_year:
        temp_list.append(temp)
        temp += NumberDaysMonth(temp.month)
    for elem in temp_list:
        print "%s differs %d days from current date: %s" % (str(elem),
                                                            elem - Date(),
                                                            str(Date()))

    print "\n"

    #Swapping arguments works?
    print 23 + Date()
