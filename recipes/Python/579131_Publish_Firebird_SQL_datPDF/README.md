## Publish Firebird SQL data to PDF with xtopdf

Originally published: 2015-12-01 19:45:17
Last updated: 2015-12-01 19:45:18
Author: Vasudev Ram

This recipe shows how to publish data from the Firebird RDBMS to PDF, using the xtopdf toolkit and the fbd Python driver for Firebird. Firebird is a cross-platform, open source RDBMS based on the former Interbase RDBMS from Borland, which they used to bundle with some of their developmemt tools, such as Borland C++ and Borland Delphi.\n\nThe recipe reads data from a Firebird table, using the fbd Python driver for Firebird, and writes it to PDF, using the xtopdf toolkit. See:\n\nhttp://jugad2.blogspot.in/p/xtopdf-pdf-creation-library.html\n\nfor information on xtopdf.\n\nIt assumes that a Firebird database called test.fdb exists under /temp/firebird (C:\\temp\\firebird, really - the test was done on Windows), and that it has a contacts table with the structure shown in the code of the recipe.\n\nMore details and sample output are here:\n\nhttp://jugad2.blogspot.in/2014/01/by-vasudev-ram-pdf-firebird-is-cross.html\n\n