#!/usr/bin/env python
# coding: utf-8
"""
  Assumption: Input Excel Spreadsheet with these columns:

  "Date","Company","Symbol","First Name","Last Name",
  "Title","Email","Notes", "Owner First Name", "Owner Last Name"
  
  Normally you should try to use the Salesforce import Wizard or
  Apex Data Loader for importing.  This script demonstrates that 
  programmatic import can handle complex conditional logic that
  the Import Wizard or Data Loader cannot anticipate.
  
  * Apex Data Loader requires CSV file, does not directly deal with Excel
  * Apex Data Loader only loads one object type per/run.  
  * The mapping of input columns to object fields is static/declarative (normally this is good,
    but not flexible)
  * You cannot map an Account owner by name
  
  Other issues raised that this script (scripting, in general) can handle:
  
  http://success.salesforce.com/ideaView?c=09a30000000D9xt&id=08730000000Bq30AAC
  http://success.salesforce.com/ideaView?c=09a30000000D9xt&id=08730000000BrdUAAS
  
  This script uses the Salesforce (web services) API, which is only available to Unlimited, 
  Enterprise and Developer users, although I understand the API can purchased
  separately.
  
  Module Dependencies:
  sforce, salesforce-python-toolkit, http://code.google.com/p/salesforce-python-toolkit/
  suds, versions 0.3.6 to 0.3.9 ONLY (i.e. 0.4.0 WON'T WORK) Python SOAP API, https://fedorahosted.org/suds
  xlrd, Python MS-Excel reader, http://www.python-excel.org
  xlwt, Python MS-Excel writer, http://www.python-excel.org
  
  Copyright (c) 2011 Chris Wolf  cw10025 gmail
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.

"""

#-------------------- user configuration section, edit as needed ----
# WSDL generated from setup->Develop->API->Generate Enterprise WSDL
wsdlFile=r'enterprise.wsdl'

username='sforceuser'
password='sforcepw'
sectoken='xxxxxxxxxxxxxxxxx' #security token

# when these are False, an entry is created in the exception report
createMissingAccounts = True
createMissingContacts = True
#--------------------------------------------------------------------
import sys, xlrd, datetime
from xlwt import Workbook, easyxf, XFStyle
from sforce.enterprise import SforceEnterpriseClient

# missing ternary expression in Python < 2.5
tern=lambda a,b,c: (b,c)[not a]

class ImportException(Exception):
  def __init__(self, msg, sheetName, errRow):
    self.msg = msg
    self.sheetName = sheetName
    self.errRow = errRow
  def __str__(self):
    return repr("%s: '%s', row %d" % self.msg, self.sheetName, self.errRow)

#----- globals ----
# Errors XLS
errorsWorkbook = None
erroutSheet = None
erroutRow = 0
# Import XLS
importSheet = None
importRow = 0
invokingUser = None
headers = []
# Salesforce connection handle, initialized by login
sf = None

# set username, password and sectoken near top of this file
def loginToSalesforce(username, password, sectoken):
  """
  Initializes global Salesforce connection handle, "sf"
  """
  global sf
  sf = SforceEnterpriseClient(wsdlFile)
  # API login seems to always need security token
  result = sf.login(username, password, sectoken)
  print 'Connected to "%s"' % result.serverUrl
  print '  as user "%s" Org Company Name: "%s" Org Id: "%s"' % \
    (result.userInfo.userFullName, 
     result.userInfo.organizationName, 
     result.userInfo.organizationId)
  print "  org type is %s sandbox" % (tern(result.sandbox,"","NOT"))
  global invokingUser
  invokingUser = result.userInfo.userFullName

def configErrorReporting(headers):
  """
  Configure import exception log, which is an Excel spreadsheet in the same 
  format as the input format, but with an extra column added - "Error",
  which contains the error message.
  
  Can only be called after first row of input Excel spreadsheet is read
  to initialize the global, "headers"
  """
  dateFmt = easyxf(
    'font: name Arial, bold True, height 200;',
    #'borders: left thick, right thick, top thick, bottom thick;',
     num_format_str='MM-DD-YYYY'
  )
  
  headerFmt = easyxf(
    'font: name Arial, bold True, height 200;',
  )
  global errorsWorkbook, erroutSheet, erroutRow
  errorsWorkbook = Workbook()
  erroutSheet = errorsWorkbook.add_sheet('Import Errors')

  for colnum in range(0, len(headers)):
    erroutSheet.write(0, colnum, headers[colnum][0], 
    tern(headers[colnum][0]==xlrd.XL_CELL_DATE, dateFmt, headerFmt))
   
  # Add extra column for error message
  erroutSheet.write(0, len(headers), "Error", headerFmt)
  erroutSheet.flush_row_data()
  erroutRow = 1
  errorsWorkbook.save('errors.xls')

def writeErrorRec(record):
  """
  Exception report spreadsheet output format same as input format and
  assumes first column is of type Date - adds an extra, last column
  for error message.
  """
  dateFmt = XFStyle()
  dateFmt.num_format_str='MM-DD-YYYY'
  defaultFmt = XFStyle()
  global erroutRow

  for colnum in range(0, len(headers)):
    erroutSheet.write(erroutRow, colnum, record[headers[colnum][0]], 
    tern(headers[colnum][0]==xlrd.XL_CELL_DATE, dateFmt, defaultFmt))
                                     
  # add extra column for error message                                    
  erroutSheet.row(erroutRow).write(len(headers), record['Error'])  
  
  erroutRow += 1
  
  # flush every 200 rows...
  #if ((erroutRow % 200) + 1 == 200):
  # since, xlwt uses aggressive caching, we must
  # write each row manually, or the data may be lost upon exception
  erroutSheet.flush_row_data()  
  errorsWorkbook.save('errors.xls')
  
def createContact(record):
  """
    Create a partially populated Contact record, associated with the 
    Account ("Company") specified in the Excel record.
  """
  global importSheet, importRow
  contact              = sf.generateObject('Contact')
  contact.AccountId    = record['AccountId']
  contact.FirstName    = record['First Name']
  contact.LastName     = record['Last Name']
  contact.Title        = record['Title']
  contact.Email        = record['Email']
  contact.Description  = record['Notes']
  result               = sf.create(contact)
  
  if result.success != True:
    msg = "Error: Can't create Contact record for %s, result was %s" % (str(record), result)      
    raise ImportError(msg, importSheet, importRow)
    
  print "New Contact record for %s, %s, Id = %s" \
    % (contact.LastName, contact.FirstName, result.id)

  return result

def createAccount(record):
  """
    Create a partially populated Account record, corresponding to the 
    Company specified in the Excel record.
  """
  global importSheet, importRow
  ownerId = None
  setOwner = False
  if record['Owner First Name'] != None and len(record['Owner First Name']) > 0 and \
     record['Owner Last Name'] != None and len(record['Owner Last Name']) > 0:
    setOwner = True
   
  if setOwner:  
    result = sf.query(
      u"select Id from User where FirstName = '%s' and LastName = '%s'"                 
      % (record['Owner First Name'].replace(u"'", u"\\'") , record['Owner Last Name'].replace(u"'", u"\\'"))
    )
  
    if result.size > 1:
      print "Warning: Multiple users with name \"%s %s\" - using first found." \
        % (record['Owner First Name'], record['Owner Last Name'])
    elif result.size == 1:    
      ownerId = result.records[0].Id
    else:
      global invokingUser
      print "Warning: no owning User found for  \"%s %s\" - owner will be \"%s\" " \
        % (record['Owner First Name'], record['Owner Last Name'], invokingUser)
  
  account               = sf.generateObject('Account')
  account.Name          = record['Company']
  account.TickerSymbol  = record['Symbol']  # just used to mark records for testing
  if (setOwner and ownerId != None):
    account.OwnerId     = ownerId
  result                = sf.create(account)
  
  if result.success != True:
    global importSheet, importRow
    msg = "Error: Can't create Account record for %s, result was %s" % (str(record), result)      
    raise ImportError(msg, importSheet, importRow)
    
    
  print "New Account record for %s, Id = %s" % (account.Name, result.id)

  return result

def handleAccountContact(record):
  """ 
    Input to this function is a single record from the import data
    Excel file.  Here, we perform two queries, one to get the AccountId
    and one to get the ContactId, then we add these as new fields to
    the record and pass it back to the caller.
    
    If the Account does not exit - create it, if the contact does not
    exist, then create that too.
  """
  global createMissingAccounts
  
  accountId = None
  result = sf.query(u"select Id, Name from Account where Name = '%s'" % (record['Company']).replace(u"'", u"\\'"))

  if result.size > 1:
    #r['Error'] = 'dup accounts'
    print "Warning: more then one Account record for %s - using first one" % record['Company'] 
    #writeErrorRec(record)
    #return None
    accountId = result.records[0].Id  #.encode('ascii', 'ignore')
    
  if result.size < 1:
    if createMissingAccounts == True:
      accountId = createAccount(record).id
    else:  
      record['Error'] = 'no account'
      print "Error: no Account record for %s" % record['Company']
      writeErrorRec(record)
      return None
  else:
    accountId = result.records[0].Id    

  record['AccountId'] = accountId

  # try contact lookup via email...
  if record['Email'] != None and len(record['Email']) > 0:
    result = sf.query(
      u"""
      select Id, FirstName, LastName, Title, Email from Contact
      where Email = '%s'
      """ % (record['Email'])
    )
  else:
    result = None

  # ...if none, try contact lookup via first & last name
  if result == None or result.size < 1:
    result = sf.query(
      u"""
      select Id, FirstName, LastName, Title, Email from Contact
      where FirstName = '%s' and LastName = '%s'
      """ % (record['First Name'].replace(u"'", u"\\'") , record['Last Name'].replace(u"'", u"\\'") )
    )

  if result.size == 1:
    record['ContactId'] = result.records[0].Id
  elif result.size > 1:
    print result
    print "Warning: more then one Contact record for %s, %s  %s - using first found." \
      % (record['Last Name'], record['First Name'], record['Email'])
    record['ContactId'] = result.records[0].Id
  else:
    if createMissingAccounts == True:
      newContactResult = createContact(record)
      record['ContactId'] = newContactResult.id
    else:
      record['Error'] = 'no contact'
      print "Error: no Contact record for %s, %s %s" \
        % (record['Last Name'], record['First Name'], record['Email'])
      writeErrorRec(record)
      return None

  return record

def importData(fileName):
  """
    Main entry point - opens import data Excel sheet (assumed to be first 
    sheet) and processes each record, one at a time.
  """
  global importSheet, importRow, headers
  book = xlrd.open_workbook(fileName)
  importSheet = book.sheet_by_index(0)
  
  print "importing from %s" % importSheet.name
    
  # get cell value types from first-non header data row (2nd), since headers are all of type text  
  for colnum in range(0, importSheet.ncols):
    headers.append((importSheet.cell(0, colnum).value, importSheet.cell(1, colnum).ctype))
 
  configErrorReporting(headers)
  
  for importRow in range(1, importSheet.nrows):
    record = {}
    for colnum in range(0, importSheet.ncols):
      if headers[colnum][1] == xlrd.XL_CELL_DATE:
        dateTuple = xlrd.xldate_as_tuple(importSheet.cell(rowx=importRow, colx=colnum).value, book.datemode)
        date = datetime.date(dateTuple[0], dateTuple[1], dateTuple[2])
        # required format for xsd:Date type, for web service call
        record[headers[colnum][0]] = date.isoformat()
      else:
        value = importSheet.cell_value(rowx=importRow, colx=colnum)
        if isinstance(value, basestring):
          record[headers[colnum][0]] = value.strip()
        else:
          record[headers[colnum][0]] = value
      #print "%s: %s" % (type(record[headers[colnum]]), record[headers[colnum]])

    record = handleAccountContact(record)

  book.unload_sheet(importSheet.name)

if len(sys.argv) != 2:
  print "%s: Error: must pass Excel file name argument on command line" % sys.argv[0]
  print "e.g.: %s importdata.xls" % sys.argv[0]
  sys.exit(1)

#configErrorReporting()

# old-style exception handling because MacOSX only has Python-2.4
try:
  try:
    loginToSalesforce(username, password, sectoken)
    importData(sys.argv[1])
    erroutSheet.flush_row_data()  
    errorsWorkbook.save('errors.xls')
  except KeyboardInterrupt:
    print "Abort requested by user..."
  except ImportException, e:
    print e
    raise # re-raise for stacktrace
  except:
    print "Error, caught %s: %s " % (sys.exc_info()[0], sys.exc_info()[1])
    raise # re-raise for stacktrace
finally:
  if errorsWorkbook != None and erroutSheet != None:
    erroutSheet.flush_row_data()  
    errorsWorkbook.save('errors.xls')  
