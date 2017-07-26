"""splits a large text file into smaller ones, based on line count

Original is left unmodified.

Resulting text files are stored in the same directory as the original file.

Useful for breaking up text-based logs or blocks of login credentials.

"""

import os

def split_file(filepath, lines_per_file=100):
    """splits file at `filepath` into sub-files of length `lines_per_file`
    """
    lpf = lines_per_file
    path, filename = os.path.split(filepath)
    with open(filepath, 'r') as r:
        name, ext = os.path.splitext(filename)
        try:
            w = open(os.path.join(path, '{}_{}{}'.format(name, 0, ext)), 'w')
            for i, line in enumerate(r):
                if not i % lpf:
                    #possible enhancement: don't check modulo lpf on each pass
                    #keep a counter variable, and reset on each checkpoint lpf.
                    w.close()
                    filename = os.path.join(path,
                                            '{}_{}{}'.format(name, i, ext))
                    w = open(filename, 'w')
                w.write(line)
        finally:
            w.close()

def test():
    """demonstrates the utility of split_file() function"""
    testpath = "/tmp/test_split_file/"
    if not os.path.exists(testpath): os.mkdir(testpath)
    testfile = os.path.join(testpath, "test.txt")
    with open(testfile, 'w') as w:
        for i in range(1, 10001):
            w.write("email{}@myserver.net\tb4dpassw0rd{}\n".format(i, i))
    split_file(testfile, 1000)
