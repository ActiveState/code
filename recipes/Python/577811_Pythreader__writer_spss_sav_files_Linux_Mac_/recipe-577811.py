#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SavReaderWriter.py: A cross-platform Python interface to the IBM SPSS
Statistics Input Output Module. Read or Write SPSS system files (.sav, .zsav)
"""

# libspssdio.so.1, libspssdio.dylib, spssio32.dll + associated libaries and
# documentation can be downloaded here:
# https://www.ibm.com/developerworks/mydeveloperworks/wikis/home/wiki/We70df3195ec8_4f95_9773_42e448fa9029/page/Downloads%20for%20IBM%C2%AE%20SPSS%C2%AE%20Statistics?lang=en
# ANY FEEDBACK ON THIS CODE IS WELCOME: "@".join(["fomcl", "yahoo.com"])
# Mac support added Oct-22-2011: by Rich Sadowsky
# "@".join(["rich", "richsad.com"])


## January 2013:
# changed implementation of freeMemory method (again!)

## December 2012:
# -Added support for slicing, indexing, array slicing + other special methods
# -Added support for writing spss date fields
# -Added support for almost all meta data (missing values, sets, roles, etc.)
# -Added support for 64 bit Windows (tested with Win7) and other OSs
#   (z/Linux, Solaris, HP Linux, IBM AIX (untested though)
# -Added support for reading and writing zlib compressed (.zsav) files
# -Removed pesky segfault error when freeing memory
# -Removed errors related to encoding
# -Removed error that prevented files originating from big-endian systems
#   being read properly in little-endian systems (and vice versa)
# -Changed some Reader defaults (verbose=False, returnHeader=False)
# -Renamed SavDataDictionaryReader into SavHeaderReader
##


__author__ = "Albert-Jan Roskam" + " " + "@".join(["fomcl", "yahoo.com"])
__version__ = "3.1.1"

# change this to 'True' in case you experience segmentation
# faults related to freeing memory.
segfaults = False

from ctypes import *
import ctypes.util
import struct
import sys
import platform
import os
import re
import operator
import math
import locale
import datetime
import time
import getpass
import encodings
import functools
import gc
try:
    import psyco
    psycoOk = True  # reading 66 % faster
except ImportError:
    print ("NOTE. Psyco module not found. Install this module " +
           "to increase reader performance")
    psycoOk = False
try:
    import numpy
    numpyOk = True
except ImportError:
    print ("NOTE. Numpy module not found. Install this module " +
           "to use array slicing")
    numpyOk = False
try:
    from cWriterow import cWriterow  # writing 66 % faster
    cWriterowOK = True
except ImportError:
    print ("NOTE. cWriterow module not found. Install this module " +
            "to increase writer performance")
    cWriterowOK = False

retcodes = {
    0: "SPSS_OK",
    1: "SPSS_FILE_OERROR",
    2: "SPSS_FILE_WERROR",
    3: "SPSS_FILE_RERROR",
    4: "SPSS_FITAB_FULL",
    5: "SPSS_INVALID_HANDLE",
    6: "SPSS_INVALID_FILE",
    7: "SPSS_NO_MEMORY",
    8: "SPSS_OPEN_RDMODE",
    9: "SPSS_OPEN_WRMODE",
    10: "SPSS_INVALID_VARNAME",
    11: "SPSS_DICT_EMPTY",
    12: "SPSS_VAR_NOTFOUND",
    13: "SPSS_DUP_VAR",
    14: "SPSS_NUME_EXP",
    15: "SPSS_STR_EXP",
    16: "SPSS_SHORTSTR_EXP",
    17: "SPSS_INVALID_VARTYPE",
    18: "SPSS_INVALID_MISSFOR",
    19: "SPSS_INVALID_COMPSW",
    20: "SPSS_INVALID_PRFOR",
    21: "SPSS_INVALID_WRFOR",
    22: "SPSS_INVALID_DATE",
    23: "SPSS_INVALID_TIME",
    24: "SPSS_NO_VARIABLES",
    27: "SPSS_DUP_VALUE",
    28: "SPSS_INVALID_CASEWGT",
    30: "SPSS_DICT_COMMIT",
    31: "SPSS_DICT_NOTCOMMIT",
    33: "SPSS_NO_TYPE2",
    41: "SPSS_NO_TYPE73",
    45: "SPSS_INVALID_DATEINFO",
    46: "SPSS_NO_TYPE999",
    47: "SPSS_EXC_STRVALUE",
    48: "SPSS_CANNOT_FREE",
    49: "SPSS_BUFFER_SHORT",
    50: "SPSS_INVALID_CASE",
    51: "SPSS_INTERNAL_VLABS",
    52: "SPSS_INCOMPAT_APPEND",
    53: "SPSS_INTERNAL_D_A",
    54: "SPSS_FILE_BADTEMP",
    55: "SPSS_DEW_NOFIRST",
    56: "SPSS_INVALID_MEASURELEVEL",
    57: "SPSS_INVALID_7SUBTYPE",
    58: "SPSS_INVALID_VARHANDLE",
    59: "SPSS_INVALID_ENCODING",
    60: "SPSS_FILES_OPEN",
    70: "SPSS_INVALID_MRSETDEF",
    71: "SPSS_INVALID_MRSETNAME",
    72: "SPSS_DUP_MRSETNAME",
    73: "SPSS_BAD_EXTENSION",
    74: "SPSS_INVALID_EXTENDEDSTRING",
    75: "SPSS_INVALID_ATTRNAME",
    76: "SPSS_INVALID_ATTRDEF",
    77: "SPSS_INVALID_MRSETINDEX",
    78: "SPSS_INVALID_VARSETDEF",
    79: "SPSS_INVALID_ROLE",

    -15: "SPSS_EMPTY_DEW",
    -14: "SPSS_NO_DEW",
    -13: "SPSS_EMPTY_MULTRESP",
    -12: "SPSS_NO_MULTRESP",
    -11: "SPSS_NO_DATEINFO",
    -10: "SPSS_NO_CASEWGT",
    -9: "SPSS_NO_LABEL",
    -8: "SPSS_NO_LABELS",
    -7: "SPSS_EMPTY_VARSETS",
    -6: "SPSS_NO_VARSETS",
    -5: "SPSS_FILE_END",
    -4: "SPSS_EXC_VALLABEL",
    -3: "SPSS_EXC_LEN120",
    -2: "SPSS_EXC_VARLABEL",
    -1: "SPSS_EXC_LEN64"}

allFormats = {
    1: ("SPSS_FMT_A", "Alphanumeric"),
    2: ("SPSS_FMT_AHEX", "Alphanumeric hexadecimal"),
    3: ("SPSS_FMT_COMMA", "F Format with commas"),
    4: ("SPSS_FMT_DOLLAR", "Commas and floating dollar sign"),
    5: ("SPSS_FMT_F", "Default Numeric Format"),
    6: ("SPSS_FMT_IB", "Integer binary"),
    7: ("SPSS_FMT_PIBHEX", "Positive integer binary - hex"),
    8: ("SPSS_FMT_P", "Packed decimal"),
    9: ("SPSS_FMT_PIB", "Positive integer binary unsigned"),
    10: ("SPSS_FMT_PK", "Positive integer binary unsigned"),
    11: ("SPSS_FMT_RB", "Floating point binary"),
    12: ("SPSS_FMT_RBHEX", "Floating point binary hex"),
    15: ("SPSS_FMT_Z", "Zoned decimal"),
    16: ("SPSS_FMT_N", "N Format- unsigned with leading 0s"),
    17: ("SPSS_FMT_E", "E Format- with explicit power of 10"),
    20: ("SPSS_FMT_DATE", "Date format dd-mmm-yyyy"),
    21: ("SPSS_FMT_TIME", "Time format hh:mm:ss.s"),
    22: ("SPSS_FMT_DATE_TIME", "Date and Time"),
    23: ("SPSS_FMT_ADATE", "Date format dd-mmm-yyyy"),
    24: ("SPSS_FMT_JDATE", "Julian date - yyyyddd"),
    25: ("SPSS_FMT_DTIME", "Date-time dd hh:mm:ss.s"),
    26: ("SPSS_FMT_WKDAY", "Day of the week"),
    27: ("SPSS_FMT_MONTH", "Month"),
    28: ("SPSS_FMT_MOYR", "mmm yyyy"),
    29: ("SPSS_FMT_QYR", "q Q yyyy"),
    30: ("SPSS_FMT_WKYR", "ww WK yyyy"),
    31: ("SPSS_FMT_PCT", "Percent - F followed by %"),
    32: ("SPSS_FMT_DOT", "Like COMMA, switching dot for comma"),
    33: ("SPSS_FMT_CCA", "User Programmable currency format"),
    34: ("SPSS_FMT_CCB", "User Programmable currency format"),
    35: ("SPSS_FMT_CCC", "User Programmable currency format"),
    36: ("SPSS_FMT_CCD", "User Programmable currency format"),
    37: ("SPSS_FMT_CCE", "User Programmable currency format"),
    38: ("SPSS_FMT_EDATE", "Date in dd/mm/yyyy style"),
    39: ("SPSS_FMT_SDATE", "Date in yyyy/mm/dd style")}

MAXLENGTHS = {
    "SPSS_MAX_VARNAME": (64, "Variable name"),
    "SPSS_MAX_SHORTVARNAME": (8, "Short (compatibility) variable name"),
    "SPSS_MAX_SHORTSTRING": (8, "Short string variable"),
    "SPSS_MAX_IDSTRING": (64, "File label string"),
    "SPSS_MAX_LONGSTRING": (32767, "Long string variable"),
    "SPSS_MAX_VALLABEL": (120, "Value label"),
    "SPSS_MAX_VARLABEL": (256, "Variable label"),
    "SPSS_MAX_7SUBTYPE": (40, "Maximum record 7 subtype"),
    "SPSS_MAX_ENCODING": (64, "Maximum encoding text")}

supportedDates = {  # uses ISO dates wherever applicable.
    "DATE": "%Y-%m-%d",
    "JDATE": "%Y-%m-%d",
    "EDATE": "%Y-%m-%d",
    "SDATE": "%Y-%m-%d",
    "DATETIME": "%Y-%m-%d %H:%M:%S",
    "WKDAY": "%A %H:%M:%S",
    "ADATE": "%Y-%m-%d",
    "WKDAY": "%A",
    "MONTH": "%B",
    "MOYR": "%B %Y",
    "WKYR": "%W WK %Y"}

userMissingValues = {
    "SPSS_NO_MISSVAL": 0,
    "SPSS_ONE_MISSVAL": 1,
    "SPSS_TWO_MISSVAL": 2,
    "SPSS_THREE_MISSVAL": 3,
    "SPSS_MISS_RANGE": -2,
    "SPSS_MISS_RANGEANDVAL": -3}


class SPSSIOError(Exception):
    """
    Error class for the IBM SPSS Statistics Input Output Module
    """

    def __init__(self, msg=u"Unknown", retcode=None):
        if isinstance(retcode, int):
            code = retcodes.get(retcode, retcode)
        elif isinstance(retcode, list):
            code = ", ".join([retcodes.get(retcodex) for retcodex in retcode])
        else:
            code = "unknown code %r" % retcode
        msg = "%s [retcode: %r]" % (msg, code)
        Exception.__init__(self, msg)


class Generic(object):
    """
    Class for methods and data used in reading as well as writing
    IBM SPSS Statistics data files
    """

    def __init__(self, savFileName, ioUtf8=False, ioLocale=None):
        """Constructor. Note that interface locale and encoding can only
        be set once"""
        locale.setlocale(locale.LC_ALL, "")
        self.savFileName = savFileName
        self.libc = cdll.LoadLibrary(ctypes.util.find_library("c"))
        self.spssio = self.loadLibrary()

        self.wholeCaseIn = self.spssio.spssWholeCaseIn
        self.wholeCaseOut = self.spssio.spssWholeCaseOut

        self.encoding_and_locale_set = False
        if not self.encoding_and_locale_set:
            self.encoding_and_locale_set = True
            self.ioLocale = ioLocale
            self.ioUtf8 = ioUtf8

    def _encodeFileName(self, fn):
        """Helper function to encode unicode file names into bytestring file
        names encoded in the file system's encoding. Needed for C functions
        that have a c_char_p filename argument.
        http://effbot.org/pyref/sys.getfilesystemencoding.htm
        http://docs.python.org/2/howto/unicode.html under 'unicode filenames'"""
        if not isinstance(fn, unicode):
            return fn
        elif sys.platform.startswith("win"):
            return self.wide2utf8(fn)
        else:
            encoding = sys.getfilesystemencoding()
            encoding = "utf-8" if not encoding else encoding  # actually, ascii
        try:
            return fn.encode(encoding)
        except UnicodeEncodeError, e:
            msg = ("File system encoding %r can not be used to " +
                   "encode file name %r [%s]")
            raise ValueError(msg % (encoding, fn, e))

    def loadLibrary(self):
        """This function loads and returns the SPSSIO libraries,
        depending on the platform."""
        path = os.path.abspath(".")
        is_32bit = platform.architecture()[0] == "32bit"
        pf = sys.platform.lower()
        load = WinDLL if pf.startswith("win") else CDLL
        if pf.startswith("win"):
            os.environ["PATH"] += ";" + path
            spssio = load("spssio32") if is_32bit else load("spssio64")
        elif pf.startswith("lin"):  # most linux flavours, incl zLinux
            spssio = load("libspssdio.so.1")
        elif pf.startswith("darwin") or pf.startswith("mac"):
            spssio = load("libspssdio.dylib")
        elif pf.startswith("aix") and not is_32bit:
            spssio = load("libspssdio.so.1")
        elif pf.startswith("hp-ux"):
            spssio = load("libspssdio.sl.1")
        elif pf.startswith("sunos") and not is_32bit:
            spssio = load("libspssdio.so.1")
        else:
            msg = "Your platform (%r) is not supported" % pf
            raise NotImplementedError(msg)
        return spssio

    def errcheck(self, res, func, args):
        """This function checks for errors during the execution of
        function <func>"""
        if not res:
            msg = "Error performing %r operation on file %r."
            raise IOError(msg % (func.__name__, self.savFileName))
        return res

    def wide2utf8(self, fn):
        """Take a unicode file name string and encode it to a multibyte string
        that Windows can use to represent file names (CP65001, UTF-8)
        http://msdn.microsoft.com/en-us/library/windows/desktop/dd374130"""

        from ctypes import wintypes

        _CP_UTF8 = 65001
        _CP_ACP = 0  # ANSI
        _LPBOOL = POINTER(c_long)

        _wideCharToMultiByte = windll.kernel32.WideCharToMultiByte
        _wideCharToMultiByte.restype = c_int
        _wideCharToMultiByte.argtypes = [wintypes.UINT, wintypes.DWORD,
            wintypes.LPCWSTR, c_int, wintypes.LPSTR, c_int, wintypes.LPCSTR, _LPBOOL]

        codePage = _CP_UTF8
        dwFlags = 0
        lpWideCharStr = fn
        cchWideChar = len(fn)
        lpMultiByteStr = None
        cbMultiByte = 0  # zero requests size
        lpDefaultChar = None
        lpUsedDefaultChar = None

        # get size
        mbcssize = _wideCharToMultiByte(
        codePage, dwFlags, lpWideCharStr, cchWideChar, lpMultiByteStr,
        cbMultiByte, lpDefaultChar, lpUsedDefaultChar)
        if mbcssize <= 0:
            raise WinError(mbcssize)
        lpMultiByteStr = create_string_buffer(mbcssize)

        # convert
        retcode = _wideCharToMultiByte(
        codePage, dwFlags, lpWideCharStr, cchWideChar, lpMultiByteStr,
        mbcssize, lpDefaultChar, lpUsedDefaultChar)
        if retcode <= 0:
            raise WinError(retcode)
        return lpMultiByteStr.value

    def openSavFile(self, savFileName, mode="rb", refSavFileName=None):
        """This function opens IBM SPSS Statistics data files in mode <mode>
        and returns a handle that  should be used for subsequent operations on
        the file. If <savFileName> is opened in mode "cp", meta data
        information aka the spss dictionary is copied from <refSavFileName>"""
        savFileName = os.path.abspath(savFileName)  # fdopen wants full name
        try:
            fdopen = self.libc._fdopen  # Windows
        except AttributeError:
            fdopen = self.libc.fdopen   # Linux and others
        fdopen.argtypes = [c_int, c_char_p]
        fdopen.restype = c_void_p
        fdopen.errcheck = self.errcheck
        with open(savFileName, mode) as f:
            self.fd = fdopen(f.fileno(), mode)
        if mode == "rb":
            spssOpen = self.spssio.spssOpenRead
        elif mode == "wb":
            spssOpen = self.spssio.spssOpenWrite
        elif mode == "cp":
            spssOpen = self.spssio.spssOpenWriteCopy
        elif mode == "ab":
            spssOpen = self.spssio.spssOpenAppend

        savFileName = self._encodeFileName(savFileName)
        refSavFileName = self._encodeFileName(refSavFileName)
        sav = c_char_p(savFileName)
        fh = c_int(self.fd)
        if mode == "cp":
            retcode = spssOpen(sav, c_char_p(refSavFileName), pointer(fh))
        else:
            retcode = spssOpen(sav, pointer(fh))

        if retcode > 0:
            msg = "Error opening file %r in mode %r"
            raise SPSSIOError(msg % (savFileName, mode), retcode)
        return fh.value

    def closeSavFile(self, fh, mode="rb"):
        """This function closes the sav file associated with <fh> that was open
        in mode <mode>."""
        if mode == "rb":
            spssClose = self.spssio.spssCloseRead
        elif mode == "wb":
            spssClose = self.spssio.spssCloseWrite
        elif mode == "ab":
            spssClose = self.spssio.spssCloseAppend
        retcode = spssClose(c_int(fh))
        if retcode > 0:
            raise SPSSIOError("Error closing file in mode %r" % mode, retcode)

    @property
    def releaseInfo(self):
        """This function reports release- and machine-specific information
        about the open file."""
        relInfo = ["release number", "release subnumber", "fixpack number",
                   "machine code", "floating-point representation code",
                   "compression scheme code", "big/little-endian code",
                   "character representation code"]
        relInfoArr = (c_int * len(relInfo))()
        retcode = self.spssio.spssGetReleaseInfo(c_int(self.fh), relInfoArr)
        if retcode > 0:
            raise SPSSIOError("Error getting ReleaseInfo", retcode)
        info = dict([(item, relInfoArr[i]) for i, item in enumerate(relInfo)])
        return info

    @property
    def spssVersion(self):
        """Return the SPSS version that was used to create the opened file
        as a three-tuple indicating major, minor, and fixpack version as
        ints. NB: in the transition from SPSS to IBM, a new four-digit
        versioning nomenclature is used. This function returns the old
        three-digit nomenclature. Therefore, no patch version information
        is available."""
        info = self.releaseInfo
        major = info["release number"]
        minor = info["release subnumber"]
        fixpack = info["fixpack number"]
        return major, minor, fixpack

    @property
    def fileCompression(self):
        """Get/Set the file compression.
        Returns/Takes a compression switch which may be any of the following:
        'uncompressed', 'standard', or 'zlib'. Zlib comression requires SPSS
        v21 I/O files."""
        compression = {0: "uncompressed", 1: "standard", 2: "zlib"}
        compSwitch = c_int()
        func = self.spssio.spssGetCompression
        retcode = func(c_int(self.fh), byref(compSwitch))
        if retcode > 0:
            raise SPSSIOError("Error getting file compression", retcode)
        return compression.get(compSwitch.value)

    @fileCompression.setter
    def fileCompression(self, compSwitch):
        compression = {"uncompressed": 0, "standard": 1, "zlib": 2}
        compSwitch = compression.get(compSwitch)
        func = self.spssio.spssSetCompression
        retcode = func(c_int(self.fh), c_int(compSwitch))
        invalidSwitch = retcodes.get(retcode) == 'SPSS_INVALID_COMPSW'
        if invalidSwitch and self.spssVersion[0] < 21:
            msg = "Writing zcompressed files requires >=v21 SPSS I/O libraries"
            raise ValueError(msg)
        elif retcode > 0:
            raise SPSSIOError("Error setting file compression", retcode)

    @property
    def systemString(self):
        """This function returns the name of the system under which the file
        was created aa a string."""
        sysName = create_string_buffer(42)
        func = self.spssio.spssGetSystemString
        retcode = func(c_int(self.fh), byref(sysName))
        if retcode > 0:
            raise SPSSIOError("Error getting SystemString", retcode)
        return sysName.value

    def getStruct(self, varTypes, varNames, mode="rb"):
        """This function returns a compiled struct object. The required
        struct format string for the conversion between C and Python
        is created on the basis of varType and byte order.
        --varTypes: SPSS data files have either 8-byte doubles/floats or n-byte
          chars[]/ strings, where n is always 8 bytes or a multiple thereof.
        --byte order: files are written in the byte order of the host system
          (mode="wb") and read/appended using the byte order information
          contained in the SPSS data file (mode is "ab" or "rb" or "cp")"""
        if mode in ("ab", "rb", "cp"):     # derive endianness from file
            endianness = self.releaseInfo["big/little-endian code"]
            endianness = ">" if endianness > 0 else "<"
        elif mode == "wb":                 # derive endianness from host
            if sys.byteorder == "little":
                endianness = "<"
            elif sys.byteorder == "big":
                endianness = ">"
            else:
                endianness = "@"
        structFmt = [endianness]
        ceil = math.ceil
        for varName in varNames:
            varType = varTypes[varName]
            if varType == 0:
                structFmt.append("d")
            else:
                fmt = str(int(ceil(int(varType) / 8.0) * 8))
                structFmt.append(fmt + "s")
        return struct.Struct("".join(structFmt))

    def getCaseBuffer(self):
        """This function returns a buffer and a pointer to that buffer. A whole
        case will be read into this buffer."""
        caseSize = c_long()
        retcode = self.spssio.spssGetCaseSize(c_int(self.fh), byref(caseSize))
        caseBuffer = create_string_buffer(caseSize.value)
        if retcode > 0:
            raise SPSSIOError("Problem getting case buffer", retcode)
        return caseBuffer

    @property
    def sysmis(self):
        """This function returns the IBM SPSS Statistics system-missing
        value ($SYSMIS) for the host system (also called 'NA' in other
        systems)."""
        try:
            sysmis = -1 * sys.float_info[0]  # Python 2.6 and higher.
        except AttributeError:
            self.spssio.spssSysmisVal.restype = c_float
            sysmis = self.spssio.spssSysmisVal()
        return sysmis

    @property
    def missingValuesLowHigh(self):
        """This function returns the 'lowest' and 'highest' values used for
        numeric missing value ranges on the host system. This can be used in
        a similar way as the LO and HI keywords in missing values
        specifications (cf. MISSING VALUES foo (LO THRU 0). It may be called
        at any time."""
        lowest, highest = c_double(), c_double()
        func = self.spssio.spssLowHighVal
        retcode = func(byref(lowest), byref(highest))
        return lowest.value, highest.value

    @property
    def ioLocale(self):
        """This function gets/sets the I/O Module's locale.
        This corresponds with the SPSS command SET LOCALE. The I/O Module's
        locale is separate from that of the client application. The
        <localeName> parameter and the return value are identical to those
        for the C run-time function setlocale. The exact locale name
        specification depends on the OS of the host sytem, but has the
        following form:
                   <lang>_<territory>.<codeset>[@<modifiers>]
        The 'codeset' and 'modifier' components are optional and in Windows,
        aliases (e.g. 'english') may be used. When the I/O Module is first
        loaded, its locale is set to the system default. See also:
        --https://wiki.archlinux.org/index.php/Locale
        --http://msdn.microsoft.com/en-us/library/39cwe7zf(v=vs.80).aspx"""
        if hasattr(self, "setLocale"):
            return self.setLocale
        else:
            currLocale = ".".join(locale.getlocale())
            print "NOTE. Locale not set; getting current locale: ", currLocale
            return currLocale

    @ioLocale.setter
    def ioLocale(self, localeName=""):
        if not localeName:
            localeName = ".".join(locale.getlocale())
        func = self.spssio.spssSetLocale
        func.restype = c_char_p
        self.setLocale = func(c_int(locale.LC_ALL), c_char_p(localeName))
        if self.setLocale is None:
            raise ValueError("Invalid ioLocale: %r" % localeName)
        return self.setLocale

    @property
    def fileCodePage(self):
        """This function provides the Windows code page number of the encoding
        applicable to a file."""
        nCodePage = c_int()
        func = self.spssio.spssGetFileCodePage
        retcode = func(c_int(self.fh), byref(nCodePage))
        return nCodePage.value

    def isCompatibleEncoding(self):
        """This function determines whether the file and interface encoding
        are compatible."""
        try:
            # Windows, note typo 'Endoding'!
            func = self.spssio.spssIsCompatibleEndoding
        except AttributeError:
            func = self.spssio.spssIsCompatibleEncoding
        func.restype = c_bool
        isCompatible = c_int()
        retcode = func(c_int(self.fh), byref(isCompatible))
        if retcode > 0:
            msg = "Error testing encoding compatibility: %r"
            raise SPSSIOError(msg % isCompatible.value, retcode)
        if not isCompatible.value and not self.ioUtf8:
            msg = ("NOTE. SPSS Statistics data file %r is written in a " +
                   "character encoding (%s) incompatible with the current " +
                   "ioLocale setting. It may not be readable. Consider " +
                   "changing ioLocale or setting ioUtf8=True.")
            print msg % (self.savFileName, self.fileEncoding)
        return bool(isCompatible.value)

    @property
    def ioUtf8(self):
        """This function returns/sets the current interface encoding.
        ioUtf8 = False --> CODEPAGE mode,
        ioUtf8 = True --> UTF-8 mode, aka. Unicode mode
        This corresponds with the SPSS command SHOW UNICODE (getter)
        and SET UNICODE=ON/OFF (setter)."""
        if hasattr(self, "ioUtf8_"):
            return self.ioUtf8_
        self.ioUtf8_ = self.spssio.spssGetInterfaceEncoding()
        return bool(self.ioUtf8_)

    @ioUtf8.setter
    def ioUtf8(self, ioUtf8):
        try:
            retcode = self.spssio.spssSetInterfaceEncoding(c_int(int(ioUtf8)))
            if retcode > 0 and not self.encoding_and_locale_set:
                # not self.encoding_and_locale_set --> nested context managers
                raise SPSSIOError("Error setting IO interface", retcode)
        except TypeError:
            msg = "Invalid interface encoding: %r (must be bool)"
            raise SPSSIOError(msg % ioUtf8)

    @property
    def fileEncoding(self):
        """This function obtains the encoding applicable to a file.
        The encoding is returned as an IANA encoding name, such as
        ISO-8859-1, which is then converted to the corresponding Python
        codec name. If the file contains no file encoding, the locale's
        preferred encoding is returned"""
        preferredEncoding = locale.getpreferredencoding()
        try:
            pszEncoding = create_string_buffer(20)  # is 20 enough??
            func = self.spssio.spssGetFileEncoding
            retcode = func(c_int(self.fh), byref(pszEncoding))
            if retcode > 0:
                raise SPSSIOError("Error getting file encoding", retcode)
            iana_codes = encodings.aliases.aliases
            rawEncoding = pszEncoding.value.lower()
            if rawEncoding.replace("-", "") in iana_codes:
                iana_code = rawEncoding.replace("-", "")
            else:
                iana_code = rawEncoding.replace("-", "_")
            fileEncoding = iana_codes[iana_code]
            return fileEncoding
        except AttributeError:
            print ("NOTE. Function 'getFileEncoding' not found. You are " +
                   "using a .dll from SPSS < v16.")
            return preferredEncoding
        except KeyError:
            print ("NOTE. IANA coding lookup error. Code %r " % iana_code +
                   "does not map to any Python codec.")
            return preferredEncoding

    @property
    def record(self):
        """Get/Set a whole record from/to a pre-allocated buffer"""
        retcode = self.wholeCaseIn(c_int(self.fh),
                                   byref(self.caseBuffer))
        if retcode > 0:
            raise SPSSIOError("Problem reading row", retcode)
        record = list(self.unpack_from(self.caseBuffer))
        return record

    @record.setter
    def record(self, record):
        try:
            self.pack_into(self.caseBuffer, 0, *record)
        except struct.error, e:
            msg = "Use ioUtf8=True to write unicode strings [%s]" % e
            raise TypeError(msg)
        retcode = self.wholeCaseOut(c_int(self.fh),
                                    c_char_p(self.caseBuffer.raw))
        if retcode > 0:
            raise SPSSIOError("Problem writing row:\n" + \
                              unicode(record, "utf-8"), retcode)

    def printPctProgress(self, nominator, denominator):
        """This function prints the % progress when reading and writing
        files"""
        if nominator and nominator % 10**4 == 0:
            pctProgress = (float(nominator) / denominator) * 100
            print "%2.1f%%... " % pctProgress,


class Header(Generic):

    """
    This class contains methods responsible for getting and setting meta data
    that is embedded in the IBM SPSS Statistics data file. In SPSS speak, this
    header information is known as the SPSS Data Dictionary (which has diddly
    squat to do with a Python dictionary!).
    """

    def __init__(self, savFileName, mode, refSavFileName, ioUtf8, ioLocale=None):
        """Constructor"""
        super(Header, self).__init__(savFileName, ioUtf8, ioLocale)
        self.spssio = self.loadLibrary()
        self.libc = cdll.LoadLibrary(ctypes.util.find_library("c"))
        self.fh = super(Header, self).openSavFile(savFileName, mode,
                                                  refSavFileName)
        self.varNames, self.varTypes = self.varNamesTypes
        self.vNames = dict(zip(self.varNames, self.encode(self.varNames)))

    def openSavFile(self):
        """This function returns the file handle that was opened in the
        super class"""
        return self.fh

    def decode(func):
        """Decorator to Utf-8 decode all str items contained in a dictionary
        If ioUtf8=True, the dictionary's keys and values are decoded, but only
        values that are strs, lists, or dicts. For example:
        {'v1': {'y': 'yy', 'z': 666}}-->{u'v1': {u'y': u'yy', u'z': 666}}"""
        uS = lambda x: x.decode("utf-8") if isinstance(x, str) else x
        uL = lambda x: map(uS, x) if isinstance(x, list) else x

        @functools.wraps(func)
        def wrapper(arg):
            result = func(arg)
            if not arg.ioUtf8:
                return result  # unchanged
            if isinstance(result, str):
                return uS(result)
            utf8ifiedDict = {}
            for k, v in result.iteritems():
                k, v = uS(k), uS(v)
                if isinstance(v, list):
                    v = map(uS, v)
                elif isinstance(v, dict):
                    v = dict([(uS(x), uL(uS(y))) for x, y in v.items()])
                utf8ifiedDict[k] = v
            return utf8ifiedDict
        return wrapper

    def encode(self, item):
        """Counter part of decode helper function, does the opposite of that
        function (but is not a decorator)"""
        if not self.ioUtf8:
            return item  # unchanged
        utf8dify = lambda x: x.encode("utf-8") if isinstance(x, unicode) else x
        if isinstance(item, list):
            return map(utf8dify, item)
        elif isinstance(item, dict):
            return dict([(utf8dify(x), utf8dify(y)) for x, y in item.items()])
        return utf8dify(item)

    def freeMemory(self, funcName, *args):
        """Clean up: free memory claimed by e.g. getValueLabels and
        getVarNamesTypes"""
        gc.collect()
        if segfaults:
            return
        print "... freeing" , funcName[8:]
        func = getattr(self.spssio, funcName)
        retcode = func(*args)
        if retcode > 0:
            msg = "Error freeing memory using %s" % funcName
            raise SPSSIOError(msg, retcode)

    @property
    def numberofCases(self):
        """This function reports the number of cases present in a data file.
        Prehistoric files (< SPSS v6.0) don't contain nCases info, therefore
        a guesstimate of the number of cases is given for those files"""
        nCases = c_long()
        func = self.spssio.spssGetNumberofCases
        retcode = func(c_int(self.fh), byref(nCases))
        if nCases.value == -1:
            func = self.spssio.spssGetEstimatedNofCases
            retcode = func(c_int(self.fh), byref(nCases))
        if retcode > 0:
            raise SPSSIOError("Error getting number of cases", retcode)
        return nCases.value

    @property
    def numberofVariables(self):
        """This function returns the number of variables (columns) in the
        spss dataset"""
        numVars = c_int()
        func = self.spssio.spssGetNumberofVariables
        retcode = func(c_int(self.fh), byref(numVars))
        if retcode > 0:
            raise SPSSIOError("Error getting number of variables", retcode)
        return numVars.value

    @property
    def varNamesTypes(self):
        """Get/Set variable names and types.
        --Variable names is a list of the form ['var1', var2', 'etc']
        --Variable types is a dictionary of the form {varName: varType}
        The variable type code is an integer in the range 0-32767, 0
        indicating a numeric variable (F8.2) and a positive value
        indicating a string variable of that size (in bytes)."""
        if hasattr(self, "varNames"):
            return self.varNames, self.varTypes

        # initialize arrays
        numVars = self.numberofVariables
        numVars_ = c_int(numVars)
        varNamesArr = (POINTER(c_char_p * numVars))()
        varTypesArr = (POINTER(c_int * numVars))()

        # get variable names
        func = self.spssio.spssGetVarNames
        retcode = func(c_int(self.fh), byref(numVars_),
                       byref(varNamesArr), byref(varTypesArr))
        if retcode > 0:
            raise SPSSIOError("Error getting variable names & types", retcode)

        # get array contents
        varNames = [varNamesArr[0][i] for i in xrange(numVars)]
        varTypes = [varTypesArr[0][i] for i in xrange(numVars)]
        if self.ioUtf8:
            varNames = [varName.decode("utf-8") for varName in varNames]

        # clean up
        args = (varNamesArr, varTypesArr, numVars)
        self.freeMemory("spssFreeVarNames", *args)

        return varNames, dict(zip(varNames, varTypes))

    @varNamesTypes.setter
    def varNamesTypes(self, varNamesVarTypes):
        badLengthMsg = "Empty or longer than %s chars" % \
                       (MAXLENGTHS['SPSS_MAX_VARNAME'][0])
        varNames, varTypes = varNamesVarTypes
        varNameRetcodes = {
            0: ('SPSS_NAME_OK', 'Valid standard name'),
            1: ('SPSS_NAME_SCRATCH', 'Valid scratch var name'),
            2: ('SPSS_NAME_SYSTEM' 'Valid system var name'),
            3: ('SPSS_NAME_BADLTH', badLengthMsg),
            4: ('SPSS_NAME_BADCHAR', 'Invalid character or embedded blank'),
            5: ('SPSS_NAME_RESERVED', 'Name is a reserved word'),
            6: ('SPSS_NAME_BADFIRST', 'Invalid initial char (otherwise OK)')}
        validate = self.spssio.spssValidateVarname
        func = self.spssio.spssSetVarName
        for varName in self.varNames:
            varLength = self.varTypes[varName]
            retcode = validate(c_char_p(varName))
            if retcode > 0:
                msg = "%r is an invalid variable name [%r]" % \
                      (varName, ": ".join(varNameRetcodes.get(retcode)))
                raise SPSSIOError(msg, retcode)
            retcode = func(c_int(self.fh), c_char_p(varName), c_int(varLength))
            if retcode > 0:
                msg = "Problem setting variable name %r" % varName
                raise SPSSIOError(msg, retcode)

    @property
    @decode
    def valueLabels(self):
        """Get/Set VALUE LABELS.
        Takes a dictionary of the form {varName: {value: valueLabel}:
        --{'numGender': {1: 'female', {2: 'male'}}
        --{'strGender': {'f': 'female', 'm': 'male'}}"""
        def initArrays(isNumeric=True, size=1000):
            """default size assumes never more than 1000 labels"""
            labelsArr = (POINTER(c_char_p * size))()
            if isNumeric:
                return (POINTER(c_double * size))(), labelsArr
            return (POINTER(c_char_p * size))(), labelsArr

        valueLabels = {}
        for varName in self.varNames:
            vName = self.vNames[varName]
            numLabels = c_int()

            # step 1: get array size (numeric values)
            if self.varTypes[varName] == 0:
                valuesArr, labelsArr = initArrays(True)
                func = self.spssio.spssGetVarNValueLabels
                retcode = func(c_int(self.fh), c_char_p(vName),
                               byref(valuesArr), byref(labelsArr),
                               byref(numLabels))
                valuesArr, labelsArr = initArrays(True, numLabels.value)

            # step 1: get array size (string values)
            else:
                valuesArr, labelsArr = initArrays(False)
                func = self.spssio.spssGetVarCValueLabels
                retcode = func(c_int(self.fh), c_char_p(vName),
                               byref(valuesArr), byref(labelsArr),
                               byref(numLabels))
                valuesArr, labelsArr = initArrays(False, numLabels.value)

            # step 2: get labels with array of proper size
            retcode = func(c_int(self.fh), c_char_p(vName), byref(valuesArr),
                           byref(labelsArr), byref(numLabels))
            if retcode > 0:
                msg = "Error getting value labels of variable %r"
                raise SPSSIOError(msg % varName, retcode)

            # get array contents
            if not numLabels.value:
                continue
            values = [valuesArr[0][i] for i in xrange(numLabels.value)]
            labels = [labelsArr[0][i] for i in xrange(numLabels.value)]
            valueLabelsX = [(val, lbl) for val, lbl in zip(values, labels)]
            valueLabels[varName] = dict(valueLabelsX)

            # clean up
            args = (valuesArr, labelsArr, numLabels)
            if self.varTypes[varName] == 0:
                self.freeMemory("spssFreeVarNValueLabels", *args)
            else:
                self.freeMemory("spssFreeVarCValueLabels", *args)

        return valueLabels

    @valueLabels.setter
    def valueLabels(self, valueLabels):
        if not valueLabels:
            return
        valLabN = self.spssio.spssSetVarNValueLabel
        valLabC = self.spssio.spssSetVarCValueLabel
        valueLabels = self.encode(valueLabels)
        for varName, valueLabelsX in valueLabels.iteritems():
            valueLabelsX = self.encode(valueLabelsX)
            for value, label in valueLabelsX.iteritems():
                if self.varTypes[varName] == 0:
                    retcode = valLabN(c_int(self.fh), c_char_p(varName),
                                      c_double(value), c_char_p(label))
                else:
                    retcode = valLabC(c_int(self.fh), c_char_p(varName),
                                      c_char_p(value), c_char_p(label))
                if retcode > 0:
                    msg = "Problem with setting value labels of variable %r"
                    raise SPSSIOError(msg % varName, retcode)

    @property
    @decode
    def varLabels(self):
        """Get/set VARIABLE LABELS.
        Returns/takes a dictionary of the form {varName: varLabel}.
        For example: varLabels = {'salary': 'Salary (dollars)',
                                  'educ': 'Educational level (years)'}"""
        SPSS_VARLABEL_SHORT = 120  # fixed amount
        funcS = self.spssio.spssGetVarLabel
        funcL = self.spssio.spssGetVarLabelLong
        varLabels = {}
        for varName in self.varNames:
            varLabel = create_string_buffer(SPSS_VARLABEL_SHORT + 1)
            vName = self.vNames[varName]
            retcode = funcS(c_int(self.fh), c_char_p(vName), byref(varLabel))
            if varLabel.value and len(varLabel.value) > SPSS_VARLABEL_SHORT:
                lenBuff = MAXLENGTHS['SPSS_MAX_VARLABEL']
                varLabel = create_string_buffer(lenBuff)
                retcode = funcL(c_int(self.fh), c_char_p(varName),
                                byref(varLabel), c_int(lenBuff), byref(c_int))
            varLabels[varName] = varLabel.value
            if retcode > 0:
                msg = "Error getting variable label of variable %r" % varName
                raise SPSSIOError(msg, retcode)
        return varLabels

    @varLabels.setter
    def varLabels(self, varLabels):
        if not varLabels:
            return
        func = self.spssio.spssSetVarLabel
        varLabels = self.encode(varLabels)
        for varName, varLabel in varLabels.iteritems():
            retcode = func(c_int(self.fh), c_char_p(varName),
                           c_char_p(varLabel))
            if retcode > 0:
                msg = ("Problem with setting variable label %r of variable %r"
                       % (varLabel, varName))
                raise SPSSIOError(msg, retcode)

    @property
    @decode
    def formats(self):
        """Get the PRINT FORMATS, set PRINT and WRITE FORMATS.
        Returns/takes a dictionary of the form {varName: <format_>.
        For example: formats = {'salary': 'DOLLAR8', 'gender': 'A1',
                                'educ': 'F8.2'}"""
        if hasattr(self, "varformats"):
            return self.varformats
        printFormat_, printDec_, printWid_ = c_int(), c_int(), c_int()
        func = self.spssio.spssGetVarPrintFormat
        formats = {}
        for varName in self.varNames:
            vName = self.vNames[varName]
            retcode = func(c_int(self.fh), c_char_p(vName),
                           byref(printFormat_), byref(printDec_),
                           byref(printWid_))
            if retcode > 0:
                msg = "Error getting print format for variable %r"
                raise SPSSIOError(msg % vName, retcode)
            printFormat = allFormats.get(printFormat_.value)[0]
            printFormat = printFormat.split("_")[-1]
            format_ = printFormat + str(printWid_.value)
            if self.varTypes[varName] == 0:
                format_ += ("." + str(printDec_.value))
            if format_.endswith(".0"):
                format_ = format_[:-2]
            formats[varName] = format_
        return formats

    def _splitformats(self):
        """This function returns the 'bare' formats + variable widths,
        e.g. format_ F5.3 is returned as 'F' and '5'"""
        regex = re.compile("\w+(?P<varWid>\d+)[.]?\d?", re.I)
        bareformats, varWids = {}, {}
        for varName, format_ in self.formats.iteritems():
            bareformats[varName] = re.sub(r"\d+.", "", format_)
            varWids[varName] = int(regex.search(format_).group("varWid"))
        return bareformats, varWids

    @formats.setter
    def formats(self, formats):
        if not formats:
            return
        reverseFormats = dict([(v[0][9:], k) for k, v in allFormats.items()])
        validValues = sorted(reverseFormats.keys())
        regex = "(?P<printFormat>A(HEX)?)(?P<printWid>\d+)"
        isStringVar = re.compile(regex, re.IGNORECASE)
        regex = "(?P<printFormat>[A-Z]+)(?P<printWid>\d+)\.?(?P<printDec>\d*)"
        isAnyVar = re.compile(regex, re.IGNORECASE)
        funcP = self.spssio.spssSetVarPrintFormat  # print type
        funcW = self.spssio.spssSetVarWriteFormat  # write type
        for varName, format_ in self.encode(formats).iteritems():
            format_ = format_.upper()
            gotString = isStringVar.match(format_)
            gotAny = isAnyVar.match(format_)
            msg = ("Unknown format_ %r for variable %r. " +
                   "Valid formats are: %s")
            msg = msg % (", ".join(validValues), format_, varName)
            if gotString:
                printFormat = gotString.group("printFormat")
                printFormat = reverseFormats.get(printFormat)
                printDec = 0
                printWid = int(gotString.group("printWid"))
            elif gotAny:
                printFormat = gotAny.group("printFormat")
                printFormat = reverseFormats.get(printFormat)
                printDec = gotAny.group("printDec")
                printDec = int(printDec) if printDec else 0
                printWid = int(gotAny.group("printWid"))
            else:
                raise ValueError(msg)

            if printFormat is None:
                raise ValueError(msg)

            args = (c_int(self.fh), c_char_p(varName), c_int(printFormat),
                    c_int(printDec), c_int(printWid))
            retcode1, retcode2 = funcP(*args), funcW(*args)
            if retcodes.get(retcode1) == "SPSS_INVALID_PRFOR":
                # invalid PRint FORmat
                msg = "format_ for %r misspecified (%r)"
                raise SPSSIOError(msg % (varName, format_), retcode1)
            elif retcode1 > 0:
                msg = "Error setting format_ %r for %r"
                raise SPSSIOError(msg % (format_, varName), retcode1)

    def _getMissingValue(self, varName):
        """This is a helper function for the missingValues getter
        method.  The function returns the missing values of variable <varName>
        as a a dictionary. The dictionary keys and items depend on the
        particular definition, which may be discrete values and/or ranges.
        Range definitions are only possible for numerical variables."""
        if self.varTypes[varName] == 0:
            func = self.spssio.spssGetVarNMissingValues
            args = (c_double(), c_double(), c_double())
        else:
            func = self.spssio.spssGetVarCMissingValues
            args = (create_string_buffer(9), create_string_buffer(9),
                    create_string_buffer(9))
        missingFmt = c_int()
        vName = self.vNames[varName]
        retcode = func(c_int(self.fh), c_char_p(vName),
                       byref(missingFmt), *map(byref, args))
        if retcode > 0:
            msg = "Error getting missing value for variable %r"
            raise SPSSIOError(msg % varName, retcode)

        v1, v2, v3 = [v.value for v in args]
        userMiss = dict([(v, k) for k, v in userMissingValues.iteritems()])
        missingFmt = userMiss[missingFmt.value]
        if missingFmt == "SPSS_NO_MISSVAL":
            return {}
        elif missingFmt == "SPSS_ONE_MISSVAL":
            return {"values": [v1]}
        elif missingFmt == "SPSS_TWO_MISSVAL":
            return {"values": [v1, v2]}
        elif missingFmt == "SPSS_THREE_MISSVAL":
            return {"values": [v1, v2, v3]}
        elif missingFmt == "SPSS_MISS_RANGE":
            return {"lower": v1, "upper": v2}
        elif missingFmt == "SPSS_MISS_RANGEANDVAL":
            return {"lower": v1, "upper": v2, "value": v3}

    def _setMissingValue(self, varName, **kwargs):
        """This is a helper function for the missingValues setter
        method. The function sets missing values for variable <varName>.
        Valid keyword arguments are:
        * to specify a RANGE: 'lower', 'upper', optionally with 'value'
        * to specify DISCRETE VALUES: 'values', specified as a list no longer
        than three items, or as None, or as a float/int/str
        """
        if kwargs == {}:
            return 0
        fargs = ["lower", "upper", "value", "values"]
        if set(kwargs.keys()).difference(set(fargs)):
            raise ValueError("Allowed keywords are: %s" % ", ".join(fargs))
        varName = self.encode(varName)
        varType = self.varTypes[varName]

        # range of missing values, e.g. MISSING VALUES aNumVar (-9 THRU -1).
        if varType == 0:
            placeholder = 0.0
            if "lower" in kwargs and "upper" in kwargs and "value" in kwargs:
                missingFmt = "SPSS_MISS_RANGEANDVAL"
                args = kwargs["lower"], kwargs["upper"], kwargs["value"]
            elif "lower" in kwargs and "upper" in kwargs:
                missingFmt = "SPSS_MISS_RANGE"
                args = kwargs["lower"], kwargs["upper"], placeholder
        else:
            placeholder, args = "0", None

        # up to three discrete missing values
        if "values" in kwargs:
            values = self.encode(kwargs.values()[0])
            if isinstance(values, (float, int, str)):
                values = [values]

            # check if missing values strings values are not too long
            strMissLabels = [len(v) for v in values if isinstance(v, str)]
            if strMissLabels and max(strMissLabels) > 9:
                raise ValueError("Missing value label > 9 bytes")

            nvalues = len(values) if values is not None else values
            if values is None or values == {}:
                missingFmt = "SPSS_NO_MISSVAL"
                args = placeholder, placeholder, placeholder
            elif nvalues == 1:
                missingFmt = "SPSS_ONE_MISSVAL"
                args = values + [placeholder, placeholder]
            elif nvalues == 2:
                missingFmt = "SPSS_TWO_MISSVAL"
                args = values + [placeholder]
            elif nvalues == 3:
                missingFmt = "SPSS_THREE_MISSVAL"
                args = values
            else:
                msg = "You can specify up to three individual missing values"
                raise ValueError(msg)

        # numerical vars
        if varType == 0 and args:
            func = self.spssio.spssSetVarNMissingValues
            func.argtypes = [c_int, c_char_p, c_int,
                             c_double, c_double, c_double]
            args = map(float, args)
        # string vars
        else:
            if args is None:
                raise ValueError("Illegal keyword for character variable")
            func = self.spssio.spssSetVarCMissingValues
            func.argtypes = [c_int, c_char_p, c_int,
                             c_char_p, c_char_p, c_char_p]

        retcode = func(self.fh, varName, userMissingValues[missingFmt], *args)
        if retcode > 0:
            msg = "Problem setting missing value of variable %r"
            raise SPSSIOError(msg % varName, retcode)

    @property
    @decode
    def missingValues(self):
        """Get/Set MISSING VALUES.
        User missing values are values that will not be included in
        calculations by SPSS. For example, 'don't know' might be coded as a
        user missing value (a value of 999 is typically used, so when vairable
        'age' has values 5, 15, 999, the average age is 10). This is
        different from 'system missing values', which are blank/null values.
        Takes a dictionary of the following form:
          {'someNumvar1': {'values': [999, -1, -2]}, # discrete values
           'someNumvar2': {'lower': -9, 'upper':-1}, # range "-9 THRU -1"
           'someNumvar3': {'lower': -9, 'upper':-1, 'value': 999},
           'someStrvar1': {'values': ['foo', 'bar', 'baz']},
           'someStrvar2': {'values': 'bletch'}}      # shorthand """
        missingValues = {}
        for varName in self.varNames:
            missingValues[varName] = self._getMissingValue(varName)
        return missingValues

    @missingValues.setter
    def missingValues(self, missingValues):
        if missingValues:
            for varName, kwargs in missingValues.iteritems():
                self._setMissingValue(varName, **kwargs)

    # measurelevel, colwidth and alignment must all be set or not at all.
    @property
    @decode
    def measureLevels(self):
        """Get/Set VARIABLE LEVEL (measurement level).
        Returns/Takes a dictionary of the form {varName: varMeasureLevel}.
        Valid measurement levels are: "unknown", "nominal", "ordinal", "scale",
        "ratio", "flag", "typeless". This is used in Spss procedures such as
        CTABLES."""
        func = self.spssio.spssGetVarMeasureLevel
        levels = {0: "unknown", 1: "nominal", 2: "ordinal", 3: "scale",
                  3: "ratio", 4: "flag", 5: "typeless"}
        measureLevel = c_int()
        varMeasureLevels = {}
        for varName in self.varNames:
            vName = self.vNames[varName]
            retcode = func(c_int(self.fh), c_char_p(vName),
                           byref(measureLevel))
            varMeasureLevels[varName] = levels.get(measureLevel.value)
            if retcode > 0:
                msg = "Error getting variable measurement level: %r"
                raise SPSSIOError(msg % varName, retcode)

        return varMeasureLevels

    @measureLevels.setter
    def measureLevels(self, varMeasureLevels):
        if not varMeasureLevels:
            return
        func = self.spssio.spssSetVarMeasureLevel
        levels = {"unknown": 0, "nominal": 1, "ordinal": 2, "scale": 3,
                  "ratio": 3, "flag": 4, "typeless": 5}
        for varName, level in self.encode(varMeasureLevels).iteritems():
            if level.lower() not in levels:
                msg = "Valid levels are %"
                raise ValueError(msg % ", ".join(levels.keys()))
            level = levels.get(level.lower())
            retcode = func(c_int(self.fh), c_char_p(varName), c_int(level))
            if retcode > 0:
                msg = ("Error setting variable mesasurement level. " +
                       "Valid levels are: %s")
                raise SPSSIOError(msg % ", ".join(levels.keys()), retcode)

    @property
    @decode
    def columnWidths(self):
        """Get/Set VARIABLE WIDTH (display width).
        Returns/Takes a dictionary of the form {varName: <int>}. A value of
        zero is special and means that the IBM SPSS Statistics Data Editor
        is to set an appropriate width using its own algorithm. If used,
        variable alignment, measurement level and column width all needs to
        be set."""
        func = self.spssio.spssGetVarColumnWidth
        varColumnWidth = c_int()
        varColumnWidths = {}
        for varName in self.varNames:
            vName = self.vNames[varName]
            retcode = func(c_int(self.fh), c_char_p(vName),
                           byref(varColumnWidth))
            if retcode > 0:
                msg = ("Error getting column width: %r" % varName)
                raise SPSSIOError(msg, retcode)
            varColumnWidths[varName] = varColumnWidth.value
        return varColumnWidths

    @columnWidths.setter
    def columnWidths(self, varColumnWidths):
        if not varColumnWidths:
            return
        func = self.spssio.spssSetVarColumnWidth
        for varName, varColumnWidth in varColumnWidths.iteritems():
            retcode = func(c_int(self.fh), c_char_p(varName),
                           c_int(varColumnWidth))
            if retcode > 0:
                msg = "Error setting variable colunm width"
                raise SPSSIOError(msg, retcode)

    def _setColWidth10(self):
        """Set the variable display width of string values to at least 10
        (it's annoying that SPSS displays e.g. a one-character variable in
        very narrow columns). This also sets all measurement levels to
        "unknown" and all variable alignments to "left". This function is
        only called if column widths, measurement levels and variable
        alignments are None."""
        columnWidths = {}
        for varName, varType in self.varTypes.iteritems():
            # zero = appropriate width determined by spss
            columnWidths[varName] = 10 if 0 < varType < 10 else 0
        self.columnWidths = columnWidths
        self.measureLevels = dict([(v, "unknown") for v in self.varNames])
        self.alignments = dict([(v, "left") for v in self.varNames])

    @property
    @decode
    def alignments(self):
        """Get/Set VARIABLE ALIGNMENT.
        Returns/Takes a dictionary of the form {varName: alignment}
        Valid alignment values are: left, right, center. If used, variable
        alignment, measurement level and column width all need to be set.
        """
        func = self.spssio.spssGetVarAlignment
        alignments = {0: "left", 1: "right", 2: "center"}
        alignment_ = c_int()
        varAlignments = {}
        for varName in self.varNames:
            vName = self.vNames[varName]
            retcode = func(c_int(self.fh), c_char_p(vName),
                           byref(alignment_))
            alignment = alignments[alignment_.value]
            varAlignments[varName] = alignment
            if retcode > 0:
                msg = ("Error getting variable alignment: %r" % varName)
                raise SPSSIOError(msg, retcode)
        return varAlignments

    @alignments.setter
    def alignments(self, varAlignments):
        if not varAlignments:
            return
        func = self.spssio.spssSetVarAlignment
        alignments = {"left": 0, "right": 1, "center": 2}
        for varName, varAlignment in varAlignments.iteritems():
            if varAlignment.lower() not in alignments:
                msg = "Valid alignments are %"
                raise ValueError(msg % ", ".join(alignments.keys()))
            alignment = alignments.get(varAlignment.lower())
            retcode = func(c_int(self.fh), c_char_p(varName), c_int(alignment))
            if retcode > 0:
                msg = "Error setting variable alignment for variable %r"
                raise SPSSIOError(msg % varName, retcode)

    @property
    @decode
    def varSets(self):
        """Get/Set VARIABLE SET information.
        Returns/Takes a dictionary with SETNAME as keys and a list of SPSS
        variables as values. For example: {'SALARY': ['salbegin',
        'salary'], 'DEMOGR': ['gender', 'minority', 'educ']}"""
        varSets = c_char_p()
        func = self.spssio.spssGetVariableSets
        retcode = func(c_int(self.fh), byref(varSets))
        if retcode > 0:
            msg = "Problem getting variable set information"
            raise SPSSIOError(msg, retcode)
        if not varSets.value:
            return {}
        varSets_ = {}
        for varSet in varSets.value.split("\n")[:-1]:
            k, v = varSet.split("= ")
            varSets_[k] = v.split()

        # clean up
        self.freeMemory("spssFreeVariableSets", varSets)

        return varSets_

    @varSets.setter
    def varSets(self, varSets):
        if not varSets:
            return
        varSets_ = []
        for varName, varSet in varSets.iteritems():
            varSets_.append("%s= %s" % (varName, " ".join(varSet)))
        varSets_ = c_char_p("\n".join(varSets_))
        retcode = self.spssio.spssSetVariableSets(c_int(self.fh), varSets_)
        if retcode > 0:
            msg = "Problem setting variable set information"
            raise SPSSIOError(msg, retcode)

    @property
    @decode
    def varRoles(self):
        """Get/Set VARIABLE ROLES.
        Returns/Takes a dictionary of the form {varName: varRole}, where
        varRoles may be any of the following: 'both', 'frequency', 'input',
        'none', 'partition', 'record ID', 'split', 'target'"""
        func = self.spssio.spssGetVarRole
        roles = {0: "input", 1: "target", 2: "both", 3: "none", 4: "partition",
                 5: "split", 6: "frequency", 7: "record ID"}
        varRoles = {}
        varRole_ = c_int()
        for varName in self.varNames:
            vName = self.vNames[varName]
            retcode = func(c_int(self.fh), c_char_p(vName), byref(varRole_))
            varRole = roles.get(varRole_.value)
            varRoles[varName] = varRole
            if retcode > 0:
                msg = "Problem getting variable role for variable %r"
                raise SPSSIOError(msg % varName, retcode)
        return varRoles

    @varRoles.setter
    def varRoles(self, varRoles):
        if not varRoles:
            return
        roles = {"input": 0, "target": 1, "both": 2, "none": 3, "partition": 4,
                 "split": 5,  "frequency": 6, "record ID": 7}
        func = self.spssio.spssSetVarRole
        for varName, varRole in varRoles.iteritems():
            varRole = roles.get(varRole)
            retcode = func(c_int(self.fh), c_char_p(varName), c_int(varRole))
            if retcode > 0:
                msg = "Problem setting variable role %r for variable %r"
                raise SPSSIOError(msg % (varRole, varName), retcode)

    @property
    @decode
    def varAttributes(self):
        """Get/Set VARIABLE ATTRIBUTES.
        Returns/Takes dictionary of the form:
        {'var1': {'attr name x': 'attr value x','attr name y': 'attr value y'},
         'var2': {'attr name a': 'attr value a','attr name b': 'attr value b'}}
        """
        # abbreviation for readability and speed
        func = self.spssio.spssGetVarAttributes

        # initialize arrays
        MAX_ARRAY_SIZE = 1000
        attrNamesArr = (POINTER(c_char_p * MAX_ARRAY_SIZE))()
        attrValuesArr = (POINTER(c_char_p * MAX_ARRAY_SIZE))()

        attributes = {}
        for varName in self.varNames:
            vName = self.vNames[varName]

            # step 1: get array size
            nAttr = c_int()
            retcode = func(c_int(self.fh), c_char_p(vName),
                           byref(attrNamesArr), byref(attrValuesArr),
                           byref(nAttr))
            if retcode > 0:
                msg = "@Problem getting attributes of variable %r (step 1)"
                raise SPSSIOError(msg % varName, retcode)

            # step 2: get attributes with arrays of proper size
            nAttr = c_int(nAttr.value)
            attrNamesArr = (POINTER(c_char_p * nAttr.value))()
            attrValuesArr = (POINTER(c_char_p * nAttr.value))()
            retcode = func(c_int(self.fh), c_char_p(vName),
                           byref(attrNamesArr), byref(attrValuesArr),
                           byref(nAttr))
            if retcode > 0:
                msg = "Problem getting attributes of variable %r (step 2)"
                raise SPSSIOError(msg % varName, retcode)

            # get array contents
            if not nAttr.value:
                continue
            k, v, n = attrNamesArr[0], attrValuesArr[0], nAttr.value
            attribute = dict([(k[i], v[i]) for i in xrange(n)])
            attributes[varName] = attribute

            # clean up
            args = (attrNamesArr, attrValuesArr, nAttr)
            self.freeMemory("spssFreeAttributes", *args)

        return attributes

    @varAttributes.setter
    def varAttributes(self, varAttributes):
        if not varAttributes:
            return
        func = self.spssio.spssSetVarAttributes
        for varName in self.varNames:
            attributes = varAttributes.get(varName)
            if not attributes:
                continue
            nAttr = len(attributes)
            attrNames = (c_char_p * nAttr)(*attributes.keys())
            attrValues = (c_char_p * nAttr)(*attributes.values())
            retcode = func(c_int(self.fh), c_char_p(varName),
                           pointer(attrNames), pointer(attrValues),
                           c_int(nAttr))
            if retcode > 0:
                msg = "Problem setting variable attributes for variable %r"
                raise SPSSIOError(msg % varName, retcode)

    @property
    @decode
    def fileAttributes(self):
        """Get/Set DATAFILE ATTRIBUTES.
        Returns/Takes a dictionary of the form:
        {'attrName[1]': 'attrValue1', 'revision[1]': '2010-10-09',
        'revision[2]': '2010-10-22', 'revision[3]': '2010-11-19'}
         """
        # abbreviation for readability
        func = self.spssio.spssGetFileAttributes

        # step 1: get array size
        MAX_ARRAY_SIZE = 100  # assume never more than 100 file attributes
        attrNamesArr = (POINTER(c_char_p * MAX_ARRAY_SIZE))()
        attrValuesArr = (POINTER(c_char_p * MAX_ARRAY_SIZE))()
        nAttr = c_int()
        retcode = func(c_int(self.fh), byref(attrNamesArr),
                       byref(attrValuesArr), byref(nAttr))

        # step 2: get attributes with arrays of proper size
        nAttr = c_int(nAttr.value)
        attrNamesArr = (POINTER(c_char_p * nAttr.value))()
        attrValuesArr = (POINTER(c_char_p * nAttr.value))()
        retcode = func(c_int(self.fh), byref(attrNamesArr),
                       byref(attrValuesArr), byref(nAttr))
        if retcode > 0:
            raise SPSSIOError("Problem getting file attributes", retcode)

        # get array contents
        if not nAttr.value:
            return {}
        k, v = attrNamesArr[0], attrValuesArr[0]
        attributes = dict([(k[i], v[i]) for i in xrange(nAttr.value)])

        # clean up
        args = (attrNamesArr, attrValuesArr, nAttr)
        self.freeMemory("spssFreeAttributes", *args)

        return attributes

    @fileAttributes.setter
    def fileAttributes(self, fileAttributes):
        if not fileAttributes:
            return
        attributes, valueLens = {}, []
        for name, values in fileAttributes.iteritems():
            valueLens.append(len(values))
            for value in values:
                attributes[name] = value
        #nAttr = len(fileAttributes)
        nAttr = max(valueLens)  # n elements per vector. But this may vary??
        attrNames = (c_char_p * nAttr)(*attributes.keys())
        attrValues = (c_char_p * nAttr)(*attributes.values())
        func = self.spssio.spssSetFileAttributes
        retcode = func(c_int(self.fh), pointer(attrNames),
                       pointer(attrValues), c_int(nAttr))
        if retcode > 0:
            raise SPSSIOError("Problem setting file attributes", retcode)

    def _getMultRespDef(self, mrDef):
        """Get 'normal' multiple response defintions.
        This is a helper function for the multRespDefs getter function.
        A multiple response definition <mrDef> in the string format returned
        by the IO module is converted into a multiple response definition of
        the form multRespSet = {<setName>: {"setType": <setType>, "label":
        <lbl>, "varNames": <list_of_varNames>}}. SetType may be either 'D'
        (multiple dichotomy sets) or 'C' (multiple category sets). If setType
        is 'D', the multiple response definition also includes '"countedValue":
        countedValue'"""
        regex = "\$(?P<setName>\w+)=(?P<setType>[CD])\n?"
        m = re.search(regex + ".*", mrDef, re.I | re.U)
        if not m:
            return {}
        setType = m.group("setType")
        if setType == "C":  # multiple category sets
            regex += " (?P<lblLen>\d+) (?P<lblVarNames>.+) ?\n?"
            matches = re.findall(regex, mrDef, re.I)
            setName, setType, lblLen, lblVarNames = matches[0]
        else:               # multiple dichotomy sets
            regex += ("(?P<valueLen>\d+) (?P<countedValue>\w+)" +
                      " (?P<lblLen>\d+) (?P<lblVarNames>.+) ?\n?")
            matches = re.findall(regex, mrDef, re.I | re.U)
            setName, setType, valueLen = matches[0][:3]
            countedValue, lblLen, lblVarNames = matches[0][3:]
        lbl = lblVarNames[:int(lblLen)]
        varNames = lblVarNames[int(lblLen):].split()
        multRespSet = {setName: {"setType": setType, "label": lbl,
                                 "varNames": varNames}}
        if setType == "D":
            multRespSet[setName]["countedValue"] = countedValue
        return multRespSet

    def _setMultRespDefs(self, multRespDefs):
        """Set 'normal' multiple response defintions.
        This is a helper function for the multRespDefs setter function.
        It translates the multiple response definition, specified as a
        dictionary, into a string that the IO module can use"""
        mrespDefs = []
        for setName, rest in multRespDefs.iteritems():
            print setName, rest, rest["setType"]
            if rest["setType"] not in ("C", "D"):
                continue
            rest["setName"] = setName
            mrespDef = "$%(setName)s=%(setType)s" % rest
            lblLen = len(rest["label"])
            rest["lblLen"] = lblLen
            rest["varNames"] = " ".join(rest["varNames"])
            tail = "%(varNames)s" if lblLen == 0 else "%(label)s %(varNames)s"
            if rest["setType"] == "C":  # multiple category sets
                template = " %%(lblLen)s %s " % tail
            else:                       # multiple dichotomy sets
                template = " %%(countedValue)s %%(lblLen)s %s " % tail
            mrespDef += template % rest
            mrespDefs.append(mrespDef)
        mrespDefs = "\n".join(mrespDefs)
        return mrespDefs

    def _getMultRespDefsEx(self, mrDef):
        """Get 'extended' multiple response defintions.
        This is a helper function for the multRespDefs getter function."""
        regex = ("\$(?P<setName>\w+)=(?P<setType>E) (?P<flag1>1)" +
                 "(?P<flag2>1)? (?P<valueLen>[0-9]+) (?P<countedValue>\w+) " +
                 "(?P<lblLen>[0-9]+) (?P<lblVarNames>[\w ]+)")
        matches = re.findall(regex, mrDef, re.I | re.U)
        setName, setType, flag1, flag2 = matches[0][:4]
        valueLen, countedValue, lblLen, lblVarNames = matches[0][4:]
        length = int(lblLen)
        label, varNames = lblVarNames[:length], lblVarNames[length:].split()
        return {setName: {"setType": setType, "firstVarIsLabel": bool(flag2),
                          "label": label, "countedValue": countedValue,
                          "varNames": varNames}}

    def _setMultRespDefsEx(self, multRespDefs):
        """Set 'extended' multiple response defintions.
        This is a helper function for the multRespDefs setter function."""
        mrDefs = []
        for setName, rest in multRespDefs.iteritems():
            if rest["setType"] != "E":
                continue
            rest["setName"] = setName
            v = int(rest["firstVarIsLabel"])
            rest["firstVarIsLabel"] = v if v == 1 else ""
            rest["valueLen"] = len(rest["countedValue"])
            rest["lblLen"] = len(rest["label"])
            rest["varNames"] = " ".join(rest["varNames"])
            mrDef = "$%(setName)s=%(setType)s 1%(firstVarIsLabel)s "
            mrDef += "%(valueLen)s %(countedValue)s %(lblLen)s %(label)s "
            mrDef += "%(varNames)s"
            mrDefs.append((mrDef % rest).replace("  ", " "))
        return "\n".join(mrDefs)

    @property
    @decode
    def multRespDefs(self):
        """Get/Set MRSETS (multiple response) sets.
        Returns/takes a dictionary of the form:
        --multiple category sets: {setName: {"setType": "C", "label": lbl,
          "varNames": [<list_of_varNames>]}}
        --multiple dichotomy sets: {setName: {"setType": "D", "label": lbl,
          "varNames": [<list_of_varNames>], "countedValue": countedValue}}
        --extended multiple dichotomy sets: {setName: {"setType": "E",
          "label": lbl, "varNames": [<list_of_varNames>], "countedValue":
           countedValue, 'firstVarIsLabel': <bool>}}
        For example:
        categorical  = {"setType": "C", "label": "labelC",
                       "varNames": ["salary", "educ"]}
        dichotomous1 = {"setType": "D", "label": "labelD",
                        "varNames": ["salary", "educ"], "countedValue": "Yes"}
        dichotomous2 = {"setType": "D", "label": "", "varNames":
                        ["salary", "educ", "jobcat"], "countedValue": "No"}
        extended1    = {"setType": "E", "label": "", "varNames": ["mevar1",
                        "mevar2", "mevar3"], "countedValue": "1",
                        "firstVarIsLabel": True}
        extended2    = {"setType": "E", "label":
                        "Enhanced set with user specified label", "varNames":
                        ["mevar4", "mevar5", "mevar6"], "countedValue":
                        "Yes", "firstVarIsLabel": False}
        multRespDefs = {"testSetC": categorical, "testSetD1": dichotomous1,
                        "testSetD2": dichotomous2, "testSetEx1": extended1,
                        "testSetEx2": extended2}
        """

        ## Normal Multiple response definitions
        func = self.spssio.spssGetMultRespDefs
        mrDefs = c_char_p()
        retcode = func(c_int(self.fh), pointer(mrDefs))
        if retcode > 0:
            msg = "Problem getting multiple response definitions"
            raise SPSSIOError(msg, retcode)

        multRespDefs = {}
        if mrDefs.value:
            for mrDef in mrDefs.value.split("\n"):
                for setName, rest in self._getMultRespDef(mrDef).iteritems():
                    multRespDefs[setName] = rest
            self.freeMemory("spssFreeMultRespDefs", mrDefs)

        ## Extended Multiple response definitions
        mrDefsEx = c_char_p()
        func = self.spssio.spssGetMultRespDefsEx
        retcode = func(c_int(self.fh), pointer(mrDefsEx))
        if retcode > 0:
            msg = "Problem getting extended multiple response definitions"
            raise SPSSIOError(msg, retcode)

        multRespDefsEx = {}
        if mrDefsEx.value:
            for mrDefEx in mrDefsEx.value.split("\n"):
                for setName, rest in self._getMultRespDef(mrDefEx).iteritems():
                    multRespDefsEx[setName] = rest
            self.freeMemory("spssFreeMultRespDefs", mrDefsEx)

        multRespDefs.update(multRespDefsEx)
        return multRespDefs

    @multRespDefs.setter
    def multRespDefs(self, multRespDefs):
        if not multRespDefs:
            return
        normal = self._setMultRespDefs(multRespDefs)
        extended = self._setMultRespDefsEx(multRespDefs)
        if normal and extended:
            combinedDefs = normal + " \n" + extended
        elif normal and not extended:
            combinedDefs = normal
        elif extended and not normal:
            combinedDefs = extended
        func = self.spssio.spssSetMultRespDefs
        retcode = func(c_int(self.fh), c_char_p(combinedDefs))
        if retcode > 0:
            msg = "Problem setting multiple response definitions"
            raise SPSSIOError(msg, retcode)

    @property
    @decode
    def caseWeightVar(self):
        """Get/Set WEIGHT variable.
        Takes a valid varName, and returns weight variable, if any, as a
        string."""
        varNameBuff = create_string_buffer(65)
        func = self.spssio.spssGetCaseWeightVar
        retcode = func(c_int(self.fh), byref(varNameBuff))
        if retcode > 0:
            msg = "Problem getting case weight variable name"
            raise SPSSIOError(msg, retcode)
        return varNameBuff.value

    @caseWeightVar.setter
    def caseWeightVar(self, varName):
        if not varName:
            return
        func = self.spssio.spssSetCaseWeightVar
        retcode = func(c_int(self.fh), c_char_p(varName))
        if retcode > 0:
            msg = "Problem setting case weight variable name %r" % varName
            raise SPSSIOError(msg, retcode)

    @property
    @decode
    def dateVariables(self):  # seems to be okay
        """Get/Set DATE information. This function reports the Forecasting
        (Trends) date variable information, if any, in IBM SPSS Statistics
        data files. Entirely untested and not implemented in reader/writer"""
        # step 1: get array size
        nElements = c_int()
        func = self.spssio.spssGetDateVariables
        MAX_ARRAY_SIZE = 100
        dateInfoArr = (POINTER(c_long * MAX_ARRAY_SIZE))()
        retcode = func(c_int(self.fh), byref(nElements), byref(dateInfoArr))

        # step 2: get date info with array of proper size
        dateInfoArr = (POINTER(c_long * nElements.value))()
        retcode = func(c_int(self.fh), byref(nElements), byref(dateInfoArr))
        if retcode > 0:
            raise SPSSIOError("Error getting TRENDS information", retcode)

        # get array contents
        nElem = nElements.value
        if not nElem:
            return {}
        dateInfo = [dateInfoArr[0][i] for i in xrange(nElem)]
        fixedDateInfo = dateInfo[:6]
        otherDateInfo = [dateInfo[i: i + 3] for i in xrange(6, nElem, 3)]
        dateInfo = {"fixedDateInfo": fixedDateInfo,
                    "otherDateInfo": otherDateInfo}

        # clean up
        self.freeMemory("spssFreeDateVariables", dateInfoArr)

        return dateInfo

    @dateVariables.setter
    def dateVariables(self, dateInfo):  # entirely untested!
        dateInfo = dateInfo["fixedDateInfo"] + dateInfo["otherDateInfo"]
        dateInfo = reduce(list.__add__, dateInfo)  # flatten list
        isAllFloats = all([isinstance(d, float) for d in dateInfo])
        isSixPlusTriplets = (len(dateInfo) - 6) % 3 == 0
        if not isAllFloats and isSixPlusTriplets:
            msg = ("TRENDS date info must consist of 6 fixed elements" +
                   "+ <nCases> three-element groups of other date info " +
                   "(all floats)")
            raise TypeError(msg)
        func = self.spssio.spssSetDateVariables
        dateInfoArr = (nElements * c_long)(*dateInfo)
        retcode = func(c_int(self.fh), c_int(nElements), dateInfoArr)
        if retcode > 0:
            raise SPSSIOError("Error setting TRENDS information", retcode)

    @property
    @decode
    def textInfo(self):
        """Get/Set text information.
        Takes a savFileName and returns a string of the form: "File %r built
        using SavReaderWriter.py version %s (%s)". This is akin to, but
        *not* equivalent to the SPSS syntax command DISPLAY DOCUMENTS"""
        textInfo = create_string_buffer(256)
        retcode = self.spssio.spssGetTextInfo(c_int(self.fh), byref(textInfo))
        if retcode > 0:
            raise SPSSIOError("Error getting textInfo", retcode)
        return textInfo.value

    @textInfo.setter
    def textInfo(self, savFileName):
        info = (os.path.basename(savFileName), __version__, time.asctime())
        textInfo = "File '%s' built using SavReaderWriter.py version %s (%s)"
        textInfo = textInfo % info
        if self.ioUtf8 and isinstance(savFileName, unicode):
            textInfo = textInfo.encode("utf-8")
        func = self.spssio.spssSetTextInfo
        retcode = func(c_int(self.fh), c_char_p(textInfo[:256]))
        if retcode > 0:
            raise SPSSIOError("Error setting textInfo", retcode)

    @property
    @decode
    def fileLabel(self):
        """Get/Set FILE LABEL (id string)
        Takes a file label (basestring), and returns file label, if any, as
        a string."""
        idStr = create_string_buffer(65)
        retcode = self.spssio.spssGetIdString(c_int(self.fh), byref(idStr))
        if retcode > 0:
            raise SPSSIOError("Error getting file label (id string)", retcode)
        return idStr.value

    @fileLabel.setter
    def fileLabel(self, idStr):
        if idStr is None:
            idStr = "File created by user %r at %s"[:64] % \
                    (getpass.getuser(), time.asctime())
        if self.ioUtf8 and isinstance(idStr, unicode):
            idStr = idStr.encode("utf-8")
        retcode = self.spssio.spssSetIdString(c_int(self.fh), c_char_p(idStr))
        if retcode > 0:
            raise SPSSIOError("Error setting file label (id string)", retcode)


class SavHeaderReader(Header):
    """
    This class contains methods that read the data dictionary of an SPSS
    data file. This yields the same information as the Spss command 'DISPLAY
    DICTIONARY' NB: do not confuse an Spss dictionary with a Python
    dictionary!

    Typical use:
    with SavHeaderReader(savFileName) as spssDict:
        wholeDict = spssDict.dataDictionary()
        print unicode(spssDict)
    """

    def __init__(self, savFileName, ioUtf8=False, ioLocale=None):
        """ Constructor. Initializes all vars that can be recycled """
        super(SavHeaderReader, self).__init__(savFileName, "rb", None,
                                              ioUtf8, ioLocale)
        self.fh = self.openSavFile()
        self.varNames, self.varTypes = self.varNamesTypes
        self.numVars = self.numberofVariables
        self.nCases = self.numberofCases

    def __str__(self):
        """ This function returns a report of the SPSS data dictionary
        (i.e., the header), in the encoding of the spss file"""
        return unicode(self).encode(self.fileEncoding)

    def __unicode__(self):
        """ This function returns a report of the SPSS data dictionary
        (i.e., the header)."""
        report = ""
        if self.textInfo:
            report += self.textInfo + os.linesep
        report += self.reportSpssDataDictionary(self.dataDictionary())
        return report

    def __enter__(self):
        """ This function returns the DictionaryReader object itself so
        its methods become available for use with context managers
        ('with' statements)."""
        return self

    def __exit__(self, type, value, tb):
        """ This function closes the spss data file and does some cleaning."""
        if type is not None:
            pass  # Exception occurred
        self.close()

    def close(self):
        """This function closes the spss data file and does some cleaning."""
        if not segfaults:
            self.closeSavFile(self.fh, mode="rb")

    def dataDictionary(self):
        """ This function returns all the dictionary items. It returns
        a Python dictionary based on the Spss dictionary of the given
        Spss file. This is equivalent to the Spss command 'DISPLAY
        DICTIONARY'."""
        items = ["varNames", "varTypes", "valueLabels", "varLabels",
                 "formats", "missingValues", "measureLevels",
                 "columnWidths", "alignments", "varSets", "varRoles",
                 "varAttributes", "fileAttributes", "fileLabel",
                 "multRespDefs", "caseWeightVar", "multRespDefs"]
        if self.ioUtf8:
            items = map(unicode, items)
        dataDictionary = dict([(item, getattr(self, item)) for item in items])
        return dataDictionary

    def reportSpssDataDictionary(self, dataDict):
        """ This function reports information from the Spss dictionary
        of the active Spss dataset. The parameter 'dataDict' is the return
        value of dataDictionary()"""
        report = []
        #import pprint
        #pprint.pprint(dataDict)
        for kwd, allValues in sorted(dataDict.items()):
            report.append("#" + kwd.upper())
            if hasattr(allValues, "items"):
                for varName, values in allValues.iteritems():
                    if hasattr(values, "items"):
                        isList = kwd in ("missingValues", "multRespDefs")
                        for k, v in sorted(values.iteritems()):
                            if isList and isinstance(v, (list, tuple)):
                                vStr = map(unicode.lower, map(unicode, v))
                                report.append("%s: %s -- %s" %
                                              (varName, k, ", ".join(vStr)))
                            else:
                                report.append("%s: %s -- %s" %
                                              (varName, unicode(k).strip(), v))
                    else:
                        if isinstance(values, list):
                            entry = "%s -- %s" % (varName, ", ".join(values))
                            report.append(entry)
                        elif values != "":
                            report.append("%s -- %s" % (varName, values))
            else:
                if isinstance(allValues, basestring) and allValues:
                    allValues = [allValues]
                for varName in allValues:
                    report.append(varName)
        return os.linesep.join(report)


class SavReader(Header):
    """ Read Spss system files (.sav, .zsav)

    Parameters:
    -savFileName: the file name of the spss data file
    -returnHeader: Boolean that indicates whether the first record should
        be a list of variable names (default = False)
    -recodeSysmisTo: indicates to which value missing values should
        be recoded (default = None),
    -selectVars: indicates which variables in the file should be selected.
        The variables should be specified as a list or a tuple of
        valid variable names. If None is specified, all variables
        in the file are used (default = None)
    -idVar: indicates which variable in the file should be used for use as id
        variable for the 'get' method (default = None)
    -verbose: Boolean that indicates whether information about the spss data
        file (e.g., number of cases, variable names, file size) should be
        printed on the screen (default = False).
    -rawMode: Boolean that indicates whether values should get SPSS-style
        formatting, and whether date variables (if present) should be converted
        to ISO-dates. If True, the program does not format any values, which
        increases processing speed. (default = False)
    -ioUtf8: indicates the mode in which text communicated to or from the
        I/O Module will be. Valid values are True (UTF-8 mode aka Unicode mode)
        and False (Codepage mode). Cf. SET UNICODE=ON/OFF (default = False)
    -ioLocale: indicates the locale of the I/O module. Cf. SET LOCALE (default
        = None, which corresponds to locale.getlocale()[0])

    Typical use:
    savFileName = "d:/someFile.sav"
    with SavReader(savFileName, returnHeader=True) as sav:
        header = sav.next()
        for line in sav:
            process(line)
    """

    def __init__(self, savFileName, returnHeader=False, recodeSysmisTo=None,
                 verbose=False, selectVars=None, idVar=None, rawMode=False,
                 ioUtf8=False, ioLocale=None):
        """ Constructor. Initializes all vars that can be recycled """
        super(SavReader, self).__init__(savFileName, "rb", None,
                                        ioUtf8, ioLocale)
        self.savFileName = savFileName
        self.returnHeader = returnHeader
        self.recodeSysmisTo = recodeSysmisTo
        self.verbose = verbose
        self.selectVars = selectVars
        self.idVar = idVar
        self.rawMode = rawMode

        self.header = self.getHeader(self.selectVars)
        self.bareformats, self.varWids = self._splitformats()
        self.autoRawMode = self._isAutoRawMode()

        self.ioUtf8_ = ioUtf8
        self.sysmis_ = self.sysmis
        self.numVars = self.numberofVariables
        self.nCases = self.numberofCases

        self.myStruct = self.getStruct(self.varTypes, self.varNames)
        self.unpack_from = self.myStruct.unpack_from
        self.seekNextCase = self.spssio.spssSeekNextCase
        self.caseBuffer = self.getCaseBuffer()

        if psycoOk:
            self._items = psyco.proxy(self._items)  # 3 x faster!

    def __enter__(self):
        """ This function opens the spss data file (context manager)."""
        if self.verbose and self.ioUtf8_:
            print unicode(self).replace(os.linesep, "\n")
        elif self.verbose:
            print str(self).replace(os.linesep, "\n")
        return iter(self)

    def __exit__(self, type, value, tb):
        """ This function closes the spss data file and does some cleaning."""
        if type is not None:
            pass  # Exception occurred
        self.close()

    def close(self):
        """This function closes the spss data file and does some cleaning."""
        if not segfaults:
            self.closeSavFile(self.fh, mode="rb")
        del self.spssio

    def __len__(self):
        """ This function reports the number of cases (rows) in the spss data
        file. For example: len(SavReader(savFileName))"""
        return self.nCases

    def __cmp__(self, other):
        """ This function implements behavior for all of the comparison
        operators so comparisons can be made between SavReader instances,
        or comparisons between SavReader instances and integers."""
        if not isinstance(other, (SavReader, int)):
            raise TypeError
        other = other if isinstance(other, int) else len(other)
        if len(self) < other:
            return -1
        elif len(self) == other:
            return 0
        else:
            return 1

    def __hash__(self):
        """This function returns a hash value for the object to ensure it
        is hashable."""
        return id(self)

    def __str__(self):
        """This function returns a conscise file report of the spss data file
        For example str(SavReader(savFileName))"""
        return unicode(self).encode(self.fileEncoding)

    def __unicode__(self):
        """This function returns a conscise file report of the spss data file,
        For example unicode(SavReader(savFileName))"""
        self.fileReport = self.getFileReport(self.savFileName, self.varNames,
                                             self.varTypes, self.formats,
                                             self.nCases)
        return self.fileReport

    def _isAutoRawMode(self):
        """Helper function for formatValues function. Determines whether
        iterating over each individual value is really needed"""
        hasDates = bool(set(self.bareformats.values()) & set(supportedDates))
        hasNfmt = "N" in self.bareformats
        hasRecodeSysmis = self.recodeSysmisTo is not None
        items = [hasDates, hasNfmt, hasRecodeSysmis, self.ioUtf8_]
        return False if any(items) else True

    def formatValues(self, record):
        """This function formats date fields to ISO dates (yyyy-mm-dd), plus
        some other date/time formats. The SPSS N format is formatted to a
        character value with leading zeroes. System missing values are recoded
        to <recodeSysmisTo>. If rawMode==True, this function does nothing"""
        if self.rawMode or self.autoRawMode:
            return record  # 6-7 times faster!

        for i, value in enumerate(record):
            varName = self.header[i]
            varType = self.varTypes[varName]
            bareformat_ = self.bareformats[varName]
            varWid = self.varWids[varName]
            if varType == 0:
                # recode system missing values, if present and desired
                if value > self.sysmis_:
                    pass
                else:
                    record[i] = self.recodeSysmisTo
                # format N-type values (=numerical with leading zeroes)
                if bareformat_ == "N":
                    #record[i] = str(value).zfill(varWid)
                    record[i] = "%%0%dd" % varWid % value  #15 x faster (zfill)
                # convert SPSS dates to ISO dates
                elif bareformat_ in supportedDates:
                    fmt = supportedDates[bareformat_]
                    args = (value, fmt, self.recodeSysmisTo)
                    record[i] = self.spss2strDate(*args)
            elif varType > 0:
                value = value[:varType]
                if self.ioUtf8_:
                    record[i] = value.decode("utf-8")
                else:
                    record[i] = value
        return record

    def _items(self, start=0, stop=None, step=1, returnHeader=False):
        """ This is a helper function to implement the __getitem__ and
        the __iter__ special methods. """

        if returnHeader:
            yield self.header

        if all([start == 0, stop is None, step == 1]):  # used as iterator
            retcode = 0
        else:
            retcode = self.seekNextCase(c_int(self.fh), c_long(0))  # reset

        if stop is None:
            stop = self.nCases

        selection = self.selectVars is not None
        for case in xrange(start, stop, step):
            if start:
                # only call this when iterating over part of the records
                retcode = self.seekNextCase(c_int(self.fh), c_long(case))
                if retcode > 0:
                    raise SPSSIOError("Error seeking case %d" % case, retcode)
            elif stop == self.nCases:
                self.printPctProgress(case, self.nCases)

            record = self.record

            if selection:
                record = self.selector(record)
                record = [record] if len(record) == 1 else list(record)
            record = self.formatValues(record)
            yield record

    def __iter__(self):
        """This function allows the object to be used as an iterator"""
        return self._items(0, None, 1, self.returnHeader)

    def __getitem__(self, key):
        """ This function reports the record of case number <key>.
        For example: firstRecord = SavReader(savFileName)[0].
        The <key> argument may also be a slice, for example:
        firstfiveRecords = SavReader(savFileName)[:5].
        You can also do stuff like (numpy required!):
        savReader(savFileName)[1:5, 1]"""

        is_slice = isinstance(key, slice)
        is_array_slice = key is Ellipsis or isinstance(key, tuple)

        if is_slice:
            start, stop, step = key.indices(self.nCases)
        elif is_array_slice:
            return self._get_array_slice(key, self.nCases, len(self.header))
        else:
            key = operator.index(key)
            start = key + self.nCases if key < 0 else key
            if not 0 <= start < self.nCases:
                raise IndexError("Index out of bounds")
            stop = start + 1
            step = 1

        records = self._items(start, stop, step)
        if is_slice:
            return list(records)
        return next(records)

    def _get_array_slice(self, key, nRows, nCols):
        """This is a helper function to implement array slicing with numpy"""

        if not numpyOk:
            raise ImportError("Array slicing requires the numpy library")

        is_index = False
        rstart = cstart = 0
        try:
            row, col = key
            if row < 0:
                row = nRows + row
            if col < 0:
                col = nCols + col

            ## ... slices
            if isinstance(row, slice) and col is Ellipsis:
                # reader[1:2, ...]
                rstart, rstop, rstep = row.indices(nRows)
                cstart, cstop, cstep = 0, nRows, 1
            elif row is Ellipsis and isinstance(col, slice):
                # reader[..., 1:2]
                rstart, rstop, rstep = 0, nRows, 1
                cstart, cstop, cstep = col.indices(nCols)
            elif isinstance(row, slice) and isinstance(col, slice):
                # reader[1:2, 1:2]
                rstart, rstop, rstep = row.indices(nRows)
                cstart, cstop, cstep = col.indices(nCols)
            elif row is Ellipsis and col is Ellipsis:
                # reader[..., ...]
                rstart, rstop, rstep = 0, nRows, 1
                cstart, cstop, cstep = 0, nCols, 1

            ## ... indexes
            elif isinstance(row, int) and col is Ellipsis:
                # reader[1, ...]
                rstart, rstop, rstep = row, row + 1, 1
                cstart, cstop, cstep = 0, nCols, 1
                is_index = True
            elif row is Ellipsis and isinstance(col, int):
                # reader[..., 1]
                rstart, rstop, rstep = 0, nRows, 1
                cstart, cstop, cstep = col, col + 1, 1
                is_index = True
            elif  isinstance(row, int) and isinstance(col, int):
                # reader[1, 1]
                rstart, rstop, rstep = row, row + 1, 1
                cstart, cstop, cstep = col, col + 1, 1
                is_index = True

            # ... slice + index
            elif isinstance(row, slice) and isinstance(col, int):
                # reader[1:2, 1]
                rstart, rstop, rstep = row.indices(nRows)
                cstart, cstop, cstep = col, col + 1, 1
            elif isinstance(row, int) and isinstance(col, slice):
                # reader[1, 1:2]
                rstart, rstop, rstep = row, row + 1, 1
                cstart, cstop, cstep = col.indices(nCols)

            try:
                if not 0 <= rstart < nRows:
                    raise IndexError("Index out of bounds")
                if not 0 <= cstart < nCols:
                    raise IndexError("Index out of bounds")

                key = (Ellipsis, slice(cstart, cstop, cstep))

            except UnboundLocalError:
                msg = "The array index is either invalid, or not implemented"
                raise TypeError(msg)

        except TypeError:
            # reader[...]
            rstart, rstop, rstep = 0, nRows, 1
            key = (Ellipsis, Ellipsis)

        records = self._items(rstart, rstop, rstep)
        result = numpy.array(list(records))[key].tolist()
        if is_index:
            return result[0]
        return result

    def head(self, n=5):
        """ This convenience function returns the first <n> records. """
        return self[:abs(n)]

    def tail(self, n=5):
        """ This convenience function returns the last <n> records. """
        return self[-abs(n):]

    def __contains__(self, item):
        """ This function implements membership testing and returns True if
        <idVar> contains <item>. Thus, it requires the 'idVar' parameter to
        be set. For example: reader = SavReader(savFileName, idVar="ssn")
        "987654321" in reader """
        return bool(self.get(item))

    def get(self, key, default=None, full=False):
        """ This function returns the records for which <idVar> == <key>
        if <key> in <savFileName>, else <default>. Thus, the function mimics
        dict.get, but note that dict[key] is NOT implemented. NB: Even though
        this uses a binary search, this is not very fast on large data (esp.
        the first call, and with full=True)

        Parameters:
        -key: key for which the corresponding record should be returned
        -default: value that should be returned if <key> is not found
          (default: None)
        -full: value that indicates whether *all* records for which
          <idVar> == <key> should be returned (default: False)
        For example: reader = SavReader(savFileName, idVar="ssn")
        reader.get("987654321", "social security number not found!")"""

        if not self.idVar in self.varNames:
            msg = ("SavReader object must be instantiated with an existing " +
                   "variable as an idVar argument")
            raise NameError(msg)

        #two slightly modified functions from the bisect module
        def bisect_right(a, x, lo=0, hi=None):
            if hi is None:
                hi = len(a)
            while lo < hi:
                mid = (lo + hi) // 2
                if x < a[mid][0]:
                    hi = mid  # a[mid][0], not a[mid]
                else:
                    lo = mid + 1
            return lo

        def bisect_left(a, x, lo=0, hi=None):
            if hi is None:
                hi = len(a)
            while lo < hi:
                mid = (lo + hi) // 2
                if a[mid][0] < x:
                    lo = mid + 1  # a[mid][0], not a[mid]
                else:
                    hi = mid
            return lo

        idPos = self.varNames.index(self.idVar)
        if not hasattr(self, "isSorted"):
            self.isSorted = True
            if self.varTypes[self.idVar] == 0:
                if not isinstance(key, (int, float)):
                    return default
                self.recordz = ((record[idPos], i) for i,
                                record in enumerate(iter(self)))
            else:
                if not isinstance(key, basestring):
                    return default
                self.recordz = ((record[idPos].rstrip(), i) for i,
                                record in enumerate(iter(self)))
            self.recordz = sorted(self.recordz)
        insertLPos = bisect_left(self.recordz, key)
        insertRPos = bisect_right(self.recordz, key)
        if full:
            result = [self[record[1]] for record in
                      self.recordz[insertLPos: insertRPos]]
        else:
            if insertLPos == insertRPos:
                return default
            result = self[self.recordz[insertLPos][1]]
        if result:
            return result
        return default

    def getSavFileInfo(self):
        """ This function reads and returns some basic information of the open
        spss data file."""
        return (self.numVars, self.nCases, self.varNames, self.varTypes,
                self.formats, self.varLabels, self.valueLabels)

    def memoize(f):
        """Memoization decorator
        http://code.activestate.com/recipes/577219-minimalistic-memoization/"""
        cache = {}
        MAXCACHE = 10**4

        def memf(*x):
            if x not in cache:
                cache[x] = f(*x)
            if len(cache) > MAXCACHE:
                cache.popitem()
            return cache[x]
        return memf

    @memoize
    def spss2strDate(self, spssDateValue, fmt, recodeSysmisTo):
        """This function converts internal SPSS dates (number of seconds
        since midnight, Oct 14, 1582 (the beginning of the Gregorian calendar))
        to a human-readable format"""
        try:
            if not hasattr(self, "gregorianEpoch"):
                self.gregorianEpoch = datetime.datetime(1582, 10, 14, 0, 0, 0)
            theDate = (self.gregorianEpoch +
                       datetime.timedelta(seconds=spssDateValue))
            return datetime.datetime.strftime(theDate, fmt)
        except OverflowError:
            return recodeSysmisTo
        except TypeError:
            return recodeSysmisTo
        except ValueError:
            return recodeSysmisTo

    def getFileReport(self, savFileName, varNames, varTypes,
                      formats, nCases):
        """ This function prints a report about basic file characteristics """
        bytes = os.path.getsize(savFileName)
        kb = float(bytes) / 2**10
        mb = float(bytes) / 2**20
        (fileSize, label) = (mb, "MB") if mb > 1 else (kb, "kB")
        systemString = self.systemString
        spssVersion = ".".join(map(str, self.spssVersion))
        lang, cp = locale.getlocale()
        intEnc = "Utf-8/Unicode" if self.ioUtf8 else "Codepage (%s)" % cp
        varlist = []
        line = "  %%0%sd. %%s (%%s - %%s)" % len(str(len(varNames) + 1))
        for cnt, varName in enumerate(varNames):
            lbl = "string" if varTypes[varName] > 0 else "numerical"
            format_ = formats[varName]
            varlist.append(line % (cnt + 1, varName, format_, lbl))
        info = {"savFileName": savFileName,
                "fileSize": fileSize,
                "label": label,
                "nCases": nCases,
                "nCols": len(varNames),
                "nValues": nCases * len(varNames),
                "spssVersion": "%s (%s)" % (systemString, spssVersion),
                "ioLocale": self.ioLocale,
                "ioUtf8": intEnc,
                "fileEncoding": self.fileEncoding,
                "fileCodePage": self.fileCodePage,
                "isCompatible": "Yes" if self.isCompatibleEncoding() else "No",
                "local_language": lang,
                "local_encoding": cp,
                "varlist": os.linesep.join(varlist),
                "sep": os.linesep,
                "asterisks": 70 * "*"}
        report = ("%(asterisks)s%(sep)s" +
                  "*File %(savFileName)r (%(fileSize)3.2f %(label)s) has " +
                  "%(nCols)s columns (variables) and %(nCases)s rows " +
                  "(%(nValues)s values)%(sep)s" +
                  "*The file was created with SPSS version: %(spssVersion)s%" +
                  "(sep)s" +
                  "*The interface locale is: %(ioLocale)r%(sep)s" +
                  "*The interface mode is: %(ioUtf8)s%(sep)s" +
                  "*The file encoding is: %(fileEncoding)r (Code page: " +
                  "%(fileCodePage)s)%(sep)s" +
                  "*File encoding and the interface encoding are compatible:" +
                  " %(isCompatible)s%(sep)s" +
                  "*Your computer's locale is: %(local_language)r (Code " +
                  "page: %(local_encoding)s)%(sep)s" +
                  "*The file contains the following variables:%(sep)s" +
                  "%(varlist)s%(sep)s%(asterisks)s%(sep)s")
        return report % info

    def getHeader(self, selectVars):
        """This function returns the variable names, or a selection thereof
        (as specified as a list using the selectVars parameter), as a list."""
        if selectVars is None:
            header = self.varNames
        elif isinstance(selectVars, (list, tuple)):
            diff = set(selectVars).difference(set(self.varNames))
            if diff:
                msg = "Variable names misspecified (%r)" % ", ".join(diff)
                raise NameError(msg)
            varPos = [varNames.index(v) for v in self.varNames
                      if v in selectVars]
            self.selector = operator.itemgetter(*varPos)
            header = self.selector(self.varNames)
            header = [header] if not isinstance(header, tuple) else header
        else:
            msg = ("Variable names list misspecified. Must be 'None' or a " +
                   "list or tuple of existing variables")
            raise TypeError(msg)
        return header


class SavWriter(Header):

    """ Write Spss system files (.sav, .zsav)

    Parameters:
    * Formal
    -savFileName: the file name of the spss data file. File names that end with
      '.zsav' are compressed using the ZLIB (ZSAV) compression scheme
      (requires v21 SPSS I/O files), while for file names that end with '.sav'
      the 'old' compression scheme is used (it is not possible to generate
      uncompressed files unless you modify the source code).
    -varNames: list of the variable names in the order in which they appear in
      in the spss data file.
    -varTypes: varTypes dictionary {varName: varType}, where varType == 0 means
      'numeric', and varType > 0 means 'character' of that length (in bytes)

    * Optional (the associated SPSS commands are given in CAPS)
    -valueLabels: value label dictionary {varName: {value: label}} Cf. VALUE
      LABELS (default: None)
    -varLabels: variable label dictionary {varName: varLabel}. Cf. VARIABLE
      LABEL (default: None)
    -formats: format_ dictionary {varName: printFmt} Cf. FORMATS
      (default: None)
    -missingValues: missing values dictionary {varName: {missing value spec}}
      (default: None). Cf. MISSING VALUES. For example:
          {'someNumvar1': {'values': [999, -1, -2]}, # discrete values
           'someNumvar2': {'lower': -9, 'upper':-1}, # range, cf. -9 THRU -1
           'someNumvar3': {'lower': -9, 'upper':-1, 'value': 999},
           'someStrvar1': {'values': ['foo', 'bar', 'baz']},
           'someStrvar2': {'values': 'bletch'}}
    ---The following three parameters must all three be set, if used---
    -measureLevels: measurement level dictionary {varName: <level>}
     Valid levels are: "unknown", "nominal", "ordinal", "scale",
     "ratio", "flag", "typeless". Cf. VARIABLE LEVEL (default: None)
    -columnWidths: column display width dictionary {varName: <int>}.
      Cf. VARIABLE WIDTH. (default: None --> >= 10 [stringVars] or automatic
      [numVars])
    -alignments: alignment dictionary {varName: <left/center/right>}
      Cf. VARIABLE ALIGNMENT (default: None --> left)
    ---
    -varSets: sets dictionary {setName: list_of_valid_varNames}.
      Cf. SETSMR command. (default: None)
    -varRoles: variable roles dictionary {varName: varRole}, where varRole
      may be any of the following: 'both', 'frequency', 'input', 'none',
      'partition', 'record ID', 'split', 'target'. Cf. VARIABLE ROLE
      (default: None)
    -varAttributes: variable attributes dictionary {varName: {attribName:
      attribValue} (default: None). For example: varAttributes = {'gender':
      {'Binary': 'Yes'}, 'educ': {'DemographicVars': '1'}}. Cf. VARIABLE
      ATTRIBUTES. (default: None)
    -fileAttributes: file attributes dictionary {attribName: attribValue}
      For example: {'RevisionDate[1]': '10/29/2004', 'RevisionDate[2]':
      '10/21/2005'}. Square brackets indicate attribute arrays, which must
      start with 1. Cf. FILE ATTRIBUTES. (default: None)
    -fileLabel: file label string, which defaults to "File created by user
      <username> at <datetime>" is file label is None. Cf. FILE LABEL
      (default: None)
    -multRespDefs: Multiple response sets definitions (dichotomy groups or
      category groups) dictionary {setName: <set definition>}. In SPSS syntax,
      'setName' has a dollar prefix ('$someSet'). See also docstring of
      multRespDefs method. Cf. MRSETS. (default: None)

    -caseWeightVar: valid varName that is set as case weight (cf. WEIGHT BY)
    -overwrite: Boolean that indicates whether an existing Spss file should be
      overwritten (default: True)
    -ioUtf8: indicates the mode in which text communicated to or from the
      I/O Module will be. Valid values are True (UTF-8/unicode mode, cf. SET
      UNICODE=ON) or False (Codepage mode, SET UNICODE=OFF) (default: False)
    -ioLocale: indicates the locale of the I/O module, cf. SET LOCALE (default:
      None, which is the same as locale.getlocale()[0])
    -mode: indicates the mode in which <savFileName> should be opened. Possible
      values are "wb" (write), "ab" (append), "cp" (copy: initialize header
      using <refSavFileName> as a reference file, cf. APPLY DICTIONARY).
      (default: "wb")
    -refSavFileName: reference file that should be used to initialize the
      header (aka the SPSS data dictionary) containing variable label, value
      label, missing value, etc etc definitions. Only relevant in conjunction
      with mode="cp". (default: None)

    Typical use:
    records = [['Test1', 1, 1], ['Test2', 2, 1]]
    varNames = ['var1', 'v2', 'v3']
    varTypes = {'var1': 5, 'v2': 0, 'v3': 0}
    savFileName = "test.sav"
    with SavWriter(savFileName, varNames, varTypes) as sav:
        sav.writerows(records)
    """
    def __init__(self, savFileName, varNames, varTypes, valueLabels=None,
                 varLabels=None, formats=None, missingValues=None,
                 measureLevels=None, columnWidths=None, alignments=None,
                 varSets=None, varRoles=None, varAttributes=None,
                 fileAttributes=None, fileLabel=None, multRespDefs=None,
                 caseWeightVar=None, overwrite=True, ioUtf8=False,
                 ioLocale=None, mode="wb", refSavFileName=None):
        """ Constructor. Initializes all vars that can be recycled """
        super(Header, self).__init__(savFileName, ioUtf8, ioLocale)
        self.savFileName = savFileName
        self.varNames = self.encode(varNames)
        self.varTypes = self.encode(varTypes)
        self.overwrite = overwrite
        self.mode = mode
        self.refSavFileName = refSavFileName

        self.fh = super(Header, self).openSavFile(self.savFileName, self.mode,
                                                  self.refSavFileName)
        self.myStruct = self.getStruct(self.varTypes, self.varNames, self.mode)
        self.pack_into = self.myStruct.pack_into

        self.sysmis_ = self.sysmis
        self.ioUtf8_ = ioUtf8
        self.pad_8_lookup = self._getPaddingLookupTable(self.varTypes)
        #self._getVarHandles()

        if self.mode == "wb":
            self.openWrite(self.savFileName, self.overwrite)
            self.varNamesTypes = self.varNames, self.varTypes
            self.valueLabels = valueLabels
            self.varLabels = varLabels
            self.formats = formats
            self.missingValues = missingValues
            self.measureLevels = measureLevels
            self.columnWidths = columnWidths
            self.alignments = alignments
            self.varSets = varSets
            self.varRoles = varRoles
            self.varAttributes = varAttributes
            self.fileAttributes = fileAttributes
            self.fileLabel = fileLabel
            self.multRespDefs = multRespDefs
            self.caseWeightVar = caseWeightVar
            triplet = [measureLevels, columnWidths, alignments]
            if all([item is None for item in triplet]):
                self._setColWidth10()
            self.textInfo = self.savFileName
            self.commitHeader()
            self.caseBuffer = self.getCaseBuffer()

    def __enter__(self):
        """This function returns the writer object itself so the writerow and
        writerows methods become available for use with 'with' statements"""
        return self

    def __exit__(self, type, value, tb):
        """ This function closes the spss data file."""
        if type is not None:
            pass  # Exception occurred
        self.closeSavFile(self.fh, mode="wb")
        #self.closeFile()

    def _getVarHandles(self):
        """This function returns a handle for a variable, which can then be
        used to read or write (depending on how the file was opened) values
        of the variable. If handle is associated with an output file, the
        dictionary must be written with spssCommitHeader before variable
        handles can be obtained via spssGetVarHandle. Helper function for
        __setitem__. *Not currently used*"""
        varHandles = {}
        varHandle = c_double()
        func = self.spssio.spssGetVarHandle
        for varName in self.varNames:
            retcode = func(c_int(self.fh), c_char_p(varName), byref(varHandle))
            varHandles[varName] = varHandle.value
            if retcode > 0:
                msg = "Error getting variable handle for variable %r"
                raise SPSSIOError(msg % varName, retcode)
        return varHandles

    def __setitem__(self, varName, value):
        """This function sets the value of a variable for the current case.
        The current case is not written out to the data file until
        spssCommitCaseRecord is called. *Not currently used*, but it was just
        begging to be implemented. ;-) Do NOT use in conjunction with
        wholeCaseOut. For example: self['someNumVar'] = 10
                                   self['someStrVar'] = 'foo'"""
        if not isinstance(value, (float, int, basestring)):
            raise ValueError("Value %r has wrong type: %s" %
                             value, type(value))
        varHandle = self.varHandles[varName]
        if self.varTypes[varName] == 0:
            funcN = self.spssio.spssSetValueNumeric
            retcode = funcN(c_int(self.fh), c_double(varHandle),
                            c_double(value))
        else:
            funcC = self.spssio.spssSetValueChar
            retcode = funcC(c_int(self.fh), c_double(varHandle),
                            c_char_p(value))
        if retcode > 0:
            isString = isinstance(value, basestring)
            valType = "character" if isString else "numerical"
            msg = "Error setting %s value %r for variable %r"
            raise SPSSIOError(msg % (valType, value, varName), retcode)

    def openWrite(self, savFileName, overwrite):
        """ This function opens a file in preparation for creating a new IBM
        SPSS Statistics data file"""
        if os.path.exists(savFileName) and not os.access(savFileName, os.W_OK):
            raise IOError("No write access for file %r" % savFileName)

        if overwrite or not os.path.exists(savFileName):
            # always compress files, either zsav or standard.
            if savFileName.lower().endswith(".zsav"):
                self.fileCompression = "zlib"  # only with v21 libraries!
            else:
                self.fileCompression = "standard"
        elif not overwrite and os.path.exists(savFileName):
            raise IOError("File %r already exists!" % savFileName)

    def convertDate(self, day, month, year):
        """This function converts a Gregorian date expressed as day-month-year
        to the internal SPSS date format. The time portion of the date variable
        is set to 0:00. To set the time portion if the date variable to another
        value, use convertTime."""
        d, m, y = c_int(day), c_int(month), c_int(year)
        spssDate = c_double()
        retcode = self.spssio.spssConvertDate(d, m, y, byref(spssDate))
        if retcode > 0:
            msg = "Problem converting date value '%s-%s-%s'" % (d, m, y)
            raise SPSSIOError(msg, retcode)
        return spssDate.value

    def convertTime(self, day, hour, minute, second):
        """This function converts a time given as day, hours, minutes, and
        seconds to the internal SPSS time format."""
        d, h, m, s, spssTime = (c_int(day), c_int(hour), c_int(minute),
                                c_double(float(second)), c_double())
        retcode = self.spssio.spssConvertTime(d, h, m, s, byref(spssTime))
        if retcode > 0:
            msg = ("Problem converting time value '%s %s:%s:%s'" %
                  (day, hour, minute, second))
            raise SPSSIOError(msg, retcode)
        return spssTime.value

    def spssDateTime(self, datetimeStr="2001-12-08", strptimeFmt="%Y-%m-%d"):
        """ This function converts a date/time string into an SPSS date,
        using a strptime format."""
        dt = time.strptime(datetimeStr, strptimeFmt)
        day, month, year = dt.tm_mday, dt.tm_mon, dt.tm_year
        hour, minute, second = dt.tm_hour, dt.tm_min, dt.tm_sec
        return (self.convertDate(day, month, year) +
                self.convertTime(0, hour, minute, second))

    def commitHeader(self):
        """This function writes the data dictionary to the data file associated
        with file handle 'fh'. Before any case data can be written, the
        dictionary must be committed; once the dictionary has been committed,
        no further changes can be made to it."""
        retcode = self.spssio.spssCommitHeader(c_int(self.fh))
        if retcode > 0:
            raise SPSSIOError("Problem committing header", retcode)

    def _getPaddingLookupTable(self, varTypes):
        """Helper function that returns a lookup table that maps string lengths
        to string lengths to the nearest ceiled multiple of 8. For example:
        {1:%-8s, 7:%-8s, 9: %-16s, 24: %-24s}. Purpose: Get rid of trailing
        null bytes"""
        strLengths = varTypes.values()
        return dict([(i, "%%-%ds" % (-8 * (i // -8))) for i in strLengths])

    def writerow(self, record):
        if cWriterowOK:
            cWriterow(self, record)
            return
        self.pyWriterow(record)

    def pyWriterow(self, record):
        """ This function writes one record, which is a Python list."""
        float_ = float
        for i, value in enumerate(record):
            varName = self.varNames[i]
            varType = self.varTypes[varName]
            if varType == 0:
                try:
                    value = float_(value)
                except ValueError:
                    value = self.sysmis_
                except TypeError:
                    value = self.sysmis_                    
            else:
                # Get rid of trailing null bytes --> 7 x faster than 'ljust'
                value = self.pad_8_lookup[varType] % value
                if self.ioUtf8_:
                    if isinstance(value, unicode):
                        value = value.encode("utf-8")
            record[i] = value
        self.record = record

    def writerows(self, records):
        """ This function writes all records."""
        nCases = len(records)
        for case, record in enumerate(records):
            self.writerow(record)
            self.printPctProgress(case, nCases)

if __name__ == "__main__":

    import contextlib
    import csv
    import collections
    import pprint
    import cProfile
    import pstats

    #savFileName = r"C:\Program Files\IBM\SPSS\Statistics\20\Samples\English\Employee data.sav"

   ## ---------------------------------
   ## SAV DATA DICTIONARY READER
   ## ---------------------------------

    ## ----- Typical use
    with SavHeaderReader("employee data.sav") as spssDict:
        print str(spssDict)  # prints a report of the header information
        wholeDict = spssDict.dataDictionary()

    ## ----- Copy header info from one file to another
    savFileName = "employee data.sav"
    with SavHeaderReader(savFileName) as spssDict:
        wholeDict = spssDict.dataDictionary()
    reader = SavReader(savFileName)
    writer = SavWriter('test_wholeDict.sav', **wholeDict)
    with contextlib.nested(reader, writer) as (r, w):
        for line in r:
            w.writerow(line)

    ## ---------------------------------
    ## SAV READER
    ## ---------------------------------

    ## ----- Typical use
    savFileName = "employee data.sav"
    with SavReader(savFileName, returnHeader=True) as sav:
        header = sav.next()
        for line in sav:
            pass  # do stuff

    ## ----- Explore the data file.
    ## ... Get some basic file info
    reader = SavReader(savFileName, idVar="id")
    (numVars, nCases, varNames, varTypes,
     formats, varLabels, valueLabels) = reader.getSavFileInfo()
    print "The file contains %d records" % len(reader)
    print str(reader)  # prints a file report

    ## ... Use indexing, slicing, or array slicing to access records
    print "The first six records look like this\n", reader[:6]
    print "The first record looks like this\n", reader[0]
    print "The last four records look like this\n", reader.tail(4)
    print "The first five records look like this\n", reader.head()
    if numpyOk:
        print "First column:\n", reader[..., 0]
        print "Row 4 & 5, first three cols\n", reader[4:6, :3]

    ## ... Do a binary search for records --> idVar
    print reader.get(4, "not found")             # gets 1st record where id==4
    print reader.get(4, "not found", full=True)  # gets all records where id==4

    ## ... Use a named tuple to get specific values
    record = collections.namedtuple("_", " ".join(varNames))(*reader[0])
    print record.id, record.educ, record.salary, record.bdate

    reader.close()

    ## ----- Convert file into .csv
    savFileName = "employee data.sav"
    csvFileName = "test_out.csv"
    sav = SavReader(savFileName, ioLocale="dutch")  # locale spec depends on OS
    f = open(csvFileName, "wb")
    with contextlib.nested(sav, f) as (sav, f):
        writer = csv.writer(f)
        for line in sav:
            writer.writerow(line)
        print "Done! Csv file written: %s" % f.name

    ## ---------------------------------
    ## SAV WRITER
    ## ---------------------------------

    ## ----- Write many rows
    savFileName = "another_test.zsav"  # .zsav = zlib compressed (--> v21 libs)
    records = [['Test1', 1, 1, '2010-08-11'], ['Test2', 2, 1, '1910-01-12']]
    varNames = ['var1', 'var2', 'var3', 'bdate']
    varTypes = {'var1': 50, 'var2': 0, 'var3': 0, 'bdate': 10}
    with SavWriter(savFileName, varNames, varTypes) as sav:
        sav.writerows(records)
        print "Done! %s" % sav.savFileName

    savFileName = "employee data_OUT.sav"
    varNames = ['id', 'gender', 'bdate', 'educ', 'jobcat', 'salary',
                'salbegin', 'jobtime', 'prevexp', 'minority']
    varLabels = {'gender': 'guys/gals'}
    varTypes = {'salary': 0, 'jobcat': 0, 'bdate': 0, 'minority': 0,
                'prevexp': 0, 'gender': 1, 'salbegin': 0, 'jobtime': 0,
                'educ': 0, 'id': 0}
    varSets = {'SALARY': ['salbegin', 'salary'],
               'DEMOGR': ['gender', 'minority', 'educ']}
    varAttributes = {'salary': {'DemographicVars': '1'},
                     'jobcat': {'DemographicVars': '1'},
                     'gender': {'Binary': 'Yes'},
                     'educ': {'DemographicVars': '1'}}
    fileAttributes = {'TheDate[2]': '10/21/2005',
                      'RevisionDate[2]': '10/21/2005',
                      'RevisionDate[1]': '10/29/2004'}
    missingValues = {'educ': {'values': [1, 2, 3]}, 'gender': {'values': 'x'}}
    records = [[1.0, 'm       ', 11654150400.0, 15.0, 3.0,
                57000.0, 27000.0, 98.0, 144.0, 0.0],
               [2.0, 'm       ', 11852956800.0, 16.0, 1.0,
                40200.0, 18750.0, 98.0, 36.0, 0.0]]
    with SavWriter(savFileName, varNames, varTypes,
                   varLabels=varLabels, varSets=varSets,
                   missingValues=missingValues, varAttributes=varAttributes,
                   fileAttributes=fileAttributes) as sav:
        sav.writerows(records)
        print "Done! %s" % sav.savFileName

    ## ----- Write one row
    # ... var1 is a 5-char string var, the others are numerical:
    # ... formats, varLabels, valueLabels, missingValues etc. may also be
    # ... None (default).
    records = [['Test1', 1, 1, '2010-08-11'], ['Test2', 2, 1, '1910-01-12']]
    varNames = ['var1', 'v2', 'v3', 'bdate']
    varTypes = {'var1': 41, 'v2': 0, 'v3': 0, 'bdate': 0}
    formats = {'var1': 'A41', 'v2': 'F3.1', 'v3': 'F5.1', 'bdate': 'EDATE40'}
    missingValues = {'var1': {'values': ['Test1', 'Test2']},
                     'v2': {'values': 1}}
    varLabels = {'var1': 'This is variable 1',
                 'v2': 'This is v2!',
                 'bdate': 'dob'}
    valueLabels = {'var1': {'Test1': 'Test1 value label',
                            'Test2': 'Test2 value label'},
                   'v2': {1: 'yes', 2: 'no'}}
    # This also shows how date fields can be converted into spss dates.
    # Spss dates are *stored* as the number of seconds since Oct 14, 1582, but
    # *displayed* as <format>. In this case they are displayed as EDATE
    # (European date, cf. ADATE = American date), ie. as dd.mm.yyyy
    savFileName = "test1.sav"
    with SavWriter(savFileName, varNames, varTypes,
                   valueLabels, varLabels, formats) as sav:
        pos = varNames.index("bdate")
        for record in records:
            record[pos] = sav.spssDateTime(record[pos], "%Y-%m-%d")
            sav.writerow(record)
        print "Done! %s" % sav.savFileName

    ## a test to check if non-ascii encodings work well
    ## source: http://www.omniglot.com/language/phrases/hello.htm
    greetings = [
        [0, 'Arabic', u'\u0627\u0644\u0633\u0644\u0627\u0645\u0020\u0639\u0644\u064a\u0643\u0645'],
        [1, 'Assamese', u'\u09a8\u09ae\u09b8\u09cd\u0995\u09be\u09f0'],
        [2, 'Bengali', u'\u0986\u09b8\u09b8\u09be\u09b2\u09be\u09ae\u09c1\u0986\u09b2\u09be\u0987\u0995\u09c1\u09ae'],
        [3, 'English', u'Greetings and salutations'],
        [4, 'Georgian', u'\u10d2\u10d0\u10db\u10d0\u10e0\u10ef\u10dd\u10d1\u10d0'],
        [5, 'Kazakh', u'\u0421\u04d9\u043b\u0435\u043c\u0435\u0442\u0441\u0456\u0437 \u0431\u0435'],
        [6, 'Russian', u'\u0417\u0434\u0440\u0430\u0432\u0441\u0442\u0432\u0443\u0439\u0442\u0435'],
        [7, 'Spanish', u'\xa1Hola!'],
        [8, 'Swiss German', u'Gr\xfcezi'],
        [9, 'Thai', u'\u0e2a\u0e27\u0e31\u0e2a\u0e14\u0e35'],
        [10, 'Walloon', u'Bondjo\xfb'],
        [11, 'Telugu', u'\u0c0f\u0c2e\u0c02\u0c21\u0c40'],
                 ]
    savFileName = "greetings.sav"
    varNames = ['line', u'Bondjo\xfb', 'greeting']
    varTypes = {'line': 0, u'Bondjo\xfb': 20, 'greeting': 50}
    valueLabels = {u'Bondjo\xfb': {'Thai': u'\u0e2a\u0e27\u0e31\u0e2a\u0e14\u0e35'}}
    missingValues = {'line': {'lower': 0, 'upper': 9}, u'Bondjo\xfb': {'values': u'\xa1Hola!'}}
    varLabels = {'greeting': u'\u0627\u0644\u0633\u0644\u0627\u0645\u0020\u0639\u0644\u064a\u0643\u0645'}
    with SavWriter(savFileName, varNames, varTypes, valueLabels, varLabels,
                   missingValues=missingValues, ioUtf8=True) as sav:
        sav.writerows(greetings)

    with SavReader(savFileName, ioUtf8=True)as sav:
        for lino, line in enumerate(sav):
            print lino, "%s -- %s" % (line[1].strip(), line[2]), line

    with SavHeaderReader(savFileName, ioUtf8=True)as spssDict:
        wholeDict = spssDict.dataDictionary()
        #print wholeDict["varLabels"]["greeting"]
        print unicode(spssDict)
        pprint.pprint(wholeDict)
