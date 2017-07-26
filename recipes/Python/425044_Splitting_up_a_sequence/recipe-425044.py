# Guyon Morée
# http://gumuz.looze.net/

def split_seq(seq,size):
    """ Split up seq in pieces of size """
    return [seq[i:i+size] for i in range(0, len(seq), size)]
