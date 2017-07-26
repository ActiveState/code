# By: Kevin T. Ryan (kevryan0701_AT_yahoo_DOT_com)
# 11/17/2004
#
# Inspired by a script created by  Daniel Santamaria at Tinyminds.org
# See the article "Running a Webserver with a Dynamic IP" at
# Tinyminds for the complete details.  Thanks Dan!
#
# This script simply creates a webpage that will re-direct users that type in
# your webpage name to your home server.  This would not be so interesting
# except for the fact it allows you to give people a static name (such as
# www.mywebsite.com) and then have them redirected to your server that could be
# using a DYNAMIC IP address!
#
# That is, even if you don't have a static ip address you can simply run this
# script whenever you boot your machine to automatically update the page at
# your website to point to your new ip address.
#
# One note - use at your own risk.  Not all ISP's might want you to be running a
# server from your cable or dsl modem, so check w/ them first! :)

import ftplib, socket

FTP_SERVER = "your.ftp.server"
USER_NAME = "your_username"
PASSWORD = "your_password" # Alternatively, you could request a pw every time you run this script for more security.

STANDARD_FILE_NAME = "index.html" # Can change to what you want - it will be the local and remote filename.

HTML_PAGE = """<head>
<title>Redirecting you now...</title>
<meta http-equiv='refresh' content='2;url=http://%(addr)s'>
</head>
<br />
<br />
<a href="http://%(addr)s">
<b>Click here if you are not automatically redirected to the webpage</b></a>"""

def create_redirection_page(ip=None):
    '''Creates and returns a string representation of an html page using the HTML_PAGE variable.'''
    if (ip):
        return HTML_PAGE % {'addr': ip}
    else:
        ip = get_my_ip()
        return HTML_PAGE % {'addr': ip}

def send_ftp(file_name=None):
    '''Sends the file_name (which should be a closed file object) to the server for storage.'''
    if file_name == None: file_name = STANDARD_FILE_NAME
    f = open(file_name, 'rb')
    server = ftplib.FTP(FTP_SERVER, USER_NAME, PASSWORD)
    server.storbinary("STOR " + STANDARD_FILE_NAME, f)
    f.close()
    server.quit()

def get_my_ip():
    return socket.gethostbyname(socket.gethostname())

if __name__ == "__main__":
    # First, we create the web page string.
    dynamic_redirection = create_redirection_page()
    # Then, we write it to a file.
    f = open(STANDARD_FILE_NAME, 'wb')
    f.write(dynamic_redirection)
    f.close()
    # Finally, we send it to our FTP server.
    send_ftp(STANDARD_FILE_NAME)
