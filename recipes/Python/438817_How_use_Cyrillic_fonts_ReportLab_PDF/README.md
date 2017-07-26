## How to use Cyrillic fonts in ReportLab PDF libraryOriginally published: 2005-08-06 10:02:14 
Last updated: 2005-08-06 10:02:14 
Author: Yuriy Tkachenko 
 
By default ReportLab PDF library <http://www.reportlab.com> doesn't allow\neasy using Cyrillic fonts for generating PDF documents. The following example\nexplains how to use any font in the Adobe AFM ('Adobe Font Metrics') and PFB\n('Printer Font Binary') format (aka Type 1) which supports Unicode Cyrillic\ncharacters (glyphs). It assumes that you have font files named 'a010013l.afm'\nand 'a010013l.pfb' in the same directory with this example.\nThe font files can be found in /usr/share/fonts/default/Type1 directory in\nmany Linux distributions.