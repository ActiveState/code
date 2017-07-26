"""This mixin supports autoloading."""

__docformat__ = "restructuredtext"


class AutoLoader:

    """This mixin supports autoloading.

    That means if you try to access an undefined attribute (e.g.
    ``self.Spam``), an aquarium.util.AquariumClass_ instance which uses this
    mixin will automatically import and instantiate the AquariumClass called
    ``Spam`` that is the same type of module as it is (e.g. a database module
    instance would try to import and instantiate ``aquarium.database.Spam``).
    This mixin is used by aquarium.database.DatabaseAssistant_, etc.  

    .. _aquarium.util.AquariumClass: 
       aquarium.util.AquariumClass.AquariumClass-class.html
    .. _aquarium.database.DatabaseAssistant: 
       aquarium.database.DatabaseAssistant.DatabaseAssistant-class.html

    """

    def __getattr__(self, attr):
        """Import, instantiate, and return the desired instance.
        
        Note, these instances will be cached in ``self._autoLoaderCache``.

        """
        if not self.__dict__.has_key("_autoLoaderCache"):
            self._autoLoaderCache = {}
        cache = self._autoLoaderCache 
        if not cache.has_key(attr):
            try:
                cache[attr] = self._ctx.iLib.aquariumFactory("%s.%s" %
                    (self.getModuleType(), attr))
            except ImportError:
                raise AttributeError("""\
%s instance has no attribute '%s', and AutoLoader failed too""" % 
                                     (self.__class__.__name__, attr))
        return cache[attr]

    def getModuleType(self):
        """Return the type of Aquarium module this instance is.
        
        Usually, I can automatically figure out what type of module you are,
        but if you need to get fancy, override this.

        """
        # If "self.__module__" yields something like "aquarium.screen.Screen",
        # the goal is to return "screen".
        return self.__module__.split(".")[1:-1]
