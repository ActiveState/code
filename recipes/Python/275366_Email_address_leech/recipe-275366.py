import re

def test():
    text = \
        ''' You can contact us at myname@server.site.com
            or at yourname AT server DOT site DOT com.
            Also at o u r n a m e @ s e r v e r dot s i t e dot c o m
            and t.h.e.i.r.n.a.m.e at server dot s/i/t/e DOT COM.
        '''
    for email in emailLeech(text): print email

        
DOMAINS = ["com","edu","net","org","gov","us"] #.. and so on

FLAGS = re.IGNORECASE | re.VERBOSE

AT = r'(?: @ | \b A \s* T \b)'
ADDRESSPART = r'\b (?: \w+ | \w (?:(?:\s+|\W) \w)*) \b'
DOMAIN = r'(?:%s)' % '|'.join(["(?:\s*|\W)".join(domain) for domain in DOMAINS])

NONWORD = re.compile(r'\W+')
DOT_REGEX = re.compile(r'(?: \. | \b D \s* O \s* T \b)', FLAGS)
EMAIL_REGEX = re.compile(
    (r'(?P<name>%s) \W* %s \W*' % (ADDRESSPART,AT)) +
     r'(?P<site>(?: %s \W* %s \W*)+)' % (ADDRESSPART, DOT_REGEX.pattern) +
     r'(?P<domain>%s)' % DOMAIN, FLAGS)
                           

def emailLeech(text):
    ''' An iterator over recognized email addresses within text'''
    while (True):
        match = EMAIL_REGEX.search(text)
        if not match: break
        parts = [match.group("name")] + \
                DOT_REGEX.split(match.group("site")) + \
                [match.group("domain")]
        # discard non word chars
        parts = [NONWORD.sub('',part) for part in parts]
        # discard all empty parts and make lowercase
        parts = [part.lower() for part in parts if len(part)>0]
        # join the parts
        yield "%s@%s.%s" % (parts[0], '.'.join(parts[1:-1]), parts[-1])
        text = text[match.end():]

if __name__ == '__main__': test()
