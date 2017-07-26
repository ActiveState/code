import win32com
import win32com.client

#depth: 0=immediate depth,1=w/children,infinity=all the way down

def return_dav(dav,dav_response=''):
    if dav.status > 299:
        raise 'webdav error',str(dav.status)+':'+dav.statusText
    if dav_response=='dav': return dav
    elif dav_response=='xml': return dav.responseXML
    #by default return text
    return dav.responseText    

def search_request(url,request,logon='',passwd='',depth=1):
   dav = win32com.client.Dispatch('Microsoft.XMLHTTP')
   dav.open('SEARCH',url, 0,logon, passwd)
   dav.setRequestHeader("Content-type:", "text/xml")
   dav.setRequestHeader("depth", depth)    
   dav.setRequestHeader("Translate", "f")
   dav.send(request)
   return return_dav(dav)  
   
def propfind(url,request,logon='',passwd='',depth=1):
   dav = win32com.client.Dispatch('Microsoft.XMLHTTP')
   dav.open('PROPFIND',url, 0,logon, passwd)
   dav.setRequestHeader("Content-type:", "text/xml")
   dav.setRequestHeader("depth", depth)   
   dav.setRequestHeader("Translate", "f")
   dav.send(request)
   return return_dav(dav)   

def delete(url='',logon='',passwd=''):
    dav = win32com.client.Dispatch('Microsoft.XMLHTTP')
    dav.open('DELETE',url, 0,logon, passwd)
    dav.send()
    return return_dav(dav)  

#create a collection
def mkcol(url='',logon='',passwd=''):
    dav = win32com.client.Dispatch('Microsoft.XMLHTTP')
    dav.open('MKCOL',url,0)
    dav.setRequestHeader('Content-Type:','text/xml')
    dav.send()
    return return_dav(dav)  

url='http://server/exchange/username/inbox/test'

pfind='''<?xml version="1.0" ?>
<D:propfind xmlns:D='DAV:' xmlns:m='urn:schemas:httpmail:'>
  <D:prop> <m:from/> <m:to/> <m:subject/> </D:prop>
</D:propfind>'''

search='''<?xml version="1.0"?>
<D:searchrequest xmlns:D = "DAV:" >
    <D:sql>SELECT "DAV:displayname"  FROM "%s"</D:sql>
</D:searchrequest>
'''%(url)

#may need to provide username and password
print propfind(url,pfind)
print search_request(url,search)
mkcol(url+'/test3') #make a folder
delete(url+'/test3') #remove a folder
