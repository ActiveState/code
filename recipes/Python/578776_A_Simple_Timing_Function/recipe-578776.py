''' Simple Timing Function.
This function prints out a message with the elapsed time from the 
previous call. It works with most Python 2.x platforms. The function 
uses a simple trick to store a persistent variable (clock) without
using a global variable.
'''
import time
def dur( op=None, clock=[time.time()] ):
    if op != None:
        duration = time.time() - clock[0]
        print '%s finished. Duration %.6f seconds.' % (op, duration)
    clock[0] = time.time()

# Example
if __name__ == '__main__':
    import array
    dur()   # Initialise the timing clock
    
    opt1 = array.array('H')
    for i in range(1000):
        for n in range(1000):
            opt1.append(n)
    dur('Array from append')
    
    opt2 = array.array('H')
    seq = range(1000)
    for i in range(1000):
        opt2.extend(seq)
    dur('Array from list extend')
    
    opt3 = array.array('H')
    seq = array.array('H', range(1000))
    for i in range(1000):
        opt3.extend(seq)
    dur('Array from array extend')

# Output:
# Array from append finished. Duration 0.175320 seconds.
# Array from list extend finished. Duration 0.068974 seconds.
# Array from array extend finished. Duration 0.001394 seconds.
