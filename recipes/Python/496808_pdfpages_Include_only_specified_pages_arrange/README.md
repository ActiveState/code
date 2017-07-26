###pdf-pages: Include only specified pages and arrange several on a sheet of paper

Originally published: 2006-06-20 13:16:00
Last updated: 2006-07-02 02:46:22
Author: Scott Tsai

Taking a PDF file as input, include only the specified pages and optionally arrange several pages on a sheet of paper on output.\nSimilar to the "psnup" program for Postscript.\n\nRun it like:\n$./pdf-pages --pages=2-13,17-19 --nup=1 report.pdf\nThe output file will be "report-pdf-pages.pdf".\n\nRequires the "pdflatex" program.