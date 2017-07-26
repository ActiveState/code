# ruler.py
"""
Program to display a ruler on the console.
Author: Vasudev Ram
Copyright 2016 Vasudev Ram - http://jugad2.blogspot.com

Description: Program to display a ruler on the command-line screen.
The ruler consists of repeated occurrences of the characters:
0123456789, concatenated, with interals of 10's marked above or below.

Purpose: By running this program, you can use its output as a ruler,
to find the position of your own program's output on the line, or to 
find the positions and lengths of fields in fixed- or variable-length 
records in a text file, fields in CSV files, etc.
"""

REPS = 8

def ruler(sep=' ', reps=REPS):
    for i in range(reps):
        print str(i) + ' ' * 4 + sep + ' ' * 3,
    print '0123456789' * reps

def main():

    # Without divider.
    ruler()

    # With various dividers.
    for sep in '|+!':
        ruler(sep)

if __name__ == '__main__':
    main()
