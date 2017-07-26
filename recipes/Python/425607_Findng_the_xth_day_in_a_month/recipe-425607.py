import datetime   # a thing of beauty and a joy forever

FIRST = 0
SECOND = 1
THIRD = 2
FOURTH = FORTH = 3  # for people who have finger trouble
FIFTH = 4
LAST = -1
SECONDLAST = -2
THIRDLAST = -3

MONDAY = MON = 0
TUESDAY = TUE = TUES = 1
WEDNESDAY = WED = 2
THURSDAY = THU = THUR = 3
FRIDAY = FRI = 4
SATURDAY = SAT = 5
SUNDAY = SUN = 6

JANUARY = JAN = 1
FEBRUARY = FEB = 2
MARCH = MAR = 3
APRIL = APR = 4
MAY = 5
JUNE = JUN = 6
JULY = JUL = 7
AUGUST = AUG = 8
SEPTEMBER = SEP = 9
OCTOBER = OCT = 10
NOVEMBER = NOV = 11
DECEMBER = DEC = 12

def dow_date_finder(which_weekday_in_month=FIRST,day=MONDAY,month=JANUARY,year=2000):
    dt = datetime.date(year,month,1)
    dow_lst = []
    while dt.weekday() != day:
        dt = dt + datetime.timedelta(days=1)
    while dt.month == month:
        dow_lst.append(dt)
        dt = dt + datetime.timedelta(days=7)
    return dow_lst[which_weekday_in_month]  # may raise an exception if slicing is wrong


if __name__ == "__main__":
    print "2nd tuesday of may 2005"
    print dow_date_finder(SECOND,TUESDAY,MAY,2005)
    print "last wednesday of april 2005"
    print dow_date_finder(LAST,WEDNESDAY,APRIL,2005)
    print "secondlast friday of october 2005 - short form"
    print dow_date_finder(SECONDLAST,FRI,OCT,2005)
