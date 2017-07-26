'''
    -=nero
    Monday, May 08, 2011
'''

import sys
import re
import pprint


class StateMachineFoo(object):
    '''
        This is a template for a finite state machine that is dynamically built based
        on the function names and docstring for the given functions
    '''
    
    
    def __init__(self):
        self.init_sm()
        self.state_trace = []
    
    
    def init_sm(self):
        # find all the states based on the regex
        m                   = re.compile(r'_state.*',re.I)
        
        # return a list of matches
        state_names         = filter(m.search,dir(self))
        
        # get the function pointers to all of our states
        state_ptrs          = [getattr(self,state) for state in state_names]
        
        # from the function pointers, suck up our dockstring and get our transitions
        dictm               = re.compile(r"{.*}",re.S)
        state_trans         = [eval(dictm.search(getattr(state, 'func_doc', '')).group(0)) for state in state_ptrs]
        
        # use zip to create a tuple containing our state_name/state_transition pairings, and add
        # them to the dictionary as key/value pairs
        self.state_machine   = dict(zip(state_names,state_trans))
    
    
    def __str__(self):
        return '\n'.join([
                            '\nSTATE_TRANS_DIAGRAM:',
                            '--------------------',
                            pprint.pformat(self.state_machine),
                            '\nSTATE_TRANSITION_TRACE:',
                            '-----------------------',
                            '\n'.join(self.state_trace),
                        ])
    
    
    def run(self, fname = '_state_start', announce = False):
        '''
            Enter into the state machine here. called run to
            simply because it ties in w/ threading module
            
            fname   - override the beginning state
            announce - print state name as you enter state
        '''
        self.state_trace = []

        while 'None' != fname:
            if announce:
                print '\n\n    %s' % fname.upper().center(60, '*')
            self.state_trace.append(fname)
            ret     = getattr(self, fname)()
            fname   = self.state_machine[fname][ret]

    
    def _state_start(self):
        '''
            {'SUCCESS': '_stateA', 'FAIL': '_state_stop'}
        '''
        return 'SUCCESS'
    
    
    def _state_stop(self):
        '''
            {'SUCCESS': 'None', 'FAIL': 'None'}
        '''
        return 'SUCCESS'
    
    
    def _stateA(self):
        '''
            {'SUCCESS': '_stateB','FAIL': '_error'}
        '''
        error = False
        
        if error:
            return 'FAIL'
        else:
            return 'SUCCESS'
    
    
    def _stateB(self):
        '''
            {'SUCCESS': '_stateD','FAIL':'_error'}
        '''
        error = False
        
        if error:
            return 'FAIL'
        else:
            return 'SUCCESS'
    
    
    def _stateC(self):
        '''
            {'SUCCESS': '_stateA','FAIL':'_error'}
        '''
        error = True
        
        if error:
            return 'FAIL'
        else:
            return 'SUCCESS'
    
    
    def _stateD(self):
        '''
            {'SUCCESS': '_stateE','FAIL':'_error'}
        '''
        error = False
        
        if error:
            return 'FAIL'
        else:
            return 'SUCCESS'
    
    
    def _stateE(self):
        '''
            {'SUCCESS': '_stateC','FAIL':'_error'}
        '''
        error = False
        
        if error:
            return 'FAIL'
        else:
            return 'SUCCESS'
    
    
    def _error(self):
        print "OH NO, AN ERROR!!! <EXITING>"
        print self
        sys.exit(-1)
        
if __name__ == '__main__':

    # this is a really bad way to do this, probably want python argparse module, but for
    # demo purposes, this should allow you to change your start state from the command line
    # the simple/dirty way

    sm          = StateMachineFoo()
    start_state = 'None'  
    
    if len(sys.argv) > 1:
        start_state = sys.argv[1]
    
    sm.run(start_state)
    print sm
