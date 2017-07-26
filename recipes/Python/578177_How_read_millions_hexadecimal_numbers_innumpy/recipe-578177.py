data = numpy.frombuffer(open(filename).read().replace('\n','').decode('hex'), dtype=numpy.uint32).byteswap()

# Slow version, for reference:
numpy.fromiter( (int(x, 16) for x in open(filename)), dtype=numpy.uint32)
