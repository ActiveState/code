## Decorator to check if needed modules for method are imported  
Originally published: 2014-03-18 14:11:19  
Last updated: 2014-03-18 14:11:20  
Author: Andrey Nikishaev  
  
Check if needed modules imported before run method

    Example::

        @require_module(['time'],exception=Exception)
        def get_time():
            return time.time()