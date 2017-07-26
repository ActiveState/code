class readexcel(object):
    """ Simple OS Independent Class for Extracting Data from Excel Files 
        the using xlrd module found at http://www.lexicon.net/sjmachin/xlrd.htm
        
        Versions of Excel supported: 2004, 2002, XP, 2000, 97, 95, 5, 4, 3
        xlrd version tested: 0.5.2
        
        Data is extracted by creating a iterator object which can be used to 
        return data one row at a time. The default extraction method assumes 
        that the worksheet is in tabular format with the first nonblank row
        containing variable names and all subsequent rows containing values.
        This method returns a dictionary which uses the variables names as keys
        for each piece of data in the row.  Data can also be extracted with 
        each row represented by a list.
        
        Extracted data is represented fairly logically. By default dates are
        returned as strings in "yyyy/mm/dd" format or "yyyy/mm/dd hh:mm:ss",
        as appropriate.  However, dates can be return as a tuple containing
        (Year, Month, Day, Hour, Min, Second) which is appropriate for usage
        with mxDateTime or DateTime.  Numbers are returned as either INT or 
        FLOAT, whichever is needed to support the data.  Text, booleans, and
        error codes are also returned as appropriate representations.
        
        Quick Example:
        xl = readexcel('testdata.xls')
        sheetnames = xl.worksheets()
        for sheet in sheetnames:
            print sheet
            for row in xl.getiter(sheet):
                # Do Something here
        """ 
    def __init__(self, filename):
        """ Returns a readexcel object of the specified filename - this may
        take a little while because the file must be parsed into memory """
        import xlrd
        import os.path
        if not os.path.isfile(filename):
            raise NameError, "%s is not a valid filename" % filename
        self.__filename__ = filename
        self.__book__ = xlrd.open_workbook(filename)
        self.__sheets__ = {}
        self.__sheetnames__ = []
        for i in self.__book__.sheet_names():
            uniquevars = []
            firstrow = 0
            sheet = self.__book__.sheet_by_name(i)
            for row in range(sheet.nrows):
                types,values = sheet.row_types(row),sheet.row_values(row)
                nonblank = False
                for j in values:
                    if j != '':
                        nonblank=True
                        break
                if nonblank:
                    # Generate a listing of Unique Variable Names for Use as
                    # Dictionary Keys In Extraction. Duplicate Names will
                    # be replaced with "F#"
                    variables = self.__formatrow__(types,values,False)
                    unknown = 1
                    while variables:
                        var = variables.pop(0)
                        if var in uniquevars or var == '':
                            var = 'F' + str(unknown)
                            unknown += 1
                        uniquevars.append(str(var))
                    firstrow = row + 1
                    break
            self.__sheetnames__.append(i)
            self.__sheets__.setdefault(i,{}).__setitem__('rows',sheet.nrows)
            self.__sheets__.setdefault(i,{}).__setitem__('cols',sheet.ncols)
            self.__sheets__.setdefault(i,{}).__setitem__('firstrow',firstrow)
            self.__sheets__.setdefault(i,{}).__setitem__('variables',uniquevars[:])
    def getiter(self, sheetname, returnlist=False, returntupledate=False):
        """ Return an generator object which yields the lines of a worksheet;
        Default returns a dictionary, specifing returnlist=True causes lists
        to be returned.  Calling returntupledate=True causes dates to returned
        as tuples of (Year, Month, Day, Hour, Min, Second) instead of as a
        string """
        if sheetname not in self.__sheets__.keys():
            raise NameError, "%s is not present in %s" % (sheetname,\
                                                          self.__filename__)
        if returnlist:
            return __iterlist__(self, sheetname, returntupledate)
        else:
            return __iterdict__(self, sheetname, returntupledate)
    def worksheets(self):
        """ Returns a list of the Worksheets in the Excel File """
        return self.__sheetnames__
    def nrows(self, worksheet):
        """ Return the number of rows in a worksheet """
        return self.__sheets__[worksheet]['rows']
    def ncols(self, worksheet):
        """ Return the number of columns in a worksheet """
        return self.__sheets__[worksheet]['cols']
    def variables(self,worksheet):
        """ Returns a list of Column Names in the file,
            assuming a tabular format of course. """
        return self.__sheets__[worksheet]['variables']
    def __formatrow__(self, types, values, wanttupledate):
        """ Internal function used to clean up the incoming excel data """
        ##  Data Type Codes:
        ##  EMPTY 0
        ##  TEXT 1 a Unicode string 
        ##  NUMBER 2 float 
        ##  DATE 3 float 
        ##  BOOLEAN 4 int; 1 means TRUE, 0 means FALSE 
        ##  ERROR 5 
        import xlrd
        returnrow = []
        for i in range(len(types)):
            type,value = types[i],values[i]
            if type == 2:
                if value == int(value):
                    value = int(value)
            elif type == 3:
                datetuple = xlrd.xldate_as_tuple(value, self.__book__.datemode)
                if wanttupledate:
                    value = datetuple
                else:
                    # time only no date component
                    if datetuple[0] == 0 and datetuple[1] == 0 and \
                       datetuple[2] == 0: 
                        value = "%02d:%02d:%02d" % datetuple[3:]
                    # date only, no time
                    elif datetuple[3] == 0 and datetuple[4] == 0 and \
                         datetuple[5] == 0:
                        value = "%04d/%02d/%02d" % datetuple[:3]
                    else: # full date
                        value = "%04d/%02d/%02d %02d:%02d:%02d" % datetuple
            elif type == 5:
                value = xlrd.error_text_from_code[value]
            returnrow.append(value)
        return returnrow
    
def __iterlist__(excel, sheetname, tupledate):
    """ Function Used To Create the List Iterator """
    sheet = excel.__book__.sheet_by_name(sheetname)
    for row in range(excel.__sheets__[sheetname]['rows']):
        types,values = sheet.row_types(row),sheet.row_values(row)
        yield excel.__formatrow__(types, values, tupledate)

def __iterdict__(excel, sheetname, tupledate):
    """ Function Used To Create the Dictionary Iterator """
    sheet = excel.__book__.sheet_by_name(sheetname)
    for row in range(excel.__sheets__[sheetname]['firstrow'],\
                     excel.__sheets__[sheetname]['rows']):
        types,values = sheet.row_types(row),sheet.row_values(row)
        formattedrow = excel.__formatrow__(types, values, tupledate)
        # Pad a Short Row With Blanks if Needed
        for i in range(len(formattedrow),\
                       len(excel.__sheets__[sheetname]['variables'])):
            formattedrow.append('')
        yield dict(zip(excel.__sheets__[sheetname]['variables'],formattedrow))
