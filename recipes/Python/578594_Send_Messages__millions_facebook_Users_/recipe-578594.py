#usr/bin/env/python
"""
This script can get the user data from facebook.com.
This is written for better understanding of python 
Modules required:BeautifulSoup
Author:Ajay Kumar Medepalli aka Cybercam
Blog:http://pythonnotesbyajay.blogspot.in/

"""
import smtplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.parser import Parser
from email.MIMEText import MIMEText
import urllib2
from BeautifulSoup import BeautifulSoup
import random

user_name_array=[]
def get_fb_username(id):
    try:
        url=urllib2.urlopen('https://graph.facebook.com/'+str(id)).read()
        soup = BeautifulSoup(url)
        all_attr=soup.prettify()
        print all_attr
        gend=all_attr.find("gender")
        if(all_attr[gend+9] == 'm'):
            gender='male'
        elif (all_attr[gend+9] == 'f'):
            gender = 'female'
        else:
            gender="The user didn't specify any gender"
        if all_attr.find('username') != -1:
            start_quote=all_attr.find('username')+10
            end_quote=all_attr.find('"',start_quote+1)
            user_name=all_attr[start_quote:end_quote+1].strip('"')+'@facebook.com'

            user_name_array.append(user_name)
            print "username ==>"+'\t'+user_name +'\t'+ "gender ==>"+"\t"+gender
            print "\n"
        
    except urllib2.HTTPError:
        pass


    

for i in range(4,10,1):
#for i in range(startvalue,stopvalue,stepvalue):
    get_fb_username(i+1)
print user_name_array

def send_mail():
    random_text=["hi","hello","Nice to meet you","How are you","wassup","hi!!!",'just wanted to say hi']
    server = smtplib.SMTP()
    server.connect('smtp.gmail.com', 587) # for eg. host = 'smtp.gmail.com', port = 587
    server.ehlo()
    server.starttls()
    server.login('username@gmail.com', 'password')
    #replace this with u r gmail id
    #password ==> ur gmail password
    fromaddr ='username@gmail.com'

    for i in range(len(user_name_array)-1):

        msg = email.MIMEMultipart.MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = user_name_array[i]
        msg['Subject'] = 'hi'
        
        msg.attach(MIMEText(random_text[random.randint(0,len(random_text)-1)]))
        #msg.attach(MIMEText('put some custom message.', 'plain')) 
        server.sendmail(fromaddr,user_name_array[i],msg.as_string())
    server.quit()  
send_mail()
