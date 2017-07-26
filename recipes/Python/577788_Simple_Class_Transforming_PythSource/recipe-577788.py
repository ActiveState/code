"""backport module"""

import os
import shutil
import re


class Backport:
    """A simple class for transforming Python source files.

    """

    DEFAULT_PATH = "."
    PYTHON_EXTENSION = "py"
    BACKUP_EXTENSION = "orig"
    REPLACEMENTS = {}
    IGNORE = (__file__,)

    def __init__(self, path=DEFAULT_PATH, filenames=None):
        if filenames is None:
            filenames = self.get_filenames(path)
        self.filenames = filenames

    @classmethod
    def get_filenames(cls, path):
        filenames = os.listdir(path)
        for filename in filenames[:]:
            if filename in cls.IGNORE:
                filenames.remove(filename)
                continue
            try:
                name, ext = filename.rsplit(".", 1)
            except ValueError:
                filenames.remove(filename)
                continue
            if ext == cls.BACKUP_EXTENSION:
                if not name.endswith("."+cls.PYTHON_EXTENSION):
                    filenames.remove(filename)
                elif name.count(".") > 1:
                    filenames.remove(filename)
            elif "." in name:
                filenames.remove(filename)
            elif ext != cls.PYTHON_EXTENSION:
                filenames.remove(filename)
        return filenames

    def backup(self):
        """Generate a backup file for each file."""

        for filename in self.filenames[:]:
            if not filename.endswith("."+self.PYTHON_EXTENSION):
                continue
            origfilename = filename + "." + self.BACKUP_EXTENSION
            if origfilename not in self.filenames:
                shutil.copy(filename, origfilename)
                self.filenames.append(origfilename)

    def restore(self, clean=False):
        """Restore the original files.

        If clean is True, wipe out the backup files.

        """

        for origfilename in self.filenames[:]:
            if not origfilename.endswith("."+self.BACKUP_EXTENSION):
                continue
            filename = origfilename.strip("."+self.BACKUP_EXTENSION)
            shutil.copy(origfilename, filename)
            self.filenames.append(filename)
            if clean:
                os.remove(origfilename)

    def transform(self, source):
        for old, new in self.REPLACEMENTS.items():
            source = re.sub("(?m)"+old, new, source)
        return source

    def run(self, dryrun=True):
        self.backup()
        self.restore()

        for filename in self.filenames:
            if not filename.endswith(self.PYTHON_EXTENSION):
                continue

            infile = open(filename)
            source = infile.read()
            infile.close()

            source = self.transform(source)

            if __debug__:
                print("")
                print(filename + "%%"*50)
                print(source)

            if not dryrun:
                open(filename, "w").write(source)
