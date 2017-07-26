"""
    mbsa2txt.py

    -- Reads the Microsoft Baseline Security Analyzer 1.2.1
    XML output and sends it to standard output in a readable
    text format.

    -- Usage: python mbsa2txt.py mbsaScanFile.xml    
    
    Copyright (C) 2004
    Shannon Eric Peevey
    President, EriKin Corporation
    speeves@erikin.com

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""

import sys
import string
from xml.dom import minidom

file = sys.argv[1]
mbsa = minidom.parse(file)


def getSecscan(mbsa):
    """
    Sets the first element, 'SecScan', to a variable 'secscan',
    prints out the header of the file with
    printSecScanAttributes(), and calls getCheck().
    """
    secscan = mbsa.firstChild
    secscanLength = len(secscan.childNodes)
    #print secscanLength
    
    printSecScanAttributes(secscan)
    getCheck(secscan, secscanLength)

def getCheck(secscan, secscanLength):
    """
    Sets the element, 'Check', to a variable 'check',
    loops through the 'check'-list ;) , prints the
    section header for each test with printCheckAttributes()
    and calls getAdvice().
    
    This element is a sibling to the 'IPList' element
    and contains all of the elements we need to access
    for the report.
    """
    checkx = 3 # loop iterator
    check = secscan.childNodes[checkx]
    checkLength = len(check.childNodes)
    checknumber = 1

    while checkx < (secscanLength - 2):
        printCheckAttributes(check, checknumber)
        getAdvice(check)
        if checkLength == 5:
            getDetail(check)
            
        checkx += 2
        checknumber += 1
        #print checkx
        check = secscan.childNodes[checkx]
        checkLength = len(check.childNodes)

def getAdvice(check):
    """
    Prints the text from the 'Advice' element
    under the header
    """
    # check.childNodes[1] <Advice> 
    advice = check.childNodes[1]
    adviceText = advice.childNodes[0]
    #printCheckAttr(check[y])
    print " - " + adviceText.data + "\n"

def getDetail(check):
    """
    Sets the variable 'detail' equal to the 'Detail'
    element, grabs the length of the list in 'detail'
    and calls getHeadRow().
    """
    # check.childNodes[3] <Detail>
    detail = check.childNodes[3]
    detailLength = len(detail.childNodes)
    #print detailLength
    getHeadRow(detail, detailLength)

def getHeadRow(detail, detailLength):
    """
    Sets the variable 'headrow' equal to the 'Head'
    or 'Row' elements.  (Which are siblings under
    'Detail'), grabs the length of the list in 'headrow',
    and loops through the list.  While looping through
    'headrow', it calls gradeText() and getCol().
    """
    # check.childNodes[checkx}.childNodes[detailx] <Head> and <Row>
    headrowx = 1 # loop iterator
    headrow = detail.childNodes[headrowx]
    headrowLength = len(headrow.childNodes)
    #print "detailLength = " + str(detailLength)
    #print "headrowLength = " + str(headrowLength)

    while headrowx <= (detailLength - 2):
        gradeText = setGrade(headrow)
        getCol(headrow, headrowLength, gradeText, headrowx)

        headrowx = headrowx + 2
        #print "headrowx = " + str(headrowx)
        if headrowx <= (detailLength - 2):
            headrow = detail.childNodes[headrowx]
            headrowLength = len(headrow.childNodes)

    print "\n"

def getCol(headrow, headrowLength, gradeText, headrowx):
    """
    Sets the variable 'col' equal to the 'Col' elements
    and prints out the values for each column.
    """
    colx = 1 # loop iterator
    col = headrow.childNodes[colx]
    x = ""
    while colx < headrowLength:
        colText = col.childNodes[0]
        if colx == 1:
            #x = colText.data
            if gradeText != "":
                x = "  -- " + gradeText + " | " + colText.data
            elif gradeText == "" and headrowx == 1:
                x = "  -- Test Result " + "\t" + " | " + colText.data
            else:
                x = "  -- " + "\t"*2 + " | " + colText.data
        else:
            x = x + "  |  " + colText.data
            
        #print colx
        colx += 2
        if colx < headrowLength:
            col = headrow.childNodes[colx]

    if x != "":
        print x

def printSecScanAttributes(secscan):
    """
    Prints the header for the SecurityScan xml
    file in a dictionary type format:

    Computer Name:  DOMAIN\computer
    IP Address:  192.168.1.2
    Scan Date:  2004-01-01 hh:mm:ss
    Security Assessment: 2
    """
    domain = secscan.attributes["Domain"]
    machine = secscan.attributes["Machine"]
    ip = secscan.attributes["IP"]
    date = secscan.attributes["Date"]
    grade = secscan.attributes["Grade"]
	
    print "\n\n"
    print "Computer Name: " + domain.value + "\\" + machine.value
    print "IP Address: " + ip.value
    print "Scan Date: " + date.value
    print "Security Assessment: " + grade.value	
    print "\n\n"

def setGrade(headrow):
    """
    Returns 'gradeText' based on grade.value.  This is
    numeric in the xml, but I just give them the text
    values that are used in the MBSA interface.  These are:

    0 == Check Passed
    1 == Additional Information
    2 == Check Failed (Critical)
    3 == Check Failed (Non-Critical)
    4 == Note Message
    5 == Check Passed
    """
    grade = ""
    gradeText = ""
    if headrow.hasAttributes() != False:
        grade = headrow.attributes["Grade"]
        #print grade.value
        if grade.value == '0':
            gradeText = "Check Passed"
        elif grade.value == '1':
            gradeText = "Additional Information"
        elif grade.value == '2':
            gradeText = "Check Failed (Critical)"
        elif grade.value == '3':
            gradeText = "Check Failed (Non-Critical)"
        elif grade.value == '4':
            gradeText = "Note Message"
        elif grade.value == '5':
            gradeText = "Check Passed"

    return gradeText
                   
def printCheckAttributes(check, checknumber):
    """
    Grabs the value of the attribute 'Name' from the
    Check element and prints it to standard output.
    """
    name = check.attributes["Name"]

    print str(checknumber) + ". " + name.value + "\n"

getSecscan(mbsa)
