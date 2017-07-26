import win32file as _win32file
import sys as _sys


class FolderSize:
    """
    This class implements an efficient technique for
    retrieving the size of a given folder or volume in
    cases where some action is needed based on a given
    size.

    The implementation is designed to handle situations
    where a specific size is desired to watch for,
    in addition to a total size, before a subsequent
    action is taken. This dramatically improves
    performance where only a small number of bytes
    are sufficient to call off a search instead of
    waiting for the entire size.
    
    In addition, the design is set to handle problems
    encountered at points during the search, such as
    permission errors. Such errors are captured so that
    a user could further investigate the problem and why
    it occurred. These errors do not stop the search from
    completing; the total size returned is still provided,
    minus the size from folders with errors.

    When calling a new search, the errors and total size
    from the previous search are reset; however, the stop
    size persists unless changed.
    """

    def __init__(self):

        # This is the total size returned. If a stop size
        # is provided, then the total size will be the last
        # bytes counted after the stop size was triggered.
        self.totalSize = 0

        # This mapping holds any errors that have occurred
        # during the search. The key is the path name, and
        # its value is a string of the error itself.
        self.errors = {}

        # This is the size where the search will end. The default
        # is -1 and it represents no stop size.
        self._stopSize = -1

        # This prints verbose information on path names.
        self.verbose = 0

    def enableStopSize(self, size=0):
        """
        This public method enables the stop size
        criteria. If the number of bytes thus far
        calculated exceeds this size, the search is
        stopped.

        The default value is zero bytes and means anything
        greater will end the search.
        """

        if type(size) != int:
            print "Error: size must be an integer"
            _sys.exit(1)
        
        self._stopSize = size

    def disableStopSize(self):
        """
        This public method disables the stop size
        criteria. When disabled, the total size of
        a folder is retrieved.
        """

        self._stopSize = -1

    def showStopSize(self):
        """
        This public method displays the current
        stop size in bytes.
        """

        print self._stopSize

    def searchPath(self, path):
        """
        This public method initiates the process
        of retrieving size data. It accepts either
        a UNC or local drive path.
        """

        # Reset the values on every new invocation.
        self.totalSize = 0
        self.errors = {}

        self._getSize(path)

    def _getSize(self, path):
        """
        This private method calculates the total size
        of a folder or volume, and accepts a UNC or
        local path.
        """

        if self.verbose: print path

        # Get the list of files and folders.
        try:
            items = _win32file.FindFilesW(path + "\\*")
        except _win32file.error, details:
            self.errors[path] = str(details[-1])
            return

        # Add the size or perform recursion on folders.
        for item in items:

            attr = item[0]
            name = item[-2]
            size = item[5]
            
            if attr & 16:
                if name != "." and name != "..":
                    self._getSize("%s\\%s" % (path, name))

            self.totalSize += size

            if self._stopSize > -1:
                if self.totalSize > self._stopSize:
                    return


if __name__ == "__main__":

    # Get the size of entire folder.
    sizer = FolderSize()
    sizer.searchPath(r"d:\users1\jsmith")
    print sizer.totalSize

    # Enable stop size (in bytes). Default is zero if no arg provided.
    sizer.enableStopSize(1024)
    sizer.searchPath(r"d:\users1\jsmith")
    if sizer.totalSize > 1024:
        print "The folder meets the criteria."
    elif sizer.totalSize == 0:
        print "The folder is empty."
    else:
        print "The folder has some data but can be skipped."

    # If the total size is zero, make sure no errors have occurred.
    # It may mean the initial path failed. Otherwise, errors are always from
    # subfolders.
    if sizer.totalSize == 0 and sizer.errors:
        print sizer.errors
