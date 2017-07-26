import wx, os, sys
errorframe = None

def watcherrors(function):
     '''function decorator to display Exception information.'''
     def substitute(*args, **kwargs):
         try:
             return function(*args, **kwargs)
         except Exception:
             error_type, error, traceback = sys.exc_info()
             mb = wx.MessageDialog(errorframe,
                         '%s\n\nClick OK to see traceback' % error,
                         'Error in Run',
                         wx.OK | wx.CANCEL | wx.ICON_ERROR)
             if wx.ID_OK == mb.ShowModal():
                 mb.Destroy()
                 from traceback import extract_tb
                 trace = ['%s line %s in %s:\n\t%s' % (
                              os.path.split(filename)[1], line, fun, text)
                          for filename, line, fun, text in
                                  extract_tb(traceback)]
                 mb = wx.MessageDialog(errorframe,
                         '\n'.join(['%s\n' % error] + trace),
                         'Run Error w/ Traceback',
                         wx.OK | wx.ICON_ERROR)
                 result = mb.ShowModal()
             mb.Destroy()
             raise  # Optional-- you may want to squech some errors here

         try:
             substitute.__doc__ = function.__doc__
         except AttributeError:
             pass

         return substitute

# You can use it as follows to wrap functions and methods:
'''
class ....

     @watcherrors
     def something(somearg)
         if somearg is not None:
                 raise ValueError(somearg)
     ...
'''

# Alternative: (watcherrors is defined almost as above)

def augmentedwatch(holder, framefieldname):
    def watcherrors(function:
        '...' # -- same as above
        def substitute(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception:
                error_type, error, traceback = sys.exc_info()
                ### new code:
                errorframe = getattr(holder, framefieldname, None) 
                '...' # -- same as above
        return substitute
    return watcherrors

# You use this as follows to wrap functions and methods, where 
# holder is an expression at "first import" time that will, at
# the time of one of the uncaught exceptions, have an attribute 
# named 'frame':
''' 
class ....

     @augmentedwatch(holder, 'frame')
     def something(somearg)
         if somearg is not None:
                 raise ValueError(somearg)
     ...
'''
