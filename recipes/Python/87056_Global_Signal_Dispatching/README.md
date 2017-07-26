## Global Signal DispatchingOriginally published: 2001-11-06 13:33:51 
Last updated: 2001-12-11 19:30:28 
Author: Patrick O'Brien 
 
This module, dispatcher.py, provides global signal dispatching services suitable for a wide variety of purposes, similar to Model-View-Controller or Model-View-Presenter patterns. This particular implementation allows a looser coupling than most Observer patterns. It also does transparent cleanup through the use of weak references and weak reference callbacks. This version defaults to using weak references, but provides an option to not use weak references for those cases where weak references are problematic (lambdas and such).