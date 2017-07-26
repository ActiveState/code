# FileSystemList -- manage a list of files, directories and other
# file system objects. Optionally recurse directories
# and ensure that each item in the list is a regular file. 
#
# Version 0.1
# Jan. 1, 2004: initial working version
#
# by: Eamonn Sullivan (eamonn_sullivan@blueyonder.co.uk)
#
import sys, os, os.path, glob

from stat import *

from types import StringType, ListType

# we lose all the tar*() methods on python2.2
try:
    import tarfile
    COMPAT23 = True
except ImportError:
    # we're running on something less than python2.3
    COMPAT23 = False

class FSList(list):
    """
    File System List class: a subclass of list designed for
    manipulating objects in the file system.

    flist = FSList([pattern = '', [recursive = False, [file_only = False]]])

    - pattern can be a string or a list of files and subdirectories. It can
      also contain wildcards (*, ? or []), in which case the pattern
      will be expanded automatically using glob.glob()
    - recursive controls whether files matching pattern in subdirectories
      are added to the list.
    - file_only is a convenience option for when you just want a list
      of the regular files matching the patter (i.e., no directories,
      special files like devices).
    - It doesn't follow links or symlinks. At least I don't think it does.
    - Computed properties:  size (total size of all regular files, in bytes)
                            smallest (smallest item)
                            largest
                            newest  (most recent modification time)
                            oldest  (oldest modification time)
                            
    The same init options are also available on extend and append methods.

    flist.extend('./*.c', recursive=True, file_only=True)

    Extends the list with all C files in the current directory and
    any subdirectories.

    Note, append works like it would on a normal list. For example:

    flist.append('./*.c', recursive=True)

    would add a list to the list (i.e., flist = [..., ..., [..., ...]]

    Attempts to add items that aren't in the filesystem raise ValueError:

    >>> test = fslist.FSList()
    >>> test[0] = 'This isn't a file.'
    Traceback ...
    ValueError: Item not found on file system: This isn't a file.
    >>> test.append('fslist.py')
    >>> test.extend('wx*.py')
    >>> print test
    ['fslist.py', 'wxEdit.py', 'wxMailitEd.py', 'wxSendIt.py', 'wxtestcode.py']
    >>>

    FSList doesn't keep track of underlying filesystem changes, but you can
    test if all the files are still there by testing the instance in a
    boolean context.

    >>> import fslist
    >>> test = fslist.FSList('*.py')
    >>> print test
    ['email-unpack.py', 'FileSystemList.py', 'fslist.py', ...]
    >>> if test:
	print 'Everything's Still there!'
    else:
	print 'Something has changed!'

    Also included are methods for compressing all of the files on the list
    in tar, tar.gz, tar.bz2 (bzip2) and zip formats. The methods return the
    data as a stream, for use in file operations. For example:

    >>> import fslist
    >>> flist = fslist.FSList('*.py')
    >>> f = file('testing.tar', 'w+b')
    >>> f.write(flist.tar())
    >>> f.close
    >>> f = file('testing.tar.gz', 'w+b')
    >>> f.write(flist.targz())
    >>> f.close
    >>> f = file('testing.tar.bz2', 'w+b')
    >>> f.write(flist.tarbz2())
    >>> f.close
    >>> f = file('testing.zip', 'w+b')
    >>> f.write(flist.zip())
    >>> f.close

    On Python 2.2, only the zip() is defined. 

    """
       
    def __init__(self, pattern = '', recursive = False, file_only = False):
        """
        I do ugly type testing in here because I haven't quite
        grasped the concepts, I guess. I assume any user of this won't
        want to end up with a list containing a list when an instance is
        created.
        They just want a list, at least at first, so I type test to append()
        or extend().         
        """
        list.__init__(self)

        # if pattern is empty, we don't have to do any more
        if pattern != '':
            # assume at first that it's a single string. 
            try:
               temp = self._populate(pattern, recursive, file_only)
               # if wildcards, need to extend the list
               self._extendOrAppend(temp)
            except TypeError:
               # we may have been passed a list. Process
               # each separately, any of which can have wildcards.
               for fname in pattern:
                    if isinstance(fname, StringType):
                       temp = self._populate(fname, recursive, file_only)
                       self._extendOrAppend(temp)
                    else:
                        # Even lists can have lists!
                        # I'll break, though, if there are lists in lists in
                        # lists.
                        for f in fname:
                            temp = self._populate(f, recursive, file_only)
                            self._extendOrAppend(temp)
                            

    def getSize(self):
        """
           Return the total size of the regular files in the list. Used for
           the read-only property 'size'.
        """
        totsize = 0
        try:
            for name in self:
                if os.path.isfile(name):
                    totsize += os.path.getsize(name)
        except TypeError:
            # there may be lists buried in this list, unwind first
            temp = self._unwind()
            for name in temp:
                if os.path.isfile(name):
                    totsize += os.path.getsize(name)
        return totsize

    def getSmallest(self):
        """
            Returns the smallest file. Yes, this is ugly.
        """
        flist_copy = []
        try:
            flist_copy = zip(map(os.path.getsize, self), self)
        except TypeError:
            # there may be lists of lists
            temp = self._unwind()
            flist_copy = zip(map(os.path.getsize, temp), temp)
        flist_copy.sort()
        try:
            size, fname = flist_copy[0]
        except IndexError:
            # probably an empty list
            return None
        return fname

    def getLargest(self):
        """
            Returns the largest file. Yes, this is ugly.
        """
        flist_copy = []
        try:
            flist_copy = zip(map(os.path.getsize, self), self)
        except TypeError:
            # there may be lists of lists
            temp = self._unwind()
            flist_copy = zip(map(os.path.getsize, temp), temp)
        flist_copy.sort()
        try:
            size, fname = flist_copy[(len(flist_copy)-1)]
        except IndexError:
            # probably an empty list
            return None
        return fname

    def getOldest(self):
        """
            Returns the file earliest last-modified time.
        """
        flist_copy = []
        try:
            flist_copy = zip(map(os.path.getmtime, self), self)
        except TypeError:
            # there may be lists of lists
            temp = self._unwind()
            flist_copy = zip(map(os.path.getmtime, temp), temp)
        flist_copy.sort()
        try:
            time, fname = flist_copy[0]
        except IndexError:
            # probably an empty list
            return None
        return fname

    def getNewest(self):
        """
            Returns the file modified most recently.
        """
        flist_copy = []
        try:
            flist_copy = zip(map(os.path.getmtime, self), self)
        except TypeError:
            # there may be lists of lists
            temp = self._unwind()
            flist_copy = zip(map(os.path.getmtime, temp), temp)
        flist_copy.sort()
        try:
            time, fname = flist_copy[(len(flist_copy)-1)]
        except IndexError:
            # probably an empty list
            return None
        return fname

    # some read-only properties
    size = property(getSize, \
                    doc='Total size of all the regular files in the list.')
    smallest = property(getSmallest, \
                        doc='The smallest item in the list, by bytes.')    
    largest = property(getLargest, \
                       doc='The largest item in the list, by bytes.')    
    oldest = property(getOldest, \
                    doc='The item with the oldest last-modification time.')    
    newest = property(getNewest, \
                 doc='The item with the most recent last-modification time.')

    def sort_by_size(self):
        """
            Sort the list in by number of bytes
        """
        flist_copy = []
        temp = []
        try:
            flist_copy = zip(map(os.path.getsize, self), self)
        except TypeError:
            # there may be lists of lists
            temp = self._unwind()
            flist_copy = zip(map(os.path.getsize, temp), temp)
        flist_copy.sort()
        self[:] = [item for size, item in flist_copy]

    def sort_by_mtime(self):    
        """
            Sort the last modification time
        """
        flist_copy = []
        temp = []
        try:
            flist_copy = zip(map(os.path.getmtime, self), self)
        except TypeError:
            # there may be lists of lists
            temp = self._unwind()
            flist_copy = zip(map(os.path.getmtime, temp), temp)
        flist_copy.sort()
        self[:] = [item for time, item in flist_copy]
                
    def append(self, pattern, recursive = False, file_only = False):
        """
            subclass the append method to handle wildcards, recursing
            and file filter. 
        """
        # expand any wildcards, recurse if asked, filter on files, etc.
        temp = self._populate(pattern, recursive, file_only)
        # then just append.
        super(FSList, self).append(temp)

    def extend(self, pattern, recursive = False, file_only = False):
        """
            subclass the extend method to handle wildcards, recursing
            and file filter. 
        """
        # expand any wildcards, recurse if asked, filter on files, etc.
        temp = self._populate(pattern, recursive, file_only)
        # then extend.
        super(FSList, self).extend(temp)


    # methods used only internally

    def _unwind(self):
        """
            Unwinds lists that have embedded lists inside them.
            The os.path functions used in newest(), largest(), etc.
            choke on lists of files. I am sure there is an easier way.
        """
        result = str(self).replace('[','')
        result = result.replace(']','') 
        unwoundlist = result.split(',')
        x = 0
        while x < len(unwoundlist):
            unwoundlist[x] = unwoundlist[x].strip(" \'\"")
            x += 1
        return unwoundlist

    def _extendOrAppend(self, data):
        """
            A kludge to ensure that the list is created correctly in __init__
            This extends or appends the list, depending on whether we are
            adding a list or a string.
        """
        if isinstance(data, StringType):
            super(FSList, self).append(data)
        elif isinstance(data, ListType):
            super(FSList, self).extend(data)        
   
    def _populate(self, pattern, recursive = False, file_only = False):
        """
            The main workhorse function for adding files to the list.
            Returns the pattern, if it's just a filesystem item and
            it exists in the filesystem. Returns a list if pattern contains
            wildcards, or None, if the wildcards do not match anything.
        """
        temp = []
        wildcard = False

        # look for wildcard characters in the pattern
        if ('*' in pattern) or ('?' in pattern)\
         or ('[' in pattern):
            wildcard = True
        # items added to the list must exist on the filesystem.
        if not wildcard and not os.path.exists(pattern):
            raise ValueError, ("Item not found on file system: %s"% pattern)

        # if it's a directory, assume they want every file there.
        if os.path.isdir(pattern):
            pattern = os.path.join(pattern, '*')
            wildcard = True
        # expand any wildcards
        if wildcard:
            temp.extend(glob.glob(pattern))

        # walk through any directories, if requested,
        # using the same pattern, if any.
        if recursive:
            path, filter = os.path.split(pattern)

            # Go through the path, finding all the directories
            if wildcard:
                # try os.walk first, which is in python2.3
                try:
                    for root, dirs, files in os.walk(path):
                        for dir in dirs:
                            temp.extend(glob.glob(\
                                os.path.join(root, dir, filter)))
                except AttributeError:
                    # probably running on something less than python2.3
                    dirlist = self._walktree_compat(path)
                    for dir in dirlist:
                        temp.extend(glob.glob(os.path.join(dir, filter)))

        # Finally, kill any links that got through from glob
        # and remove anything that's not a file, if requested.
        temp2 = []
        name = ''
        while True:
            try:
                # use pop() on the theory that it saves memory
                # (one list is reduced while the other grows).
                # That's probably not true, but I wouldn't know.
                name = temp.pop()
                try:
                    mode = os.stat(name)[ST_MODE]
                except OSError, err:
                    import errno
                    if err.errno != errno.ENOENT: raise
                    # file not found. Most likely a broken symlink
                    continue
                if file_only and S_ISREG(mode) and not S_ISLNK(mode):
                    temp2.append(name)
                elif not S_ISLNK(mode):
                    temp2.append(name)
            except IndexError:
                break
        temp = temp2
            
        # Return the list found
        if len(temp) > 0:
            return temp
        elif len(temp) == 0 and wildcard:
            # the wildcard search didn't find anything
            return None
        else:
            return pattern

    def _walktree_compat(self, top):
        '''
           recursively descend the directory tree rooted at top.
           Return all of the directories as a list. This should work
           on python2.2
        '''

        dirlist = []
        templist = []
        try:
            templist = os.listdir(top)
        except OSError, err:
            import errno
            if err.errno == errno.ENOENT:
                return []

        for f in templist:
            pathname = os.path.join(top, f)
            try:
                mode = os.stat(pathname)[ST_MODE]
            except OSError, err:
                import errno
                if err.errno == errno.ENOENT:
                    continue
            if S_ISDIR(mode):
                # It's a directory, recurse into it
                dirlist.append(pathname)
                dirlist.extend(self._walktree_compat(pathname))
        return dirlist
    

    def __setitem__(self, key, value):
        """
            Override this method to ensure that only valid filesystem
            objects are added. Raises ValueError if not.
            
        """
        if not os.path.exists(value):
            raise ValueError, ("Item not found on file system: %s"% value)
        else:
            super(FSList, self).__setitem__(key, value)

    def __nonzero__(self):
        """
            Return True if all the items still exist on the filesystem,
            false otherwise. Also returns false if there are no items
            yet (i.e., it's an empty list).
        """
        if len(self) > 0:
            for name in self:
                if not os.path.exists(name):
                    return False
            return True
        else:
            return False

    def zip(self):
        """
            return a data stream of the files compressed in zip format.
            Returns None if the list is empty. 
        """
        import cStringIO, zipfile
        fobj = cStringIO.StringIO()
        # make sure the list contains something
        if len(self) >= 0:
            try:
                zip = zipfile.ZipFile(fobj, "w", zipfile.ZIP_DEFLATED)
            except:
                sys.stderr.write("Unable to open zip file.")
                raise
            try:
                for name in self:
                    # only add files
                    if os.path.isfile(name):
                        zip.write(name)
                zip.close()
                return fobj.getvalue()
            finally:
                fobj.close()
        else:
            # return None if the list is empty. 
            return None

    if COMPAT23:
        def targz(self):
            """
                return a data stream of the files in gzipped tar format.
                Returns None if the list is empty. 
            """
            import tarfile, cStringIO
            # Create file in memory. I use cStringIO for speed. 
            fobj = cStringIO.StringIO()
            # if the list contains anything
            if len(self) >= 0:
                # create the tarfile using the cStringIO buffer
                try:
                    tar = tarfile.open('', "w:gz", fobj)
                except:
                    sys.stderr.write("Unable to open tar.gz file.")
                    raise
                try:
                    for name in self:
                        # only add files
                        if os.path.isfile(name):
                            try:
                                tar.add(name)
                            except ValueError:
                                # it can't store extremely long names
                                # so tell which ones and continue
                                sys.stderr.write('Warning: Unable to store: ')
                                sys.stderr.write(name)
                                sys.stderr.write('\n')
                    tar.close()
                    return fobj.getvalue()
                finally:
                    fobj.close()
            else:
                # return None if the list is empty
                return None


        def tarbz2(self):
            """
                return a data stream of the files in tar format, compressed
                with bzip2.
                Returns None if the list is empty. 
            """
            import tarfile, cStringIO, bz2
            fobj = cStringIO.StringIO()
            # make sure the list contains something
            if len(self) >= 0:
                try:
                    tar = tarfile.open('', "w", fobj)
                except:
                    sys.stderr.write("Can't open file for bzip2 compression.")
                    raise
                try:
                    for name in self:
                        # only add files
                        if os.path.isfile(name):
                            try:
                                tar.add(name)
                            except ValueError:
                                # it can't store extremely long names
                                # so tell which ones and continue
                                # TODO: MAYBE TRY TRUNCATING NAMES HERE
                                sys.stderr.write('Warning: Unable to store: ')
                                sys.stderr.write(name)
                                sys.stderr.write('\n')
                    tar.close()
                    # I compress using bzip2 only at this point
                    # because I get an error if I try to do it with
                    # tarfile.open. It says file-like objects aren't
                    # supported. 
                    return bz2.compress(fobj.getvalue())
                finally:
                    fobj.close()
            else:
                # return None if the list is empty. 
                return None

        def tar(self):
            """
                return a data stream of the files in uncompressed tar format.
                Returns None if the list is empty. 
            """
            import cStringIO, tarfile
            fobj = cStringIO.StringIO()
            # check the list contains something
            if len(self) >= 0:
                try:
                    tar = tarfile.open('', "w", fobj)
                except:
                    sys.stderr.write("Unable to open tar file.")
                    raise
                try:
                    for name in self:
                        # only add files
                        if os.path.isfile(name):
                            try:
                                tar.add(name)
                            except ValueError:
                                # it can't store extremely long names
                                # so tell which ones and continue
                                sys.stderr.write('Warning: Unable to store: ')
                                sys.stderr.write(name)
                                sys.stderr.write('\n')
                    tar.close()
                    return fobj.getvalue()
                finally:
                    fobj.close()

            else:
                # return None if the list is empty
                return None

     
if __name__ == '__main__':

    import time
    
    # change these to suit your system
    # single wildcard pattern
    pattern1 = ['../../*.doc', False, False, 'singlewild']
    # a list of wildcard patterns
    pattern2 = [['../*.py', '*'], True, False, 'wildlist']
    # a list with an embedded list (tests _unwind)
    pattern3 = [['../*.jpg', '../*.gif', ['../*.py', '../*.txt']], \
                True, True, 'listlist']
    # a straight filename
    pattern4 = ['fslist.py', False, True, 'singlefile']
    # a list of patterns, some of which probably don't exist
    pattern5 = [['../*.py','*.xxx','*.not'], True, True, 'brokenlist']

    for arg in (pattern1, pattern2, pattern3, pattern4, pattern5):

        print 'Testing pattern:', arg[3]
        print 'Pattern:', arg[0]

        test = FSList(arg[0], recursive=arg[1], file_only=arg[2])
        if len(test) > 0:
            print "Number of files:", len(test)
            print "Total size:", test.size
            print "The smallest file is %s: %i bytes."%\
              (test.smallest, os.path.getsize(test.smallest))
            print "The largest file is %s: %i bytes."%\
              (test.largest, os.path.getsize(test.largest))
            print "The oldest file is %s: %s."%\
              (test.oldest, time.ctime(os.path.getmtime(test.oldest)))
            print "The newest file is %s: %s."%\
              (test.newest, time.ctime(os.path.getmtime(test.newest)))

            if len(test) > 3:
                test.sort_by_size()
                print "Three smallest files:"
                print "Name:           Size:"
                print "%s              %i"%(test[0], os.path.getsize(test[0]))
                print "%s              %i"%(test[1], os.path.getsize(test[1]))
                print "%s              %i"%(test[2], os.path.getsize(test[2]))

                test.sort_by_mtime()
                print "Three oldest files:"
                print "Name:       Size:"
                print "%s          %s"%(test[0], \
                                        time.ctime(os.path.getmtime(test[0])))
                print "%s          %s"%(test[1], \
                                        time.ctime(os.path.getmtime(test[1])))
                print "%s          %s"%(test[2], \
                                        time.ctime(os.path.getmtime(test[2])))


            try:
                if not COMPAT23: 
                    f = file(('testresults/'+arg[3]+'P22'+'.zip'), "w+b")
                else:
                    f = file(('testresults/'+arg[3]+'P23'+'.zip'), "w+b")
                f.write(test.zip())
            finally:
                f.close()
                

            if COMPAT23:

                try:
                    f = file(('testresults/'+arg[3]+'.tar'), "w+b")
                    f.write(test.tar())
                finally:
                    f.close()
                try:
                    f = file(('testresults/'+arg[3]+'.tgz'), "w+b")
                    f.write(test.targz())
                finally:
                    f.close()
                try:
                    f = file(('testresults/'+arg[3]+'.tbz'), "w+b")
                    f.write(test.tarbz2())
                finally:
                    f.close()
