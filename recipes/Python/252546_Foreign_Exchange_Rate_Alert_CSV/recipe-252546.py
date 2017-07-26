import string
import smtplib
import urllib2


# configure ur threshold rate, smtp server here 
# threshold rate for CAD --> USD noon rate 
thresholdRate=1.10
smtpServer='test-smtp-server'
fromaddr='foo@bar.com' 
toaddrs='you@corp.com'
# end of configuration

url='http://www.bankofcanada.ca/stats/assets/csv/fx-seven-day.csv'   
f=urllib2.urlopen(url,timeout=60)

# read all in for efficency as it is a small file anyways. 
data=f.read()
start=data.find('U.S. dollar (close)')
rate=string.strip(data[start:].split('\n')[0].split(',')[-1])
if float(rate) > thresholdRate:
   #send email 
   msg = ('Subject: Bank of Canada Noon Foreign Exchange Rates %s for 1 USD ' % rate) 
   server = smtplib.SMTP(smtpServer)
   #server.set_debuglevel(1)
   server.sendmail(fromaddr, toaddrs, msg)
   server.quit()
f.close()
