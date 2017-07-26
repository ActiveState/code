def EnsureDefinition(name, definition, target=__builtins__.__dict__):
    """
    EnsureDefinition(name, definition, target)

    Ensure that a name exists in the given target namespace (a dictionary). If 
    it does exist, do nothing. If it doesn't, execute the definition in the 
    target.
    """
    print 'Checking for %s in target...' % name,
    if target.has_key(name):
        print 'found.'
    else:
        print 'not found! Defining with %s' % definition
        exec definition in target

EnsureDefinition('False','False = 0')
EnsureDefinition('True','True = not False')
EnsureDefinition('bool','''
def bool(x):
    if x:
        return True
    else:
        return False
'''

# Output for Python version < 2.2.1:
#
# Checking for False in target... not found! Defining with False = 0
# Checking for True in target... not found! Defining with True = not False
# Checking for bool in target... not found! Defining with def bool(x):
#     if x:
#         return True
#     else:
#         return False
