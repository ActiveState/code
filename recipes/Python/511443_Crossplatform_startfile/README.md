## Cross-platform startfile and mailto functions

Originally published: 2007-04-01 07:35:42
Last updated: 2008-09-20 04:39:16
Author: Antonio Valentino

This recipe provides a couple of cross-platform utility functions, 'open' and 'mailto', for opening files and URLs in the registered default application and for sending e-mails using the user's preferred composer.\nThe python standard library already provides the os.startfie function that allows the user to open a generic file in the associated application but it only works on Windows.\nThe 'webbrowser' module is cross-platform but only handles a specific kind of application, the web browser, and it is useless if one wants to open e.g. a source code python file in the user's preferred text editor.\nThe 'open' function simply opens the file or URL passed as parameter in the system registered application.\nThe 'mailto' function starts the user's preferred e-mail composer and pre-fills the 'to', 'cc','bcc' and 'subject' headers if corresponding parameters are provided. It also handles parameters for the message body and for attachments.