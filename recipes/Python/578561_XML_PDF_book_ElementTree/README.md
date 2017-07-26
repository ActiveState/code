## XML to PDF book with ElementTree and xtopdf  
Originally published: 2013-06-16 19:14:58  
Last updated: 2013-06-16 19:14:58  
Author: Vasudev Ram  
  
This recipe shows how to create a PDF book from XML text content. It requires my xtopdf toolkit, the ElementTree module (from Python's standard library) and the open source version of the ReportLab toolkit.

Create an XML template file like this:

<?xml version="1.0"?>
<book>
        <chapter>
        Chapter 1 content here.
        </chapter>

        <chapter>
        Chapter 2 content here.
        </chapter>
</book>

Then populate the chapter elements with the text of each of the chapters of your book, as text. Call that file, your_book.xml, say.

Then run:

python XMLtoPDFBook.py your_book.xml your_book.pdf

Now the contents of your book will be in your_book.pdf

More details and the full code here:

http://jugad2.blogspot.in/2013/06/create-pdf-books-with-xmltopdfbook.html

- Vasudev Ram
dancingbison.com

