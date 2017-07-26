import fileinput

def sort_file():
    """ Sort the lines in the file named on standard input,
    outputting the sorted lines on stdout.

    Example call (from command line)
    sort_file.py unsorted.txt > sorted.txt
    """
    lines=[] # give lines variable a type of list
    for line in fileinput.input(): lines.append(line.rstrip())
    lines.sort()
    for line in lines: print line

if __name__ == "__main__":
    sort_file()
