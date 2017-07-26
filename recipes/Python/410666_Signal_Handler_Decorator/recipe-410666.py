# a decorator to wrap signal handlers
import signal

def signal_handler( signal_number ):
    """
    A decorator to set the specified function as handler for a signal.
    This function is the 'outer' decorator, called with only the (non-function) 
    arguments
    """
    
    # create the 'real' decorator which takes only a function as an argument
    def __decorator( function ):
        signal.signal( signal_number, function )
        return function
    
    return __decorator
   

    
if __name__ == "__main__":
    """test the decorator"""
    
    sigterm_received = False
    
    @signal_handler(signal.SIGTERM)
    def handle_sigterm(signum, frame):
        """handle sigterm for test"""
        global sigterm_received
        sigterm_received = True
        
    assert not sigterm_received

    # send ourselves sigterm    
    import os
    import time
    os.kill(os.getpid(), signal.SIGTERM)
    
    time.sleep(0.1)
        
    assert sigterm_received
    print "OK"
