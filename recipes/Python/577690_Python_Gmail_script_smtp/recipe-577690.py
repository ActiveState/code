#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#       gmail.py
#

import sys
import os
import smtplib
import getpass
import ConfigParser
from optparse import OptionParser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

'''
Usage: gmail.py [options] arg1

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  image FILE to attach
  -t EMAIL, --to=EMAIL  email destination
  -o NAME, --from=NAME  name of origin
  -b BODY, --body=BODY  BODY message
  -s SUBJECT, --subject=SUBJECT
                        SUBJECT message

Config file example "gmail.cfg"

[Default]
fromaddr = Server email Name
toaddrs  = destination@example.com

[Gmail]
username = MYGMAILUSER
password = MYGMAILPASS

'''
# Program epilog
epilog = \
"""
gmail is configured using a config file only. 
If none is supplied, it will read gmail.cfg 
from current directory or ~/.gmail.cfg.
"""

def main():
    usage = "usage: %prog [options] arg"
    version = "%prog 1.0"
    parser = OptionParser(usage=usage, version=version, epilog=epilog)
    parser.add_option("-f", "--file", dest="image_file",
                  help="image FILE to attach", metavar="FILE")
    parser.add_option("-c", "--conf", dest="config_file",
                  help="config FILE", metavar="CONFIG",
                  default='gmail.cfg')
    parser.add_option("-t", "--to", dest="toaddrs",
                  help="email destination", metavar="EMAIL",
                  default=None)
    parser.add_option("-o", "--from", dest="fromaddr",
                  help="name of origin", metavar="NAME",
                  default=None)
    parser.add_option("-b", "--body", dest="body",
                  help="BODY message", metavar="BODY",
                  default='')
    parser.add_option("-s", "--subject", dest="subject",
                  help="SUBJECT message", metavar="SUBJECT",
                  default='')
    (options, args) = parser.parse_args()
    # Run the program
    process(options, args)

def process(options, args):
    config = get_config(options)
    # Write the email
    msg = MIMEMultipart()
    msg['From'] = config['fromaddr']
    msg['To'] = config['toaddrs']
    msg['Subject'] = options.subject
    body = options.body
    msg.attach(MIMEText(body, 'plain'))
    # Attach image
    if options.image_file:
        try:
            filename = open(options.image_file, "rb")
            attach_image = MIMEImage(filename.read())
            attach_image.add_header('Content-Disposition', 
                                    'attachment; filename = %s'%options.image_file)
            msg.attach(attach_image)
            filename.close()
        except:
            msg.attach(MIMEText('Image attachment error', 'plain'))
    # Converting email to text
    text = msg.as_string()
    
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(config['username'],config['password'])
    server.sendmail(config['fromaddr'], config['toaddrs'], text)
    server.quit()

def get_config(options):
    conf = {}
    # Read Config File
    config = ConfigParser.RawConfigParser()
    config.read([options.config_file, os.path.expanduser('~/.gmail.cfg')])
    # Gmail Credentials
    try:
        conf['username'] = config.get('Gmail', 'username')
        conf['password'] = config.get('Gmail', 'password')
    except:
        conf['username'] = raw_input('Input Gmail username: ')
        conf['password'] = getpass.getpass('Input Gmail password: ')
    # Email Default
    if options.fromaddr == None:
        try:
            conf['fromaddr'] = config.get('Default', 'fromaddr')
        except:
            conf['fromaddr'] = 'Python Gmail'
    else:
        conf['fromaddr'] = options.fromaddr
    if options.toaddrs == None:
        try:
            conf['toaddrs']  = config.get('Default', 'toaddrs')
        except:
            conf['toaddrs'] = raw_input('Input email destination: ')
    else:
        conf['toaddrs'] = options.toaddrs
    return conf

if __name__ == '__main__':
    main()
