# Oracle database regex search
# FB36 - 201007117

import sys
import csv
import re
import cx_Oracle

connection = raw_input("Enter Oracle DB connection (uid/pwd@database) : ")
searchStr = raw_input("Enter regex search string : ")
p = re.compile(searchStr)

printHeader = True # include column headers in each table output

orcl = cx_Oracle.connect(connection)
curs = orcl.cursor()

sql = "select * from tab" # get a list of all tables
curs.execute(sql)

for row_data in curs:
    if not row_data[0].startswith('BIN$'): # skip recycle bin tables
        tableName = row_data[0]
        sql = "select * from " + tableName
        curs2 = orcl.cursor()
        curs2.execute(sql)

        # search the table and create a list of rows that matches the search regex
        matchedRows = []
        for row_data in curs2:
            # print row_data
            for col in row_data:
                if p.match(str(col)):
                    matchedRows.append(row_data)
                    
        # if some rows mathed then output them
        if len(matchedRows) > 0:
            csv_file_dest = tableName + ".csv"
            outputFile = open(csv_file_dest,'w') # 'wb'
            output = csv.writer(outputFile, dialect='excel')

            if printHeader: # add column headers if requested
                cols = []
                for col in curs2.description:
                    cols.append(col[0])
                output.writerow(cols)

            for rows in matchedRows: # add table rows
                output.writerow(rows)

            outputFile.close()
