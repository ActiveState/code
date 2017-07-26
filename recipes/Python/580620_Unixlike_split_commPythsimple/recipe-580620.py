import sys
import os

OUTFIL_PREFIX = "out_"

def make_out_filename(prefix, idx):
    '''Make a filename with a serial number suffix.'''
    return prefix + str(idx).zfill(4)

def split(in_filename, lines_per_file):
    '''Split the input file in_filename into output files of 
    lines_per_file lines each. Last file may have less lines.'''
    in_fil = open(in_filename, "r")
    outfil_idx = 1
    out_filename = make_out_filename(OUTFIL_PREFIX, outfil_idx)
    out_fil = open(out_filename, "w")
    # Using chain assignment feature of Python.
    line_count = tot_line_count = file_count = 0
    # Loop over the input and split it into multiple files.
    # A text file is an iterable sequence, from Python 2.2,
    # so the for line below works.
    for lin in in_fil:
        # Bump vars; change to next output file.
        if line_count >= lines_per_file:
            tot_line_count += line_count
            line_count = 0
            file_count += 1
            out_fil.close()
            outfil_idx += 1
            out_filename = make_out_filename(OUTFIL_PREFIX, outfil_idx)
            out_fil = open(out_filename, "w")
        line_count += 1
        out_fil.write(lin)
    in_fil.close()
    out_fil.close()
    sys.stderr.write("Output is in file(s) with prefix {}\n".format(OUTFIL_PREFIX))
        
def usage():
    sys.stderr.write(
    "Usage: {} in_filename lines_per_file\n".format(sys.argv[0]))

def main():

    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    try:
        # Get and validate in_filename.
        in_filename = sys.argv[1]
        # If input file does not exist, exit.
        if not os.path.exists(in_filename):
            sys.stderr.write("Error: Input file '{}' not found.\n".format(in_filename))
            sys.exit(1)
        # If input is empty, exit.
        if os.path.getsize(in_filename) == 0:
            sys.stderr.write("Error: Input file '{}' has no data.\n".format(in_filename))
            sys.exit(1)
        # Get and validate lines_per_file.
        lines_per_file = int(sys.argv[2])
        if lines_per_file <= 0:
            sys.stderr.write("Error: lines_per_file cannot be less than or equal to 0.\n")
            sys.exit(1)
        # If all checks pass, split the file.
        split(in_filename, lines_per_file) 
    except ValueError as ve:
        sys.stderr.write("Caught ValueError: {}\n".format(repr(ve)))
    except IOError as ioe:
        sys.stderr.write("Caught IOError: {}\n".format(repr(ioe)))
    except Exception as e:
        sys.stderr.write("Caught Exception: {}\n".format(repr(e)))
        raise

if __name__ == '__main__':
    main()
