#!/usr/bin/env python
"""This module provides a versioned output file.

When you write to such a file, it saves a versioned backup of any
existing file contents.

For usage examples see main()."""

import sys, os, glob, string, marshal

class VersionedOutputFile:
    """This is like a file object opened for output, but it makes
    versioned backups of anything it might otherwise overwrite."""

    def __init__(self, pathname, numSavedVersions=3):
        """Create a new output file.
        
        `pathname' is the name of the file to [over]write.
        `numSavedVersions' tells how many of the most recent versions
        of `pathname' to save."""
        
        self._pathname = pathname
        self._tmpPathname = "%s.~new~" % self._pathname
        self._numSavedVersions = numSavedVersions
        self._outf = open(self._tmpPathname, "wb")

    def __del__(self):
        self.close()

    def close(self):
        if self._outf:
            self._outf.close()
            self._replaceCurrentFile()
            self._outf = None

    def asFile(self):
        """Return self's shadowed file object, since marshal is
        pretty insistent on working w. pure file objects."""
        return self._outf

    def __getattr__(self, attr):
        """Delegate most operations to self's open file object."""
        return getattr(self.__dict__['_outf'], attr)
    
    def _replaceCurrentFile(self):
        """Replace the current contents of self's named file."""
        self._backupCurrentFile()
        os.rename(self._tmpPathname, self._pathname)

    def _backupCurrentFile(self):
        """Save a numbered backup of self's named file."""
        # If the file doesn't already exist, there's nothing to do.
        if os.path.isfile(self._pathname):
            newName = self._versionedName(self._currentRevision() + 1)
            os.rename(self._pathname, newName)

            # Maybe get rid of old versions.
            if ((self._numSavedVersions is not None) and
                (self._numSavedVersions > 0)):
                self._deleteOldRevisions()

    def _versionedName(self, revision):
        """Get self's pathname with a revision number appended."""
        return "%s.~%s~" % (self._pathname, revision)
    
    def _currentRevision(self):
        """Get the revision number of self's largest existing backup."""
        revisions = [0] + self._revisions()
        return max(revisions)

    def _revisions(self):
        """Get the revision numbers of all of self's backups."""
        
        revisions = []
        backupNames = glob.glob("%s.~[0-9]*~" % (self._pathname))
        for name in backupNames:
            try:
                revision = int(string.split(name, "~")[-2])
                revisions.append(revision)
            except ValueError:
                # Some ~[0-9]*~ extensions may not be wholly numeric.
                pass
        revisions.sort()
        return revisions

    def _deleteOldRevisions(self):
        """Delete old versions of self's file, so that at most
        self._numSavedVersions versions are retained."""
        
        revisions = self._revisions()
        revisionsToDelete = revisions[:-self._numSavedVersions]
        for revision in revisionsToDelete:
            pathname = self._versionedName(revision)
            if os.path.isfile(pathname):
                os.remove(pathname)
                
def main():
    """Module mainline (for isolation testing)"""
    basename = "TestFile.txt"
    if os.path.exists(basename):
        os.remove(basename)
    for i in range(10):
        outf = VersionedOutputFile(basename)
        outf.write("This is version %s.\n" % i)
        outf.close()

    # Now there should be just four versions of TestFile.txt:
    expectedSuffixes = ["", ".~7~", ".~8~", ".~9~"]
    expectedVersions = []
    for suffix in expectedSuffixes:
        expectedVersions.append("%s%s" % (basename, suffix))
    matchingFiles = glob.glob("%s*" % basename)
    for filename in matchingFiles:
        if filename not in expectedVersions:
            sys.stderr.write("Found unexpected file %s.\n" % filename)
        else:
            # Unit tests should clean up after themselves...
            os.remove(filename)

    # Finally, here's an example of how to use versioned
    # output files in concert with marshal.
    import marshal

    outf = VersionedOutputFile("marshal.dat")
    # Marshal out a sequence:
    marshal.dump([1, 2, 3], outf.asFile())
    outf.close()
    os.remove("marshal.dat")

if __name__ == "__main__":
    main()
