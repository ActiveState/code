## How to use Cyrillic fonts in ReportLab PDF library  
Originally published: 2005-08-06 10:02:14  
Last updated: 2005-08-06 10:02:14  
Author: Yuriy Tkachenko  
  
By default ReportLab PDF library <http://www.reportlab.com> doesn't allow
easy using Cyrillic fonts for generating PDF documents. The following example
explains how to use any font in the Adobe AFM ('Adobe Font Metrics') and PFB
('Printer Font Binary') format (aka Type 1) which supports Unicode Cyrillic
characters (glyphs). It assumes that you have font files named 'a010013l.afm'
and 'a010013l.pfb' in the same directory with this example.
The font files can be found in /usr/share/fonts/default/Type1 directory in
many Linux distributions.