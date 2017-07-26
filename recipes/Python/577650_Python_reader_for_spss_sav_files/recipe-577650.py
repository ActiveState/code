#!/usr/bin/env python
# -*- coding: cp1252 -*-

""" A Python interface to the IBM SPSS Statistics Input Output Module
(Windows: spssio32.dll)"""

# spssio32.dll and documentation can be downloaded here:
# https://www.ibm.com/developerworks/mydeveloperworks/wikis/home/wiki/We70df3195ec8_4f95_9773_42e448fa9029/page/Downloads%20for%20IBM%C2%AE%20SPSS%C2%AE%20Statistics?lang=en
# TO DO: make this work under Linux. When I tried the .so file,
# I had a hard time finding all the necessary dependencies.
# The .so file versions that are needed are rather old.
# NOTE: If you downloaded this previously, use the current version as it
#       is *MUCH* faster!!
# ANY FEEDBACK ON THIS CODE IS WELCOME: "@".join(["fomcl", "yahoo.com"])

from __future__ import with_statement # only Python 2.5
import sys
import os
import ctypes
import struct
import operator
import math
import locale
import datetime
try:
    import psyco
    psyco.full()
except ImportError:
    print "NOTE. Psyco module not found. Install this module to increase program performance"

__author__  =  'Albert-Jan Roskam'
__version__ =  '2.0.0'

retcodes =    {0: 'SPSS_OK',
               1: 'SPSS_EXC_LEN64',
               2: 'SPSS_EXC_VARLABEL',
               3: 'SPSS_FILE_RERROR',
               4: 'SPSS_EXC_VALLABEL',
               5: 'SPSS_FILE_END',
               6: 'SPSS_NO_VARSETS',
               7: 'SPSS_EMPTY_VARSETS',
               8: 'SPSS_NO_LABELS',
               9: 'SPSS_NO_LABEL',
               10: 'SPSS_NO_CASEWGT',
               11: 'SPSS_NO_DATEINFO',
               12: 'SPSS_NO_MULTRESP',
               13: 'SPSS_EMPTY_MULTRESP',
               14: 'SPSS_NO_DEW',
               15: 'SPSS_EMPTY_DEW',
               16: 'SPSS_SHORTSTR_EXP',
               17: 'SPSS_INVALID_VARTYPE',
               18: 'SPSS_INVALID_MISSFOR',
               19: 'SPSS_INVALID_COMPSW',
               20: 'SPSS_INVALID_PRFOR',
               21: 'SPSS_INVALID_WRFOR',
               22: 'SPSS_INVALID_DATE',
               23: 'SPSS_INVALID_TIME',
               24: 'SPSS_NO_VARIABLES',
               25: 'SPSS_MIXED_TYPES',
               27: 'SPSS_DUP_VALUE',
               28: 'SPSS_INVALID_CASEWGT',
               29: 'SPSS_INCOMPATIBLE_DICT',
               30: 'SPSS_DICT_COMMIT',
               31: 'SPSS_DICT_NOTCOMMIT',
               33: 'SPSS_NO_TYPE2',
               41: 'SPSS_NO_TYPE73',
               45: 'SPSS_INVALID_DATEINFO',
               46: 'SPSS_NO_TYPE999',
               47: 'SPSS_EXC_STRVALUE',
               48: 'SPSS_CANNOT_FREE',
               49: 'SPSS_BUFFER_SHORT',
               50: 'SPSS_INVALID_CASE',
               51: 'SPSS_INTERNAL_VLABS',
               52: 'SPSS_INCOMPAT_APPEND',
               53: 'SPSS_INTERNAL_D_A',
               54: 'SPSS_FILE_BADTEMP',
               55: 'SPSS_DEW_NOFIRST',
               56: 'SPSS_INVALID_MEASURELEVEL',
               57: 'SPSS_INVALID_7SUBTYPE',
               58: 'SPSS_INVALID_VARHANDLE',
               59: 'SPSS_INVALID_ENCODING',
               60: 'SPSS_FILES_OPEN',
               70: 'SPSS_INVALID_MRSETDEF',
               71: 'SPSS_INVALID_MRSETNAME',
               72: 'SPSS_DUP_MRSETNAME',
               73: 'SPSS_BAD_EXTENSION',
               74: 'SPSS_INVALID_EXTENDEDSTRING',
               75: 'SPSS_INVALID_ATTRNAME',
               76: 'SPSS_INVALID_ATTRDEF',
               77: 'SPSS_INVALID_MRSETINDEX',
               78: 'SPSS_INVALID_VARSETDEF',
               79: 'SPSS_INVALID_ROLE'}

printTypes =  {1: ('SPSS_FMT_A', 'Alphanumeric'),
               2: ('SPSS_FMT_AHEX', 'Alphanumeric hexadecimal'),
               3: ('SPSS_FMT_COMMA', 'F Format with commas'),
               4: ('SPSS_FMT_DOLLAR', 'Commas and floating dollar sign'),
               5: ('SPSS_FMT_F', 'Default Numeric Format'),
               6: ('SPSS_FMT_IB', 'Integer binary'),
               7: ('SPSS_FMT_PIBHEX', 'Positive integer binary - hex'),
               8: ('SPSS_FMT_P', 'Packed decimal'),
               9: ('SPSS_FMT_PIB', 'Positive integer binary unsigned'),
               10: ('SPSS_FMT_PK', 'Positive integer binary unsigned'),
               11: ('SPSS_FMT_RB', 'Floating point binary'),
               12: ('SPSS_FMT_RBHEX', 'Floating point binary hex'),
               15: ('SPSS_FMT_Z', 'Zoned decimal'),
               16: ('SPSS_FMT_N', 'N Format- unsigned with leading 0s'),
               17: ('SPSS_FMT_E', 'E Format- with explicit power of 10'),
               20: ('SPSS_FMT_DATE', 'Date format dd-mmm-yyyy'),
               21: ('SPSS_FMT_TIME', 'Time format hh:mm:ss.s'),
               22: ('SPSS_FMT_DATE_TIME', 'Date and Time'),
               23: ('SPSS_FMT_ADATE', 'Date format dd-mmm-yyyy'),
               24: ('SPSS_FMT_JDATE', 'Julian date - yyyyddd'), 
               25: ('SPSS_FMT_DTIME', 'Date-time dd hh:mm:ss.s'),
               26: ('SPSS_FMT_WKDAY', 'Day of the week'),
               27: ('SPSS_FMT_MONTH', 'Month'),
               28: ('SPSS_FMT_MOYR', 'mmm yyyy'),
               29: ('SPSS_FMT_QYR', 'q Q yyyy'),
               30: ('SPSS_FMT_WKYR', 'ww WK yyyy'),
               31: ('SPSS_FMT_PCT', 'Percent - F followed by %'),
               32: ('SPSS_FMT_DOT', 'Like COMMA, switching dot for comma'),
               33: ('SPSS_FMT_CCA', 'User Programmable currency format'),
               34: ('SPSS_FMT_CCB', 'User Programmable currency format'),
               35: ('SPSS_FMT_CCC', 'User Programmable currency format'),
               36: ('SPSS_FMT_CCD', 'User Programmable currency format'),
               37: ('SPSS_FMT_CCE', 'User Programmable currency format'),
               38: ('SPSS_FMT_EDATE','Date in dd/mm/yyyy style'),
               39: ('SPSS_FMT_SDATE', 'Date in yyyy/mm/dd style')}

class SavReader(object):
    """ Read Spss system files (.sav)

    Parameters:
    -savFileName: the file name of the spss data file
    -returnHeader: Boolean that indicates whether the first record should
        be a list of variable names (default is True)
    -recodeSysmisTo: indicates to which value missing values should
        be recoded (default = ""),
    -selectVars: indicates which variables in the file should be selected.
        The variables should be specified as a list or a tuple of
        valid variable names. If None is specified, all variables
        in the file are used (default = None)
    -verbose: Boolean that indicates whether information about the spss data file
        (e.g., number of cases, variable names, file size) should be printed on
        the screen (default = True).
    -rawMode: Boolean that indicates whether values should get SPSS-style formatting,
        and whether date variables (if present) should be converted to ISO-dates. If True.
        the program does not format any values, which increases processing speed.
        (default = False)
    -interfaceEncoding: indicates the mode in which text communicated to or from the
        I/O Module will be. Valid values are 'UTF-8' or 'CODEPAGE' (default = 'CODEPAGE')

    Typical use:
    savFileName = "d:/someFile.sav"
    with SavReader(savFileName) as sav:
        header = sav.next()
        for line in sav:
            process(line)
    """

    def __init__(self, savFileName, returnHeader=True, recodeSysmisTo="",
                 verbose=True, selectVars=None, rawMode=False, interfaceEncoding="CODEPAGE"):
        """ Constructor. Initializes all vars that can be recycled """

        self.savFileName = savFileName
        self.returnHeader = returnHeader
        self.recodeSysmisTo = recodeSysmisTo
        self.verbose = verbose
        self.selectVars = selectVars
        self.rawMode = rawMode
                                          
        self.gregorianEpoch = datetime.datetime(1582, 10, 14, 0, 0, 0)
        #self.CUT_OFF = self.getSystemSysmisVal(self.spssio)
        self.CUT_OFF = -1 * sys.float_info[0]

        self.numVars = ctypes.c_int()
        self.numVarsPtr = ctypes.byref(self.numVars)
        self.nCases = ctypes.c_long()
        self.numofCasesPtr = ctypes.byref(self.nCases)
        
        self.printType = ctypes.c_int()
        self.printDec = ctypes.c_int()
        self.printWid = ctypes.c_int()
        self.printTypePtr = ctypes.byref(self.printType)
        self.printDecPtr = ctypes.byref(self.printDec)
        self.printWidPtr = ctypes.byref(self.printWid)

        self.attribNames = ctypes.c_char_p()
        self.attribText = ctypes.c_char_p()
        self.nAttributes = ctypes.c_int()
        self.attribNamesPtr = ctypes.byref(self.attribNames)
        self.attribTextPtr = ctypes.byref(self.attribText)
        self.nAttributesPtr = ctypes.byref(self.nAttributes)

        self.numValue = ctypes.c_double()
        self.numValuePtr = ctypes.byref(self.numValue)
        self.assumedCharWid = 200 # hmmmm...
        self.charValue = ctypes.create_string_buffer(self.assumedCharWid)
        self.charValuePtr = ctypes.byref(self.charValue)
        self.valueSize = ctypes.c_int(self.assumedCharWid)

        self.interfaceEncodingIn = interfaceEncoding        
        self.retcode, self.spssio, self.fh, self.numVars_, \
          self.nCases_, self.varNames, self.varTypes, self.printTypesFile, \
          self.printTypeLabels, self.varWids = self._readBasicSavFileInfo()
        self.interfaceEncoding, self.encoding = self.getInterfaceEncoding(self.spssio)
        self.header = self.getHeader(self.selectVars)

    def __enter__(self):
        """ This function opens the spss data file."""
        return self.readSavFile(self.returnHeader, self.recodeSysmisTo,
                                self.selectVars, self.rawMode, self.encoding)

    def __exit__(self, type, value, tb):
        """ This function closes the spss data file."""
        if type is not None:
            pass # Exception occurred
        self.spssio.spssCloseRead(self.fh)
        del self.spssio
        
    def _readBasicSavFileInfo(self):
        """ This function reads and returns some basic information of the open
        spss data file. It returns the following variables:
        retcode: the return code (0 means OK)
        spssio: the spss i/o C module, opened with ctypes.windll.spssio32
        fh: the file handle
        numVars: the number of variables in the spss data file
        nCases: the number of cases (records) in the spss data file
        varNames: a list of the var names  in the spss data file
        varTypes: a dictionary with var names as keys and var types as values
        printTypesFile: a dictionary with var names as keys and print types as values
        printTypeLabels: a dictionary with var names as keys and print type labels as values
        varWids: : a dictionary with var names as keys and var widths as values
        NOT FOR GENERAL USE; see getSavFileInfo
        """
        self.retcode, self.spssio, self.fh = self.loadSavFile(self.savFileName,
                                                              self.interfaceEncodingIn)
        numVars = self.getNumberofVariables(self.fh, self.spssio)[1]
        nCases = self.getNumberofCases(self.fh, self.spssio)[1]
        varNames, varTypes_ = self.getVarInfo(self.fh, self.spssio)
        self.fileEncoding = self.getFileEncoding(self.fh)[1]
        self.fileCodePage = self.getFileCodePage(self.fh)[1]
        
        varTypes, printTypesFile, varWids, printDecs, \
                  printWids = {}, {}, {}, {}, {}
        for i, varName in enumerate(varNames):
            varTypes[varName] = varTypes_[i]
            retcode, printType, printDec, printWid = \
                     self.getVarPrintFormat(self.fh, self.spssio, varName)
            printTypesFile[varName] = printType
            varWids[varName] = printWid
            printDecs[varName] = printDec
            printWids[varName] = printWid
            
        printTypeLabels = dict([(varName,
                                 printTypes[printType][0])
                                for varName, printType in printTypesFile.iteritems()])

        fmts = dict([(varName, printTypeLabels[varName].split("_")[-1])
                     for varName in varNames])
        if self.verbose:
            print self.getFileReport(self.savFileName, varNames, varTypes, fmts,
                               printDecs, printWids, nCases)

        return retcode, self.spssio, self.fh, numVars, nCases, varNames, \
               varTypes, printTypesFile, printTypeLabels, varWids

    def getSavFileInfo(self):
        """ This function reads and returns some basic information of the open
        spss data file. Returns numVars, nCases, varNames, varTypes, printTypesFile,
        printTypeLabels, varWids. Suitable for use without context manager ('with' statement)
        See also _readBasicSavFileInfo method."""
        return self.numVars_, self.nCases_, self.varNames, self.varTypes, self.printTypesFile, \
          self.printTypeLabels, self.varWids
        
    def loadSavFile(self, savFileName, interfaceEncoding):
        """ This function loads the spss I/O file (.dll or .so file) and opens
        the spss data file for reading."""
        platform = sys.platform.lower()
        if platform.startswith("win"):
            try:
                os.environ["PATH"] += ";" + os.path.abspath(".")
                spssio = ctypes.windll.spssio32
                self.libc = ctypes.cdll.msvcrt
                fopen = self.libc._fdopen # libc.fopen() won't work on windows
            except WindowsError, e:
                msg = "Cannot find spssio32.dll in '%s'.\n" % os.path.abspath(".") + \
                      "Py file and Dll should live in the same directory [%s]." % e
                raise Exception, msg
        elif platform.startswith("linux"):
            # add library search path to LD_LIBRARY_PATH environment variable
            # Type this in the terminal **before** running the program:
            # LD_LIBRARY_PATH=/path/of/additional/sofiles
            # export LD_LIBRARY_PATH
            # also need libirc.so from intel-icc8-libs_8.0-1_i386 (?) but this is broken.
            # or perhaps intel-icc9-libs-9.0-025.i386 (?)
            path = os.path.abspath(".")
            os.environ["PATH"] += ":" + path
            libicuuc = ctypes.CDLL("libicuuc.so.32.0")
            libicudata = ctypes.CDLL("libicudata.so.32")
            libicu32 = ctypes.CDLL("libicu.so.32.0") # ??
            spssio = ctypes.CDLL("%s/libspssdio.so.1" % path)
            self.libc = ctypes.CDLL("libc.so.6")
            fopen = self.libc.fopen
        else:
            msg = "Your platform ('%s') is not supported" % platform
            raise NotImplementedError, msg

        self.setInterfaceEncoding(spssio, interfaceEncoding)
        
        if os.path.exists(self.savFileName):
            fh = fopen(self.savFileName, "rb")
            fhPtr = ctypes.byref(ctypes.c_int(fh))
            retcode = spssio.spssOpenRead(ctypes.c_char_p(self.savFileName), fhPtr)
            return retcode, spssio, fh
        else:
            raise Exception, "File '%s' does not exist!" % self.savFileName
            
    def getNumberofVariables(self, fh, spssio):
        """ This function reports the number of variables present in a data file."""
        retcode = spssio.spssGetNumberofVariables(fh, self.numVarsPtr)
        return retcode, self.numVars.value

    def getVarNameAndType(self, fh, spssio, iVar):
        """ Get variable name and type. The variable type code is an integer
        in the range 0-32767, 0 indicating a numeric variable and a positive
        value indicating a string variable of that size."""
        varNameBuff = ctypes.create_string_buffer(65)
        varNamePtr = ctypes.byref(varNameBuff)
        varType = ctypes.c_int()
        varTypePtr = ctypes.byref(varType)
        retcode = spssio.spssGetVarInfo(fh, iVar, varNamePtr, varTypePtr)
        return varNameBuff.value, varType.value

    def getVarInfo(self, fh, spssio):
        """ This function gets the name and type of one of the variables
        present in a data file."""
        spssio.spssGetNumberofVariables(fh, self.numVarsPtr)
        varNames, varTypes = [], []
        for iVar in range(self.numVars.value):
            varName, varType = self.getVarNameAndType(fh, spssio, iVar)
            varNames.append(varName)
            varTypes.append(varType)
        return varNames, varTypes

    def getNumberofCases(self, fh, spssio):
        """ This function reports the number of cases present in a data file"""
        retcode = spssio.spssGetNumberofCases(fh, self.numofCasesPtr)
        return retcode, self.nCases.value

    def getVarPrintFormat(self, fh, spssio, variable):
        """ This function reports the print format of a variable. Format
        type, number of decimal places, and field width are returned. """
        self.varName = ctypes.c_char_p(variable)
        retcode = spssio.spssGetVarPrintFormat(fh,
                                self.varName,
                                self.printTypePtr,
                                self.printDecPtr,
                                self.printWidPtr)
        return retcode, self.printType.value, self.printDec.value, \
               self.printWid.value

    def getSystemSysmisVal(self, spssio):
        """This function returns the IBM SPSS Statistics system-missing
        value for the host system."""
        # returns Inf. Function not currently used.
        spssio.spssSysmisVal.restype = ctypes.c_float
        return spssio.spssSysmisVal()

    def formatValue(self, fh, spssio, variable, value, printTypeLabel,
                    varWid, recodeSysmisTo):
        """ This function formats date fields to ISO dates (yyyy-mm-dd), plus
        some other date/time formats. The SPSS N format is formatted to a
        character value with leading zeroes."""
        supportedDates = {'SPSS_FMT_DATE':     '%Y-%m-%d',
                          'SPSS_FMT_JDATE':    '%Y-%m-%d',
                          'SPSS_FMT_EDATE':    '%Y-%m-%d',
                          'SPSS_FMT_SDATE':    '%Y-%m-%d',
                          'SPSS_FMT_DATE_TIME':'%Y-%m-%d %H:%M:%S',
                          'SPSS_FMT_WKDAY':    '%A %H:%M:%S',
                          'SPSS_FMT_ADATE':    '%Y-%m-%d',
                          'SPSS_FMT_WKDAY':    '%A',
                          'SPSS_FMT_MONTH':    '%B',
                          'SPSS_FMT_MOYR':     '%B %Y',
                          'SPSS_FMT_WKYR':     '%W WK %Y'}
        if printTypeLabel in supportedDates:
            fmt = supportedDates[printTypeLabel]
            return self.spss2strDate(value, fmt, recodeSysmisTo)
        elif printTypeLabel == 'SPSS_FMT_N':
            value = str(value).zfill(varWid)
            return value
        else:
            return value
    
    def spss2strDate(self, spssDateValue, fmt, recodeSysmisTo):
        """ This function converts internal SPSS dates (number of seconds
        since midnight, Oct 14, 1582 (the beginning of the Gregorian calendar))
        to a human-readable format """
        try:
            theDate = self.gregorianEpoch + datetime.timedelta(seconds=spssDateValue)
            return datetime.datetime.strftime(theDate, fmt)
        except TypeError:
            return recodeSysmisTo
        except ValueError:
            return recodeSysmisTo
        except OverflowError:
            return recodeSysmisTo

    def encodeStringValues(self, record, encoding):
        """ This function encodes string values in a record in the encoding
        of the SPSS data file. """
        encodedRecord = []
        for value in record:
            if isinstance(value, str):
                try:
                    value = value.decode(self.fileEncoding, "replace").encode(encoding)
                except UnicodeEncodeError:
                    value = value.decode(self.fileEncoding, "replace").encode("UTF-8")
            encodedRecord.append(value)
        return encodedRecord

    def formatRecord(self, record, recodeSysmisTo):
        """ This function formats the values in a record according to the
        formats given in the SPSS file dictionary."""
        formattedRecord = []
        for rawValue, varName in zip(record, self.varNames):
            value = recodeSysmisTo if rawValue <= self.CUT_OFF else rawValue
            if self.printTypeLabels[varName] != 'SPSS_FMT_F':
                value = self.formatValue(self.fh, self.spssio, varName, rawValue,
                                         self.printTypeLabels[varName],
                                         self.varWids[varName], recodeSysmisTo)
            formattedRecord.append(value)
        return formattedRecord
    
    def getFileEncoding(self, fh):
        """This function obtains the encoding applicable to a file.
        The encoding is returned as an IANA encoding name, such as
        ISO-8859-1. """
        self.pszEncoding = ctypes.create_string_buffer(20) # is 20 enough??
        self.pszEncodingPtr = ctypes.byref(self.pszEncoding)
        retcode = self.spssio.spssGetFileEncoding(self.fh, self.pszEncodingPtr)
        return retcode, self.pszEncoding.value

    def getFileCodePage(self, fh):
        """This function provides the Windows code page
        number of the encoding applicable to a file.""" 
        self.nCodePage = ctypes.c_int()
        self.nCodePagePtr = ctypes.byref(self.nCodePage)
        retcode = self.spssio.spssGetFileCodePage(self.fh, self.nCodePagePtr)
        return retcode, self.nCodePage.value

    def setInterfaceEncoding(self, spssio, interfaceEncoding):
        """This function sets the current interface encoding."""
        self.icodes = {"UTF-8": 0, "CODEPAGE": 1}
        interfaceEncoding = interfaceEncoding.upper()
        if interfaceEncoding not in self.icodes.keys():
            msg = "Invalid interface encoding ('%s'), valid values are 'UTF-8' or 'CODEPAGE'" % \
                  interfaceEncoding
            raise Exception, msg
        retcode = spssio.spssSetInterfaceEncoding(ctypes.c_int(self.icodes[interfaceEncoding]))
        return retcode
    
    def getInterfaceEncoding(self, spssio):
        """This function returns the current interface encoding.
        ('UTF-8' or 'CODEPAGE') and the specific current codepage (e.g. cp1252)"""
        swapped = dict(zip(self.icodes.values(), self.icodes.keys()))
        interfaceEncoding = swapped[spssio.spssGetInterfaceEncoding()]
        encoding = locale.getpreferredencoding()if interfaceEncoding == "CODEPAGE" else "UTF-8"
        return interfaceEncoding, encoding

    def getFileReport(self, savFileName, varNames, varTypes, fmts, printDecs,
                      printWids, nCases):
        """ This function prints a report about basic file characteristics """
        bytes = os.path.getsize(savFileName)
        kb = float(bytes) / 2**10
        mb = float(bytes) / 2**20
        (fileSize, label) = (mb, "MB") if mb > 1 else (kb, "kB")
        line1 = [os.linesep + "*" * 70]
        line2 = ["*File '%s' (%5.2f %s) has %s columns (variables) and %s rows (%s values)" % \
              (savFileName, fileSize, label, len(varNames), nCases, len(varNames) * nCases)]
        line3 = ["*The file encoding is: %s (Code Page: %s)" % (self.fileEncoding, self.fileCodePage)]
        loc, cp = locale.getlocale()
        line4 = ["*Your computer's locale is: %s (Code page: %s)" % (loc, cp)]
        line5 = ["*The file contains the following variables:"]
        lines = []
        for cnt, varName in enumerate(varNames):
            label = "string" if varTypes[varName] > 0 else "numerical"
            lines.append("%03d. %s (%s%d.%d - %s)" % (cnt+1, varName, fmts[varName], \
                                                      printWids[varName], printDecs[varName], label))
        lineN = ["*" * 70]
        report = os.linesep.join(line1 + line2 + line3 + line4 + line5 + lines + lineN)
        return report

    def conversionFormatCtoPy(self, varNames, varTypes):
        """ This function generates a struct format string for the conversion
        between C and Python values. SPSS data files are assumed to have either
        8-byte doubles/floats or n-byte chars[]/strings, where n is always
        8 bytes or a multiple thereof."""
        structFmt = ""
        if sys.byteorder == "little":
            endianness = "<"
        elif sys.byteorder == "big":
            endianness = ">"
        else:
            endianness = "@"
        structFmt += endianness
        for v in varNames:
            if varTypes[v] == 0:
                structFmt += "d"
            else:
                fmt = str(int(math.ceil(varTypes[v] / 8.0) * 8))
                structFmt += fmt + "s"
        return structFmt

    def getCaseBuffer(self):
        """ This function returns a buffer and a pointer to that buffer. A whole
        case will be read into this buffer."""
        self.caseSize = ctypes.c_long()
        self.caseSizePtr = ctypes.byref(self.caseSize)
        self.retcode = self.spssio.spssGetCaseSize(self.fh, self.caseSizePtr)
        self.caseBuffer = ctypes.create_string_buffer(self.caseSize.value)
        self.caseBufferPtr = ctypes.byref(self.caseBuffer)
        return self.caseBuffer, self.caseBufferPtr

    def getHeader(self, selectVars):
        if selectVars is None:
            header = self.varNames
        elif isinstance(selectVars, (list, tuple)):
            diff = set(selectVars).difference(set(self.varNames))
            if diff:
                msg = "Variable names misspecified ('%s')" % ", ".join(diff)
                raise Exception, msg
            varPos = [self.varNames.index(v) for v in self.varNames if v in selectVars]
            self.selector = operator.itemgetter(*varPos)
            header = self.selector(self.varNames)
            header = [header] if not isinstance(header, tuple) else header
        else:
            raise Exception, "Variable names list misspecified. " + \
                  "Must be 'None' or a list or tuple of existing variables"    
        return header

    def readSavFile(self, returnHeader, recodeSysmisTo, selectVars, rawMode, encoding):
        """ This is the main function of this class. It is a generator, which
        returns one record of the spss data file at a time. """
        
        debug = False
        if retcodes[self.retcode] == "SPSS_OK":
            if returnHeader:
               yield self.header

            # avoiding dots inside the loops
            # http://wiki.python.org/moin/PythonSpeed/PerformanceTips#Avoiding_dots...
            containsStringvars = max([varType for varName, varType in self.varTypes.items()
                                      if varName in self.header]) > 0
            self.caseBuffer, self.caseBufferPtr = self.getCaseBuffer()
            structFmt = self.conversionFormatCtoPy(self.varNames, self.varTypes)
            unpack = struct.unpack
            wholeCaseIn = self.spssio.spssWholeCaseIn
            print "Pct progress ...",
            for case in range(self.nCases_):
                retcode = wholeCaseIn(self.fh, self.caseBufferPtr)
                if retcodes[retcode] != 'SPSS_OK':
                    print "WARNING: Record %s is faulty" % case+1
                    continue
                record = unpack(structFmt, self.caseBuffer.raw)
                if selectVars is not None:
                    record = self.selector(record)
                    record = [record] if not isinstance(record, tuple) else record
                if containsStringvars:
                    record = self.encodeStringValues(record, encoding)
                if not rawMode:
                    record = self.formatRecord(record, self.recodeSysmisTo)
                if debug and (case+1) % 10 == 0:        
                    print "record", case+1, record
                pctProgress = (float(case) / self.nCases_) * 100
                if pctProgress % 5 == 0:
                    print "%2.1f%%... " % pctProgress,
                yield record
        else: 
            try:
                print "Error", retcodes[retcode]
            except KeyError:
                print "Unknown error code (%d)" % retcode
            finally:
                raise Exception, "You fail!"

def calculateFrequency(sav):
    """ This function returns a frequency count for each variable in
    the spss data file """
    freqs = {}
    for lino, line in enumerate(sav):
        if lino == 0:
            varNames = line
        else:
            for varName in varNames:
                value = line[varNames.index(varName)]
                value = "(missing)" if value == "" else value
                try:
                    freqs[varName]
                except KeyError:
                    freqs[varName] = {}
                try:
                    freqs[varName][value] += 1
                except KeyError:
                    freqs[varName][value] = 1
    return freqs

if __name__ == "__main__":

    help(SavReader)

    import contextlib, csv

    ## ----- Get some basic file info
    savFileName = r"C:\Program Files\IBM\SPSS\Statistics\19\Samples\English\Employee data.sav"
    numVars, nCases, varNames, varTypes, printTypesFile, printTypeLabels, varWids = \
             SavReader(savFileName).getSavFileInfo()


    ## ----- Typical use    
    with SavReader(savFileName, selectVars=['id'], recodeSysmisTo=999) as sav:
        header = sav.next()
        for line in sav:
            pass # do stuff

    ## ----- Convert file to .csv
    with contextlib.nested(SavReader(savFileName, selectVars=None, verbose=True,
                                     rawMode=False, interfaceEncoding="UTF-8"),
                           open(csvFileName, "wb")) as (sav, f):
        writer = csv.writer(f)
        for line in sav:
            writer.writerow(line)
        print "Done! Csv file written: %s" % f.name

    ## ----- Run frequency counts
    def main(savFileName=savFileName):
        with SavReader(savFileName) as sav:
            freqs = calculateFrequency(sav)
        for var, values in freqs.iteritems():
            print "\n\n", 10 * "*", var.upper(), 10 * "*"
            for val, freq in values.iteritems():
                print val, "--", freq
    #main(savFileName)
