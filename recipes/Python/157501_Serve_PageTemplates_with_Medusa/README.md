## Serve PageTemplates with Medusa  
Originally published: 2002-10-18 17:16:53  
Last updated: 2002-10-18 17:16:53  
Author: Troy Melhase  
  
This recipe combines the delicious PageTemplates package with the flavorful Medusa package to serve up rendered PageTemplates from the file system.

Why not just use Zope you say?  As far as I know, the current Zope release isn't an option with Python 2.2 code.  The project for which this recipe was devised requires Python 2.2.

Ingredients you'll need:

1.	Python 2.2.  If you're using 2.1, try Zope instead, as it does everything this recipe can do plus a whole lot more.

2.	ExtensionClass and friends.  There is more than one way to get ExtensionClass installed, but the method I've used successfully is to install StandaloneZODB.  That package is available here:  http://www.zope.org/Products/StandaloneZODB

3.	PageTemplates, TAL, and ZTUtils packages.  These are available in the Zope source releases but must be installed manually.  Again, there's more than one way to make these packages available in your system.  The method I've used is to copy the package directories from the Zope source archive into the Python lib/site-packages/ directory.  The Zope source is available from this link:  http://www.zope.org/Products

4.	Medusa.  I used Medusa 0.5.2 to develop this recipe, but you may have an equally pleasant experience with other versions.  You can get Medusa here:  http://oedipus.sourceforge.net/medusa/

5.	A Medusa startup script.  As with all Medusa handlers, you must explicitly construct a PageTemplates handler and associate it with an HTTP server.  You can modify a copy of the sample startup script included with Medusa or create your own.

6.	Some PageTemplates.  The code below reads PageTemplates markup from files stored in your file system.  Give your markup files a ".pt" or ".ptx" extension, and the handler will try to render them as PageTemplates before returning their markup.

Once you have all these items in place, modify your Medusa start up script:

1.	Save the code below as "pagetemplate_handler.py", and bring it into your script:  import pagetemplate_handler

2.	Construct a pagetemplate_handler.pagetemplate_handler, pagetemplate_handler.pagetemplate_xml_handler, or both.   These types need a filesystem object, just like the default_handler.

3.	Associate your pagetemplate_handler with your HTTP server.