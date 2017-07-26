from winreg import *

def main():
    for hive in Registry():
        show_all(hive)

def show_all(key, level=0):
    if level:
        title(repr(key), level)
    else:
        title('HIVE ' + repr(key), level)
    for name in key.values:
        if name:
            point('%r = %r' % (name, key.values[name]), level + 1)
        else:
            point('(Default) = %r' % key.values[name], level + 1)
    for name in key.keys:
        try:
            show_all(key.keys[name], level + 1)
        except WindowsError:
            title('ERROR: %s' % name, level + 1)

def title(string, level):
    point(string, level)
    point('=' * len(string), level)

def point(string, level):
    print '  ' * level + string

if __name__ == '__main__':
    main()
