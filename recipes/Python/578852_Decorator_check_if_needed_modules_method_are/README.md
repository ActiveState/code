## Decorator to check if needed modules for method are imported

Originally published: 2014-03-18 14:11:19
Last updated: 2014-03-18 14:11:20
Author: Andrey Nikishaev

Check if needed modules imported before run method\n\n    Example::\n\n        @require_module(['time'],exception=Exception)\n        def get_time():\n            return time.time()