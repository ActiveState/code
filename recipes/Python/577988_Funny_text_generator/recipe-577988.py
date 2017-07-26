# -*- coding: iso-8859-1 -*-
"""Generate a text with words looking like those in a given text,
based on the frequency of character sequences
"""

import string
import io
import random

class TextGenerator:

    def __init__(self,txt,seq_len=5):
        """txt = original text 
        seq_len = sequence length ; 3 to 6 give the best results"""
        # dictionary mapping sequences of seq_len chararcters to the list 
        # of characters following them in the original text
        self.followers = {}
        for i in range(len(txt)-2*seq_len):
            sequence = txt[i:i+seq_len] # sequence of seq_len characters
            next_char = txt[i+seq_len] # the character following this sequence
            if sequence in self.followers:
                self.followers[sequence].append(next_char)
            else:
                self.followers[sequence]=[next_char]

        # sequences that start with an uppercase letter
        starts = [ key for key in self.followers 
            if key[0] in string.ascii_uppercase ]
        if not starts: # just in case...
            starts = list(self.followers.keys())

        # build a distribution of these sequences with the same frequency
        # as in the original text
        self.starts = []
        for key in starts:
            for i in range(len(self.followers[key])):
                self.starts.append(key)
        
    def random_text(self,length=5000):
        """length = length of the generated text"""
        # pick a start at random and initialize
        # generated text with this sequence
        sequence = random.choice(self.starts)
        gen_text = io.StringIO()
        gen_text.write(sequence)

        for j in range(length):
            # pick a character among those following current sequence
            next_char = random.choice(self.followers[sequence])
            gen_text.write(next_char)
            sequence = sequence[1:]+next_char
        return gen_text.getvalue()

if __name__=="__main__":
    import re
    txt = open('hamlet.txt').read()
    txt = re.sub("\n+",'\n',txt)
    gen = TextGenerator(txt)
    res = gen.random_text(3000)
    out = open('result.txt','w')
    out.write(res)
    out.close()
