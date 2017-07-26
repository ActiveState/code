#####################################################
# title: BashReader
# auther: max baseman
# date: 03/19/07 4:23
# email: dos.fool@gmail.com
# discription: checks bash and writes it
#####################################################
import urllib2
from sys import stdout
from time import sleep
bash=urllib2.urlopen("http://www.bash.org/?latest")
WEB=open("/Users/thefool/Desktop/max/programs/sites/bash.html",'w') # change to path of html 

for line in bash:
    WEB.write(line)
    
