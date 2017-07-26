#===============================================================================
# Calendar Maker.pyw
#===============================================================================

import CGIHTTPServer
import socket
import sys
import thread
import webbrowser

def main():
    try:
        socket.socket().connect(('127.0.0.1', 80))
        webbrowser.open('http://127.0.0.1/htbin/index.py')
    except:
        if len(sys.argv) > 1:
            sys.argv[1] = '80'
        else:
            sys.argv.append('80')
        thread.start_new_thread(CGIHTTPServer.test, ())
        webbrowser.open('http://127.0.0.1/htbin/index.py')
        s = socket.socket()
        s.bind(('', 8080))
        s.listen(1)
        s.accept()

if __name__ == '__main__':
    main()

#===============================================================================
# htbin\__init__.py
#===============================================================================



#===============================================================================
# htbin\index.py
#===============================================================================

import cgitb; cgitb.enable()

from xml_stream import *
import xml.sax.xmlreader
import xml.sax.saxutils
import StringIO
import getpass
import z_html
import z_cgi
import sys
import os

################################################################################

FIRST_FORM = '''\
<html>
    <head>
        <title>
            Calendar Maker
        </title>
    </head>
        <center>%s
            <table>
                <tr>
                    <td>
                        <form method="post" action="%s">
                            <table>
                                <tr>
                                    <td>
                                        Month:
                                    </td>
                                    <td>
                                        <input type="text" name="month">
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        Year:
                                    </td>
                                    <td>
                                        <input type="text" name="year">
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <input type="submit" value="New" name="select">
                                    </td>
                                    <td>
                                    </td>
                                </tr>
                            </table>
                            <hr>
                            <table>
                                <tr>
                                    <td>
                                        File:
                                    </td>
                                    <td>
                                        <input type="file" name="filename">
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <input type="submit" value="Load" name="select">
                                    </td>
                                    <td>
                                    </td>
                                </tr>
                            </table>
                        </form>
                        <hr>
                        <a href="http://127.0.0.1:8080/"><b><font color="red">Shutdown</font></b></a>
                    </td>
                </tr>
            </table>
        </center>
    </body>
</html>'''

################################################################################

SECOND_FORM = '''\
<html>
    <head>
        <title>%s</title>
    </head>
    <body>
        <form method="post" action="%s">
            <input type="hidden" name="month" value="%s">
            <input type="hidden" name="year" value="%s">
%s
%s
        </form>
    </body>
</html>'''

################################################################################

THIRD_FORM = '''\
<html>
    <head>
        <title>
            %s
        </title>
    </head>
    <body>
%s
    </body>
</html>'''

################################################################################

def main():
    if z_cgi.dictionary.has_key('select'):
        try:
            show_month()
        except Exception, error:
            if isinstance(error, SystemExit): raise
            show_first('\n            <h1><font color="red"><u>ERROR</u></font></h1>')
    elif z_cgi.dictionary.has_key('month'):
        show_print()
    else:
        show_first()

def show_first(error=''):
    z_cgi.print_html(FIRST_FORM % (error, os.path.basename(sys.argv[0])))

def show_month():
    # region V2
    try:
        error = True
        try:
            month = int(z_cgi.dictionary['month'])
            error = False
        except:
            m = z_cgi.dictionary['month'].lower()
            for month, name in enumerate(z_html.calendar.month_name):
                if name.lower().startswith(m):
                    error = False
                    break
        assert not error
        year = int(z_cgi.dictionary['year'])
        create_month_form(year, month)
    except Exception, error:
        if isinstance(error, SystemExit): raise
        assert z_cgi.dictionary['select'] == 'Load'
        create_month_form()
    # endregion

# region V2
class MonthParser:

    def __init__(self):
        self.days = {}
        self.__month = False
        self.__year = False
        self.__textarea = None

    def __getattr__(self, name):
        return Event

    def startElement(self, name, attrs):
        if name == 'Month':
            self.__month = True
        elif name == 'Year':
            self.__year = True
        elif name == 'TextArea':
            self.__textarea = attrs.getValue('day')

    def characters(self, content):
        if self.__month:
            self.__month = False
            self.month = int(content)
        elif self.__year:
            self.__year = False
            self.year = int(content)
        elif self.__textarea is not None:
            self.days[int(self.__textarea)] = str(content)
            self.__textarea = None
# endregion

def create_month_form(year=None, month=None):
    # region V2
    if z_cgi.dictionary['select'] == 'Load':
        load = True
        filename = os.path.join('C:\\Documents and Settings\\%s\\Desktop' % getpass.getuser(), z_cgi.dictionary['filename'])
        s = Stream(filename)
        s.minimize()
        parser = MonthParser()
        s.parse(parser)
        year = parser.year
        month = parser.month
    else:
        load = False
    # endregion
    m_a_y = '%s %s' % (z_html.calendar.month_name[month], year)
    h_month = z_html.HTML_Month(month, year, 0, '    ')
    h_month.set_month(height='100%', width='100%', border=1)
    h_month.set_week(valign='top')
    h_month.set_day(width='14%')
    for x in range(z_html.calendar.monthrange(year, month)[1]):
        # region V2
        if load:
            try:
                h_month.mutate(x + 1, '<textarea name="ta%s">%s</textarea>' % (x, parser.days[x]))
                h_month.special(x + 1, True)
            except:
                h_month.mutate(x + 1, '<textarea name="ta%s"></textarea>' % x)
        else:
            h_month.mutate(x + 1, '<textarea name="ta%s"></textarea>' % x)
        # endregion
    h_table = z_html.HTML_Table(1, 1, 3, '    ')
    if load:
        h_table.special(0, 0, True)
    h_table.mutate(0, 0, '<b>%s</b>\n%s' % (m_a_y, h_month.html()))
    h_table.set_table(width='100%', height='100%')
    # region V2
    controls = z_html.HTML_Table(2, 3, 3, '    ')
    controls.mutate(0, 0, 'HTML:')
    controls.mutate(0, 1, '<input type="text" name="filename" value="%s.htm">' % m_a_y)
    controls.mutate(0, 2, '<input type="submit" value="Create" name="action">')
    controls.mutate(1, 0, 'XML:')
    controls.mutate(1, 1, '<input type="text" name="xml", value="%s.xml">' % m_a_y)
    controls.mutate(1, 2, '<input type="submit" value="Save" name="action">')
    # endregion
    data = SECOND_FORM % (m_a_y,
                          os.path.basename(sys.argv[0]),
                          month,
                          year,
                          h_table.html(),
                          controls.html())
    z_cgi.print_html(data)

def show_print():
    month = int(z_cgi.dictionary['month'])
    year = int(z_cgi.dictionary['year'])
    create_print(month, year)

def create_print(month, year):
    # region V2
    if z_cgi.dictionary['action'] == 'Save':
        save = True
        stream = [startDocument(),
                  startElement('Calendar', xml.sax.xmlreader.AttributesImpl({})),
                  startElement('Date', xml.sax.xmlreader.AttributesImpl({})),
                  startElement('Month', xml.sax.xmlreader.AttributesImpl({})),
                  characters(str(month)),
                  endElement('Month'),
                  startElement('Year', xml.sax.xmlreader.AttributesImpl({})),
                  characters(str(year)),
                  endElement('Year'),
                  endElement('Date'),
                  startElement('Days', xml.sax.xmlreader.AttributesImpl({}))]
    else:
        save = False
    # endregion
    m_a_y = '%s %s' % (z_html.calendar.month_name[month], year)
    h_month = z_html.HTML_Month(month, year, 0, '    ')
    h_month.set_month(height='100%', width='100%', border=1)
    h_month.set_week(valign='top')
    h_month.set_day(width='14%')
    for x in range(z_html.calendar.monthrange(year, month)[1]):
        h_month.mutate(x + 1, '<br>'.join(z_cgi.dictionary['ta%s' % x].splitlines()))
        # region V2
        if save and z_cgi.dictionary['ta%s' % x]:
            stream.extend([startElement('TextArea', xml.sax.xmlreader.AttributesImpl({'day': str(x)})),
                           characters(z_cgi.dictionary['ta%s' % x]),
                           endElement('TextArea')])
        # endregion
    h_table = z_html.HTML_Table(1, 1, 2, '    ')
    h_table.mutate(0, 0, '<b>%s</b>\n%s' % (m_a_y, h_month.html()))
    h_table.set_table(width='100%', height='100%')
    # region V2
    name = 'C:\\Documents and Settings\\%s\\Desktop' % getpass.getuser()
    if save:
        stream.extend([endElement('Days'),
                       endElement('Calendar'),
                       endDocument()])
        data = StringIO.StringIO()
        xml_gen = xml.sax.saxutils.XMLGenerator(data)
        for event in stream:
            event(xml_gen)
        stream = Stream(data.getvalue())
        stream.maximize('    ')
        stream.parse(xml.sax.saxutils.XMLGenerator(file(os.path.join(name, z_cgi.dictionary['xml']), 'w')))
    # endregion
    data = THIRD_FORM % (m_a_y, h_table.html())
    # region V2
    if z_cgi.dictionary['action'] == 'Create':
        file(os.path.join(name, z_cgi.dictionary['filename']), 'w').write(data)
    # endregion
    z_cgi.print_html(data)

if __name__ == '__main__':
    z_cgi.execute(main, 'code')

#===============================================================================
# htbin\xml_stream.py
#===============================================================================

'''Module for XML event streams.

This module provides several classes for creating,
saving, and delaying the processing of XML events.'''

__version__ = '1.0'

import os as _os
import sys as _sys
import xml.sax as _xml_sax

################################################################################

class Event:

    'Event(*args) -> Event'

    def __init__(self, *args):
        'Initialize the Event object.'
        self.__args = args

    def __repr__(self):
        'Return the object\'s representation.'
        return '%s(%s)' % (self.__class__.__name__, ', '.join(map(repr, self.__args)))

    def __call__(self, handler=None):
        'Either return arguments or process handler.'
        if handler is None:
            return self.__args
        else:
            getattr(handler, self.__class__.__name__)(*self.__args)

class setDocumentLocator(Event): pass
class startDocument(Event): pass
class endDocument(Event): pass
class startPrefixMapping(Event): pass
class endPrefixMapping(Event): pass
class startElement(Event): pass
class endElement(Event): pass
class startElementNS(Event): pass
class endElementNS(Event): pass
class characters(Event): pass
class ignorableWhitespace(Event): pass
class processingInstruction(Event): pass
class skippedEntity(Event): pass

################################################################################

class Stream:

    'Stream(filename_or_stream_or_string) -> Stream'

    def __init__(self, filename_or_stream_or_string):
        'Initialize the Stream object.'
        self.__stream = []
        if isinstance(filename_or_stream_or_string, str):
            if _os.path.exists(filename_or_stream_or_string):
                _xml_sax.parse(filename_or_stream_or_string, self)
            else:
                _xml_sax.parseString(filename_or_stream_or_string, self)
        else:
            _xml_sax.parse(filename_or_stream_or_string, self)
        self.__maximized = self.__minimized = False

    def __getattr__(self, name):
        'Dynamically create and bind Methods.'
        self.__dict__[name] = Method(self.__stream, name)
        return self.__dict__[name]

    def __iter__(self):
        'Return an iterator.'
        return iter(self.__stream)

    def parse(self, handler):
        'Simulate events on a handler.'
        for event in self:
            event(handler)

    def maximize(self, style):
        'Prepare the stream for printing.'
        if not self.__maximized:
            self.minimize()
            self.__minimized = False
            self.__maximized = True
            if isinstance(self.__stream[0], setDocumentLocator):
                index =  2
            else:
                index =  1
            level = 0
            cancel = False
            while True:
                event = self.__stream[index]
                if isinstance(event, (startPrefixMapping, startElement, startElementNS)):
                    self.__stream.insert(index, characters(style * level))
                    index += 2
                    if not isinstance(self.__stream[index], (endDocument, endPrefixMapping, endElement, endElementNS)):
                        self.__stream.insert(index, characters('\n'))
                        index += 1
                        level += 1
                elif isinstance(event, (endPrefixMapping, endElement, endElementNS)):
                    if not isinstance(self.__stream[index - 1], (startDocument, startPrefixMapping, startElement, startElementNS)):
                        level -= 1
                        if cancel:
                            cancel = False
                            index += 1
                        else:
                            self.__stream.insert(index, characters(style * level))
                            index += 2
                    else:
                        index += 1
                    self.__stream.insert(index, characters('\n'))
                    index += 1
                elif isinstance(event, endDocument):
                    break
                elif isinstance(event, characters):
                    del self.__stream[index - 1]
                    cancel = True

    def minimize(self):
        'Prepare the stream for data extraction.'
        if not self.__minimized:
            self.__maximized = False
            self.__minimized = True
            if isinstance(self.__stream[0], setDocumentLocator):
                index = 2
            else:
                index = 1
            inside = True
            while index < len(self.__stream):
                event = self.__stream[index]
                if isinstance(event, (startPrefixMapping, startElement, startElementNS)):
                    inside = True
                    index = self.__prune(index)
                elif isinstance(event, (endDocument, endPrefixMapping, endElement, endElementNS)):
                    if inside:
                        inside = False
                        index = self.__join(index)
                    else:
                        index = self.__prune(index)
                index += 1

    def __prune(self, index):
        'Private class method.'
        temp = index - 1
        event = self.__stream[temp]
        while not isinstance(event, (startDocument, startPrefixMapping, endPrefixMapping, startElement, endElement, startElementNS, endElementNS)):
            if isinstance(event, characters):
                del self.__stream[temp]
                index -= 1
            temp -= 1
            event = self.__stream[temp]
        return index

    def __join(self, index):
        'Private class method.'
        temp = index - 1
        event_1 = self.__stream[temp]
        while not isinstance(event_1, (startDocument, startPrefixMapping, startElement, startElementNS)):
            if isinstance(event_1, characters):
                event_2 = self.__stream[temp - 1]
                if isinstance(event_2, characters):
                    self.__stream[temp] = characters(event_2()[0] + event_1()[0])
                    del self.__stream[temp - 1]
                    index -= 1
            temp -= 1
            event_1 = self.__stream[temp]
        return index

################################################################################

class Method:

    'Method(stream, name) -> Method'

    def __init__(self, stream, name):
        'Initialize the Method object.'
        self.__stream = stream
        self.__name = name

    def __call__(self, *args):
        'Dynamically create and add events to the stream.'
        self.__stream.append(globals()[self.__name](*args))

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())

#===============================================================================
# htbin\z_cgi.py
#===============================================================================

'''Support module for use by CGI scripts.

This module provides several functions and variables
that help with printing text and accessing form data.'''

__version__ = 1.3

################################################################################

class File:
    def __init__(*args, **kwargs):
        pass
    def flush(*args, **kwargs):
        pass
    def isatty(*args, **kwargs):
        pass
    def write(*args, **kwargs):
        pass
    def writelines(*args, **kwargs):
        pass

################################################################################

import sys

out = sys.stdout
sys.stdout = File()

def execute(main, exception):
    'Execute main unless exception.'
    if exception != string:
        main()
    else:
        print_self()

def print_html(text):
    'Print text as HTML.'
    out.write('Content-Type: text/html\n\n' + text)
    sys.exit(0)

def print_plain(text):
    'Print text as plain.'
    out.write('Content-Type: text/plain\n\n' + text)
    sys.exit(0)

def print_self():
    'Print __main__ as plain.'
    print_plain(file(sys.argv[0]).read())

################################################################################

import os

def export():
    'Exports string and dictionary.'
    global string, dictionary
    try:
        string = str(os.environ['QUERY_STRING'])
    except:
        try:
            string = sys.stdin.read()
        except:
            string = str()
    try:
        dictionary = dict([(decode(parameter), decode(value)) for parameter, value in [item.split('=') for item in string.replace('+', ' ').split('&')]])
    except:
        dictionary = dict()

def decode(string):
    'Receives, decodes, and returns string.'
    index = string.find('%')
    while index != -1:
        string = string[:index] + chr(int(string[index+1:index+3], 16)) + string[index+3:]
        index = string.find('%', index + 1)
    return string

################################################################################

if __name__ == '__main__':
    print_self()
else:
    export()

#===============================================================================
# htbin\z_html.py
#===============================================================================

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
        self.__special = z_matrix.Matrix(rows, columns, False)
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

    def special(self, row, column, special):
        self.__special[row][column] = special

    def set_table(self, **attributes):
        'Sets the attributes for the table.'
        self.__table_attributes = self.__parse(attributes)
        return self

    def set_row(self, **attributes):
        'Sets the attributes for each row.'
        self.__row_attributes = self.__parse(attributes)
        return self

    def set_cell(self, **attributes):
        'Sets the attributes for each cell.'
        self.__cell_attributes = self.__parse(attributes)
        return self

    def __parse(self, attributes):
        'Parses the attributes into a string.'
        return ''.join([' %s="%s"' % (key, attributes[key]) for key in sorted(attributes)])

    def html(self):
        'Returns the HTML code for the current table.'
        html = self.__indent_style * self.__indent_level + '<table' + self.__table_attributes + '>\n'
        for row, s_row in zip(self.__matrix, self.__special):
            html += self.__indent_style * (self.__indent_level + 1) + '<tr' + self.__row_attributes + '>\n'
            for cell, special in zip(row, s_row):
                html += self.__indent_style * (self.__indent_level + 2) + '<td' + self.__cell_attributes + '>\n'
                if special:
                    html += cell + '\n'
                else:
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

    def special(self, day, special):
        row, column = self.__row_column(day)
        self.__table.special(row, column, special)

    def __row_column(self, day):
        'Calculates the row and column of day.'
        assert 1 <= day <= self.__alldays
        index = day + self.__weekday
        return index / 7, index % 7

    def set_month(self, **attributes):
        'Set the attributes for the month.'
        self.__table.set_table(**attributes)
        return self

    def set_week(self, **attributes):
        'Set the attributes for each week.'
        self.__table.set_row(**attributes)
        return self

    def set_day(self, **attributes):
        'Set the attributes for each day.'
        self.__table.set_cell(**attributes)
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

#===============================================================================
# htbin\z_matrix.py
#===============================================================================

'''Module for arrays and matrices.

This module provides the Array and Matrix classes
which create mutable storage with immutable size.'''

__version__ = 1.0

################################################################################

class Array:

    'Array(length[, value]) -> Array'

    def __init__(self, length, value=None):
        'Initialize the Array object.'
        assert isinstance(length, int) and length > 0
        self.__data = [value] * length

    def __repr__(self):
        'Return the object\'s representation.'
        return repr(self.__data)

    def __len__(self):
        'Return the object\'s length.'
        return len(self.__data)

    def __getitem__(self, key):
        'Return the specified item.'
        return self.__data[key]

    def __setitem__(self, key, value):
        'Assign the value to the key.'
        self.__data[key] = value

    def __delitem__(self, key):
        'Delete the specified item.'
        self.__data[key] = None

    def __itet__(self):
        'Return the object\'s iterator.'
        return iter(self.__data)

    def __contains__(self, item):
        'Return the item\'s membership status.'
        return item in self.__data

class Matrix:

    'Matrix(rows, columns[, value]) -> Matrix'

    def __init__(self, rows, columns, value=None):
        'Initialize the Matrix object.'
        assert isinstance(rows, int) and rows > 0
        self.__data = [Array(columns, value) for row in range(rows)]
        
    def __repr__(self):
        'Return the object\'s representation.'
        return repr(self.__data)

    def __len__(self):
        'Return the object\'s length.'
        return len(self.__data)

    def __getitem__(self, key):
        'Return the specified item.'
        return self.__data[key]

    def __setitem__(self, key, value):
        'Assign the value to the key.'
        self.__data[key] = Array(len(self.__data[key]), value)

    def __delitem__(self, key):
        'Delete the specified item.'
        self.__data[key] = Array(len(self.__data[key]))

    def __iter__(self):
        'Return the object\'s iterator.'
        return iter(self.__data)

    def __contains__(self, item):
        'Return the item\'s membership status.'
        for row in self.__data:
            if item in row:
                return True
        return False

################################################################################

if __name__ == '__main__':
    import sys
    sys.stdout.write('Content-Type: text/plain\n\n' + file(sys.argv[0]).read())
