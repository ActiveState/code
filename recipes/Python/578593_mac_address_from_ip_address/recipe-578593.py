import os,re
file=open('/root/info.txt','w+')

r=raw_input('ip\n\r')
os.system('ping -c 1 '+r+' > /root/info.txt')
os.system("arp -a "+r+" | awk '{print $4}'  > /root/info.txt")
data=file.read()
print data
