'''
    BuiltExtensionFinder(
        {'buildpath0': dotted_module_name0,
         ....
         'buildpath1': dotted_module_name1,
         }
         )

    creates a built c-extension module finder. This allows for a single code repository
    to have all of its extensions built using python setup.py build_ext with different
    python versions and have these extensions loadable without installation into the
    different python areas.

    #eg:
    import sys
    from builtextensionfinder import BuiltExtensionFinder
    sys.meta_path.append(
        BuiltExtensionFinder(
            {r'c:\code\hg-repos\reportlab\build':(
                'reportlab.graphics._renderPM',
                'reportlab.lib._rl_accel',
                ),
                r'c:\code\hg-repos\pyRXP\build': 'pyRXPU',
            }
            )
        )
    '''
__all__=('BuiltExtensionFinder',)
import sys, os
from distutils.util import get_platform
if sys.version_info[:2]<(3,4):
    import imp
    class BuiltExtensionFinder(object):
        libname = 'lib.%s-%d.%d' % (get_platform(),sys.version_info[0],sys.version_info[1])
        EXTENSION_SUFFIXES = tuple(x[0] for x in imp.get_suffixes() if x[2]==imp.C_EXTENSION)
        def __init__(self,build_roots={}):
            self.overrides = {}
            for k, V in build_roots.items():
                if not isinstance(V,(list,tuple)):
                    V = (V,)
                for v in V:
                    self.overrides[v] = os.path.join(k,self.libname,*v.split('.'))
            self.module = None

        def find_module(self, name, path=None):
            if name in self.overrides:
                fnroot = self.overrides[name]
                alt_paths = [os.path.dirname(fnroot)]
                modname = name.split('.')[-1]
                for sfx in self.EXTENSION_SUFFIXES:
                    fn = fnroot + sfx
                    if os.path.isfile(fn):
                        try:
                            fpd = imp.find_module(modname,alt_paths)
                            if fpd:
                                try:
                                    try:
                                        m = imp.load_module(name,fpd[0],fpd[1],fpd[2])
                                        if m:
                                            m.__loader__ = self
                                            self.module = m
                                            return self
                                    except:
                                        pass
                                finally:
                                    if fpd[0]: fpd[0].close()
                        except:
                            continue

        def load_module(self, name):
            if not self.module:
                raise ImportError("Unable to load module %s" % name)
            sys.modules[name] = m = self.module
            self.module = None
            return m
else:
    from importlib.abc import MetaPathFinder
    from importlib.machinery import ExtensionFileLoader, ModuleSpec
    class BuiltExtensionFinder(MetaPathFinder):
        libname = 'lib.%s-%d.%d' % (get_platform(),sys.version_info[0],sys.version_info[1])
        from importlib.machinery import EXTENSION_SUFFIXES
        def __init__(self,build_roots={}):
            self.overrides = {}
            for k, V in build_roots.items():
                if not isinstance(V,(list,tuple)):
                    V = (V,)
                for v in V:
                    self.overrides[v] = os.path.join(k,self.libname,*v.split('.'))
        def find_spec(self,name,path,target=None):
            if name in self.overrides:
                fnroot=self.overrides[name]
                for sfx in self.EXTENSION_SUFFIXES:
                    fn = fnroot + sfx
                    if os.path.isfile(fn):
                        spec = ModuleSpec(
                                name=name,
                                loader=ExtensionFileLoader(name,fn),
                                origin=fn,
                                is_package=False,
                                )
                        return spec
