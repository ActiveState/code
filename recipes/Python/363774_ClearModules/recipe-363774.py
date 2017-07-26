"""Clear ``sys.modules`` of specific types of modules if one is stale."""

__docformat__ = "restructuredtext"


_lastModuleUpdate = time.time()
def clearModules():
    """Clear ``sys.modules`` of specific types of modules if one is stale.

    See ``properties.CLEAR_MODULES``.

    I took this method out of the ``InternalLibrary`` class so that you can
    call it *really* early, even before you create a ``Context`` to pass to
    ``InternalLibrary``.

    """
    global _lastModuleUpdate
    if not properties.CLEAR_MODULES:
        return
    deleteTheseTypes = properties.CLEAR_MODULES
    if not isinstance(deleteTheseTypes, list):
        # Update Seamstress Exchange's properties file if you change this.
        deleteTheseTypes = ["aquarium.layout","aquarium.navigation",
                            "aquarium.screen", "aquarium.widget"]
    deleteThese = [
        moduleName
        for moduleType in deleteTheseTypes
            for moduleName in sys.modules.keys()
                if (moduleName == moduleType or 
                    moduleName.startswith(moduleType + "."))
    ]
    for i in deleteThese:
        try:
            file = sys.modules[i].__file__
        except AttributeError:
            continue
        if file.endswith(".pyc") and os.path.exists(file[:-1]):
            file = file[:-1]
        ST_MTIME = 8
        if (_lastModuleUpdate < os.stat(file)[ST_MTIME]):
            staleModules = True
            break
    else:
        staleModules = False
    if staleModules: 
        for i in deleteThese:           # You can't modify a dictionary 
            del sys.modules[i]          # during an iteration.
    _lastModuleUpdate = time.time()
