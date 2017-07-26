#------------------------------------------------------
#Bluetooth Functions
#Scanning is done by BluetoothScan()
#Device serive browsing is done by GetInfo(DevAdd)
#logging of known devices
# announce when device comes into range
#announce when device goes out of range
# announce when device changes name
#mmmm ambitious but what the hell....
#Written by SIone
import sys
import os
import time
import urllib, string
global scan,lastscan,test
scan=[]#-----------------for the current scan of bluetooth device
lastscan=[]#-------------where to save scan results after comparison.
test=[]#-----------------for assement of scans (tempory copy)

print "Bluetooth monitoring program now running"
def morefound():#----Used if the scan just done has more items than the previous scan.
    for v in scan:#---------------------------step through the list of devices found in the scan just done
        c=0#----------------------------------reset the match counter to zero
        for x in lastscan:#-------------------step though the list of devices from the previous scan.
            if (v==x):#----------------------Test for matching device names
                c=c+1#-----------------------and increment the counter
        if (c==0):#---------------------------If the counter is zero then add the item from the new scan list to
            test.append(v)#---------------------the test tempory list
            
def lessfound():#-------------------------Used if the scan just done has less items than the last scan.
    for x in lastscan:#-------------------Step through the items in the last scan list
        c=0#------------------------------ and reset the counter
        for v in scan:#-------------------- Step through the items in the list from the scan just done.
            if (v==x):#---------------------IF device name matches in both lists
                c=c+1#------------------------then increment the match counter.
        if (c==0):#-------------------------IF the counter remains zero then device name is new
            test.append(x)#------------------so add it to the tempory list
            
def samefound():#---------------------------------used as a sanity check when the status of devices is the same.
    pass
    print"------ SAME FOUND!!!!!!"
            
def ndsSay(ndsWords):#----------Function for talking
    print ndsWords#-------------DEBUG! print word to say in Idle.
    zcmd='espeak "'+ndsWords+'"'#concatinate the command
    f=os.popen(zcmd)#------------send the command to terminal.

def BluetoothScan():#-----------------------Performs the actual scan for Bluetooth Devices
    f = os.popen("hcitool scan")#-----------Sends the command to the terminal
    for i in f.readlines():#-----------------Step through the list of information returned from the above command.
        if (i.find(":") != -1):#-------------search for the ":" symbol.
            DevAdd =i[1:18]#-----------------If it's found then strip out the device bluetooth address
            DevLab=i[19:-1]#------------------and then strip out the device name
            x=DevLab#------------------------a copy of the Device label/name
            scan.append(x)#-------------------add the device to the array
            
while 1:#------------------------------------------start to loop forever
    BluetoothScan()#--------------------------------Perform the scan for devices
    n=len(scan)#------------------------------------Get the number of elements of the scan just performed
    o=len(lastscan)#--------------------------------Get the number of elements of the previous scan
    if (n>o):#--------------------------------------If there are more devices found now
        morefound()#---------------------------------then find out which devices names have come into range.
        abc ="Devices arrived into range:"#----------the sentence is prepared for......
        print abc#------------------------------------ display in idle
        ndsSay(abc)#---------------------------------- and announcement
        for lines in test:#------------------------------now stepping over the devices fresh into range
            abc = lines+" at "+str(time.asctime())#----- and preparing a sentance for.......
            print abc#---------------------------------- display in IDLE
            ndsSay(lines)#------------------------------ and announcement
            log = open("BlueMon.txt","a")#------------Open the logfile in append mode
            log.write("Entered Range: ")#-------------then write this
            log.write(abc)#---------------------------and the details about the device thats come into range
            log.write("\n")#--------------------------and add a new line to make the log file easy to read by eye.
            log.close()#------------------------------ and then close it off.
    if (o>n):#--------------------------------------If there are fewer devices found now than last time.....
        lessfound()#-------------------------------- Then find out which devices had left range
        abc= "Devices now out of range:"#----------- prepare a sentance for.....
        print abc#----------------------------------  display in IDLE
        ndsSay(abc)#--------------------------------  and then make the announcement.
        for lines in test:#-------------------------  now go over the list of devices now out of range
            abc= lines+" at "+str(time.asctime())#--  and create a sentance with the details
            print abc#------------------------------  and display the sentanc in IDLE
            ndsSay(lines)#--------------------------  then make the announcement
            log = open("BlueMon.txt","a")#----------   open the log file
            log.write("Left Range: ")#--------------   and write this information to it
            log.write(abc)#-------------------------   and the details about the device label etc,
            log.write("\n")#------------------------  with the new line to tidy the file up for us humans
            log.close()#---------------------------- and then close it up
    if (o==n):#-----------------------------------------this is for sanity checking, to make sure we know that the
        samefound()#------------------------------------ program is infact still running

    lastscan=scan#---------------------------------now make the current scan list the last scan list
    scan=[]#-----------------------------------------and clear the current scan list
    test=[]#----------------------------------------- and the tempory list used for testing
    n=0#--------------------------------------------reset the length indicator of the new scan list
    o=0#---------------------------------------------and the indicator of the last scan list
    time.sleep(5)#-----------------------------------wait 5 seconds...
    print ".",#--------------------------------------and print a fullstop.
    time.sleep(5)#------------------------------------this is done to stop problems that occur when the 
    print ".",#--------------------------------------- bluetooth radio is hammered with scan commands
    time.sleep(5)#------------------------------------ so its best to wait about 30 seconds between scans
    print ".",#--------------------------------------- to enable every thing to flow nicely behind the scenes
    time.sleep(5)
    print ".",
    time.sleep(5)
    print ".",
    time.sleep(5)
    print ".",
    time.sleep(5)
    print ".",
    time.sleep(5)
    print ".",
    time.sleep(5)
    print ".",
    time.sleep(5)
    print ".",
    time.sleep(5)
    print ".",
    time.sleep(5)
    print ".",
    time.sleep(5)
    print "."
    time.sleep(5)
    print#---------------------------------at this point the progam will loop back and do another scan!
