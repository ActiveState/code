# queryCSV.py
# FB - 201010111
# Query a CSV file.

# example CSV file: myData.csv
# id,code name,value
# 36,abc,7.6
# 40,def,3.6
# 9,ghi,6.3
# 76,def,99

# example query expression
query = 'id > 36 and code_name == "def" and value <= 100'

print 'Query:'
print query
print

import csv
csvData = csv.reader(open('myData.csv'))
csvTable = []
isHeader = True
for row in csvData:
    if isHeader:
        isHeader = False
        headerRow = row
        for i in range(len(headerRow)):
            # replace spaces w/ underscores in column headers
            headerRow[i] = headerRow[i].replace(' ', '_')
    else:
        csvTable.append(row)

# determine column types: string/int/float
colType = []
for i in range(len(headerRow)):
    isFloat = True
    isInt = True
    for j in range(len(csvTable)):
        try:
            v = float(csvTable[j][i])
            if not v == int(v):
                isInt = False
        except ValueError:
            isFloat = False
            isInt = False

    colT = ''
    if isInt:
        colT = 'int'
    elif isFloat:
        colT = 'float'
    else:
        colT = 'string'
    colType.append(colT)

    # print headerRow[i], colT
    
# run the query
for j in range(len(csvTable)):
    # assign the column variables
    for i in range(len(headerRow)):
        if colType[i] == 'string':
            exec(headerRow[i] + '=' + '"' + csvTable[j][i] + '"')
        elif colType[i] == 'float':
            exec(headerRow[i] + '=' + 'float("' + csvTable[j][i] + '")')
        elif colType[i] == 'int':
            exec(headerRow[i] + '=' + 'int("' + csvTable[j][i] + '")')

    # output the rows matching the query
    if eval(query):
        print headerRow
        print csvTable[j]
        print
