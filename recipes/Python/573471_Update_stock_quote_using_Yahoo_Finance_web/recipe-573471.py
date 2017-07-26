# -*- coding: UTF-8 -*-
"""Usage: update_quote.py [log_filename]

This script will scan your Excel spreadsheet for stock symbols. It will fetch
the stock quote from the web and update the data in the spreadsheet.

The spreadsheet should have a table on active sheet. The first row should be the
header names and the first column should have the stock symbols. Blank cells is
used to delimit the range of the table.

(Last updated 2008-06-22 11:02:56)
"""


import csv
import datetime
import sys
from pprint import pprint
from StringIO import StringIO
import urllib
from win32com.client import Dispatch

# Yahoo stock quote URL
URL = "http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=sl1d1t1c1ohgv&e=.csv"

# header of CSV, used to match header name in spreadsheet
QUOTE_HEADER = [
"Symbol",
"Price",
"Last Trade",
"Last Time",
"Change",
"Open",
"Day High",
"Day Low",
"Volume",
]

LOG_DATA_FETCHED = True

LOG_FILENAME = 'quotes%s.csv'


def log(msg):
    print(msg.encode('utf-8'))

def scan_spreadsheet(xl):
    symbols = []
    for row in range(2,999):
        value = xl.Cells(row,1).value
        if not value:
            break
        symbols.append(value)

    header_map = {}
    for col in range(1,99):
        value = xl.Cells(1,col).value
        if not value:
            break
        header_map[value.lower()] = col

    # quote (0 based) col number -> spreadsheet (1 based) col
    quote_col_map = [header_map.get(header.lower(), None)
                        for header in QUOTE_HEADER]

    return symbols, quote_col_map

def fetch_quote(symbols, timestamp, cached_file=None):
    url = URL % '+'.join(symbols)

    if not cached_file:
        # fetch
        log('Fetching %s' % url)
        fp = urllib.urlopen(url)
        try:
            data = fp.read()
        finally:
            fp.close()

        # log result
        if LOG_DATA_FETCHED:
            log_filename = LOG_FILENAME % timestamp.replace(':','-')
            out = open(log_filename, 'wb')
            try:
                log('Fetched %s bytes logged in %s' % (len(data), log_filename))
                out.write(data)
            finally:
                out.close()
    else:
        data = open(cached_file,'rb').read()

    return StringIO(data)

def update_spreadsheet(xl, fp , header_map):
    # don't want to update symbol (col 0)
    header_map[0] = None

    update_count = 0
    reader = csv.reader(fp)
    for y_0, row in enumerate(reader):

        row_num = y_0+2
        # take at most number of values defined in QUOTE_HEADER
        row = row[:len(QUOTE_HEADER)]

        # make sure the quoted symbol match what we have requested
        quote_symbol = unicode(row[0],'utf-8')
        excel_symbol = xl.Cells(row_num,1).value
        if excel_symbol == quote_symbol :
            log('Updating %s'% quote_symbol)
        else:
            log('Wrong Symbol %s != %s' % (excel_symbol , quote_symbol))
            continue

        # update data on that row
        for x_0, value in enumerate(row):
            col_num = header_map[x_0]
            if col_num:
                xl.Cells(row_num,col_num).value = value
        update_count += 1

    log('Updated %s rows'% update_count)

def main(argv):
    cache_pathname = argv[1] if len(argv) > 1 else None

    now = datetime.datetime.now()
    timestamp = now.isoformat()[:19]
    log('\nDate: %s'% timestamp)

    # Open Excel
    xl = Dispatch("Excel.Application")
    xl.Visible = 1
    try:
        pathname = xl.ActiveWorkbook.Fullname
    except:
        log('Error: No active excel workbook.')
        sys.exit(-1)
    filename = pathname.rpartition('\\')[2]

    # scan for symbols to lookup
    symbols, quote_col_map = scan_spreadsheet(xl)
    log('Updating spreadsheet %s #symbol: %s'% (filename, len(symbols)))
    if symbols:
        data_fp = fetch_quote(symbols, timestamp, cache_pathname)
        update_spreadsheet(xl, data_fp, quote_col_map)

if __name__ =='__main__':
    if '--help' in sys.argv:
        print __doc__
        sys.exit()

    main(sys.argv)
