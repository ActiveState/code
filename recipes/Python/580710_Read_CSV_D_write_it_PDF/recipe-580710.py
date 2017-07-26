First, the D program, read_csv.d:

/**************************************************
File: read_csv.d
Purpose: A program to read CSV data from a file and 
write it to standard output.
Author: Vasudev Ram
Date created: 2016-10-25
Copyright 2016 Vasudev Ram
Web site: https://vasudevram.github.io
Blog: http://jugad2.blogspot.com
Product store: https://gumroad.com/vasudevram
**************************************************/

import std.algorithm;
import std.array;
import std.csv;
import std.stdio;
import std.file;
import std.typecons;

int main()
{
    try {
        stderr.writeln("Reading CSV data from file.");
        auto file = File("input.csv", "r");
        foreach (record;
            file.byLine.joiner("\n").csvReader!(Tuple!(string, string, int)))
        {
            writefln("%s works as a %s and earns $%d per year",
                     record[0], record[1], record[2]);
        }
    } catch (CSVException csve) {
        stderr.writeln("Caught CSVException: msg = ", csve.msg, 
        " at row, col = ", csve.row, ", ", csve.col);
    } catch (FileException fe) {
        stderr.writeln("Caught FileException: msg = ", fe.msg);
    } catch (Exception e) {
        stderr.writeln("Caught Exception: msg = ", e.msg);
    }
    return 0;
}

It can be compiled with the command:

dmd read_csv.d

Next the Python program, StdinToPDF.py:

# StdinToPDF.py

# Read the contents of stdin (standard input) and write it to a PDF file 
# whose name is specified as a command line argument.
# Author: Vasudev Ram - http://www.dancingbison.com
# This program is part of the xtopdf toolkit:
#     https://bitbucket.org/vasudevram/xtopdf

import sys
from PDFWriter import PDFWriter

try:
    with PDFWriter(sys.argv[1]) as pw:
        pw.setFont("Courier", 12)
        for lin in sys.stdin:
            pw.writeLine(lin)
except Exception, e:
    print "ERROR: Caught exception: " + repr(e)
    sys.exit(1)

And last, the command-line pipeline that runs the two programs above:

read_csv | python StdinToPDF.py csv_output.pdf

After running the pipeline above, the final output (the CSV data, converted to PDF) will be in the file csv_output.pdf, which you can view in any suitable PDF viewer  program, such as Foxit PDF Reader or Windows or evince on Linux.
