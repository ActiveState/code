import msvcrt
import time

def PrintStatic(Value, Prefix=''):
    ValStr = Prefix + `Value`
    map(lambda x:msvcrt.putch(x),ValStr + len(ValStr) * '\x08')

for i in range(50):
    PrintStatic(i, '        ')
    time.sleep(0.1)
PrintStatic('Completed.')
 
