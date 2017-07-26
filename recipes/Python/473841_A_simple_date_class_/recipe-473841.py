# to get the local (current / here) time
import time

# allows quick, easy creation of enumeration objects
def enum(*names):
    class enum(object):
        def __setattr__(self, parameter, value):
            raise AttributeError
        def __delattr__(self, parameter):
            raise AttributeError
    obj = enum()
    for value, parameter in enumerate(names):
        obj.__dict__[parameter] = value
    return obj

# an enumeration object with the list attributes
format = enum('mdyy', 'yymd', 'mdy', 'ymd')

class date:

    def __init__(self, form, string=None):
        self.__form = form
        if string:
            self.__set_via_string(string)
        else:
            temp = time.localtime()
            self.__year = temp.tm_year
            self.__month = temp.tm_mon
            self.__day = temp.tm_mday

    def __set_via_string(self, string):
        numbers = string.split('/')
        assert len(numbers) == 3
        for index in range(len(numbers)):
            numbers[index] = int(numbers[index])
        if self.__form == format.mdyy or self.__form == format.mdy:
            self.__year = numbers[2]
            self.__month = numbers[0]
            self.__day = numbers[1]
        elif self.__form == format.yymd or self.__form == format.ymd:
            self.__year = numbers[0]
            self.__month = numbers[1]
            self.__day = number[2]
        else:
            raise 'bad format'

    def __set_via_string_DEPRECATED(self, string):
        length = len(string)
        if self.__form == format.mdyy:
            if length == 10:
                assert string[2] == '/' and string[5] == '/'
                self.__year = int(string[6:])
                self.__month = int(string[:2])
                self.__day = int(string[3:5])
            elif length == 8:
                self.__year = int(string[4:])
                self.__month = int(string[:2])
                self.__day = int(string[2:4])
            else:
                raise 'bad string'
        elif self.__form == format.yymd:
            if length == 10:
                assert string[4] == '/' and string[7] == '/'
                self.__year = int(string[:4])
                self.__month = int(string[5:7])
                self.__day = int(string[8:])
            elif length == 8:
                self.__year = int(string[:4])
                self.__month = int(string[4:6])
                self.__day = int(string[6:])
            else:
                raise 'bad string'
        elif self.__form == format.mdy:
            if length == 8:
                assert string[2] == '/' and string[5] == '/'
                self.__year = int(string[6:])
                self.__month = int(string[:2])
                self.__day = int(string[3:5])
            elif length == 6:
                self.__year = int(string[4:])
                self.__month = int(string[:2])
                self.__day = int(string[2:4])
            else:
                raise 'bad string'
        elif self.__form == format.ymd:
            if length == 8:
                assert string[2] == '/' and string[5] == '/'
                self.__year = int(string[:2])
                self.__month = int(string[3:5])
                self.__day = int(string[6:])
            elif length == 6:
                self.__year = int(string[:2])
                self.__month = int(string[2:4])
                self.__day = int(string[4:])
            else:
                raise 'bad string'
        else:
            raise 'bad format'

    def GetDate(self, form=None):
        if form is None:
            form = self.__form
        if form == format.mdyy:
            return str(self.__month)[-2:].zfill(2) + '/' + str(self.__day)[-2:].zfill(2) + '/' + str(self.__year)[-4:].zfill(4)
        elif form == format.yymd:
            return str(self.__year)[-4:].zfill(4) + '/' + str(self.__month)[-2:].zfill(2) + '/' + str(self.__day)[-2:].zfill(2)
        elif form == format.mdy:
            return str(self.__month)[-2:].zfill(2) + '/' + str(self.__day)[-2:].zfill(2) + '/' + str(self.__year)[-2:].zfill(2)
        elif form == format.ymd:
            return str(self.__year)[-2:].zfill(2) + '/' + str(self.__month)[-2:].zfill(2) + '/' + str(self.__day)[-2:].zfill(2)
        else:
            raise 'bad format'

    def GetDateShort(self):
        return time.strftime('%a %b %d, %Y', time.strptime(self.GetDate(format.mdyy), '%m/%d/%Y'))

    def GetDateLong(self):
        return time.strftime('%A %B %d, %Y', time.strptime(self.GetDate(format.mdyy), '%m/%d/%Y'))

    def GetDay(self):
        return self.__day

    def GetMonth(self):
        return self.__month

    def GetYear(self):
        return self.__year

    def GetDayOfWeek(self):
        wday = time.strptime(self.GetDate(format.mdyy), '%m/%d/%Y').tm_wday
        wday += 1
        if wday == 7:
            return 0
        return wday

    def GetJulianDay(self):
        return time.strptime(self.GetDate(format.mdyy), '%m/%d/%Y').tm_yday

    def IsValid(self):
        try:
            time.strptime(self.GetDate(format.mdyy), '%m/%d/%Y')
            return True
        except:
            return False

    def AddDays(self, days):
        temp = time.localtime(time.mktime(time.strptime(self.GetDate(format.mdyy), '%m/%d/%Y')) + int(days) * (60 * 60 *24))
        self.__year = temp.tm_year
        self.__month = temp.tm_mon
        self.__day = temp.tm_mday
        return self

    def AddYears(self, years):
        self.__year += int(years)
        return self

    def AddMonths(self, months):
        candidate_month = self.__month + int(months)
        if 0 < candidate_month < 13:
            self.__month = candidate_month
        elif candidate_month > 12:
            self.__year += candidate_month / 12
            self.__month = ((candidate_month - 1) % 12) + 1
        elif candidate_month < 1:
            candidate_month = abs(candidate_month) + 1
            self.__year -= candidate_month / 12
            self.__month = 13 - (((candidate_month - 1) % 12) + 1)
        else:
            raise 'there is a problem if this runs'
        return self

    def SubtractDays(self, days):
        return self.AddDays(-days)

    def SubtractYears(self, years):
        return self.AddYears(-years)

    def SubtractMonths(self, months):
        return self.AddMonths(-months)

    def DateDiff(self, form, string):
        temp = date(form, string)
        now = self.__get_relative_day()
        then = temp.__get_relative_day()
        return int(abs(now - then))

    def __get_relative_day(self):
        return time.mktime(time.strptime(self.GetDate(format.mdyy), '%m/%d/%Y')) / (60 * 60 * 24)

    def YearsOld(self):
        temp = date(format.mdyy)
        candidate_year = temp.GetYear() - self.GetYear()
        if temp.GetMonth() - self.GetMonth() > 0:
            return candidate_year
        elif temp.GetMonth() - self.GetMonth() < 0:
            return candidate_year - 1
        else:
            if self.GetDay() - temp.GetDay() <= 0:
                return candidate_year
            else:
                return candidate_year - 1
