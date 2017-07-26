"""
LineOrientedStateMachine.py

State machine for processing text files on a line-by-line basis using regular 
expressions to determine transition to next state. 

Subclass LineOrientedStateMachine, determine states, then set up dictionaries
for navigation using regular expressions as keys to states as values. Extract
information from regular expression match objects, and accumulate processed
information in 'cargo' object. Unmatched line accumulate in the cargo.buffer until the next state is reached.

See ExampleStateMachine below. Developed from sample code in "Text Processing 
in Python" by David Mertz,pp. 274-280, which can be found at 
http://gnosis.cx/TPiP/chap4.txt. Code below processes Mertz's example 
identically.

Jack Trainor 2008
"""

import sys
import string
import re
import StringIO

class InitializationError(Exception): pass

class StateMachine:
    """ from David Mertz """
    def __init__(self):
        self.handlers = []
        self.startState = None
        self.endStates = []

    def addState(self, handler, endState=False):
        self.handlers.append(handler)
        if endState:
          self.endStates.append(handler)

    def setStart(self, handler):
        self.startState = handler

    def run(self, cargo=None):
        if not self.startState:
            raise InitializationError, "must call .setStart() before .run()"
        if not self.endStates:
            raise InitializationError, "at least one state must be an endState"
        handler = self.startState
        while True:
            (newState, cargo) = handler(cargo)
            if newState in self.endStates:
                newState(cargo)
                break
            elif newState not in self.handlers:
                raise RuntimeError, "Invalid target %s" % newState
            else:
                handler = newState
        return self

class Cargo(object):
    def __init__(self):
        self.path = ""
        self.fp = None
        self.navigation = {}
        self.matchObject = None
        self.buffer = None
        self.errorMsg = ""

class LineOrientedStateMachine(StateMachine):
    def __init__(self, fp):
        StateMachine.__init__(self)
        self.fp = fp

    def match(self, cargo, compiledRe, line):
        cargo.matchObject = compiledRe.match(line)
        return (cargo.matchObject != None)

    def readLoop(self, cargo):
        """ Keep reading lines until a change to next state is triggered """
        cargo.buffer = []
        next = ()
        while not next:
            line = cargo.fp.readline()
            
            if not line:
                next = self.END, (cargo)
            else:
                for matchRe in cargo.navigation.keys():
                    if self.match(cargo, matchRe, line):
                        state = cargo.navigation[matchRe]
                        next = state, (cargo)
                        break
                    
            if not next:
                cargo.buffer.append(line)
                #print "BUFFER:", line
            
        return next
    
    def getErrorNext(self, cargo, errorMsg):
        cargo.errorMsg = errorMsg
        return (self.ERROR, (cargo))
        
    def END(self, cargo):
        cargo.fp.close()
        print "Normal termination"
        
    def ERROR(self, cargo):
        cargo.fp.close()
        print "Error:", cargo.errorMsg



class ExampleCargo(Cargo):
    def __init__(self):
        Cargo.__init__(self)
        self.company = ""
        self.amount = 0

class ExampleStateMachine(LineOrientedStateMachine):
    COMPANY_RE = re.compile(r"^>> (.*)\s*$")
    ORDER_RE = re.compile(r"^\s*(\w+)\s+(\d+)([Kk]*).*$")
    COMMENT_START_RE = re.compile(r"^\*(.*)$")
    COMMENT_END_RE = re.compile(r"^(.*)\*$")
    def __init__(self, fp):
        LineOrientedStateMachine.__init__(self, fp)        
        self.addState(self.START)
        self.addState(self.COMPANY)
        self.addState(self.ORDER)
        self.addState(self.COMMENT_START)
        self.addState(self.COMMENT_END)
        self.addState(self.END, endState=True)
        self.addState(self.ERROR, endState=True)       
        self.setStart(self.START)

    def START(self, cargo):
        cargo = ExampleCargo()
        cargo.fp = self.fp
        cargo.navigation = {self.COMPANY_RE       : self.COMPANY,
                            self.COMMENT_START_RE : self.COMMENT_START                          
                            }
        next = self.readLoop(cargo)
        return next
    
    def COMPANY(self, cargo):
        cargo.company = cargo.matchObject.group(1)
        cargo.amount = 0
        cargo.navigation = {self.COMPANY_RE       : self.COMPANY,
                            self.ORDER_RE         : self.ORDER,
                            self.COMMENT_START_RE : self.COMMENT_START                          
                            }
        #print "COMPANY:", cargo.company
        next = self.readLoop(cargo)
        return next

    def ORDER(self, cargo):
        product = cargo.matchObject.group(1)
        quantity = getQuantity(cargo.matchObject.group(2) + cargo.matchObject.group(3))
        price = getProductPrice(cargo.company, product)
        cargo.amount += quantity * price       
        cargo.navigation = {self.COMPANY_RE       : self.COMPANY,
                            self.ORDER_RE         : self.ORDER,
                            self.COMMENT_START_RE : self.COMMENT_START                          
                            }
        #print "ORDER:", product, quantity, price, cargo.amount
        next = self.readLoop(cargo)
        if (next[0] != self.ORDER):
            printInvoice(cargo.company, cargo.amount)
        return next

    def COMMENT_START(self, cargo):
        comment = cargo.matchObject.group(1)        
        #print "COMMENT:", comment
        if comment and comment[-1] == "*":
            next = self.COMMENT_END, (cargo)
        else:
            cargo.navigation = {self.COMMENT_END_RE : self.COMMENT_END }
            next = self.readLoop(cargo)
        return next

    def COMMENT_END(self, cargo):
        commentLine = cargo.matchObject.group(1)        
        cargo.navigation = {self.COMPANY_RE       : self.COMPANY,
                            self.ORDER_RE         : self.ORDER,
                            self.COMMENT_START_RE : self.COMMENT_START                          
                            }
        next = self.readLoop(cargo)
        return next
 

REPORT = """
MONTHLY REPORT -- April 2002
===================================================================

Rules:
 - Each buyer has price schedule for each item (func of quantity).
 - Each buyer has a discount schedule based on dollar totals.
 - Discounts are per-order (i.e.  contiguous block)
 - Buyer listing starts with line containing ">>", then buyer name.
 - Item quantities have name-whitespace-number, one per line.
 - Comment sections begin with line starting with an asterisk,
   and ends with first line that ends with an asterisk.

>> Acme Purchasing

  widgets      100
  whatzits    1000
  doodads     5000
  dingdongs   20

* Note to Donald: The best contact for Acme is Debbie Franlin, at
* 413-555-0001.  Fallback is Sue Fong (call switchboard). *

>> Megamart

doodads   10k
whatzits  5k

>> Fly-by-Night Sellers
   widgets        500
   whatzits      4
   flazs         1000

* Note to Harry: Have Sales contact FbN for negotiations *

*
Known buyers:
>>  Acme
>>  Megamart
>>  Standard (default discounts)
*

*** LATE ADDITIONS ***

>> Acme Purchasing
widgets      500     (rush shipment)**
"""

#-- General support functions
# Discount consists of dollar requirement and a percentage reduction
# Each buyer can have an ascending series of discounts, the highest
# one applicable to a month is used.
discount_schedules = {
    "STANDARD"  : [(5000,10),(10000,20),(15000,30),(20000,40)],
    "ACME"      : [(1000,10),(5000,15),(10000,30),(20000,40)],
    "MEGAMART"  : [(2000,10),(5000,20),(10000,25),(30000,50)],
    "BAGOBOLTS" : [(2500,10),(5000,15),(10000,25),(30000,50)],
  }
item_prices = {
    "STANDARD"  : {'widgets':1.0, 'whatzits':0.9, 'doodads':1.1,
                 'dingdongs':1.3, 'flazs':0.7},
    "ACME"      : {'widgets':0.9, 'whatzits':0.9, 'doodads':1.0,
                 'dingdongs':0.9, 'flazs':0.6},
    "MEGAMART"  : {'widgets':1.0, 'whatzits':0.8, 'doodads':1.0,
                 'dingdongs':1.2, 'flazs':0.7},
    "BAGOBOLTS" : {'widgets':0.8, 'whatzits':0.9, 'doodads':1.1,
                 'dingdongs':1.3, 'flazs':0.5},
  }
discount_types = {
    "STANDARD"  : "standard",
    "ACME"      : "negotiated",
    "MEGAMART"  : "negotiated"
    }

def getCompanyId(company):
    if company.upper().find("ACME") >= 0:
        return "ACME"
    elif company.upper().find("MEGAMART") >= 0:
        return "MEGAMART"
    else:
        return "STANDARD"

def getDiscountSchedule(company):
    return discount_schedules.get(getCompanyId(company), discount_schedules["STANDARD"])

def getProductPrice(company, product):
    prices = item_prices.get(getCompanyId(company), item_prices["STANDARD"])
    return prices[product]

def getDiscountType(company):
    return discount_types.get(getCompanyId(company), discount_types["STANDARD"])

def getDiscountedAmount(company, amount):
    multiplier = 1.0
    for threshhold, percent in getDiscountSchedule(company):
        if amount >= threshhold: multiplier = 1 - float(percent)/100
    return amount * multiplier

def getQuantity(quantity):
    quantity = string.replace(string.upper(quantity),'K','000')
    quantity = int(quantity)
    return quantity

def printInvoice(company, amount):
    print "Company name:", company, "(%s discounts)" % getDiscountType(company)
    print "Invoice total: $", getDiscountedAmount(company, amount), '\n'


def main():
    parser = ExampleStateMachine(StringIO.StringIO(REPORT)).run()

if __name__ == "__main__":
    main()
