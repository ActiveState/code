"""
This sample connects to the running instances of IE on your computer and prints out
the URL, Cookie- if any, and the HTML content of the site.

You need to generate stub files for IE and MSHTML using the readtlb tool of ctypes.

python ctypes\com\tools\readtlb.py c:\winnt\system32\MSHTML.TLB > mshtml.py
python ctypes\com\tools\readtlb.py C:\windows\system32\SHDOCVW.DLL > ie6.py

Known Issues:
Filters out Explorer sinces we don't expect it to have HTML content or cookies. Explorer and IExplore are part of the Shell and therefore IShellWindows.

The mshmtl.py file must be fixed manually by inserting this at the top, otherwise you get NameErrors:
 
 LONG_PTR = c_long
 UINT_PTR = c_uint 
 wireHGLOBAL = wireHWND = wireHDC = wireHBITMAP = c_int 
 SAFEARRAY = POINTER # I"m quite sure this is wrong

usage:
python IEconnect.py

You need the good ctypes module from http://starship.python.net/crew/theller/ctypes/

Sample based on information from 
http://support.microsoft.com/default.aspx?scid=http://support.microsoft.com:80/support/kb/articles/Q176/7/92.ASP&NoWebContent=1

By Eric Koome
email ekoome@yahoo.com

"""
from ctypes import *
from ctypes.com import GUID, HRESULT, IUnknown, CreateInstance
from ctypes.com.automation import IDispatch, VARIANT, BSTR, oleaut32
from ctypes.wintypes import DWORD
from win32con import NULL
from ie6 import ShellWindows, IShellWindows, InternetExplorer, IWebBrowser2 #generated from SHDOCVW.DLL
from mshtml import IHTMLDocument2, IHTMLElement # generated using MSHTML.TLB

            
def IsInternetExplorer(name):
    import re
    from types import NoneType
    if type(re.search(r'iexplore.exe$',name)) != NoneType:
        return True
    else:
        return False
    
# Lets create an instance of ShellWindows Interface
pItf = CreateInstance(ShellWindows)
windows = pItf

#Get num of IE window by using IShellwindows
nCount = c_long()
hret = windows._get_Count(byref(nCount))
#print "nCount", nCount
for i in range(nCount.value):
        
    #Get IDispatch interfaces from IshellWindows
    disp = POINTER(IDispatch)()
    va = VARIANT(i)
    from ctypes.com.automation import VT_I4

    # apparently IE doesn't like VT_INT (which automation uses),
    # it has to be VT_I4
    oleaut32.VariantChangeType(byref(va), byref(va), 0, VT_I4)
    hret = windows.Item(va, byref(disp))
    oleaut32.VariantClear(byref(va))
    #print "disp",disp

    #Get IwebBrowser2 Interfaces from IDispatch
    browser = POINTER(IWebBrowser2)()
    if disp != NULL:
            hret = disp.QueryInterface(byref(IWebBrowser2._iid_),
                                       byref(browser))
            #print "browser", browser
            
    #Get the full path of the EXE (IE or explorer)
    if browser != None:
        Name = BSTR()
        hret = browser._get_FullName(byref(Name))
        
        #Lets Check whether we are dealing with IE 
        if IsInternetExplorer(Name.value):

            #Get browsing URL string
            url= BSTR()
            hret = browser._get_LocationURL(byref(url))
            print "url", url.value

            #Get IHTMLDocument2 from IWebBrowser2
            htmlDisp = POINTER(IDispatch)()
            hret = browser._get_Document(byref(htmlDisp))
            #print "htmlDisp", htmlDisp
            doc = POINTER(IHTMLDocument2)()
            if htmlDisp != NULL:
                try:
                    hret = htmlDisp.QueryInterface(byref(IHTMLDocument2._iid_), byref(doc))
                    #print "doc", doc
                except:
                    pass

            #Call get_cookie method of IHTMLDocument2
            if doc != NULL:
                cookie = BSTR()
                try:
                    hret = doc._get_cookie(byref(cookie))
                    print "cookie", cookie
                except:
                    pass
                
                #Get IHTMLElement from IHTMLDocument2
                element = POINTER(IHTMLElement)()
                hret = doc._get_body(byref(element))
                #print "element", element
                
                #Call get_outerHTML of IHTMLElement
                if element != NULL:
                    html = BSTR()
                    try:
                        hret = element._get_outerHTML(byref(html))
                        print "html",html
                    except:
                        pass
        

    
    
