import datetime

def get_date(yr,mth,day):
        if mth<1:
            yr=yr-((abs(mth)/12)+1)
            mth=mth+((abs(mth)/12)+1)*12
        if mth>12:
            yr=yr+(mth/12)
            mth=mth-(mth/12)*12

        begin_mth= datetime.date(yr, mth, 1)
        return begin_mth + datetime.timedelta(day - 1)

today = datetime.date.today()
print 'now\t\t\t',get_date(today.year, today.month, today.day)
print '36 mths ago\t\t',get_date(today.year, today.month-36, today.day)
print '35 mths ago\t\t',get_date(today.year, today.month-35, today.day)
print '36 mths from now\t',get_date(today.year, today.month+36, today.day)
print '35 mths from now\t',get_date(today.year, today.month+35, today.day)
print '50 days ago\t\t',get_date(today.year, today.month, today.day-50)
print '2 years ago\t\t',get_date(today.year-2, today.month, today.day)
