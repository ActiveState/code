"""This script unpacks a source distribution into a temporary
directory, builds a windows installer on the fly, executes it, and
cleans everything up afterward.

You could create a shortcut to this script on the desktop by simply
dragging it there, then you can drag'n drop zip or tar.gz files onto
it."""

import sys, os, zipfile, tempfile
from distutils.dir_util import mkpath, remove_tree

try:
    # Use Lars Gustaebel's tarfile module, if available:
    # http://www.gustaebel.de/lars/tarfile/
    # Needs version 0.3.3 (or higher?)
    import tarfile
    tarfile.is_tarfile
    tarfile.TarFileCompat
except (ImportError, AttributeError):
    tarfile = None

def create_file(pathname, data):
    mkpath(os.path.dirname(pathname))
    file = open(pathname, "wb")
    file.write(data)
    file.close()

def extract(distro):
    dir = tempfile.mktemp()
    if zipfile.is_zipfile(distro):
        file = zipfile.ZipFile(distro)
    elif tarfile and tarfile.is_tarfile(distro):
        file = tarfile.TarFileCompat(distro, "r", tarfile.TAR_GZIPPED)
    else:
        if tarfile:
            raise TypeError, "%r does not seem to be a zipfile or tarfile" % distro
        else:
            raise TypeError, "%r does not seem to be a zipfile" % distro
    os.mkdir(dir)
    for info in file.infolist():
        if info.filename[-1] != '/':
            data = file.read(info.filename)
            create_file(os.path.join(dir, info.filename), data)
    return dir

def install():
    if len(sys.argv) != 2:
        raise Exception, "Usage: python install.py <zip-or-tar.gz file>"
    distro = sys.argv[1]
    dir = extract(distro)
    print "Extracted to", dir
    import glob
    setup_files = glob.glob(os.path.join(dir, "*", "setup.py"))
    if len(setup_files) != 1:
        raise Exception, "Could not determine setup script to use"
    setup_file = setup_files[0]
    os.chdir(os.path.dirname(setup_file))
    print "Building windows installer..."
    os.system("%s %s -q bdist_wininst" % (sys.executable, setup_file))
    print "Running windows installer..."
    exe_file = glob.glob("dist/*.exe")[0]
    os.system(exe_file)
    print "Removing", dir
    remove_tree(dir)

if __name__ == '__main__':
    try:
        install()
    except Exception, detail:
        print detail
    raw_input("Press return to exit...")
