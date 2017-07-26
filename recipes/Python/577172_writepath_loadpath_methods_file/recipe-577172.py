def _write_path(path, text, encoding, create_backup=False, log=None):
    """Write content to a path.
    
    @param path {str}
    @param text {unicode}
    @param encoding {str} The file encoding to use.
    @param create_backup {bool} Default False. Whether to create a backup
        file. The path of the backup will be `<path>.bak`. If that path
        exists it will be overwritten.
    @param log {logging.Logger} A logger to use for logging. No logging is
        done if it this is not given.
    """
    import os
    from os.path import exists, split, join
    import codecs
    
    # Write out new content to '.foo.tmp'.
    dir, base = split(path)
    tmp_path = join(dir, '.' + base + '.tmp')
    f = codecs.open(tmp_path, 'wb', encoding=encoding)
    try:
        f.write(text)
    finally:
        f.close()
    
    # Backup to 'foo.bak'.
    if create_backup:
        bak_path = path + ".bak"
        if exists(bak_path):
            os.rename(path, bak_path)
    elif exists(path):
        os.remove(path)
    
    # Move '.foo.tmp' to 'foo'.
    os.rename(tmp_path, path)
    if log:
        log.info("wrote `%s'", path)

def _load_path(path, encoding="utf-8", log=None):
    """Return the content of the given path.
    
    @param path {str}
    @param encoding {str} Default 'utf-8'.
    @param log {logging.Logger} A logger to use for logging. No logging is
        done if it this is not given.
    @returns {2-tuple} (<text>, <encoding>) where `text` is the
        unicode text content of the file and `encoding` is the encoding of
        the file. `text` is None if there was an error. Errors are logged
        via `log.error`.
    """
    import codecs
    try:
        f = codecs.open(path, 'rb', encoding)
    except EnvironmentError, ex:
        if log:
            log.error("could not open `%s': %s", path, ex)
        return None, None
    else:
        try:
            try:
                text = f.read()
            except UnicodeDecodeError, ex:
                if log:
                    log.error("could not read `%s': %s", path, ex)
                return None, None
        finally:
            f.close()
    return text, encoding
