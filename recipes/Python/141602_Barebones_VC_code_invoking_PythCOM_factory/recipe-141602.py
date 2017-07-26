# Python code
from win32com . server . register import UseCommandLine
from win32api import MessageBox
from win32com . client import Dispatch
from win32ui import MessageBox

class StemmerFactory :
    _reg_clsid_ = "{602D10EB-426C-4D6F-A4DF-C05572EB780B}"
    _reg_desc_ = "LangTech Stemmer"
    _reg_progid_ = "LangTech.Stemmer"
    _public_methods_ = [ 'new' ]

    def new ( self, scriptFile ) :
        self . scriptFile = scriptFile
        stemmer = Dispatch ( "LangTech.Stemmer.Product" )
        return stemmer

class Stemmer :
    _reg_clsid_ = "{B306454A-CAE6-4A74-ACAD-0BB11EF256DD}"
    _reg_desc_ = "LangTech Stemmer Product"
    _reg_progid_ = "LangTech.Stemmer.Product"
    _public_methods_ = [ 'stemWord' ]

    def stemWord ( self, word ) :
        # extremely simple stemming: if the word ends in 's' then drop the 's'
        if word [ -1 ] == "s":
            return word [ : -1 ]
        else:
            return word

if __name__ == '__main__' :
    UseCommandLine ( StemmerFactory )
    UseCommandLine ( Stemmer )

#----------------------------------------
#
# C++

#include <comdef.h>
#include <initguid.h>

DEFINE_GUID(CLSID_StemmerFactory,
  0x602D10EB, 0x426C, 0x4D6F, 0xA4, 0xDF, 0xC0, 0x55, 0x72, 0xEB, 0x78, 0x0B);

DISPID rgDispId ;
OLECHAR * rgszNames [ ] = { OLESTR ( "new" ) };
DISPPARAMS DispParams;
VARIANT VarResult;
EXCEPINFO excepinfo;
UINT uArgErr;
VARIANTARG * pvarg = NULL;
_bstr_t stemmedWord;
HRESULT hr;
IDispatch * stemmerFactory;
IDispatch * stemmer;

if ( FAILED ( hr = CoInitialize ( NULL ) ) ) {
    MessageBox ( 0, "CoInitialize failure", "Fault", MB_OK );
    break;
}

if ( FAILED ( hr = CoCreateInstance (
    CLSID_StemmerFactory,
    NULL,
    CLSCTX_INPROC_SERVER,
    IID_IDispatch,
    ( LPVOID * ) & stemmerFactory ) ) ) {
    MessageBox ( 0, "CoCreateInstance failure", "Fault", MB_OK );
    break;
}

if ( FAILED ( hr = stemmerFactory -> GetIDsOfNames (
    IID_NULL,
    rgszNames,
    1,
    LOCALE_SYSTEM_DEFAULT,
    & rgDispId
    ) ) ) {
    MessageBox ( 0, "GetIDsOfNames failure", "Fault", MB_OK );
    break;
}

DispParams.cArgs = 1;
DispParams.cNamedArgs = 0;
DispParams.rgdispidNamedArgs = 0;

pvarg = new VARIANTARG [ DispParams . cArgs ];
if ( pvarg == NULL ) {
    MessageBox ( 0, "Insufficient 1st memory", "Fault", MB_OK );
    break;
}

pvarg -> vt = VT_BSTR;
pvarg -> bstrVal = SysAllocString ( L"engRules.pl" );

DispParams.rgvarg = pvarg;

if ( FAILED ( hr = stemmerFactory -> Invoke (
    rgDispId,
    IID_NULL,
    LOCALE_SYSTEM_DEFAULT,
    DISPATCH_METHOD,
    & DispParams,
    & VarResult,
    & excepinfo,
    & uArgErr
    ) ) ) {
    MessageBox ( 0, "1st Invoke failure", "Fault", MB_OK );
    break;
}

delete ( pvarg );

stemmer = VarResult.pdispVal;

pvarg = new VARIANTARG [ DispParams . cArgs ];
if ( pvarg == NULL ) {
    MessageBox ( 0, "Insufficient 2nd memory", "Fault", MB_OK );
    break;
}

pvarg -> vt = VT_BSTR;
pvarg -> bstrVal = SysAllocString ( L"cats" );

DispParams.rgvarg = pvarg;

if ( FAILED ( hr = stemmer -> Invoke (
    rgDispId,
    IID_NULL,
    LOCALE_SYSTEM_DEFAULT,
    DISPATCH_METHOD,
    & DispParams,
    & VarResult,
    & excepinfo,
    & uArgErr
    ) ) ) {
    MessageBox ( 0, "2nd Invoke failure", "Fault", MB_OK );
    break;
}

delete ( pvarg );

stemmedWord = VarResult.bstrVal;

MessageBox (
    0,
    ( const char * ) stemmedWord,
    "Resulting Stemmed Word",
    MB_OK
    );

CoUninitialize ( );
