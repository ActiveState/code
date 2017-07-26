#! /usr/bin/env python2.7
# vim: et sw=4 ts=4:
"""
DESCRIPTION:
    A Command Line Interface (CLI) program to send email.
    If the value to an argument is a file path and the file exists, the file
    will be read line by line and the values in the file will be used.
    When supplying multiple email addresses as an argument, a comma should be
    used to separate them.
    Arguments with spaces should be encolsed in double quotes (").
AUTHOR:
    sfw geek
NOTES:
    <PROG_NAME> = ProgramName
    <FILE_NAME> = <PROG_NAME>.py = ProgramName.py

    Static Analysis:
        pychecker.bat <FILE_NAME>
        pylint <FILE_NAME>
    Profile code:
        python -m cProfile -o <PROG_NAME>.prof <FILE_NAME>
    Vim:
        Remove redundant trailing white space: '\s\+$'.
    Python Style Guide:
        http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
    Docstring Conventions:
        http://www.python.org/dev/peps/pep-0257
"""


# TODO:
#   Implement BCC functionality (FUNC_BCC).


# FUTURE STATEMENTS (compiler directives).
# Enable Python 3 print() functionality.
from __future__ import print_function


# VERSION.
# http://en.wikipedia.org/wiki/Software_release_life_cycle
# Phase Year.Month.Day.Build (YYYY.MM.DD.BB).
__version__ = '2012.08.20.01'
__release_stage__ = 'General Availability (GA)'


# MODULES.
# http://google-styleguide.googlecode.com/svn/trunk/pyguide.html#Imports_formatting
# Standard library imports.
import argparse
import datetime
import email.mime.multipart
import email.mime.text
import email.utils
import os
import smtplib
import sys


# CONSTANTS.
PROGRAM_NAME = sys.argv[0]

# Linux/Unix programs generally use 2 for command line syntax errors and 1 for all other kind of errors.
SYS_EXIT_CODE_SUCCESSFUL = 0
SYS_EXIT_CODE_GENERAL_ERROR = 1
SYS_EXIT_CODE_CMD_LINE_ERROR = 2

COMMA_SPACE = email.utils.COMMASPACE


# DEFINITIONS.
def usage():
    """Return string detailing how this program is used."""

    return '''
    A Command Line Interface (CLI) program to send email.
    If the value to an argument is a file path and the file exists, the file
    will be read line by line and the values in the file will be used.
    When supplying multiple email addresses as an argument, a comma should be
    used to separate them.
    Arguments with spaces should be encolsed in double quotes (").'''

def getProgramArgumentParser():
    """Return argparse object containing program arguments."""

    argParser = argparse.ArgumentParser(description=usage())

    # Mandatory parameters (though not set as required=True or can not use -V on own).
    mandatoryGrp = argParser.add_argument_group('mandatory arguments', 'These arguments must be supplied.')
    mandatoryGrp.add_argument('-b', '--body', action='store', dest='body', type=str,
        help='Body of email.  All lines from file used if file path provided.')
    mandatoryGrp.add_argument('-f', '--from', action='store', dest='frm', type=str,
        help='Who the email is from.  Only first line of file used if file path provided.')
    mandatoryGrp.add_argument('-m', '--machine', action='store', dest='smtphost', type=str,
        help='The name of SMTP host used to send the email.  Only first line of file used if file path provided.')
    mandatoryGrp.add_argument('-s', '--subject', action='store', dest='subject', type=str,
        help='The subject of the email.  Only first line of file used if file path provided.')
    mandatoryGrp.add_argument('-t', '--to', action='store', dest='to', type=str,
        help='Who the email is to be sent to.  One email address per line if file path provided.')

    # Optional parameters.
    optionalGrp = argParser.add_argument_group('extra optional arguments', 'These arguments are not mandatory.')
    optionalGrp.add_argument('-c', '--cc', action='store', dest='cc', type=str,
        help='Who the email is to be Carbon Copied (CC) to.  One email address per line if file path provided.')
    # TODO: FUNC_BCC
    #optionalGrp.add_argument('-B', '--bcc', action='store', dest='bcc', type=str,
    #    help='Who the email is to be Blind Carbon Copied (BCC) to.  One email address per line if file path provided.')
    optionalGrp.add_argument('-d', '--debug', action='store_true', dest='debug',
        help='Increase verbosity to help debugging.')
    optionalGrp.add_argument('-D', '--duration', action='store_true', dest='duration',
        help='Print to standard output the programs execution duration.')
    optionalGrp.add_argument('-V', '--version', action='store_true', dest='version',
        help='Print the version number to the standard output.  This version number should be included in all bug reports.')

    return argParser

def printVersionDetailsAndExit():
    """Print to standard output programs version details and terminate program."""

    msg = '''
NAME:
    {0}
VERSION:
    {1}
    {2}'''.format(PROGRAM_NAME, __version__, __release_stage__)
    print(msg)
    sys.exit(SYS_EXIT_CODE_SUCCESSFUL)

def getDaySuffix(day):
    """Return st, nd, rd, or th for supplied day."""

    if 4 <= day <= 20 or 24 <= day <= 30:
        return 'th'
    return ['st', 'nd', 'rd'][day % 10 - 1]

def printProgramStatus(started, stream=sys.stdout):
    """Print program duration information."""

    NEW_LINE = '\n'
    DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f (%a %d{0} %b %Y)'
    finished = datetime.datetime.now()
    delta = finished - started
    dateTimeStr = started.strftime(DATE_TIME_FORMAT.format(getDaySuffix(started.day)))
    msg = '{1}Started:  {0}{1}'.format(dateTimeStr, NEW_LINE)
    dateTimeStr = finished.strftime(DATE_TIME_FORMAT.format(getDaySuffix(finished.day)))
    msg += 'Finished: {0}{1}'.format(dateTimeStr, NEW_LINE)
    msg += 'Duration: {0} (days hh:mm:ss:ms)'.format(delta)
    print(msg, file=stream)

def getFileContentsOrParameterValue(filePathOrValue):
    """Return list of file contents if parameter is file path, otherwise
    parameter as first entry."""

    data = []
    if os.path.isfile(filePathOrValue):
        with open(filePathOrValue) as foSrc:
            for srcLine in foSrc:
                data.append(srcLine.strip())
    else:
        data.append(filePathOrValue)
    return data

def main():
    """Program entry point."""

    # Store when program started.
    started = datetime.datetime.now()

    # Get parameters supplied to application.
    argParser = getProgramArgumentParser()
    args = argParser.parse_args()

    # Logic for displaying version details or program help.
    if args.version:
        printVersionDetailsAndExit()
    if not (args.smtphost and args.to and args.frm and args.subject and args.body):
        if args.version:
            printVersionDetailsAndExit()
        argParser.print_help()
        sys.exit(SYS_EXIT_CODE_CMD_LINE_ERROR)

    # Process program arguments to get email parts.
    # From can only have one value regardless if stored in file or not (first line in file used).
    fromVal = getFileContentsOrParameterValue(args.frm)[0]
    toData = getFileContentsOrParameterValue(args.to)
    subjectVal = getFileContentsOrParameterValue(args.subject)[0]
    bodyData = getFileContentsOrParameterValue(args.body)
    smtpHostVal = getFileContentsOrParameterValue(args.smtphost)[0]

    # Build multipart MIME message (email).
    multipartMimeMsg = email.mime.multipart.MIMEMultipart()
    multipartMimeMsg['Date'] = email.utils.formatdate(localtime=True)
    multipartMimeMsg['From'] = fromVal
    multipartMimeMsg['To'] = COMMA_SPACE.join(toData)
    multipartMimeMsg['Subject'] = subjectVal
    multipartMimeMsg.attach(email.mime.text.MIMEText(email.utils.CRLF.join(bodyData)))

    # Process optional arguments.
    if args.cc:
        ccData = getFileContentsOrParameterValue(args.cc)
        multipartMimeMsg['Cc'] = COMMA_SPACE.join(ccData)
        toData.extend(ccData) # TODO: check?
    # TODO: FUNC_BCC
    #if args.bcc:
    #    bccData = getFileContentsOrParameterValue(args.bcc)
    #    multipartMimeMsg['Bcc'] = COMMA_SPACE.join(bccData)
    #    toData.extend(bccData) # TODO: similar to CC but is blindness enforced?

    # Python 3.3 supports with statement (context manager) for smtplib.SMTP().
    # http://docs.python.org/dev/library/smtplib.html
    # with smtplib.SMTP(smtpHostVal) as smtpSvr:
    try:
        smtpSvr = smtplib.SMTP(smtpHostVal)
        if args.debug:
            # Increase display verbosity.
            smtpSvr.set_debuglevel(1)
        smtpSvr.sendmail(fromVal, toData, multipartMimeMsg.as_string())
    finally:
        smtpSvr.quit()

    if args.duration:
        printProgramStatus(started)


# Program entry point.
if __name__ == '__main__':
    main()
