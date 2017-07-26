'''
entrypoint.py
2011 JUL 14
@author: Yoav Glazner 
'''

def entry_point(f):
    '''
    example:
        @entry_point
        def main():
            print("hello world")
    '''
    if f.__module__ == '__main__':
        f()
    return f
