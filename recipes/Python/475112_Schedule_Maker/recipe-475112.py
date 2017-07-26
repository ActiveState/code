################################################################################
# index.py
################################################################################

import html_help
import os
import sys
import time
import Zcgi

KEYS = 'description', 'start', 'end', 'sunday', 'monday', \
       'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'

class soft_dict:
    
    def __init__(self, dictionary, format):
        self.__dictionary = dictionary
        self.__format = format
        
    def __getitem__(self, key):
        try:
            if self.__dictionary[key]:
                return self.__format % self.__dictionary[key]
        except:
            pass
        return ''

class WeekError:

    def __init__(self, string):
        self.__string = string

    def __str__(self):
        return self.__string

def main():
    if Zcgi.dictionary is None:
        show_form()
    elif has_keys(Zcgi.dictionary, KEYS):
        show_table()
    else:
        show_form()

def show_form(error=''):
    if error:
        error = '\t\t<b>' + error + '</b>\n'
    values = soft_dict(Zcgi.dictionary, ' value="%s"')
    Zcgi.print_html('''<html>
\t<head>
\t\t<title>
\t\t\tSchedule Maker
\t\t</title>
\t</head>
\t<body>
%s\t\t<form action="%s">
\t\t\tDescription:<br>
\t\t\t<input type="text"%s name="description" size="25"><br>
\t\t\tStart Date:<br>
\t\t\t<input type="text"%s name="start" size="25"><br>
\t\t\tEnd Date:<br>
\t\t\t<input type="text"%s name="end" size="25"><br>
\t\t\tSunday:<br>
\t\t\t<input type="text"%s name="sunday" size="25"><br>
\t\t\tMonday:<br>
\t\t\t<input type="text"%s name="monday" size="25"><br>
\t\t\tTuesday:<br>
\t\t\t<input type="text"%s name="tuesday" size="25"><br>
\t\t\tWednesday:<br>
\t\t\t<input type="text"%s name="wednesday" size="25"><br>
\t\t\tThursday:<br>
\t\t\t<input type="text"%s name="thursday" size="25"><br>
\t\t\tFriday:<br>
\t\t\t<input type="text"%s name="friday" size="25"><br>
\t\t\tSaturday:<br>
\t\t\t<input type="text"%s name="saturday" size="25"><br>
\t\t\t<input type="submit" value="Create Schedule">
\t\t</form>
\t</body>
</html>''' % tuple([error, os.path.basename(sys.argv[0])] \
                   + unpack(values, KEYS)))

def has_keys(dictionary, keys):
    for key in keys:
        if not dictionary.has_key(key):
            return False
    return True

def show_table():
    values = Zcgi.dictionary
    if not values['description']:
        show_form('You must enter a description.')
    try:
        start = time.strptime(values['start'], '%m/%d/%y')
        end = time.strptime(values['end'], '%m/%d/%y')
    except:
        show_form('Dates must be in the MM/DD/YY format.')
    try:
        assert time.mktime(end) > time.mktime(start)
    except:
        show_form('The end date must come after the start date.')
    try:
        check_week(values, KEYS[3:])
    except WeekError, problem:
        show_form(str(problem))
    html = create_html(values['description'], start, end, unpack(values, KEYS[3:]))
    Zcgi.print_html(html)

def unpack(values, keys):
    unpacked = []
    for key in keys:
        unpacked.append(values[key])
    return unpacked

def check_week(dictionary, keys):
    for key in keys:
        try:
            if not dictionary[key]:
                continue
            hm = dictionary[key].split('-')
            assert len(hm) == 2
            first = time.strptime(hm[0].strip(), '%H:%M')
            second = time.strptime(hm[1].strip(), '%H:%M')
            dictionary[key] = hm[0].strip() + ' - ' + hm[1].strip()
        except:
            raise WeekError(key.capitalize() + ' should be in the HH:MM - HH:MM format.')
        try:
            assert second.tm_hour * 60 + second.tm_min > first.tm_hour * 60 + first.tm_min
        except:
            raise WeekError('Start time must come before end time on ' + key.capitalize() + '.')

def create_html(description, start, end, week):
    html = '''<html>
\t<head>
\t\t<title>
\t\t\tThe Schedule
\t\t</title>
\t</head>
\t<body>
\t\t<center>
'''
    start_month = start.tm_year * 12 + (start.tm_mon - 1)
    end_month = end.tm_year * 12 + (end.tm_mon - 1)
    for month in range(start_month, end_month + 1):
        html += html_help.html_table(1, 1, 3, '\t').mutate(0, 0, create_month_html(description, start, end, week, month)).html() + '\n'
        if month != end_month:
            html += '\t\t\t<hr>\n'
    return html + '\t\t</center>\n\t</body>\n</html>'

def create_month_html(description, start, end, week, month):
    start = time.mktime(start) - 43200
    end = time.mktime(end) + 43200
    now = time.strptime(str((month / 12) % 100).zfill(2) + ' ' +  str(month % 12 + 1) + ' 01', '%y %m %d')
    html = '<b>' + time.strftime('%B %Y', now) + '</b>\n'
    html_month = html_help.html_month((month / 12) % 100, month % 12 + 1, 0, '\t')
    html_month.table_option('border="1" width="800"').row_option('valign="top"').column_option('width="14%"')
    now_month = now.tm_mon
    while now.tm_mon == now_month:
        mktime = time.mktime(now)
        if start <= mktime <= end:
            week_day = (now.tm_wday + 1) % 7
            if week[week_day]:
                html_month.mutate(now.tm_mday, '<b>' + description + '</b><br>\n' + week[week_day])
        now = time.localtime(mktime + 86400)
    return html + html_month.html()

if __name__ == '__main__':
    Zcgi.execute(main, 'cgi')

################################################################################
# html_help.py
################################################################################

import time
import Zam

class html_table:

    def __init__(self, rows, columns, indent, style):
        self.__matrix = Zam.matrix(rows, columns, '')
        self.__indent = indent
        self.__style = style
        self.__table_option = ''
        self.__row_option = ''
        self.__column_option = ''

    def mutate(self, row, column, text):
        assert type(text) is str
        self.__matrix[row][column] = text
        return self

    def access(self, row, column):
        return self.__matrix[row][column]

    def table_option(self, string):
        assert type(string) is str
        self.__table_option = string
        return self

    def row_option(self, string):
        assert type(string) is str
        self.__row_option = string
        return self

    def column_option(self, string):
        assert type(string) is str
        self.__column_option = string
        return self

    def html(self):
        html = self.__style * self.__indent + '<table'
        if self.__table_option:
            html += ' ' + self.__table_option
        html += '>\n'
        for row in self.__matrix:
            html += self.__style * (self.__indent + 1) + '<tr'
            if self.__row_option:
                html += ' ' + self.__row_option
            html += '>\n'
            for item in row:
                html += self.__style * (self.__indent + 2) + '<td'
                if self.__column_option:
                    html += ' ' + self.__column_option
                html += '>\n'
                html += ''.join([self.__style * (self.__indent  + 3) + line + '\n' for line in item.splitlines()])
                html += self.__style * (self.__indent + 2) + '</td>\n'
            html += self.__style * (self.__indent + 1) + '</tr>\n'
        return html + self.__style * self.__indent + '</table>'

class html_month:

    def __init__(self, year, month, indent, style):
        matrix = self.__make_matrix(year, month)
        self.__table = html_table(len(matrix) + 1, 7, indent, style)
        for index, item in enumerate(('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')):
            self.__table.mutate(0, index, '<b>' + item + '</b>')
        for row in range(len(matrix)):
            for column in range(7):
                if matrix[row][column]:
                    self.__table.mutate(row + 1, column, '<b>' + str(matrix[row][column]).zfill(2) + '</b>\n<hr>\n')

    def __make_matrix(self, year, month):
        rows = [Zam.array(7, 0)]
        row = 0
        now = time.localtime(time.mktime(time.strptime(str(year).zfill(2) + ' ' + str(month).zfill(2) + ' 01', '%y %m %d')) + 14400)
        self.__first_day = (now.tm_wday + 1) % 7
        once = False
        while now.tm_mon == month:
            if once:
                if now.tm_wday == 6:
                    rows.append(Zam.array(7, 0))
                    row += 1
            else:
                once = True
            rows[row][(now.tm_wday + 1) % 7] = now.tm_mday
            self.__days_in_month = now.tm_mday
            now = time.localtime(time.mktime(now) + 86400)
        return rows

    def mutate(self, day, text):
        row, column = self.__get_pos(day)
        self.__table.mutate(row, column, self.__table.access(row, column)[:15] + text)
        return self

    def access(self, day):
        row, column = self.__get_pos(day)
        return self.__table.access(row, column)[15:]

    def __get_pos(self, day):
        assert 1 <= day <= self.__days_in_month
        pos = self.__first_day - 1 + day
        return pos / 7 + 1, pos % 7

    def table_option(self, string):
        self.__table.table_option(string)
        return self

    def row_option(self, string):
        self.__table.row_option(string)
        return self

    def column_option(self, string):
        self.__table.column_option(string)
        return self

    def html(self):
        return self.__table.html()

################################################################################
# Zam.py
################################################################################

# Name & Description
# ==================

'''Support module for array and matrix use.

This module provides two classes that emulate one and two
dimentional lists with fixed sizes but mutable internals.'''

# Data & Imports
# ==============

__all__ = ['array', 'matrix']
__version__ = '1.1'

import sys

# Public Names
# ============

class array(object):

    '''array(length) -> new array
    array(length, value) -> initialized from value'''

    def __init__(self, length, value=None):
        '''x.__init__(...) initializes x'''
        self.__data = range(length)
        for index in range(length):
            self.__data[index] = value

    def __repr__(self):
        '''x.__repr__() <==> repr(x)'''
        return repr(self.__data)

    def __len__(self):
        '''x.__len__() <==> len(x)'''
        return len(self.__data)

    def __getitem__(self, key):
        '''x.__getitem__(y) <==> x[y]'''
        return self.__data[key]

    def __setitem__(self, key, value):
        '''x.__setitem__(i, y) <==> x[i]=y'''
        self.__data[key] = value

    def __delitem__(self, key):
        '''x.__delitem__(y) <==> del x[y]'''
        self.__data[key] = None

    def __iter__(self):
        '''x.__iter__() <==> iter(x)'''
        return iter(self.__data)

    def __contains__(self, value):
        '''x.__contains__(y) <==> y in x'''
        return value in self.__data

class matrix(object):

    '''matrix(rows, columns) -> new matrix
    matrix(rows, columns, value) -> initialized from value'''

    def __init__(self, rows, columns, value=None):
        '''x.__init__(...) initializes x'''
        self.__data = array(rows)
        for index in range(rows):
            self.__data[index] = array(columns, value)

    def __repr__(self):
        '''x.__repr__() <==> repr(x)'''
        return repr(self.__data)

    def __len__(self):
        '''x.__len__() <==> len(x)'''
        return len(self.__data)

    def __getitem__(self, key):
        '''x.__getitem__(y) <==> x[y]'''
        return self.__data[key]

    def __setitem__(self, key, value):
        '''x.__setitem__(i, y) <==> x[i]=y'''
        self.__data[key] = array(len(self.__data[key]), value)

    def __delitem__(self, key):
        '''x.__delitem__(y) <==> del x[y]'''
        self.__data[key] = array(len(self.__data[key]))

    def __iter__(self):
        '''x.__iter__() <==> iter(x)'''
        return iter(self.__data)

    def __contains__(self, value):
        '''x.__contains__(y) <==> y in x'''
        for item in self.__data:
            if value in item:
                return True
        return False

# Private Names
# =============

def main():
    print 'Content-Type: text/plain'
    print
    print file(sys.argv[0]).read()

# Execute Main
# ============

if __name__ == '__main__':
    main()

################################################################################
# Zcgi.py
################################################################################

# Name & Description
# ==================

'''Support module for use by CGI scripts.

This module provides several functions and variables
that help with printing text and accessing form data.'''

# Data & Imports
# ==============

__all__ = ['execute', 'print_html', 'print_plain', 'print_self',
           'dictionary', 'string']
__version__ = '1.2'

import os
import sys
import types

# Public Names
# ============

def execute(main, exception):
    '''execute(function main, str exception)

    Execute main unless exception.'''
    assert_type((types.FunctionType, main), (str, exception))
    if exception == string:
        print_self()
    else:
        main()

def print_html(text):
    '''print_html(str text)

    Print text as HTML.'''
    assert_type((str, text))
    print 'Content-Type: text/html'
    print
    print text
    sys.exit(0)

def print_plain(text):
    '''print_plain(str text)

    Print text as plain.'''
    assert_type((str, text))
    print 'Content-Type: text/plain'
    print
    print text
    sys.exit(0)

def print_self():
    '''print_self()

    Print __main__ as plain.'''
    print 'Content-Type: text/plain'
    print
    print file(sys.argv[0]).read()
    sys.exit(0)

# Private Names
# =============

def export():
    global dictionary, string
    dictionary = string = None
    try:
        string = os.environ['QUERY_STRING']
        temp = string.replace('+', ' ').split('&')
        for index in range(len(temp)):
            temp[index] = temp[index].split('=')
        dictionary = dict()
        for parameter, value in temp:
            dictionary[decode(parameter)] = decode(value)
    except:
        pass

def decode(string):
    assert_type((str, string))
    index = string.find('%')
    while index != -1:
        string = string[:index] + chr(int(string[index+1:index+3], 16)) + string[index+3:]
        index = string.find('%', index + 1)
    return string

def assert_type(*tuples):
    for types, objects in tuples:
        if type(objects) is not types:
            raise TypeError

# Execute Conditional
# ===================

if __name__ == '__main__':
    print_self()
else:
    export()
