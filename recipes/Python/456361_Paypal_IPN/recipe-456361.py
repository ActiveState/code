 #!/usr/bin/python24
import cgi
import time
import MySQLdb
from traceback import format_exception
from sys import exc_info
from string import split
from string import strip
from sys import exit
from urllib import urlencode
import urllib2


DATADIR = "/home/user/data/"
PP_URL = "https://www.sandbox.paypal.com/cgi-bin/webscr"
#PP_URL = "https://www.paypal.com/cgi-bin/webscr"
# non testing is www.paypal.com and /cgi-bin/webscr

# note we used the fields custom and option_selection1 and 
# option_selection2 to pass item characteristics



def confirm_paypal(f,f1):
    # f is the form handle to the cgi form passed by paypal
    # f1 is a file handle to a log text file
    
    newparams={}
    for key in f.keys():
        newparams[key]=f[key].value

    newparams["cmd"]="_notify-validate"
    params=urlencode(newparams)
    f1.write(params + "\n")

    f1.write(PP_URL + "\n")
    req = urllib2.Request(PP_URL)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    fo = urllib2.urlopen(PP_URL, params)
    ret = fo.read()
    if ret == "VERIFIED":
        f1.write(" verified send back ok\n")
        print "Status: 200 Ok\n"
    else:
        f1.write(" ERROR did not verify\n")
        exit(0)

    return ret


def write_db(f, f1):

    f1.write("... updating database\n")

    try:
        invoice = f['invoice'].value

        try:
            street = f['address_street'].value
            city = f['address_city'].value
            zipc = f['address_zip'].value
            country = f["address_country_code"].value
            firstn = f['first_name'].value
            lastn = f['last_name'].value

        except KeyError:
            street = ""
            city = ""
            zipc = ""
            country = ""
            firstn = ""
            lastn = ""
    
        try:
            #some countries don't have states
            state = f['address_state'].value
        except KeyError:
            state =""

        if f.has_key("custom"):
                payer_url = f["custom"].value

        query = "INSERT INTO names VALUES ('" + invoice + "', '" + \
        firstn + "', '" + lastn + "', '" +  street + "', '" +  city + "', '" + state + "', '" +  zipc + "', '" +  \
        country + "', '" +  f['payer_email'].value + "', '" +  \
        payer_url + "', '" +  f['option_selection1'].value + "', '" +  f['option_selection2'].value + "')"

        f1.write(query + "\n")
        db = MySQLdb.connect(host="localhost", user="username", passwd="passwd",db="db")
        cursor = db.cursor()
        cursor.execute (query)

    except:
        f1.write(''.join(format_exception(*exc_info())))



if __name__=="__main__":
    import cgitb; cgitb.enable()
    #can disable cgitb if not req.

    f1 = open(DATADIR + "log1.txt",'a')
    f1.write("############ " +str(time.ctime(time.time())) + " starting request\n ")
    try:
        f = cgi.FieldStorage()
        f1.write(repr(f) + "\n\n")
        a = confirm_paypal(f, f1)
        
        if not f['payment_status'].value == "Completed":
            # We want want to respond to anything that isn't a payment - but we won't insert into our database
             f1.write("### Not Completed so going to exit....\n")
             exit(0)
        else:
            f1.write("### Completed so going to write data...\n")

        write_db(f, f1)

    except:
        f1.write(''.join(format_exception(*exc_info())))

    
