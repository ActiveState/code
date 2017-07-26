================================================================================
html_help.py
================================================================================
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
        self.matrix = matrix = self.__make_matrix(year, month)
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
================================================================================
Zam.py
================================================================================
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
