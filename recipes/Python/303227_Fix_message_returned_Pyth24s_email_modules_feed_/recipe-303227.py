import email
import email.FeedParser
import re
import sys
import sgmllib

# How much of the text must be outside the ASCII range
# before we guess that it's a binary part. Threshold
# picked almost at random.
kGuessBinaryThreshold=0.2
kGuessBinaryRE=re.compile("[\\0000-\\0025\\0200-\\0377]") # Non ASCII characters

# How much of the text must be HTML tags before we guess
# that it's HTML. Threshold picked almost at random.
kGuessHTMLThreshold=0.05


# For stripping HTML tags. Very slightly modified from
# Alex Martelli's news post <9cpm4202cv1@news1.newsguy.com>
# of May 2, 2001, Subject: Stripping HTML tags from a string

class Cleaner(sgmllib.SGMLParser):
  entitydefs={"nbsp": " "} # I'll break if I want to

  def __init__(self):
    sgmllib.SGMLParser.__init__(self)
    self.result = []
  def do_p(self, *junk):
    self.result.append('\n')
  def do_br(self, *junk):
    self.result.append('\n')
  def handle_data(self, data):
    self.result.append(data)
  def cleaned_text(self):
    return ''.join(self.result)

def stripHTML(text):
  c=Cleaner()
  try:
    c.feed(text)
  except sgmllib.SGMLParseError:
    return text
  else:
    t=c.cleaned_text()
    return t


def guessIsBinary(text):
  lt=len(text)
  if lt==0:
    return False
  nMatches=float(len(kGuessBinaryRE.findall(text)))
  return nMatches/lt>=kGuessBinaryThreshold

# This does some relatively expensive parsing to
# try to figure out if the text is HTML. In cases
# in which it's used often, a simple regular
# expression would be faster and might be
# sufficiently accurate.
def guessIsHTML(text):
  lt=len(text)
  if lt==0:
    return False
  textWithoutTags=stripHTML(text)
  tagsChars=float(lt-len(textWithoutTags))
  if tagsChars==0:
    return False
  return lt/tagsChars>=kGuessHTMLThreshold

def getMungedMessage(openFile):
  openFile.seek(0)
  p=email.FeedParser.FeedParser()
  p.feed(openFile.read())
  m=p.close()

  # Fix up multipart content-type when message isn't multi-part
  if m.get_content_maintype()=="multipart" and not m.is_multipart():
    
    t=m.get_payload(decode=1)

    if guessIsBinary(t):
      # Use generic "opaque" type
      m.set_type("application/octet-stream")
    elif guessIsHTML(t):
      m.set_type("text/html")
    else:
      m.set_type("text/plain")

  return m
