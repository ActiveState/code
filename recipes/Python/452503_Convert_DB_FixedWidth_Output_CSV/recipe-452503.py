# Ian Maurer 
# http://itmaurer.com/
# Convert a Fixed Width file to a CSV with Headers
#
# Requires following format:
#
# header1      header2 header3
# ------------ ------- ----------------
# data_a1      data_a2 data_a3

def writerow(ofile, row):
    for i in range(len(row)):
        row[i] = '"' + row[i].replace('"', '') + '"'
    data = ",".join(row)
    ofile.write(data)
    ofile.write("\n")

def convert(ifile, ofile):
    header = ifile.readline().strip()
    while not header:
        header = ifile.readline().strip()

    hticks = ifile.readline().strip()
    csizes = [len(cticks) for cticks in hticks.split()]
    
    line = header
    while line:

        start, row = 0, []
        for csize in csizes:
            column = line[start:start+csize].strip()
            row.append(column)
            start = start + csize + 1

        writerow(ofile, row)
        line = ifile.readline().strip()

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        ifile = open(sys.argv[1], "r")
        ofile = open(sys.argv[2], "w+")
        convert(ifile, ofile)
        
    else:
        print "Usage: python convert.py <input> <output>"
