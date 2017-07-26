# Oracle database string search
# FB - 20130726
import sys
import os
import csv
import re
import cx_Oracle

connection = raw_input("Enter Oracle DB connection (uid/pwd@database) : ")
searchStr = raw_input("Enter search string : ")
cs = raw_input("Case-sensitive search (y/n): ").lower()
rs = raw_input("Regex search (y/n): ").lower()
wc = raw_input("Whole column must match (y/n): ").lower()

if cs == 'n':
    caseSensitive = False
elif cs == 'y':
    caseSensitive = True
else:
    print "Wrong choice!"
    os._exit(1)

if rs == 'n':
    regexSearch = False
elif rs == 'y':
    regexSearch = True
else:
    print "Wrong choice!"
    os._exit(1)

if wc == 'n':
    wholeColumn = False
elif wc == 'y':
    wholeColumn = True
else:
    print "Wrong choice!"
    os._exit(1)

if regexSearch:
    if caseSensitive:
        searchStr = re.compile(searchStr)
    else:
        searchStr = re.compile(searchStr, re.IGNORECASE)

print2Screen = True
printHeader = True # include column headers in each table output

curs = cx_Oracle.connect(connection).cursor()

tables = curs.execute("select table_name from user_tables").fetchall()
for tableNameTuple in tables:
    tableName = tableNameTuple[0]
    print "Searching table: " + tableName
    sql = "select * from " + tableName
    curs.execute(sql)

    # search the table and create a list of rows that contains the search string
    matchedRows = []
    for row_data in curs:
        # print row_data
        for col in row_data:
            colStr = str(col).strip()

            if wholeColumn: # match if search string fully matches column value
                if regexSearch:
                    if searchStr.match(colStr):
                        matchedRows.append(row_data)
                else:
                    if caseSensitive:
                        if colStr == searchStr:
                            matchedRows.append(row_data)
                    else: # not case sensitive
                        if colStr.lower() == searchStr.lower():
                            matchedRows.append(row_data)
            else: # match if search string included anywhere in column value
                if regexSearch:
                    if searchStr.search(colStr):
                        matchedRows.append(row_data)
                else:
                    if caseSensitive:
                        if colStr.find(searchStr) >= 0:
                            matchedRows.append(row_data)
                    else: # not case sensitive
                        if colStr.lower().find(searchStr.lower()) >= 0:
                            matchedRows.append(row_data)
                
    # if some rows mathed then output them
    if len(matchedRows) > 0:
        print "Found match in table " + tableName
        if print2Screen:
            print matchedRows
            print

        # create a CSV file for the table that has any match   
        csv_file_dest = tableName + ".csv"
        outputFile = open(csv_file_dest,'w') # 'wb'
        output = csv.writer(outputFile, dialect='excel')

        if printHeader: # add column headers if requested
            cols = []
            for col in curs.description:
                cols.append(col[0])
            output.writerow(cols)

        for rows in matchedRows: # add table rows
            output.writerow(rows)

        outputFile.close()
