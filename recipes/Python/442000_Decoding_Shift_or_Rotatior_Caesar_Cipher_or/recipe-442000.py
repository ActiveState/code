class ShiftDecoder:
    """Decode text encoded with a shift cypher, a code that, like rot13,
    maps character[i] of the alphabet to character[(i+n)%26], for some n.
    The algorithm is simple: first train the decoder on some sample text.
    Training means keeping counts of how often each 2-character sequence
    occurs.  Then, when given a text to decode, try each of the 26 possible
    shifts (rotations) and choose the one that has the highest probability
    according to the counts of 2-character sequences."""
    def __init__(self, training_text):
        self.counts = DefaultDict(1)
        for bi in bigrams(text):
            self.counts[bi] += 1

    def score(self, plaintext):
        "Return a score for text based on how common letters pairs are."
        s = 1.0
        for bi in bigrams(plaintext):
            s = s * self.counts[bi]
        return s

    def decode(self, ciphertext):
        "Return the shift decoding of text with the best score."
        all_shifts = [shift_encode(ciphertext, n) for n in range(len(alphabet))]
        return argmax(all_shifts, self.score)


alphabet = 'abcdefghijklmnopqrstuvwxyz'

def shift_encode(plaintext, n):
    "Encode text with a shift cipher that moves each letter up by n letters."
    from string import maketrans
    code = alphabet[n:] + alphabet[:n]
    trans = maketrans(alphabet + alphabet.upper(), code + code.upper())
    return plaintext.translate(trans)

def bigrams(text):
    "Return a list of all consecutive pairs of letters in text."
    return [text[i:i+2] for i in range(len(text) - 1)]

def argmax(sequence, fn):
    "Return the element e of sequence with maximum fn(e) value."
    best_fn, best_e = max([(fn(e), e) for e in sequence])
    return best_e

class DefaultDict(dict):
    "Dictionary with a default value for unknown keys."
    def __init__(self, default):
        self.default = default

    def __getitem__(self, key):
        return self.get(key, self.default)
