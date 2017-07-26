import fnmatch
import os
import os.path
import collections
import sys

WalkedDir = collections.namedtuple("WalkedDir", "path subdirs files depth")

def filter_walk(top, file_pattern=None, dir_pattern=None, depth=None, onerror=None, followlinks=False, onloop=None):
    """filter_walk is similar to os.walk, but offers the following additional features:
        - yields a named tuple of (path, subdirs, files, depth)
        - allows a recursion depth limit to be specified
        - allows independent glob-style filters for filenames and subdirectories
        - emits a message to stderr and skips the directory if a symlink loop is encountered when following links

       Selective walks are always top down, as the directory listings must be altered to provide
       the above features.

       If not None, depth must be at least 0. A depth of zero can be useful to get separate
       filtered subdirectory and file listings for a given directory.

       onerror is passed to os.walk to handle os.listdir errors
       followlinks is passed to os.walk and enables the symbolic loop detection
       onloop (if provided) can be used to override the default symbolic loop handling. It is
       called with the directory path as an argument when a loop is detected. Any false return
       value will skip the directory as normal, any true value means the directory will be processed.
    """
    if depth is not None and depth < 0:
        msg = "Depth limit must be None or greater than 0 ({!r} provided)"
        raise ValueError(msg.format(depth))
    if onloop is None:
        def onloop(path):
            msg = "Symlink {!r} refers to a parent directory, skipping\n"
            sys.stderr.write(msg.format(path))
            sys.stderr.flush()
    if followlinks:
        real_top = os.path.abspath(os.path.realpath(top))
    sep = os.sep
    initial_depth = top.count(sep)
    for path, walk_subdirs, files in os.walk(top, topdown=True,
                                             onerror=onerror,
                                             followlinks=followlinks):
        # Check for symlink loops
        if followlinks and os.path.islink(path):
            # We just descended into a directory via a symbolic link
            # Check if we're referring to a directory that is
            # a parent of our nominal directory
            relative = os.path.relpath(path, top)
            nominal_path = os.path.join(real_top, relative)
            real_path = os.path.abspath(os.path.realpath(path))
            path_fragments = zip(nominal_path.split(sep), real_path.split(sep))
            for nominal, real in path_fragments:
                if nominal != real:
                    break
            else:
                if not onloop(path):
                    walk_subdirs[:] = []
                    continue
        # Filter files, if requested
        if file_pattern is not None:
            files = fnmatch.filter(files, file_pattern)
        # We hide the underlying generator's subdirectory list, since we
        # clear it internally when we reach the depth limit (if any)
        if dir_pattern is None:
            subdirs = walk_subdirs[:]
        else:
            subdirs = fnmatch.filter(walk_subdirs, dir_pattern)
        # Report depth
        current_depth = path.count(sep) - initial_depth
        yield WalkedDir(path, subdirs, files, current_depth)
        # Filter directories and implement depth limiting
        if depth is not None and current_depth >= depth:
            walk_subdirs[:] = []
        else:
            walk_subdirs[:] = subdirs
