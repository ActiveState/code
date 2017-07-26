"""Run asyncore/asynchat dispatchers in the GTK main event loop.

This module integrates asyncore/asynchat channels with the GTK main loop, by
automatically adding and maintaining gobject.io_add_watch():es.

Usage: asyncore.socket_map = AutoWatch(asyncore.socket_map)

"""

import asyncore
import UserDict

import gobject

# Make sure asyncore.readwrite() will work properly
import select
for mask in 'IN PRI OUT ERR HUP NVAL'.split():
    assert getattr(gobject, 'IO_' + mask) == getattr(select, 'POLL' + mask)
del select, mask


IO_PRIORITY = gobject.PRIORITY_DEFAULT_IDLE


class AutoWatch(UserDict.DictMixin):
    def __init__(self, mapping=None, **kwargs):
        # socket -> (source_id, mask) map, for io_add_watch and source_remove
        self._watch_map = dict()
        # fd -> socket map, for the interface
        self._fd_map = dict()
        if mapping is not None:
            self.update(mapping)
        if kwargs:
            self.update(kwargs)

    def __getitem__(self, fd):
        return self._fd_map[fd]

    def __setitem__(self, fd, obj):
        if fd in self._fd_map:
            self._remove_watch(self._fd_map[fd])
        source_id = gobject.idle_add(self._add_watch, obj,
                                     priority=IO_PRIORITY)
        self._watch_map[obj] = (source_id, 'idle_add')
        self._fd_map[fd] = obj

    def __delitem__(self, fd):
        self._remove_watch(self._fd_map.pop(fd))

    def __contains__(self, fd):
        return fd in self._fd_map

    def __iter__(self):
        return iter(self._fd_map)

    def keys(self):
        return self._fd_map.keys()

    def iteritems(self):
        return self._fd_map.iteritems()

    def _add_watch(self, obj):
        mask = self._get_mask(obj)
        if mask:
            source_id = gobject.io_add_watch(obj, mask, self._handle_io,
                                             priority=IO_PRIORITY)
            self._watch_map[obj] = (source_id, mask)
            return False

        # This should be exceptional. The channel is still open, but is neither
        # readable nor writable. Retry until it is, but with a timeout_add() to
        # preserve CPU.
        if self._watch_map[obj][1] == 'idle_add':
            source_id = gobject.timeout_add(200, self._add_watch, obj,
                                            priority=gobject.PRIORITY_LOW)
            self._watch_map[obj] = (source_id, 'timeout_add')
            return False

        return True

    def _remove_watch(self, obj):
        gobject.source_remove(self._watch_map.pop(obj)[0])

    def _get_mask(self, obj):
        mask = 0
        if obj.readable():
            mask |= gobject.IO_IN | gobject.IO_PRI
        if obj.writable():
            mask |= gobject.IO_OUT
        # Only watch for errors if the socket is either readable or writable
        if mask:
            mask |= gobject.IO_ERR | gobject.IO_HUP | gobject.IO_NVAL
        return mask

    def _handle_io(self, obj, mask):
        asyncore.readwrite(obj, mask)

        # Make sure objects removed during the readwrite() aren't re-added
        if obj._fileno not in self._fd_map:
            return False

        # If read-/writability has changed, change watch mask
        if self._get_mask(obj) != self._watch_map[obj][1]:
            source_id = gobject.idle_add(self._add_watch, obj,
                                         priority=IO_PRIORITY)
            self._watch_map[obj] = (source_id, 'idle_add')
            return False

        return True
