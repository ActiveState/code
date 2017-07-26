import os, string

def replaceFile(oldname, newname):
    """ Rename file 'oldname' to 'newname'.
    """
    if os.name == 'nt' and os.path.exists(oldname):
        # POSIX rename does an atomic replace, WIN32 rename does not. :-(
        try:
            os.remove(newname)
        except OSError, exc:
            import errno
            if exc.errno != errno.ENOENT: raise exc

    # rename it
    os.rename(oldname, newname)


class FileMorpher:
    """ A class that enables a client to securely update an existing file,
        including the ability to make an automated backup version.
    """

    def __init__(self, filename, **kw):
        """ The constructor takes the filename and some options.

            backup -- boolean indicating whether you want a backup file
                (default is yes)
        """
        self.filename = filename
        self.do_backup = kw.get('backup', 1)

        self.stream = None
        self.basename, ext = os.path.splitext(self.filename)


    def __del__(self):
        if self.stream:
            # Remove open temp file
            self.__close()
            os.remove(self.__tempfile())


    def __tempfile(self):
        return self.basename + ".tmp"


    def __close(self):
        """ Close temp stream, if open.
        """
        if self.stream:
            self.stream.close()
            self.stream = None


    def load(self):
        """ Load the content of the original file into a string and
            return it. All I/O exceptions are passed through.
        """
        file = open(self.filename, "rt")
        try:
            content = file.read()
        finally:
            file.close()

        return content


    def save(self, content):
        """ Save new content, using a temporary file.
        """
        file = self.opentemp()
        file.write(content)
        self.commit()


    def opentemp(self):
        """ Open a temporary file for writing and return an open stream.
        """
        assert not self.stream, "Write stream already open"

        self.stream = open(self.__tempfile(), "wt")

        return self.stream        


    def commit(self):
        """ Close the open temp stream and replace the original file,
            optionally making a backup copy.
        """
        assert self.stream, "Write stream not open"

        # close temp file
        self.__close()

        # do optional backup and rename temp file to the correct name
        if self.do_backup:
            replaceFile(self.filename, self.basename + ".bak")
        replaceFile(self.__tempfile(), self.filename)


if __name__ == "__main__":
    # prepare test file
    test = open('foo.txt', 'wt')
    test.write('\txxx\nline 2\n\t\t2 tabs\n')
    test.close()

    # load the file's content
    file = FileMorpher('foo.txt')
    text = file.load()

    # detab it, this could also be done shorter by file.save()
    stream = file.opentemp()
    stream.write(string.expandtabs(text))
    file.commit()
