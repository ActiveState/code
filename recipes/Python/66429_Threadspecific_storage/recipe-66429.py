try:
    import thread
except:
    """We're running on a single-threaded OS (or the Python interpreter has
    not been compiled to support threads) so return a standard dictionary.

    """
    _tss = {}
    def get_thread_storage():
        return _tss
else:
    _tss = {}
    _tss_lock = thread.allocate_lock()
    def get_thread_storage():
        """Return a thread-specific storage dictionary."""
        thread_id = thread.get_ident() # Identify the calling thread.
        tss = _tss.get(thread_id)
        if tss is None: # First time being called by this thread.
            try: # Entering critical section.
                _tss_lock.acquire()
                _tss[thread_id] = tss = {} # Create a thread-specific dictionary.
            finally:
                _tss_lock.release()
        return tss
