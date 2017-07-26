from urllib2 import urlopen
from bs4 import BeautifulSoup
import requests
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
 
app = QApplication(sys.argv)
 
URL= 'http://sdpdr.nic.in/annauniv/Authentication'
 
#get  userdata
RegisterNumber = raw_input("Enter the registration number : ")
DateofBirth = raw_input("Enter the date of birth [DD-MM-YYYY] : ")
 
 
def main():
    # Start a session so we can have persistant cookies
 
    # Session() &gt;&gt; http://docs.python-requests.org/en/latest/api/#request-sessions
    session = requests.Session()
 
    # This is the form data that the page sends when logging in
 
    login_data = {
    'username': RegisterNumber,
    'password': DateofBirth,
    'submit': 'id',
    }
    print login_data
 
    # Authenticate
    r = session.post(URL, data = login_data)
 
    # Try accessing a page that requires you to be logged in
    r = session.get('http://sdpdr.nic.in/annauniv/result')
 
    web = QWebView()
    web.load(QUrl("http://sdpdr.nic.in/annauniv/result"))
    #web.show()
 
    printer = QPrinter()
    printer.setPageSize(QPrinter.A4)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName("result.pdf")
 
# convertion of page to pdf format
 
def convertIt(main):
    web.print_(printer)
    print "Pdf generated"
    QApplication.exit()
 
    QObject.connect(web, SIGNAL("loadFinished(bool)"), convertIt)
 
    sys.exit(app.exec_())
 
if __name__ == '__main__':# main method
   main()
