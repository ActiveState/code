class InterpolationEvaluationException(KeyError):
    pass 

class expression_dictionary(dict):
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            try:
                return eval(key,self)
            except Exception, e:
                raise InterpolationEvaluationException(key, e)


# ---------- Usage ---------------

# Evaluate expressions in the context of a dictionary...
>>> my_dict = {'x': 1, 'y': 2}
>>> print "The sum of %(x)s and %(y)s is %(x+y)s" % expression_dictionary(my_dict)
  The sum of 1 and 2 is 3

# or use in conjunction with locals() or globals() to evaluate in a namespace.
>>> ft = 14410.0
>>> ns = expression_dictionary(locals())
>>> print "  Summit altitude: %(ft)0.1f feet (%(ft * 0.3048)0.1f meters)" % ns
  Summit altitude: 14410.0 feet (4392.2 meters)
