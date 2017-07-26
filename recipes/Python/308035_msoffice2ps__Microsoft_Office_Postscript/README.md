## msoffice2ps - a Microsoft Office to Postscript converter

Originally published: 2004-10-12 02:17:43
Last updated: 2007-08-27 08:32:13
Author: Mustafa Görmezer

This Python module converts Microsoft Office documents to Postscript via an installed Postscript printer driver. For example you can build your own Microsoft Office to PDF Converter with Ghostscript. Ready to run applications (webbased or batch converter) you can find at http://win32com.goermezer.de/content/view/156/192/ .\n\nThis script needs Pywin32 from Marc Hammond (http://sourceforge.net/projects/pywin32/) and an installed Postscript printer driver.\n\nSimply import msoffice2ps and make a msoffice2ps.word('c:\\\\testfile.doc', 'c:\\\\testfile.ps', 'ps_printername') to convert a Wordfile to Postscript.