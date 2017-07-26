# This is derived from code provided by the Django Project. 
# Original code is licensed under the terms of the BSD license.
# See https://github.com/django/django/blob/master/LICENSE for full original license terms
import re

re_caps = re.compile(r'(?:^|(?<=[\.\?\!]))(^\s*|\s+)([a-z])')
def recapitalize(text):
     """Recapitalizes text, placing caps after end-of-sentence punctuation."""
     text = text.lower()
     text = re_caps.sub(lambda x: x.group(1) + x.group(2).upper(), text)
     return text

if __name__ == "__main__":
    print(recapitalize("first sentence. SECOND SENTENCE? tHiRd SeNtEnCe, "
                       "and it is still third sentence! FOURTH sentence."))
    print(recapitalize("\r\nfirst sentence.  second.sentence?\n"
                       "tHiRd;SeNtEnCe, and it is still third sentence!"
                       "\tFOURTH sentence."))
