indices = xrange(sys.maxint)

for item, index in zip(sequence, indices):
    something(item, index)

# same semantics as:
for index in range(len(sequence)):
    something(sequence[index], index)

# but the change-of-emphasis allows greater
# clarity in some usage contexts.

# Further alternatives exist of course:

class Indexed:
    def __init__(self, seq):
        self.seq = seq
    def __getitem__(self, i):
        return self.seq[i], i

for item, index in Indexed(sequence):
    something(item, index)

# or equivalently:
def Indexed(sequence):
    return zip(sequence, indices)
