def all_members(aClass):
    members = {}
    bases = list(aClass.__bases__)
    bases.reverse()
    for base in bases:
        members.update(all_members(base))
    members.update(vars(aClass))
    return members

class Eggs:
    eggs = 'eggs'
    spam = None

class Spam:
    spam = 'spam'

class Breakfast(Spam, Eggs):
    eggs = 'scrambled'

print all_members(Eggs)
print all_members(Spam)
print all_members(Breakfast)

# Output:
# {'spam': None, '__doc__': None, 'eggs': 'eggs', '__module__': '__main__'}
# {'spam': 'spam', '__doc__': None, '__module__': '__main__'}
# {'__doc__': None, 'eggs': 'scrambled', 'spam': 'spam', '__module__': '__main__'}
