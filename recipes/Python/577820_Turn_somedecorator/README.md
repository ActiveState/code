###Turn @some_decorator() into @some_decorator

Originally published: 2011-08-02 23:53:02
Last updated: 2011-08-04 18:48:36
Author: Eric Snow

A decorator factory is a function that returns a decorator based on the arguments you pass in.  Sometimes you make a decorator factory to cover uncommon use cases.  In that case you'll probably use default arguments to cover your common case.\n\nThe problem with this, however, is that you still have to use the call syntax (with no arguments) to get the common-use-case decorator, as demonstrated in the recipe title.  This recipe effectively makes it so that your decorator factory and your common-use-case decorator have the same name (and actually the same object).