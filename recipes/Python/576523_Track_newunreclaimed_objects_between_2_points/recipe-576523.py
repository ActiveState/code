# Author: David Decotigny 2008 Oct 3
#  @brief Routines to determine which new objects are reachable
#  between 2 points in the code

import gc, cPickle as pickle, weakref, sys, traceback


#
# Method 1: use weak ref to track new live objects
# Advantages: we have live pointers to the new live objects. And fast
# Drawbacks: doesn't track many types (such as list, dict, etc.) but
#            generally this is not a problem because: if they contain
#            sub-objects, these objects might most probably be track-able
#
class RefTracker(object):
    """
    The scan() method will apply the given callback to the list of
    new objects created since last call to scan() (or since the
    construction, for the 1st time).
    """
    def __init__(self):
        self._not_tracked_types = set()
        self._current_refs      = dict()
        self.scan()

    def _get_objects(self):
        return gc.get_objects()
        
    def _scan(self, callback_new_object):
        """
        This is NOT MT-safe and will not work for most builtin types
        """
        objs = self._get_objects()
        
        # First: remove the objects that are not available anymore
        to_remove = []
        for oid, ref in self._current_refs.iteritems():
            if ref() is None:
                to_remove.append(oid)
        for oid in to_remove:
            del self._current_refs[oid]
        del to_remove

        # Create the list of objects that are brand new:
        for obj in objs:
            try:
                my_ref = self._current_refs[id(obj)]
                # The object was already recorded last time.
                # If the recorded object were not the current one,
                # it would mean that the recorded object had been
                # deallocated... this is caught by the previous loop
                #
                # Do some sanity checks, just to make sure:
                assert my_ref() is not None
                assert my_ref() == obj
            except KeyError:
                # This is a new object. Try to make a weak-ref out of it:
                try:
                    wref = weakref.ref(obj)
                except TypeError:
                    # Track only weak-ref-friendly objects, remember
                    # the types of the objects we couldn't weak-reference:
                    self._not_tracked_types.add(str(type(obj)))
                    continue
                # Ok, good, we have a weak ref. Record it:
                self._current_refs[id(obj)] = wref
                # We also want to know that it's a new thing
                try:
                    if callback_new_object:
                        callback_new_object(obj)
                        del obj
                except:
                    traceback.print_exc()

    def scan(self, callback_new_object = None):
        """Call the callback on each new object"""
        # We need this in order to free the refs still held
        # by _scan due to the callback (approx explanation...)
        gc.collect()
        self._scan(callback_new_object)
        gc.collect()

    @property
    def not_tracked_types(self):
        """Return the list of type names of the objects that could not
        be tracked"""
        return self._not_tracked_types

    @staticmethod
    def _print_new_obj(obj):
        """Callback used by scan_and_print_new_objs"""
        print "New obj:", repr(obj)

    def scan_and_print_new_objs(self, msg = None):
        # Print list of new objs, making sure that the list is
        # correctly garbage-collected by the GC
        print "\n# -- %s:" % (msg or "New objects")
        self.scan(self._print_new_obj)
        print "# ---------------\n"



#
# Method 2: Keep track of the garbage list
# Advantages: we have live pointers to the new live objects. And fast
# Drawbacks: will only show the object /after/ the GC had tried to
#            reclaim them, not as soon as they have been
#            creaded. Still useful to debug leaks... But: are we sure
#            that lost objects are only found in cycles ??? Same
#            type restrictions as for method 1 ???
#
class GarbageTracker(RefTracker):
    def _get_objects(self):
        return gc.garbage


#
# Method 3: approximate method storing signatures of objects to a file
#           and comparing the signatures. The signature consist of a pair
#           object id / str(type(obj))
# Advantages: all object types can potentially be tracked. Can allow
#             basic offline analysis
# Drawbacks: might not see some new objects if they are at the same address
#            as previous ones having the same signature. Slow
#

first_time = True
def make_gc_snapShot(filename, name):
        """Append the signatures to a file, giving them the given
        'name'. A signature is a pair object_id / type_name"""
	global first_time
	if first_time:
		gc.collect()
		first_time = False
	contents = []
	for o in gc.get_objects():
		try:
			tname = o.__class__.__name__
		except AttributeError:
			tname = str(type(o))
		contents.append((id(o), tname))
		del tname
	f = open(filename, 'a')
	pickle.dump((name, contents), f)
	f.close()
	del contents
	del f

class GCSnapshot(object):
        """Used to read a set of signatures from the file"""
	def __init__(self, stream):
		self.name, contents = pickle.load(stream)
		self._contents = set(contents)

	def __sub__(self, other):
                """Give the differences between 2 sets of
                signatures. Return a set of pairs object_id /
                type_name"""
		return self._contents - other._contents

	def reach(self, ids):
            """
            \param ids Iterable of object id, as returned by x[0],
            with x in the result of (snapshot2 - snapshot1)
            
            Return a dict id -> object with that id currently known.

            The objects recorded with these id might have been
            replaced by new ones... so we might end-up seeing objects
            that don't correspond to the original ones. This is
            especially true after a gc.collect()
            """
            result = dict()
            for obj in gc.get_objects():
                if id(obj) in ids:
                    result[id(obj)] = obj
            return result


def read_snapshots(filename):
        """Sequentially reads the sets of signatures from a file. For
        each set of signatures, a GCSnapshot is created with the
        stored name. return the dict set name -> GCSnapshot object"""
	result = dict()
	f = open(filename, 'r')
	while 1:
		try:
			snap = GCSnapshot(f)
			result[snap.name] = snap
		except (EOFError, pickle.UnpicklingError):
			break
	f.close()
	return result


#### BEGIN: ONLY FOR THE TESTS
class Dummy:
    def __init__(self):
        print "INFO: ctor", self
    def __del__(self):
        print "INFO: dtor", self

# A pair of mutually-referencing objects with __del__ methods
# See http://docs.python.org/library/gc.html#gc.garbage
# for an explanation why they are not automatically reclaimable
class ObjectReferencer:
    def __init__( self, obj ):
        print "INFO: ctor", self
        self.reference = obj

    def __del__(self):
        print "INFO: dtor", self


class ReferencerCreator:
    def __init__( self ):
        print "INFO: ctor", self
        self.attribute = ObjectReferencer( self )

    def __del__(self):
        print "INFO: dtor", self

    def break_cycle(self):
        # Necessary to break the cycle that prevents the GC from
        # doing its job
        print "INFO: break_cycle", self
        self.attribute = None


def _test1():
    """Tests for method 1 (RefTracker)"""
    print "*** Method 1 (RefTracker) ***"

    r = RefTracker()
    d = Dummy()
    print "del dummy now..."
    del d
    r.scan_and_print_new_objs("After creation/del of Dummy()")

    # Contains a cycle: will not be freed by GC...
    o = ReferencerCreator()
    print "del obj now..."
    del o
    r.scan_and_print_new_objs("After creation/del of ReferencerCreator")

    # The same, but we break the cycle
    o = ReferencerCreator()
    print "break_cycle now..."
    o.break_cycle()
    print "del obj now..."
    del o        
    r.scan_and_print_new_objs("After creation/break_cycle/del of ReferencerCreator")

    print "Types not tracked:"
    for typ in r.not_tracked_types:
        print "  %s" % typ

    print "End of test method 1."


def _test2():
    """Tests for method 2 (GarbageTracker)"""
    print "*** Method 2 (GarbageTracker) ***"

    r = GarbageTracker()
    d = Dummy()
    print "del dummy now..."
    del d
    r.scan_and_print_new_objs("After creation/del of Dummy()")

    # Contains a cycle: will not be freed by GC...
    o = ReferencerCreator()
    print "del obj now..."
    del o
    r.scan_and_print_new_objs("After creation/del of ReferencerCreator")

    # The same, but we break the cycle
    o = ReferencerCreator()
    print "break_cycle now..."
    o.break_cycle()
    print "del obj now..."
    del o        
    r.scan_and_print_new_objs("After creation/break_cycle/del of ReferencerCreator")

    print "Types not tracked:"
    for typ in r.not_tracked_types:
        print "  %s" % typ

    print "End of test method 2."


def _test3():
    """Tests for method 3 (compare signatures)"""
    import os
    
    print "*** Method 3 (compare signatures) ***"
    fname = "/tmp/gc-%s-snapshot" % os.environ["USER"]
    make_gc_snapShot(fname, "0")
    make_gc_snapShot(fname, "1")
    l = list()
    l.append(l)
    make_gc_snapShot(fname, "2")
    l.append(42)
    t = ReferencerCreator()
    make_gc_snapShot(fname, "3")

    # Now analyzing
    snaps = read_snapshots(fname)
    os.remove(fname)

    print "Between 2 and 1, diff is:"
    diff21 = snaps["2"] - snaps["1"]
    for d in diff21:
        print "  ", d

    print "Between 2 and 1, diff as live objects is:"
    for obj in snaps["3"].reach([d[0] for d in diff21]).itervalues():
        print "  ", obj

    print "Between 3 and 2, diff is:"
    diff32 = snaps["3"] - snaps["2"]
    for d in diff32:
        print "  ", d
        
    print "Between 3 and 2, diff as live objects is:"
    for obj in snaps["3"].reach([d[0] for d in diff32]).itervalues():
        print "  ", obj

    print "Between 3 and 1, diff is:"
    diff31 = snaps["3"] - snaps["1"]
    for d in diff31:
        print "  ", d
        
    print "Between 3 and 1, diff as live objects is:"
    for obj in snaps["3"].reach([d[0] for d in diff31]).itervalues():
        print "  ", obj

    print "End of test method 3."
#### END: ONLY FOR THE TESTS


if __name__ == "__main__":
    _test1()
    _test2()
    _test3()
    print "Bye."
