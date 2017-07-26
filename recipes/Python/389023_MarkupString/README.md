###MarkupString

Originally published: 2005-02-21 11:45:07
Last updated: 2005-02-23 19:17:32
Author: Thomas Hinkle

A subclass of String that allows simple handling of pango markup or other simple XML markup. The goal here is to allow a slice of a python markup string to "do the right thing" and preserve formatting correctly. In other word, MarkupString(&lt;i&gt;Hello World&lt;/i&gt;)[6:] = "&lt;i&gt;World&lt;/i&gt;"