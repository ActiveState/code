ReplaceString = """

This message contained an attachment that was stripped out. 

The original type was: %(content_type)s
The filename was: %(filename)s, 
(and it had additional parameters of:
%(params)s)

"""

import re
BAD_CONTENT_RE = re.compile('application/(msword|msexcel)', re.I)
BAD_FILEEXT_RE = re.compile(r'(\.exe|\.zip|\.pif|\.scr|\.ps)$')

def sanitise(msg):
    # Strip out all payloads of a particular type
    ct = msg.get_content_type()
    # We also want to check for bad filename extensions
    fn = msg.get_filename()
    # get_filename() returns None if there's no filename
    if BAD_CONTENT_RE.search(ct) or (fn and BAD_FILEEXT_RE.search(fn)):
        # Ok. This part of the message is bad, and we're going to stomp
        # on it. First, though, we pull out the information we're about to
        # destroy so we can tell the user about it.

        # This returns the parameters to the content-type. The first entry
        # is the content-type itself, which we already have.
        params = msg.get_params()[1:] 
        # The parameters are a list of (key, value) pairs - join the
        # key-value with '=', and the parameter list with ', '
        params = ', '.join([ '='.join(p) for p in params ])
        # Format up the replacement text, telling the user we ate their
        # email attachment.
        replace = ReplaceString % dict(content_type=ct, 
                                       filename=fn, 
                                       params=params)
        # Install the text body as the new payload.
        msg.set_payload(replace)
        # Now we manually strip away any paramaters to the content-type 
        # header. Again, we skip the first parameter, as it's the 
        # content-type itself, and we'll stomp that next.
        for k, v in msg.get_params()[1:]:
            msg.del_param(k)
        # And set the content-type appropriately.
        msg.set_type('text/plain')
        # Since we've just stomped the content-type, we also kill these
        # headers - they make no sense otherwise.
        del msg['Content-Transfer-Encoding']
        del msg['Content-Disposition']
    else:
        # Now we check for any sub-parts to the message
        if msg.is_multipart():
            # Call the sanitise routine on any subparts
            payload = [ sanitise(x) for x in msg.get_payload() ]
            # We replace the payload with our list of sanitised parts
            msg.set_payload(payload)
    # Return the sanitised message
    return msg

# And a simple driver to show how to use this
import email, sys
m = email.message_from_file(open(sys.argv[1]))
print sanitise(m)
