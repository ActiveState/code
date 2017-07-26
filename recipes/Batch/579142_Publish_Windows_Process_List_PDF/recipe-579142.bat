1: Run TASKLIST and redirect its output to a text file.

$ tasklist > tasklist.out

2: Sort the file into another file.

$ sort /+65 tasklist.out > tasklist.srt

(Sort the output of TASKLIST by the character position of the Mem Usage field.)

3: Go edit tasklist to put the header lines back at the top :)
[ They get dislodged by the sort. ]

4: Pipe the sorted task list to StdinToPDF, to generate the PDF output.

$ type tasklist.srt | python StdinToPDF.py tasklist.pdf
