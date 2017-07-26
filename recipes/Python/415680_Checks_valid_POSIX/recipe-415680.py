def isValidPosixFilename(name, NAME_MAX=255):
    """Checks for a valid POSIX filename

    Filename: a name consisting of 1 to {NAME_MAX} bytes used to name a file.
        The characters composing the name may be selected from the set of
        all character values excluding the slash character and the null byte.
        The filenames dot and dot-dot have special meaning.
        A filename is sometimes referred to as a "pathname component".

    name: (base)name of the file
    NAME_MAX: is defined in limits.h (implementation-defined constants)
              Maximum number of bytes in a filename
              (not including terminating null).
              Minimum Acceptable Value: {_POSIX_NAME_MAX}
              _POSIX_NAME_MAX: Maximum number of bytes in a filename
                               (not including terminating null).
                               Value: 14
                               
    More information on http://www.opengroup.org/onlinepubs/009695399/toc.htm
    """

    return 1<=len(name)<= NAME_MAX and "/" not in name and  "\000" not in name
