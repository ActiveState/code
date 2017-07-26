import new

class Compose(object):
    def __init__(self, *parts):
        self.parts = parts
    def __call__(self, cls):
        conflicts = dict()
        parts = self.parts + (cls,)
        for i, part1 in enumerate(parts):
            for partn in parts[i+1:]:
                for attr in dir(part1):
                    if attr[:2] == attr[-2:] == '__':
                        continue
                    if getattr(partn, attr, None):
                        if attr not in conflicts:
                            conflicts[attr] = [part1]
                        conflicts[attr].append(partn)
        if conflicts:
            text = []
            for key, lst in conflicts.items():
                text.append('    %s:' % key)
                for c in lst:
                    text.append('        %s' % c)
            text = '\n'.join(text)
            raise TypeError("Conflicts while composing:\n%s" % text)
        for part in self.parts:
            for attr in dir(part):
                if attr[:2] == attr[-2:] == '__':
                    continue
                thing = getattr(part, attr)
                thing = getattr(thing, '__func__', None) or thing
                if callable(thing):
                    setattr(cls, attr, new.instancemethod(thing, None, cls))
                else:
                    setattr(cls, attr, thing)
        return cls
