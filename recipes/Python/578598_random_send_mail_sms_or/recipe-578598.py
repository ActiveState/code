#/usr/bin/env python
# -*- coding: utf-8 -*-

import time, random, sys, os, smtplib

if sys.version < '3':
    from Tkinter import *
else:
    from tkinter import *

randommsgnext="randommsgnext.txt"
# delay between two msg is  2-5 hours
mydelayfrom=2 * 3600 #
mydelayto=5 * 3600

#which time to call me up, 0 is Monday
timesOn=((0,"07:00","09:55"),
         (0,"11:40","22:00"),
         (1,"07:00","11:30"),
         (1,"15:15","22:00"),
         (2,"07:00","10:45"),
         (2,"14:20","22:00"),
         (3,"14:20","22:00"),
         (4,"07:00","12:30"),
         (4,"14:20","22:00"),
)

def sendMail():
    # sends mail
    s = smtplib.SMTP(smtp)
    s.login(name, password)

    subject="Reminder"
    fromaddr=fromadr
    toaddrs= [toadr]
    text= "Do what you should do.\n%s" % time.ctime()
    msg = ("Subject: %s\nFrom: %s\nTo: %s\n\n%s" % (subject, fromaddr, ", ".join(toaddrs), text))

    s.sendmail(fromaddr, toaddrs, msg)
    s.quit()

def sendSMS():
    # sends sms
    message={'user': user, 'password': password, 'sender': fromnumber, 'recipient': tonumber, 'message': "goodbye"}
    if sys.version < '3':
        import urllib
        params = urllib.urlencode(message)
        f=urllib.urlopen(http, params)
    else:
        import urllib.parse
        import urllib.request
        params = urllib.parse.urlencode(message)
        f = urllib.request.urlopen(http % params)

def showMessage():
    # show tkinter box
    root=Tk()
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x, y))
    root.protocol('WM_TAKE_FOCUS', root.update )
    root.wait_visibility(root)
    root.attributes('-topmost',1)
    label=Label(root, text="S bohem", width="10").pack({"side": "left"})
    button=Button(text="OK", width="10", command=lambda:root.destroy()).pack()
    root.mainloop()



def hours2dec(what):
    # convert 5:30 to 5.5
    if type(what)==type(""):
        what=what.split(":")
    return int(what[0])+int(what[1])/60.0


def checktime(nowtime):
    # send msg only at timesOn
    for day, timefrom, timeto in timesOn:
        timefromdec= hours2dec(timefrom)
        timetodec=hours2dec(timeto)
        timenowdec=hours2dec([nowtime.tm_hour,nowtime.tm_min])

        if nowtime.tm_wday == day and timefromdec<=timenowdec<=timetodec:
            return True

    return False

def timenextwritef():
    # write the next time to file
    f=open(randommsgnext,"w")
    timenext=time.mktime (nowtime)+delaysec
    f.write(time.ctime(timenext)+"\n")
    f.close()
    os.utime(randommsgnext, None)

nowtime=time.localtime()
os.chdir(os.path.dirname(sys.argv[0]))
while True:
    # run indefinitely
    delaysec=random.randint(mydelayfrom,mydelayto)
    timenextwritef()
    time.sleep(delaysec)   # sleep
    nowtime=time.localtime()
    if checktime(nowtime):
        print (str(nowtime.tm_hour)+":"+str(nowtime.tm_min)+":"+str(nowtime.tm_sec))
#         sendMail()
#         sendSMS()
#         showMessage()
