from datetime import datetime
from functools import wraps

def dynamic(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        for key, value in fn.__annotations__.items():
            try:
                kwargs[key] = value()
            except TypeError:
                pass
            
        return fn(*args, **kwargs)
    return wrapper


# Example

@dynamic
def printNow(l:list, now:datetime.now):
    l.append(len(l))
    
    print('List:', l, ' id:', id(l))
    print('Now:', now)
    
# Test

for i in range(3):
    printNow()
    print()
