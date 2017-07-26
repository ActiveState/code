## XYAPTU: Lightweight XML/HTML Document Template Engine for Python 
Originally published: 2002-11-13 08:07:57 
Last updated: 2002-11-18 15:01:35 
Author: Mario Ruggier 
 
Xyaptu builts on Alex Martelli's generic and elegant module, YAPTU (Yet Another Python Template Utility), to instantiate XML/HTML document templates that include python code for presentational purposes. The goal is _not_ to be able to embed program logic in a document template. This is counter productive if a separation of content and logic is desired. The goal _is_ to be able to prepare arbitrarily complex presentation templates, while offering a simple and open-ended means to hook in application data. A page template may therefore contain anything that targeted clients will accept, with the addition of five XML tags and one 'pcdata' expression token, as mark-up for the python code that defines the coupling between the presentation to the application data.