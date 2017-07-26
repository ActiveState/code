import csv, collections, copy

'''
# CSV TEST FILE 'test.csv'

TBLID,DATETIME,VAL
C1,01:01:2011:00:01:23,5
C2,01:01:2012:00:01:23,8
C3,01:01:2013:00:01:23,4
C4,01:01:2011:01:01:23,9
C5,01:01:2011:02:01:23,1
C6,01:01:2011:03:01:23,5
C7,01:01:2011:00:01:23,6
C8,01:01:2011:00:21:23,8
C9,01:01:2011:12:01:23,1


#usage

>>> import CustomDictReader
>>> import pprint
>>> test = CustomDictReader.CSVRW()
>>> success, thedict = test.createCsvDict('TBLID',',',None,'test.csv')
>>> pprint.pprint(dict(d))
{'C1': OrderedDict([('TBLID', 'C1'), ('DATETIME', '01:01:2011:00:01:23'), ('VAL', '5')]),
 'C2': OrderedDict([('TBLID', 'C2'), ('DATETIME', '01:01:2012:00:01:23'), ('VAL', '8')]),
 'C3': OrderedDict([('TBLID', 'C3'), ('DATETIME', '01:01:2013:00:01:23'), ('VAL', '4')]),
 'C4': OrderedDict([('TBLID', 'C4'), ('DATETIME', '01:01:2011:01:01:23'), ('VAL', '9')]),
 'C5': OrderedDict([('TBLID', 'C5'), ('DATETIME', '01:01:2011:02:01:23'), ('VAL', '1')]),
 'C6': OrderedDict([('TBLID', 'C6'), ('DATETIME', '01:01:2011:03:01:23'), ('VAL', '5')]),
 'C7': OrderedDict([('TBLID', 'C7'), ('DATETIME', '01:01:2011:00:01:23'), ('VAL', '6')]),
 'C8': OrderedDict([('TBLID', 'C8'), ('DATETIME', '01:01:2011:00:21:23'), ('VAL', '8')]),
 'C9': OrderedDict([('TBLID', 'C9'), ('DATETIME', '01:01:2011:12:01:23'), ('VAL', '1')])}

'''

class CustomDictReader(csv.DictReader):
    '''
        override the next() function and  use an
        ordered dict in order to preserve writing back
        into the file
    '''

    def __init__(self, f, fieldnames = None, restkey = None, restval = None, dialect ="excel", *args, **kwds):
        csv.DictReader.__init__(self, f, fieldnames = None, restkey = None, restval = None, dialect = "excel", *args, **kwds)

    def next(self):
        if self.line_num == 0:
            # Used only for its side effect.
            self.fieldnames
        row = self.reader.next()
        self.line_num = self.reader.line_num

        # unlike the basic reader, we prefer not to return blanks,
        # because we will typically wind up with a dict full of None
        # values
        while row == []:
            row = self.reader.next()
        d = collections.OrderedDict(zip(self.fieldnames, row))

        lf = len(self.fieldnames)
        lr = len(row)
        if lf < lr:
            d[self.restkey] = row[lf:]
        elif lf > lr:
            for key in self.fieldnames[lr:]:
                d[key] = self.restval
        return d

class CSVRW(object):

    def __init__(self):
        self.file_name = ""
        self.csv_delim = ""
        self.csv_dict  = collections.OrderedDict()

    def setCsvFileName(self, name):
        '''
            @brief stores csv file name
            @param name- the file name
        '''
        self.file_name = name

    def getCsvFileName():
        '''
            @brief getter
            @return returns the file name
        '''
        return self.file_name

    def getCsvDict(self):
        '''
            @brief getter
            @return returns a deep copy of the csv as a dictionary
        '''
        return copy.deepcopy(self.csv_dict)

    def clearCsvDict(self):
        '''
            @brief resets the dictionary
        '''
        self.csv_dict = collections.OrderedDict()

    def updateCsvDict(self, newCsvDict):
        '''
            creates a deep copy of the dict passed in and
            sets it to the member one
        '''
        self.csv_dict = copy.deepcopy(newCsvDict)

    def createCsvDict(self,dictKey, delim, handle = None, name = None, readMode = 'rb', **kwargs):
        '''
            @brief create a dict from a csv file where:
                the top level keys are the first line in the dict, overrideable w/ **kwargs
                each row is a dict
                each row can be accessed by the value stored in the column associated w/ dictKey

                that is to say, if you want to index into your csv file based on the contents of the
                third column, pass the name of that col in as 'dictKey'

            @param dictKey  - row key whose value will act as an index
            @param delim    - csv file deliminator
            @param handle   - file handle (leave as None if you wish to pass in a file name)
            @param name     - file name   (leave as None if you wish to pass in a file handle)
            @param readMode - 'r' || 'rb'
            @param **kwargs - additional args allowed by the csv module
            @return bool    - SUCCESS|FAIL
        '''
        retVal         = (False, None)
        self.csv_delim = delim

        try:
            reader = None
            if isinstance(handle, file):
                self.setCsvFileName(handle.name)
                reader = CustomDictReader(handle, delim, **kwargs)
            else:
                if None == name:
                    name = self.getCsvFileName()
                else:
                    self.setCsvFileName(name)
                reader = CustomDictReader(open(name, readMode), delim, **kwargs)

            for row in reader:
                self.csv_dict[row[dictKey]] = row

            retVal = (True, self.getCsvDict())

        except IOError:
            retVal = (False, 'Error opening file')

        return retVal

    def createCsv(writeMode, outFileName = None, delim = None):
        '''
            @brief create a csv from self.csv_dict
            @param writeMode   - 'w' || 'wb'
            @param outFileName - file name || file handle
            @param delim       - csv deliminator
            @return none
        '''
        if None == outFileName:
            outFileName = self.file_name
        if None == delim:
            delim = self.csv_delim

        with open(outFileName, writeMode) as fout:
            for key in self.csv_dict.values():
                fout.write(delim.join(key.keys()) + '\n')
                break

            for key in self.csv_dict.values():
                fout.write(delim.join(key.values()) + '\n')
