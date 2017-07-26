'''Support module for CGI applications.

This modules provides access to the HTML_Table and HTML_Month
classes which provide abstractions to the HTML code involved.'''

__version__ = 1.1

################################################################################

import calendar
import z_matrix

class HTML_Table:

    'HTML_Table(rows, columns, indent_level, indent_style) -> new HTML_Table'

    def __init__(self, rows, columns, indent_level, indent_style):
        'x.__init__(...) initializes x'
        self.__matrix = z_matrix.Matrix(rows, columns, '')
        self.__indent_level = indent_level
        self.__indent_style = indent_style
        self.__table_attributes = ''
        self.__row_attributes = ''
        self.__cell_attributes = ''

    def mutate(self, row, column, text):
        'Mutates a cell in the HTML table.'
        assert type(text) is str
        self.__matrix[row][column] = text
        return self

    def access(self, row, column):
        'Accesses a cell in the HTML table.'
        return self.__matrix[row][column]

    def set_table(self, *attributes):
        'Sets the attributes for the table.'
        self.__table_attributes = self.__parse(attributes)
        return self

    def set_row(self, *attributes):
        'Sets the attributes for each row.'
        self.__row_attributes = self.__parse(attributes)
        return self

    def set_cell(self, *attributes):
        'Sets the attributes for each cell.'
        self.__cell_attributes = self.__parse(attributes)
        return self

    def __parse(self, attributes):
        'Parses the attributes into a string.'
        return ''.join([' %s="%s"' % (parameter, value) for parameter, value in attributes])

    def html(self):
        'Returns the HTML code for the current table.'
        html = self.__indent_style * self.__indent_level + '<table' + self.__table_attributes + '>\n'
        for row in self.__matrix:
            html += self.__indent_style * (self.__indent_level + 1) + '<tr' + self.__row_attributes + '>\n'
            for cell in row:
                html += self.__indent_style * (self.__indent_level + 2) + '<td' + self.__cell_attributes + '>\n'
                html += ''.join([self.__indent_style * (self.__indent_level  + 3) + line + '\n' for line in cell.splitlines()])
                html += self.__indent_style * (self.__indent_level + 2) + '</td>\n'
            html += self.__indent_style * (self.__indent_level + 1) + '</tr>\n'
        return html + self.__indent_style * self.__indent_level + '</table>'

class HTML_Month:

    'HTML_Month(month, year, indent_level, indent_style) -> new HTML_Month'

    def __init__(self, month, year, indent_level, indent_style):
        'x.__init__(...) initializes x'
        calendar.setfirstweekday(calendar.SUNDAY)
        matrix = calendar.monthcalendar(year, month)
        self.__table = HTML_Table(len(matrix) + 1, 7, indent_level, indent_style)
        for column, text in enumerate(calendar.day_name[-1:] + calendar.day_name[:-1]):
            self.__table.mutate(0, column, '<b>%s</b>' % text)
        for row, week in enumerate(matrix):
            for column, day in enumerate(week):
                if day:
                    self.__table.mutate(row + 1, column, '<b>%02d</b>\n<hr>\n' % day)
        self.__weekday, self.__alldays = calendar.monthrange(year, month)
        self.__weekday = ((self.__weekday + 1) % 7) + 6

    def mutate(self, day, text):
        'Mutates a day in the HTML month.'
        row, column = self.__row_column(day)
        self.__table.mutate(row, column, '<b>%02d</b>\n<hr>\n%s' % (day, text))
        return self

    def access(self, day):
        'Accesses a day in the HTML month.'
        row, column = self.__row_column(day)
        return self.__table.access(row, column)[15:]

    def __row_column(self, day):
        'Calculates the row and column of day.'
        assert 1 <= day <= self.__alldays
        index = day + self.__weekday
        return index / 7, index % 7

    def set_month(self, *attributes):
        'Set the attributes for the month.'
        self.__table.set_table(*attributes)
        return self

    def set_week(self, *attributes):
        'Set the attributes for each week.'
        self.__table.set_row(*attributes)
        return self

    def set_day(self, *attributes):
        'Set the attributes for each day.'
        self.__table.set_cell(*attributes)
        return self

    def html(self):
        'Returns the HTML code for the current month.'
        return self.__table.html()

################################################################################

if __name__ == '__main__':
    import sys
    print 'Content-Type: text/plain'
    print
    print file(sys.argv[0]).read()
