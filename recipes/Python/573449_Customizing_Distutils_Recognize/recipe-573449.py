# setup.py -- customized Python Disutils distribution / installation script

# Written By: Chadwick Stryker

from distutils.core import setup, Distribution
from os.path import join as pjoin
import os, sys

def committed_rev():
    """
    Fetches the last committed rev to the repository and returns it.  This uses
    the pysvn module.  If anything goes wrong it sets the revision to zero.
    """
    try:
        import pysvn
        client = pysvn.Client()
        revs = []
        # search through the directory tree, starting at setup.py's directory
        for root, dirs, files in os.walk(sys.path[0]):
            # don't search through the .svn directories
            if '.svn' in dirs:
                dirs.remove('.svn')
            # get the revision info for each file, one at a time
            for f in files:
                try:
                    # try to get the SVN info. When checking a non working-copy
                    # directory, an exception will be raised
                    entry = client.info(pjoin(root,f))
                    # verify that the commit revision for the file is a number
                    if entry.commit_revision.kind != \
                        pysvn.opt_revision_kind.number:
                        raise
                    # if we made it this far (i.e. no exception raised), 
                    # remember the revision of the file for later
                    revs.append(entry.commit_revision.number)
                # otherwise, if client.info() fails or an exception is raised, 
                # then skip this file
                except:
                    pass
        # return the highest revision number of any file found in our search
        return max(revs)
    # if an unhandled exception occurs, then abort the search process and 
    # return a rev of zero. An example would be an ImportError generated if
    # the pysvn module is not installed on the system
    except Exception, msg:
        print msg,
        print '-- aborting search for subversion repository revision number'
        return 0

class svnDistribution(Distribution):
    """
    This subclass of the Distribution class is Subversion aware and
    searches to find the overall revision of the current working copy.
    """
    def __init__(self, attrs):
        # this does most of the work...
        build_num = committed_rev()
        if build_num:
            # if there is SVN revision data, assign the new version number
            attrs['version'] = '%i' % build_num
            try:
                # then try to create a user specified version file
                filename, format  = attrs['version_file']
                file(filename,'w').write(format % build_num)
            # in case a 'version_file' attribute was not set, do nothing
            except KeyError:
                pass
        # the parent class does not know about 'version_file', so delete it
        del attrs['version_file']
        Distribution.__init__(self, attrs)

setup(  name='example',
        description='example python module',
        author='Chad Stryker',
        author_email="example@example.net",
        py_modules=['example'],
        
        # the following attributes are used with the version number feature...
        
        # use this version ID if .svn data cannot be found
        version='SVN data unavailable', 
        distclass = svnDistribution,
        # the version_file attribute is understood by the svnDistribution class
        # and provides a way for the version information to be accessible by 
        # the module after it is installed
        version_file = ('_version.py', \
            '#This file is generated automatically\nversion = "%i"')
        )
