#coding:utf-8
#学习分析html。


mydir="c://html//"
f=file(mydir+"1.htm")
in_data=f.read()

#print in_data
f.close()



in_data="<html><head>wo</head><script>weofewf</script></html>"

#检查下文件是不是得到了

import HTMLParser




class MyParser(HTMLParser.HTMLParser):

   
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.script=[]
        self.li=[]
        self.flag=1

##    #输出所有的链接的东西   
##    def handle_starttag(self, tag, attrs):
##        # 这里重新定义了处理开始标签的函数
##        if tag == 'a':
##            # 判断标签<a>的属性
##            for name,value in attrs:
##                if name == 'href':
##                    print value
                    

##    #处理文档类型声明 
##    def handle_decl(self,decl):
##        print decl



    #处理标签中所夹的数据 
    def handle_data(self,data):
        if self.flag==1:
            self.script.append(data)
        else:
            self.li.append(data)


    def handle_starttag(self, tag, attrs):
        if  tag=="<script>":
            self.flag=1
        else:
            self.flag=0



    def handle_endtag(self,tag):
        print "<=="+tag

   
    #输出所有的可见的文字。图片，链接，格式，排版全部去掉。                
##MyParser类基于原来的类。但是我们根本没有写什么东西，为何
##还可以工作呢？显然所有的基本判断我们原来的类已经给我们分析了。
##
##
##但是我想把这些数据组合的拿出来，我应该如何做呢？




#我想把一个特定的标签中所夹的数据给显示出来，该如何做呢？
#handle_data把它遇到的所有的数据都显示出来了，不好，如何进行选择了。

my = MyParser()
# 传入要分析的数据，是html的。
#原来我们可以在已经存在的类上面添加我们自己的函数
my.feed(in_data)
print my.script
for i in  my.li:
    print i
