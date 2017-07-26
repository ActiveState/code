import sys
import os

OUTFIL_PREFIX = "out_"

def error_exit(message, code=1):
    sys.stderr.write("Error:\n{}".format(str(message)))
    sys.exit(code)

def err_write(message):
    sys.stderr.write(message)

def make_out_filename(prefix, idx):
    '''Make a filename with a serial number suffix.'''
    return prefix + str(idx).zfill(4)

def bsplit(in_filename, bytes_per_file):
    '''Split the input file in_filename into output files of 
    bytes_per_file bytes each. Last file may have less bytes.'''

    in_fil = open(in_filename, "rb")
    outfil_idx = 1
    out_filename = make_out_filename(OUTFIL_PREFIX, outfil_idx)
    out_fil = open(out_filename, "wb")

    byte_count = tot_byte_count = file_count = 0
    c = in_fil.read(1)

    # Loop over the input and split it into multiple files 
    # of bytes_per_file bytes each (except possibly for the 
    # last file, which may have less bytes.
    while c != '':
        byte_count += 1
        out_fil.write(c)
        # Bump vars; change to next output file.
        if byte_count >= bytes_per_file:
            tot_byte_count += byte_count
            byte_count = 0
            file_count += 1
            out_fil.close()
            outfil_idx += 1
            out_filename = make_out_filename(OUTFIL_PREFIX, outfil_idx)
            out_fil = open(out_filename, "wb")
        c = in_fil.read(1)
    # Clean up.
    in_fil.close()
    if not out_fil.closed:
        out_fil.close()
    if byte_count == 0:
        os.remove(out_filename)
        
def usage():
    err_write(
    "Usage: [ python ] {} in_filename bytes_per_file\n".format(
        sys.argv[0]))
    err_write(
    "splits in_filename into files with bytes_per_file bytes\n".format(
        sys.argv[0]))

def main():

    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    try:
        # Do some checks on arguments.
        in_filename = sys.argv[1]
        if not os.path.exists(in_filename):
            error_exit(
            "Input file '{}' not found.\n".format(in_filename))
        if os.path.getsize(in_filename) == 0:
            error_exit(
            "Input file '{}' has no data.\n".format(in_filename))
        bytes_per_file = int(sys.argv[2])
        if bytes_per_file <= 0:
            error_exit(
            "bytes_per_file cannot be less than or equal to 0.\n")
        # If all checks pass, split the file.
        bsplit(in_filename, bytes_per_file) 
    except ValueError as ve:
        error_exit(str(ve))
    except IOError as ioe:
        error_exit(str(ioe))
    except Exception as e:
        error_exit(str(e))

if __name__ == '__main__':
    main()
