class MyZipFile(ZipFile):
    def __init__(self, file, mode="r", compression=ZIP_STORED):
        ZipFile.__init__(self, file, mode, compression)

    def lines(self, name, split="\n", bs=100*1024*1024):
        """ Generator function to allow iteration over content of a file.

        The content of the file is read in chunks (maximal size = <bs>),
        split by the character <split>, and provided for iteration.
        The intention is to prevent the need to store the entire amount
        of decompressed data in memory (which does not work for bigger zip-files).

        Choose <bs> as high as possible before having to fear OutOfMemory exceptions,
        as this will give maximum performance.
        The default value of 100 MB does a good job for me.
        """

        if self.mode not in ("r", "a"):
            raise RuntimeError, 'read() requires mode "r" or "a"'
        if not self.fp:
            raise RuntimeError, \
                  "Attempt to read ZIP archive that was already closed"
        zinfo = self.getinfo(name)
        filepos = self.fp.tell()
        
        self.fp.seek(zinfo.file_offset, 0)
        bytes = self.fp.read(zinfo.compress_size)
        self.fp.seek(filepos, 0)
        if zinfo.compress_type == ZIP_STORED:
            for line in bytes.split(split): yield line
        elif zinfo.compress_type == ZIP_DEFLATED:
            if not zlib:
                raise RuntimeError, \
                      "De-compression requires the (missing) zlib module"
            dc = zlib.decompressobj(-15)

            # While most of this routine is copied from the read() method of
            # the original ZipFile class definition, the following code is
            # specific to the new functionality. We decompress chunks,
            # split them, and "yield" the pieces as long as there is either
            # one more left or no more compressed data available. Then we "yield"
            # the rest.
            # The "decompress('Z')"-stund is again taken from the original code.
            rest = ""
            while True:
                # += was faster than + was faster than "%s%s" % (a,b)
                rest += dc.decompress(bytes, bs)
                rs = rest.split(split)
                bytes = dc.unconsumed_tail
                rl = len(rs)
                if rl == 1:
                    rest = rs[0]
                else:
                    for i in xrange(rl - 1): yield rs[i]
                    rest = rs[-1]
                if len(bytes) == 0: break
            ex = dc.decompress('Z') + dc.flush()
            if ex: rest = rest + ex
            if len(rest) > 0:
                for r in rest.split(split): yield r
        else:
            raise BadZipfile, \
                  "Unsupported compression method %d for file %s" % \
                  (zinfo.compress_type, name)


def main():
    # to test this, change the file names to something you have
    zfn = "results_0067.zip"
    fn = "properties.csv"

    z = MyZipFile(zfn, "r", ZIP_DEFLATED)
    for line in z.lines(fn):
        print "+",
    z.close()

if __name__ == "__main__": main()
