# CSV to Flat-file Converter
# FB - 20150802
import sys

delimiterInputFile = "," # ";" "|"
delimiterOutputFile = " " # "" "," ";" "|"

if len(sys.argv) != 3:
    print "USAGE:"
    print "[python] CSV2FlatFile.py InputFile OutputFile"
    sys.exit()

inputFileName = sys.argv[1]
outputFileName = sys.argv[2]

inputFile = open(inputFileName, "r")
inputFileLines = inputFile.readlines()
inputFile.close()
if len(inputFileLines) == 0:
    print "No input data!"
    sys.exit()
# strip EOL
for j, inputFileLine in enumerate(inputFileLines):
    inputFileLines[j] = inputFileLines[j].strip()

numColumns = len(inputFileLines[0].split(delimiterInputFile))
maxColumnLengths = [0 for i in range(numColumns)]
# find max length for each column
for inputFileLine in inputFileLines:
    inputFileLineList = inputFileLine.split(delimiterInputFile)
    for i in range(numColumns):
        if len(inputFileLineList[i]) > maxColumnLengths[i]:
            maxColumnLengths[i] = len(inputFileLineList[i])
    
outputFile = open(outputFileName, "w")
for inputFileLine in inputFileLines:
    inputFileLineList = inputFileLine.split(delimiterInputFile)
    for i in range(numColumns):
        inputFileLineList[i] = inputFileLineList[i].ljust(maxColumnLengths[i])
    outputFileLine = delimiterOutputFile.join(inputFileLineList)
    outputFile.write(outputFileLine + "\n")
outputFile.close()
