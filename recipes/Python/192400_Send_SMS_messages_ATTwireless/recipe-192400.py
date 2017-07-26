# Written by Sam Hendley
# Class to send SMS text message to ATT phones
import urllib
import string
"""This class allows you to send SMS messages to any ATT wireless phone
I built this by going to the ATT text send site and searching the source
to find out exactly what fields it needs, there is a 110 character limit"""
class ATTAlerter:
    def __init__(self,number,subject,whofrom):
        """number must be a string of format 'xxx-xxx-xxxx'"""
        self.number = number
        self.subject = self.toHtml(subject)
        self.whofrom = self.toHtml(whofrom)
    def SendMessage(self, message):
        """Message is string to send to user"""
        self.message = self.toHtml(message)
        num = len(self.message)+len(self.whofrom)+len(self.subject)
        if num > 110:
            return 2
        astring = 'http://www.mobile.att.net/messagecenter/pagersend.cgi?pin="'
        astring = astring + self.number
        astring = astring + '"&from="'
        astring = astring + self.whofrom
        astring = astring + '"&subject="'
        astring = astring + self.subject
        astring = astring + '"&message="'
        astring = astring + self.message
        astring = astring + '"&size="'
        astring = astring + str(num)+'"'
        #print astring
        
        myUrlclass = urllib.FancyURLopener()
        try:
            webPage = myUrlclass.open(astring)
            #print webPage
        except IOError:
            print 'webaddress failed'
            return -1
        #while 1:
        data = webPage.read(8192)
        if data:
            #print str(data)
            if string.find(str(data),"<TITLE>400 Bad Request</TITLE>") != -1:
                return 4
        else:
            return 3
        
        webPage.close()
        return 0
    def toHtml(self,str):
        str = string.replace(str, ' ','%20')
        #print str
        return str


######################################################################
######    Test function  replace ###-###-#### wiht your number
######################################

alerter = ATTAlerter.ATTAlerter('###-###-####','Test Message','Python Script')
alerter.SendMessage('This message came from python!!')

###############################################################
