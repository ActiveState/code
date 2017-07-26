# 22-01-04
#
# Date Utils
# By Fuzzyman see www.voidspace.org.uk/atlantibots/pythonutils.html

def datetoday(day, month, year):
    d = day
    m = month
    y = year
    if m < 3:
        z = y-1
    else:
        z = y
    dayofweek = ( 23*m//9 + d + 4 + y + z//4 - z//100 + z//400 )
    if m >= 3:
        dayofweek -= 2
    dayofweek = dayofweek%7
    return dayofweek



months = [ 'january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december' ]

days =[ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
       'Sunday' ]

d = int(raw_input("Day of the month 1-31 >>"))
m = int(raw_input("Month 1-12 >>"))
y = int(raw_input("Year e.g. 1974 >>"))


dayofweek = days[datetoday(d, m, y)-1]

print dayofweek
