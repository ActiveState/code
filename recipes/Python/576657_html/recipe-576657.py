#coding:utf-8

import HTMLParser
html=HTMLParser.HTMLParser


class   MyHtmlparser(html):
        def __init__(self):
                html.__init__(self)
                self.lidata=[]
                self.dic={}#用来登记获得的tag和其相应的属性

        
        def handle_data(self,data):
                self.lidata.append(data)

        def handle_starttag(self,tag,attrs):
                self.dic[tag]=attrs
                




        def handle_endtag(self,tag):
                pass
                
mydir="c://html//"
f=file(mydir+"1.htm")
in_data=f.read()
f.close()
my = MyHtmlparser()
my.feed(in_data)


for i in my.lidata:
        print i

for i in my.dic:
        print i 
