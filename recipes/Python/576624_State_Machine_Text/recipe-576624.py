"""
LineStateMachine.py

General state machine mechanism plus a specialized version,
LineStateMachine, for processing text files based on regular expression 
line matching.

Implementing a specific LineStateMachine
========================================
* Analyze states necessary for state machine
* Create states as subclasses of LineState.
  - Set ID for state.
  - Determine regular expression that signal transitions.
  - Set TRANSITIONS list for list of regexes and corresponding next states.
  - Order TRANSITIONS so that more general regexes are tested later, e.g.
    testing (.*) first will prevent any other transitions from being tested.
  - Write handler to extract info cargo match_object for current line,
    then call LineState.handle() to continue processing text.
* Subclass LineStateCargo to contain information to be shared and accumulated
  between states over course of text processing.
* Subclass LineStateMachine.
  - Add states to initializer.
  - Start LineStateMachine by calling run() with start state and cargo 
    containing text file pointer.

See ReportStateMachine example below. 

Extensively rewritten from sample code in "Text Processing in Python" by 
David Mertz, pp. 274-280, which can be found at http://gnosis.cx/TPiP/chap4.txt.

Jack Trainor 2009
"""
import string
import re

# ======================================================================
# StateMachine layer
# ======================================================================
END_STATE_ID = "END"
ERROR_STATE_ID = "ERROR"
NONE_STATE_ID = ""

class Cargo(object):
    """ Instances of Cargo and its subclasses contain information to be shared 
    and accumulated between states and returned to state machine caller. """
    def __init__(self):
        self.error_msg = ""
    
class State(object):
    """ States are instances based on class variables and a handler function. 
    The state handler runs until it hits transition to the next state. """
    ID = NONE_STATE_ID
    TRANSITIONS = []
    def handle(self, cargo):
        return NONE_STATE_ID, cargo
    
class StateMachine(object):
    """ Minimal state machine that runs based on state ids and state dictionary. """
    def __init__(self):
        self.states = {}
    
    def add_state(self, state):
        self.states[state.ID] = state

    def run(self, start_state_id, cargo):
        state_id = start_state_id
        while state_id:
            state = self.states.get(state_id, None)
            if state:
                state_id, cargo = state.handle(cargo)
            else:
                raise RuntimeError, "%s state does not exist." % state_id
        return cargo 
    
# ======================================================================
# LineStateMachine layer
# ======================================================================
class LineStateCargo(Cargo):
    """ Cargo specific to LineState's. """
    def __init__(self, fp):
        Cargo.__init__(self)
        self.fp = fp      
        # match_object is saved for next state to extract text information.
        self.match_object = None
        # buffer are unmatched lines accumulated in state for possible use.
        self.buffer = []

class LineStateTransition(object):
    def __init__(self, match_re, next_state_id):
        self.match_re = match_re
        self.next_state_id = next_state_id
    
class LineState(State):
    """ A LineState reads lines until the file ends or the LineState matches
    a compiled regex expression in its transition list, then it returns the
    next state id of that transition with the current cargo. Lines that
    don't match a transition are accumulated into cargo.buffer to be used by
    the current state or the next state. """
    ID = NONE_STATE_ID
    TRANSITIONS = []
    def handle(self, cargo):
        cargo.buffer = []
        next_state_id = NONE_STATE_ID
        while not next_state_id:
            line = cargo.fp.readline()
            if line:
                for transition in self.TRANSITIONS:
                    cargo.match_object = transition.match_re.match(line)
                    if cargo.match_object:
                        next_state_id = transition.next_state_id
                        break
            else:
                next_state_id = END_STATE_ID
                    
            if not next_state_id:
                cargo.buffer.append(line)
            
        return next_state_id, cargo

class EndState(State):
    ID = END_STATE_ID
    def handle(self, cargo):
        cargo.fp.close()
        print "Normal termination"
        return NONE_STATE_ID, cargo

class ErrorState(State):
    ID = ERROR_STATE_ID
    def handle(self, cargo):
        cargo.fp.close()
        print "Error:", cargo.error_msg
        return NONE_STATE_ID, cargo
        
class LineStateMachine(StateMachine):
    def __init__(self):
        StateMachine.__init__(self)
        self.add_state(EndState())
        self.add_state(ErrorState())

# ======================================================================
# ReportStateMachine layer
# ======================================================================
START_STATE_ID = "START"
COMPANY_STATE_ID = "COMPANY"
ORDER_STATE_ID = "ORDER"
COMMENT_START_STATE_ID = "COMMENT_START"
COMMENT_END_STATE_ID = "COMMENT_END"

COMPANY_RE = re.compile(r"^>> (.*)\s*$")
ORDER_RE = re.compile(r"^\s*(\w+)\s+(\d+)([Kk]*).*$")
COMMENT_START_RE = re.compile(r"^\*(.*)$")
COMMENT_END_RE = re.compile(r"^(.*)\*$")

class ReportStateCargo(LineStateCargo):
    def __init__(self, fp):
        LineStateCargo.__init__(self, fp)
        self.company = ""
        self.amount = 0
    
class StartState(LineState):    
    ID = START_STATE_ID
    TRANSITIONS = [ 
            LineStateTransition(COMPANY_RE, COMPANY_STATE_ID),
            LineStateTransition(COMMENT_START_RE, COMMENT_START_STATE_ID)     
        ]
    def handle(self, cargo):
        return LineState.handle(self, cargo)
    
class CompanyState(LineState):
    ID = COMPANY_STATE_ID
    TRANSITIONS = [ 
            LineStateTransition(COMPANY_RE, COMPANY_STATE_ID),
            LineStateTransition(ORDER_RE, ORDER_STATE_ID),
            LineStateTransition(COMMENT_START_RE, COMMENT_START_STATE_ID)
        ]
    def handle(self, cargo):
        cargo.company = cargo.match_object.group(1)
        cargo.amount = 0
        return LineState.handle(self, cargo)
        
class OrderState(LineState):
    ID = ORDER_STATE_ID
    TRANSITIONS = [ 
            LineStateTransition(COMPANY_RE, COMPANY_STATE_ID),
            LineStateTransition(ORDER_RE, ORDER_STATE_ID),
            LineStateTransition(COMMENT_START_RE, COMMENT_START_STATE_ID)
        ]
    def handle(self, cargo):
        product = cargo.match_object.group(1)
        quantity = get_quantity(cargo.match_object.group(2) + cargo.match_object.group(3))
        price = get_product_price(cargo.company, product)
        cargo.amount += quantity * price       
        next_state_id, cargo = LineState.handle(self, cargo)
        if next_state_id != ORDER_STATE_ID:
            print_invoice(cargo.company, cargo.amount)
        return next_state_id, cargo
        
class CommentStartState(LineState):
    ID = COMMENT_START_STATE_ID
    TRANSITIONS = [ 
            LineStateTransition(COMMENT_END_RE, COMMENT_END_STATE_ID)
        ]
    def handle(self, cargo):
        comment_line = cargo.match_object.group(1)        
        if comment_line and comment_line[-1] == "*":
            next_state_id = COMMENT_END_STATE_ID
        else:
            next_state_id, cargo = LineState.handle(self, cargo)
        return next_state_id, cargo
        
class CommentEndState(LineState):
    ID = COMMENT_END_STATE_ID
    TRANSITIONS = [ 
            LineStateTransition(COMPANY_RE, COMPANY_STATE_ID),
            LineStateTransition(ORDER_RE, ORDER_STATE_ID),
            LineStateTransition(COMMENT_START_RE, COMMENT_START_STATE_ID)
        ]
    def handle(self, cargo):
        comment_line = cargo.match_object.group(1)    
        return LineState.handle(self, cargo)
        
class ReportStateMachine(LineStateMachine):
    def __init__(self):
        LineStateMachine.__init__(self)
        self.add_state(StartState())
        self.add_state(CompanyState())
        self.add_state(OrderState())
        self.add_state(CommentStartState())
        self.add_state(CommentEndState())

# ======================================================================
# Report utility functions
# ======================================================================
# Discount consists of dollar requirement and a percentage reduction.
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

def get_company_id(company):
    if company.upper().find("ACME") >= 0:
        return "ACME"
    elif company.upper().find("MEGAMART") >= 0:
        return "MEGAMART"
    else:
        return "STANDARD"

def get_discount_schedule(company):
    return discount_schedules.get(get_company_id(company), discount_schedules["STANDARD"])

def get_product_price(company, product):
    prices = item_prices.get(get_company_id(company), item_prices["STANDARD"])
    return prices[product]

def get_discount_type(company):
    return discount_types.get(get_company_id(company), discount_types["STANDARD"])

def get_discounted_amount(company, amount):
    multiplier = 1.0
    for threshhold, percent in get_discount_schedule(company):
        if amount >= threshhold: multiplier = 1 - float(percent)/100
    return amount * multiplier

def get_quantity(quantity):
    quantity = string.replace(string.upper(quantity),'K','000')
    quantity = int(quantity)
    return quantity

def print_invoice(company, amount):
    print "Company name:", company, "(%s discounts)" % get_discount_type(company)
    print "Invoice total: $", get_discounted_amount(company, amount), '\n'

# ======================================================================
# ReportStateMachine test
# ======================================================================
REPORT = """MONTHLY REPORT -- April 2002
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

* Note to Donald: The best contact for Acme is Debbie Franklin, at
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

def test():
    import StringIO
    fp = StringIO.StringIO(REPORT)
    cargo = ReportStateMachine().run(START_STATE_ID, ReportStateCargo(fp))

if __name__ == "__main__":
    test()
