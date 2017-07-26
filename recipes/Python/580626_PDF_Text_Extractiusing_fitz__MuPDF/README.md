###PDF Text Extraction using fitz / MuPDF (PyMuPDF)

Originally published: 2016-03-17 11:56:02
Last updated: 2016-03-17 12:00:06
Author: Jorj X. McKie

Extract all the text of a PDF (or other supported container types) at very high speed.\nIn general, text pieces of a PDF page are not arranged in natural reading order, but in the order they were entered during PDF creation.\nThis script re-arranges text blocks according to their pixel coordinates to achieve a more readable output, i.e. top-down, left-right.