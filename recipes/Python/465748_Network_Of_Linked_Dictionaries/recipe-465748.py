#
# -*- coding: utf-8 -*-

"""

Linked dictionaries are dictionaries that can refer to other dictionaries (dubbed *bases*; generally,
anything that provides a ``__getitem__`` interface) for key and value retrieval::

    n = dict( iam = 'n', N = 108 )
    d = Linkdict( iam = 'd', D = 42 )
    e = Linkdict( iam = 'e', E = 43 ).addbases( d )
    f = Linkdict( iam = 'f', F = 44 )
    g = Linkdict( iam = 'g', G = 45 ).addbases( e, f )
    h = Linkdict(                   ).addbases( g )
    d.addbases( g, n ) # creating a circular reference

In this example, ``g`` is a linked dictionary that keeps a reference to ``e`` and ``f``, ``e`` refers to
``d``, and ``d`` refers to ``n`` (an standard ``dict`` instance), and, yes, back to ``g`` -- we explicitly
allow circular references (wlthough they may be of limited usefulness). The network topology may be
scrutinized using the attribute ``~.localBases`` and the method ``~.bases()`` (for the purposes of
exposition, we have here replaced the representations of ``Linkdict``\ s with pointy brackets containing the
value of the instance's ``'iam'`` entry)::

    d.localBases:        [<g>, {'iam': 'n', 'N': 108}]
    e.localBases:        [<d>]
    f.localBases:        []
    g.localBases:        [<e>, <f>]
    h.localBases:        [<g>]

    d.bases():           [<d>, <g>, <e>, <f>, {'iam': 'n', 'N': 108}]
    e.bases():           [<e>, <d>, <g>, <f>, {'iam': 'n', 'N': 108}]
    f.bases():           [<f>]
    g.bases():           [<g>, <e>, <d>, {'iam': 'n', 'N': 108}, <f>]
    h.bases():           [{}, <g>, <e>, <d>, {'iam': 'n', 'N': 108}, <f>]

As can be gleaned from the above, a depth-first resolution order is utilized: while the *local* bases of
``g`` are ``e`` and then ``f``, in the *global* bases dictionaries ``e``, ``d``, and ``n`` intervene, since
these are the objects that ``e`` links to directly or indirectly.

All standard methods of ``dict`` objects also work with instances of ``Linkdict``, however, they all work on
the entire network of objects. For example, ``g['F']`` yields ``44``, which is retrieved from ``f``, and
``del g['F']`` deletes key ``'F'`` from instance ``f``.

In order to constrain methods to the keys and values stored in a specific dictionary, use the ``local``
property, e.g. ``for k in d.local.iterkeys()`` (but read the documentation of ``Linkdict.local`` for
restrictions on usage).

Since we have introduced a level of complexity by building a network of dictionaries -- which means that any
time we address one dictionary of the network we may also touch any number of related objects -- a number of
methods that deal with *tickets* have been introduced, a ticket being defined as the triplet
``(base,key,value)``. Also, methods like ``~.keys()`` and ``~.iteritems()`` have been supplied with an
argument ``unique``, that, when set to ``False``, will allow keys and values otherwise shadowed to show up
in the result. Compare::

    g.tickets():                   [(<g>, 'iam', 'g'), (<g>, 'G', 45), (<e>, 'E', 43), (<d>, 'D', 42),
                                        ({'iam': 'n', 'N': 108}, 'N', 108), (<f>, 'F', 44)]
    g.tickets( unique = False ):   [(<g>, 'iam', 'g'), (<g>, 'G', 45), (<e>, 'iam', 'e'), (<e>, 'E', 43),
                                        (<d>, 'iam', 'd'), (<d>, 'D', 42), ({'iam': 'n', 'N': 108}, 'iam', 'n'),
                                        ({'iam': 'n', 'N': 108}, 'N', 108), (<f>, 'iam', 'f'), (<f>, 'F', 44)]
    g.keys():                      ['iam', 'G', 'E', 'D', 'N', 'F']
    g.keys( unique = False ):      ['iam', 'G', 'iam', 'E', 'iam', 'D', 'iam', 'N', 'iam', 'F']

Using tickets, instances can determine which targets to approach in the network for deletion and
modification of items. Let us say we want to modify an item in the place where it is defined, say, add
``100`` to ``g['D']``. Unfortunately, ``g['D']+=100`` doesn't give that -- instead. an item ``('D',142)``
will be added to ``g``. This, at least, is in analogy to the situation with inheritance: consider ::

    class d:
        D = 42

    class G( d ):
        pass

    g = G()
    g.D += 100
    print g.__dict__
    print d.__dict__

which yields ::

    {'D': 142}
    {'__module__': '__main__', 'D': 42, '__doc__': None}

-- that is, an attribute ``D`` has been added to ``g`` instead of ``d.D`` getting modified. So we have to
get a tad more fancy and use tickets:

    base, key, value = g.ticket( 'D' )
    base[ 'D' ] += 100

or, a bit simpler::

    g.base( 'D' ) += 100


Important Usage Note
============================================================================================================

Due to the fact that ``Linkedict`` has been derived from ``dict`` and due to the way that
``dict.__init__()`` internally works, ``dict(linkdict)`` will invariably be equivalent to
``dict(linkdict.local.iteritems())``. This may or may not be what you expect and want. In order to reduce
the *global* namespace of a linked dictionary to a standard ``dict``, use ``linkdict.asdict()`` or
``dict(linkdict.iteritems())``.


"""

############################################################################################################
#
#
#
#===========================================================================================================
class _Misfit( object ):
    pass

Misfit = _Misfit()

############################################################################################################
#
#
#
#===========================================================================================================
class Linkdict( dict ):

    #-------------------------------------------------------------------------------------------------------
    def __init__( self, *P, **Q ):
        super( Linkdict, self ).__init__( *P, **Q )
        self.localBases = []

    #-------------------------------------------------------------------------------------------------------
    @property
    def local( self ):
        """Return ``super(Linkdict,self)`` to enable named access to the local set of key/value pairs. For
        example. while ``d.iterkeys()`` iterates over all keys in the network of dictionaries,
        ``d.local.iterkeys()`` iterates only over the keys defined in ``d`` itself. This works neither for
        functionality addressed by syntactic sugar nor for methods that are not defined for standard
        dictionaries, so none of ``d.local['x']``, ``del d.local['x']``, ``len(d.local)``, and
        ``d.local.bases()`` are legal; for these, use ``d.local.get('x')``, ``d.localDelete('x')``,
        ``d.localLength()``, and ``d.localBases, respectively."""
        return super( Linkdict, self )

    #-------------------------------------------------------------------------------------------------------
    def __contains__( self, key ):
        return key in self.iterkeys()

    #-------------------------------------------------------------------------------------------------------
    def __iter__( self ):
        return self.iterkeys()

    #-------------------------------------------------------------------------------------------------------
    def __getitem__( self, key ):
        return self.asdict()[ key ]

    #-------------------------------------------------------------------------------------------------------
    def __delitem__( self, key ):
        self.pop( key )

    #-------------------------------------------------------------------------------------------------------
    def __len__( self ):
        return len( self.tickets() )

    #-------------------------------------------------------------------------------------------------------
    def localDelete( self, key ):
        self.local.pop( key )

    #-------------------------------------------------------------------------------------------------------
    def localLength( self ):
        return self.local.__len__()

    #-------------------------------------------------------------------------------------------------------
    def __eq__(  self, other ): return self._compare( other, '__eq__' )
    def __cmp__( self, other ): return self._compare( other, '__cmp__' )
    def __lt__(  self, other ): return self._compare( other, '__lt__' )
    def __le__(  self, other ): return self._compare( other, '__le__' )
    def __gt__(  self, other ): return self._compare( other, '__gt__' )
    def __ge__(  self, other ): return self._compare( other, '__ge__' )

    #-------------------------------------------------------------------------------------------------------
    def _compare( self, other, methodname ):
        d0 = self.asdict()
        if self.isLinkdict( other ):
            other = other.asdict()
        return getattr( d0, methodname)( other )

    #-------------------------------------------------------------------------------------------------------
    @classmethod
    def isLinkdict( this, other ):
        return isinstance( other, Linkdict )

    #-------------------------------------------------------------------------------------------------------
    def addbases( self, *bases ):
        self.localBases.extend( bases )
        return self

    #-------------------------------------------------------------------------------------------------------
    def bases( self ):
        return list( self.iterbases() )

    #-------------------------------------------------------------------------------------------------------
    def iterbases( self ):
        return self._iterbases( set() )

    #-------------------------------------------------------------------------------------------------------
    def _iterbases( self, _seen ):
        for collection in [ self ], self.localBases:
            for base in collection:
                baseid = id( base )
                if baseid in _seen: continue
                _seen.add( baseid )
                yield base
                if self.isLinkdict( base ):
                    for subbase in base._iterbases( _seen ):
                        yield subbase

    #-------------------------------------------------------------------------------------------------------
    def keys( self, unique = True ):
        return list( self.iterkeys( unique ) )

    #-------------------------------------------------------------------------------------------------------
    def iterkeys( self, unique = True ):
        for base, key, value in self.itertickets( unique ):
            yield key

    #-------------------------------------------------------------------------------------------------------
    def values( self, unique = True ):
        return list( self.itervalues( unique ) )

    #-------------------------------------------------------------------------------------------------------
    def itervalues( self, unique = True ):
        for base, key, value in self.itertickets( unique ):
            yield value

    #-------------------------------------------------------------------------------------------------------
    def items( self, unique = True ):
        return list( self.iteritems( unique ) )

    #-------------------------------------------------------------------------------------------------------
    def iteritems( self, unique = True ):
        for base, key, value in self.itertickets( unique ):
            yield key, value

    #-------------------------------------------------------------------------------------------------------
    def tickets( self, unique = True ):
        return list( self.itertickets( unique ) )

    #-------------------------------------------------------------------------------------------------------
    def itertickets( self, unique = True ):
        if unique:
            return self._itertickets( set() )
        return self._itertickets( None )

    #-------------------------------------------------------------------------------------------------------
    def _itertickets( self, _seen ):
        for base in self.iterbases():
            if self.isLinkdict( base ):
                items = base.local.iteritems()
            else:
                items = base.iteritems()
            for key, value in items:
                if _seen is not None:
                    if key in _seen: continue
                    _seen.add( key )
                yield base, key, value

    #-------------------------------------------------------------------------------------------------------
    def has_key( self, key ):
        return key in self

    #-------------------------------------------------------------------------------------------------------
    def clear( self ):
        isLinkdict = self.isLinkdict
        for base in self.iterbases():
            if isLinkdict( base ):
                base.local.clear()
            else:
                base.clear()

    #-------------------------------------------------------------------------------------------------------
    def asdict( self ):
        return dict( self.iteritems() )

    #-------------------------------------------------------------------------------------------------------
    def get( self, key, default = None ):
        return self.asdict.get( key, default )

    #-------------------------------------------------------------------------------------------------------
    def ticketdict( self ):
        return dict( ( key, ( base, key, value, ), ) for base, key, value in self.itertickets() )

    #-------------------------------------------------------------------------------------------------------
    def base( self, key, default = Misfit, defaultbase = None ):
        return self.ticket( key, default, defaultbase )[ 0 ]

    #-------------------------------------------------------------------------------------------------------
    def ticket( self, key, default = Misfit, defaultbase = None ):
        try:
            base, key, value = self.ticketdict()[ key ]
        except KeyError, e:
            if default is Misfit:
                raise e
            return defaultbase, key, default
        return base, key, value

    #-------------------------------------------------------------------------------------------------------
    def pop( self, key, default = Misfit ):
        base, key, value = self.popticket( key, default )
        return key

    #-------------------------------------------------------------------------------------------------------
    def popitem( self, key, default = Misfit ):
        base, key, value = self.popticket( key, default )
        return key, value

    #-------------------------------------------------------------------------------------------------------
    def popticket( self, key, default = Misfit, defaultbase = None ):
        base, key, value = self.ticket( key, default, defaultbase )
        dict.__delitem__( base, key )
        return base, key, value

    #-------------------------------------------------------------------------------------------------------
    def __unicode__( self ):
        return '<%s %s>' % ( self.__class__.__name__, self.asdict() )

    #-------------------------------------------------------------------------------------------------------
    def __repr__( self ):
        return self.__unicode__().encode()

    #-------------------------------------------------------------------------------------------------------
    def __str__( self ):
        return self.__repr__()

############################################################################################################
#
#
#
#===========================================================================================================
if __name__ == '__main__':

    #import pylon_mechanic

    class Demodict( Linkdict ):
        def __unicode__( self ):
            d = dict( self )
            try:
                return '<%s>' % ( d[ 'iam' ], )
            except KeyError:
                return unicode( d )

        def __repr__( self ):
            return self.__unicode__().encode()

        def __str__( self ):
            return self.__repr__()

    n = dict( iam = 'n', N = 108 )
    d = Demodict( iam = 'd', D = 42 )
    e = Demodict( iam = 'e', E = 43 ).addbases( d )
    f = Demodict( iam = 'f', F = 44 )
    g = Demodict( iam = 'g', G = 45 ).addbases( e, f )
    h = Demodict(                   ).addbases( g )
    d.addbases( g, n ) # creating a circular reference

    i = Demodict( iam= 'i', I = 108 ).addbases( g )
    i.local.pop( 'I' )
    print len( i )
    print i.localLength()
    print i.asdict()

    for line in """
        n
        d.asdict()
        e.asdict()
        f.asdict()
        g.asdict()
        h.asdict()
        #------------------------------------------------------------------------------------------------------------
        d.localBases
        e.localBases
        f.localBases
        g.localBases
        h.localBases
        #------------------------------------------------------------------------------------------------------------
        d.bases()
        e.bases()
        f.bases()
        g.bases()
        h.bases()
        #------------------------------------------------------------------------------------------------------------
        g.items()
        g.keys()
        g.values()
        g.local.items()
        g.tickets()
        g.tickets( unique = False )
        g.asdict()
        g.ticketdict()
        g.local.keys()
        g.keys()
        g.keys( unique = False )
        g.has_key( 'E' )
        g.popticket( 'E' )
        g.has_key( 'E' )
        e.local.items()
        g[ 'F' ]
        g == h
        g == f
        #------------------------------------------------------------------------------------------------------------
#           f.asdict()
#           g.asdict()
#           g.pop( 'F' )
#           g.pop( 'F', None )
#           f.asdict()
#           g.asdict()
#           g.clear()
        """.splitlines():
        line = line.strip()
        if not line: continue
        if line.startswith( '#' ):
            print line
        else:
            print '%-30s %s' % ( '%s:' % line, eval( line ), )
