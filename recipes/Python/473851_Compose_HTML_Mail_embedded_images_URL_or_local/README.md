###Compose HTML Mail with embedded images from URL or local file

Originally published: 2006-02-06 12:10:55
Last updated: 2006-02-06 12:10:55
Author: Catalin Constantin

The thing about this class is to "build" a mail msg object, automatic, from an URL or a local html file WITH all images included.\nThe class takes care of the image parsing / downloading / embedding + "cid: ID-here" replacements. The return is a valid MIMEMultipart("related") msg object which can be used to send valid HTML mail.