import random
import re
import StringIO

class misspell(object):
    def __init__(self):
        # create a regex to match a word with ending punctucation
        self.punctuation = re.compile('\S+[' + re.escape(",'.:;!?") + ']$')
    def misspell(self, text):
        self.text = StringIO.StringIO(text).readlines()
        misspelled = []
        for line in self.text:
            # split hyphenated words into independent words           
            line = re.sub(r'(\S+)\-(\S+)', r'\1 \2', line)
            
            # split each line in a list of words
            tokens = line.split()
        
            for token in tokens:
                # don't misspell a number
                if token.isdigit():
                    misspelled.append(token + ' ')
                    continue
                
                # don't misspell an email address or URL
                if '@' in token or '://' in token:
                    misspelled.append(token + ' ')
                    continue
                
                # does the word end with puncuation?                
                has_punc = re.match(self.punctuation, token)
                
                # explode the word to a list                
                token = list(token)

                # word doesn't end in puctuation and is longer than 4 chars
                if not has_punc and len(token) >= 4:
                    start = random.randint(1,len(token) - 3)
                    stop = start + 2
                    f,s = token[start:stop]
                    token[start:stop] = s,f
                    
                # word does end in puctuation and is longer that 5 chars
                elif has_punc and len(token) >=5:
                    start = random.randint(1,len(token) - 4)
                    stop = start + 2
                    f,s = token[start:stop]
                    token[start:stop] = s,f
                                   
                # add the word to the line
                misspelled.append((''.join(token) + ' '))
                
            # end the line                
            misspelled.append('\n')
            
        return ''.join(misspelled)

if __name__ == '__main__':
    # example usage of the misspell class
    message = """
    According to research at an English University, it doesn't matter 
    in what order the letters in a word are, the only important thing is 
    that the first and last letters be in the right places. The rest can
    be a total mess and you can still read it without problem. This is
    because the human mind does not read every letter by itself, but 
    the word as a whole."""
 
    msg = misspell()
    print msg.misspell(message)
    
