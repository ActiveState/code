##~ Veysel Nantu
import poplib
import time
import subprocess
from email import parser
from datetime import datetime

#-------------------------------------
# Send an e-mail to a g-mail address that will shutdown the computer
#
# Acceptable format: SHUTDOWN YOURSELF {DATE}
# Acceptable DATE format: YEAR-MONTH-DAY
# Example: SHUTDOWN YOURSELF 2016-26-05
# 
# To avoid from unknown shutdown mails
# We will check later if the mail is coming from a specific address
# So that only one e-mail address can shutdown your computer
# And you will decide that e-mail address
#-------------------------------------

#check the mail is came from the correct address
# for example;
# assume you enter 'mymail@hotmail.com' to from_addr
# we will check it later if the mail is coming from 'mymail@hotmail.com'

from_addr = input ("From address: ")

while True:

    #connect gmail
    pop_conn = poplib.POP3_SSL('pop.gmail.com')
    
    #make sure we are connected to POP, get POP-WELCOME message
    
    print ("\n"+str(pop_conn.getwelcome())[6:50])
    
    pop_conn.user('my_mail_address@gmail.com') #e-mail address
    pop_conn.pass_('my_mail_password') #password

    #check how many mails we have
    mail_info = pop_conn.stat()
    print ("Number of new emails: %s (%s bytes)" % mail_info)

    nmails = mail_info[0]

    #search for SUBJECT-FROM-DATE elements in the mails
    for i in range(nmails):
        for email in pop_conn.retr(i+1):
            try:
                for mail in email:
                    if "Subject" in str(mail):
                        t = str(mail)
                    if "From" in str(mail):
                        fr = str(mail)
                    if "Date" in str(mail):
                        dt = str(mail)
            except:
                #there are integers in the mails, simply pass the errors
                pass

    #command checker
    command = "SHUTDOWN YOURSELF"

    #slice all SUBJECT from mail
    bolt = t[2:-1]

    
    try:
        #slice SUBJECT's elements in a list
        boltapply = bolt.split(" ")[1]+ " " + bolt.split(" ")[2] + " " + bolt.split(" ")[3]

        #slice 'boltapply' to check if they are same with COMMAND
        boltapply_subject = boltapply.split(" ")[0]+ " " + boltapply.split(" ")[1]
        
        #slice 'boltapply' - get date part
        boltapply_date = boltapply.split(" ")[-1]

        #find current time
        timee = datetime.now()
        
        #current day - order: YEAR-MONTH-DAY
        timee_edit = str(timee.year)+"-"+"{:0>2}".format(str(timee.month))+"-"+str(timee.day)
        
        #current time - order: HOUR-MINUTE
        timee_hour = str(timee.hour) + "." + str(timee.minute )
        
        #slice 'dt' from MAIL - 'dt' is the date part from the MAILS
        dt_Edit = dt.split(" ")[5].split(":")[0] + "." + dt.split(" ")[5].split(":")[1]
        

        #check where are the MAILS from
        #so we can be sure it's from the address that we input above
        from_read = fr.split(" ")[-1].split("<")[1].split(">")[0]
    
        #first, check if YEAR-MONTH-DAY order is the same as today's DATE
        if boltapply_date == timee_edit:
            #then check if the MAIL sent before 1 HOUR, command(SHUTDOWN YOURSELF) is same as SUBJECT and is the mail came from CORRECT ADDRESS('from_addr')
            if datetime.now().hour - int(dt.split(" ")[5].split(":")[0]) == 0 and datetime.now().minute - int(dt.split(" ")[5].split(":")[1]) <= 59 and command == boltapply_subject and from_read == from_addr:
                #if all requirements are met, call "subprocess 'shutdown.exe'" and shutdown the computer in N seconds (it's 26 seconds now)
                subprocess.call(["shutdown.exe","-f","-s","-t","26"])
                
    except:
        #if SUBJECT is in wrong order
        #if there is no SUBJECT
        #if there is SUBJECT but there is no DATE
        #pass it

        # for example;
        # a subject like 'SHUTDOWN YOURSELF 2016' will end up with a TypeError (see above we are slicing SUBJECT 'boltapply')
        
        pass

    #wait 40 seconds
    time.sleep(40)
