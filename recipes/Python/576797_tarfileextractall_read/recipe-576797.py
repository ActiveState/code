def _ensure_read_access(compressedfile):
    """Ensure that the compressedfile will be readable by the user after
    extraction.

    Some tarballs have u-x set on directories. They may as well have u-r set on
    files. We reset such perms here.. so that the extracted files remain
    accessible.

    See also: http://bugs.python.org/issue6196
    """
    if isinstance(compressedfile, zipfile.ZipFile):
        return # zipfiles have no perms, I believe
    elif isinstance(compressedfile, tarfile.TarFile):
        EXECUTE = 0100
        READ = 0400
        dir_perm = EXECUTE
        file_perm = EXECUTE | READ

        # WARNING: if the tarfile had a huge of list of files, this could be a
        # potential performance bottleneck.
        for tarinfo in compressedfile.getmembers():
            tarinfo.mode |= (dir_perm if tarinfo.isdir() else file_perm)
    else:
        raise NotImplementedError, \
            "don't know how to read this of compressed file: {0}".format(compressedfile)
