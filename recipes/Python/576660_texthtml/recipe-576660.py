#coding:gb2312
#基本完成了参照文本文档产生html换行的功能
#下一步是：产生关于定位键table的处理
#然后是特殊符号的处理
import re
break_win=chr
0x0d
+chr
0x0a
bre="\x0d\x0a"
word="[^
\x0d\x0a
]+"
bre_jihe=re.compile
bre
word_jihe=re.compile
word
input=file
"d://The Zen of Python.txt","r"
.read
print bre_jihe.findall
input
word_list=word_jihe.findall
input
#print word_list
f_out=file
"c://output.txt","w"
for i in word_list:
print i
out=i+"
"
f_out.write
out
f_out.close
