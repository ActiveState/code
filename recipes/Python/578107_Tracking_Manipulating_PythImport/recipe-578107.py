"""import_state.py

A rough implementation of PEP 405.  This module centers on manipulating
the normal Python import machinery through its defined state.  Any other
approach, such as replacing builtins.__import__ is certainly legal, but
not supported here.

"""

__all__ = ['ImportState', 'default_import_state', 'globalstate']

import sys
import builtins
import site
import importlib
import _imp
from collections import namedtuple


class GlobalImportLock:
    # no need for a generic ImportLock type, since all import states
    # use the same lock
    @property
    def acquire(self):
        _imp.acquire_lock()
    @property
    def release(self):
        _imp.release_lock()
    @property
    def lock_held(self):
        _imp.lock_held()


_ImportState = namedtuple('_ImportState', (
        'modules',
        'meta_path',
        'path',
        'path_hooks',
        'path_importer_cache',
        ))


class ImportState(_ImportState):
    """A container for the import state (a la PEP 406).

    The dictionary in sys.modules is a special case, since it is part
    of the CPython interpreter state.  Binding a different dict there
    is problematic, since the import machinery may use the internal
    reference to the original dict, rather than looking up sys.modules.
    The consequence is that the _contents_ of sys.modules must be
    swapped in and out, rather than simply binding something else there.

    ImportState objects may be used as context managers, to activate the
    state temporarily.  During a with statement the dict in self.modules
    may not reflect the actual state.  However, it _will_ be correct
    before and after the with statement.

    """
    # all import states use the same lock
    lock = GlobalImportLock()

    def __init__(self, *args, **kwargs):
        self._saved = None

    def __enter__(self):
        self.lock.acquire()
        self.activate()

    def __exit__(self, *args, **kwargs):
        self.deactivate()
        self.lock.release()

    def copy(self):
        """Return a shallow copy of the import state."""
        return type(self)(self.modules.copy(), self.meta_path[:],
                          self.path[:], self.path_hooks[:],
                          self.path_importer_cache.copy())

    def activate(self, force=False):
        """Have the interpreter use this import state, saving the old."""
        if self._saved is not None and not force:
            raise TypeError("Already activated; try using a copy")

        self._saved = _ImportState(
                sys.modules.copy(),  # saving away the contents
                sys.meta_path,
                sys.path,
                sys.path_hooks,
                sys.path_importer_cache,
                )

        #sys.modules = self.modules
        sys.meta_path = self.meta_path
        sys.path = self.path
        sys.path_hooks = self.meta_path
        sys.path_importer_cache = self.path_importer_cache

        # accommodate sys.module's quirkiness
        sys.modules.clear()
        sys.modules.update(self.modules)

    def deactivate(self):
        """Restore the import state saved when this one activated."""
        if not self._saved:
            raise TypeError("Not activated yet")

        # sys.modules = self.modules
        sys.meta_path = self._saved.meta_path
        sys.path = self._saved.path
        sys.path_hooks = self._saved.path_hooks
        sys.path_importer_cache = self._saved.path_importer_cache

        # accommodate sys.module's quirkiness
        self.modules.clear()
        self.modules.update(sys.modules)
        sys.modules.clear()
        sys.modules.update(self._saved.modules)

        self._saved = None


def default_import_state(**overrides):
    """Return an ImportState with defaults to the initial import state."""
    state = {
            'modules': {},
            'meta_path': [],
            'path': site.getsitepackages(),
            'path_hooks': [],
            'path_importer_cache': {},
            }
    state.update(overrides)
    return ImportState(**state)


class GlobalImportState(ImportState):
    """An ImportState that wraps the current state"""
    # The underlying ImportState values will be ignored.
    def __new__(cls):
        return super(GlobalImportState, cls).__new__(cls, *([None]*5))
    @property
    def modules(self):
        """The cache of modules that have already been imported."""
        return sys.modules
    @property
    def meta_path(self):
        """The PEP 302 finders queried before 'path' is traversed."""
        return sys.meta_path
    @property
    def path(self):
        """The directories in which top-level packages are located."""
        return sys.path
    @property
    def path_hooks(self):
        """The PEP 302 path importers that are queried for a path."""
        return sys.path_hooks
    @property
    def path_importer_cache(self):
        """The cache of finders previously found through path_hooks."""
        return sys.path_importer_cache

globalstate = GlobalImportState()
