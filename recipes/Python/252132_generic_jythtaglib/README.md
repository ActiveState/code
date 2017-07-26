## A generic jython taglib for tomcat  
Originally published: 2003-11-17 06:23:23  
Last updated: 2003-11-17 14:33:29  
Author: Ferdinand Jamitzky  
  
These java classes implement a jython taglib which can be used to embed jython code into jsp pages. It consists of two tags:
<jython:exec> ...some code... </jython:exec>
and
<jython:get var=.../>
With these two tags you can write active jython pages.