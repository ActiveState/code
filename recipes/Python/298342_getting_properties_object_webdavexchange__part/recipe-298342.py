import win32com,win32com.client
from xml.parsers import expat

def propfind(url,request,logon='',passwd='',depth=1):
    ##pfind='''<?xml version="1.0" ?>
    ##<D:propfind xmlns:D='DAV:' xmlns:m='urn:schemas:httpmail:'>
    ##  <D:prop> <m:from/> <m:to/> <m:subject/> </D:prop>
    ##</D:propfind>'''
    ##dav=propfind(url,pfind)
   dav = win32com.client.Dispatch('Microsoft.XMLHTTP')
   dav.open('PROPFIND',url, 0) #,Logon, passwd)
   dav.setRequestHeader("Content-type:", "text/xml")
   dav.setRequestHeader("depth", depth) #0=immediate,1=w/children,infinity=all 
   dav.setRequestHeader("Translate", "f")
   dav.send(request)
   return dav.responseText  


class xml_process:
    def __init__(self,the_data,fields=[],keep_prefix=0,keep_attr=0):
        self.results=[]
        self.cur_name=None
        self.tmp=[]
        self.the_data=the_data
        self.p=expat.ParserCreate()
        self.p.StartElementHandler=self.start
        self.p.EndElementHandler=self.end
        self.p.CharacterDataHandler=self.data
        self.fields=fields
        self.keep_prefix=keep_prefix
        self.keep_attr=keep_attr
    def clean(self,data):
        tmp=''.join(data)
        return ' '.join(tmp.split())
    def start(self,name,attrs): 
        if not self.cur_name: self.cur_name=name
        tmp_name=self.cur_name
        if not self.keep_prefix:
            if self.cur_name[1]==':': tmp_name=self.cur_name[2:]
        self.attrs=attrs
        if name != self.cur_name:
            if not self.attrs or not self.keep_attr:
                if not self.fields or tmp_name.lower() in self.fields:
                    self.results.append( {tmp_name:self.clean(self.tmp)})
            else:
                if not self.fields or tmp_name.lower() in self.fields:
                 self.results.append( { tmp_name:{self.clean(self.tmp):attrs}})
            self.tmp=[]
            self.cur_name=name
    def data(self,info):  self.tmp.append(info)
    def end(self,name): pass
    def parse(self):
        if 'xml' not in self.the_data[0:50].lower(): return []
        self.p.Parse(self.the_data,1)
        results=self.results
        if self.fields:
            filter_cache={}
            results=[{}]
            
            for i in self.fields: filter_cache[i]=None
            for row in self.results:
                k,v=row.items()[0]
                #check if filter_cache is full
                full=0
                for i in filter_cache:
                    if not filter_cache[i]:
                        filter_cache[i]=1
                        full=0;break
                    full=1
                if full:
                    for i in self.fields: filter_cache[i]=None
                    full=0
                    results.append({})
                if k not in results[-1]:
                    results[-1][k]=v
        return results

#Props={}

def all_props(url,raw=0,namespace=0,logon='',passwd=''):  
    request='''<?xml version="1.0" ?>
    <D:propfind xmlns:D="DAV:">
            <D:allprop/>
    </D:propfind>'''

    text=propfind(url,request,depth=0,logon=logon,passwd=passwd)
    if raw:  return text
    elif namespace:
        xmlns=text[text.find('multistatus'):]
        xmlns=xmlns[:xmlns.find('>')]
        xmlns_ref={}
        for i in xmlns.split('xmlns:'): 
            j=i.split('=')
            if len(j)==2:
                    k,v=j
                    xmlns_ref[k]=v
        result=xml_process(text,keep_prefix=1)
        field_ref={}
        for i in result.parse(): 
            l=i.keys()[0] #l=d:busystatus
            if ':' not in l: continue
            k,v=l.split(':')
            field_ref[v]=xmlns_ref[k]
        return field_ref
    else:    
        result=xml_process(text)
        result2=[]
        for i in result.parse(): 
            field=i.keys()[0]
            result2.append(field)
        return result2


url='http://host/exchange/user/Calendar/'
print all_props(url)
print all_props(url,namespace=1)
print all_props(url,raw=1)
