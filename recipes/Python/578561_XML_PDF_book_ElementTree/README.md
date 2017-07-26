## XML to PDF book with ElementTree and xtopdf

Originally published: 2013-06-16 19:14:58
Last updated: 2013-06-16 19:14:58
Author: Vasudev Ram

This recipe shows how to create a PDF book from XML text content. It requires my xtopdf toolkit, the ElementTree module (from Python's standard library) and the open source version of the ReportLab toolkit.\n\nCreate an XML template file like this:\n\n<?xml version="1.0"?>\n<book>\n        <chapter>\n        Chapter 1 content here.\n        </chapter>\n\n        <chapter>\n        Chapter 2 content here.\n        </chapter>\n</book>\n\nThen populate the chapter elements with the text of each of the chapters of your book, as text. Call that file, your_book.xml, say.\n\nThen run:\n\npython XMLtoPDFBook.py your_book.xml your_book.pdf\n\nNow the contents of your book will be in your_book.pdf\n\nMore details and the full code here:\n\nhttp://jugad2.blogspot.in/2013/06/create-pdf-books-with-xmltopdfbook.html\n\n- Vasudev Ram\ndancingbison.com\n\n