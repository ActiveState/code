import os
FormURL = 'http://example.tld/contact.html'

...
if os.environ['HTTP_REFERER'] !=  FormURL: return
