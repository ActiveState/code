def hash_style(style):
    return tuple(sorted(style.items()))

style_pool = {} 
defaultstyle = {}   
def create_style(**kwds):
    style = defaultstyle.copy()
    style.update(kwds)
    key = hash_style(style)
    try:
        return style_pool[key]
    except KeyError:
        style_pool[key] = style
        return style

defaultstyle = create_style(textcolor='black', fontsize=10)

def updated_style(style, properties):
    new = style.copy()
    new.update(properties)
    return create_style(**new)

                    
    
class Characters:
    style = None
    def __init__(self, text, style=defaultstyle):
        self.data = text
        self.style = style

    def __len__(self):
        return len(self.data)
        
    def get_style(self, i):
        return self.style
        
    def __repr__(self):
        return "C(%s)" % repr(self.data)

    def __len(self):
        return len(self.data)
        
    def split(self, i):
        if i<0 or i>len(self):
            raise IndexError(i)
        l = Characters(self.data[:i], self.style)
        r = Characters(self.data[i:], self.style)
        return l, r
        
    def set_properties(self, i1, i2, properties):
        i1 = max(0, i1)
        i2 = min(len(self), i2)
        tmp, r = self.split(i2)
        l, tmp = tmp.split(i1)
        style = updated_style(self.style, properties)
        c = Characters(tmp.data, style)
        return Group([l, c, r])
        
    def insert(self, i, texel):
        if isinstance(texel, Characters) and texel.style is self.style:
            text = self.data[:i]+texel.data+self.data[i:]
            return Characters(text, self.style)
        a, b = self.split(i)
        return Group([a, texel, b])



class Group:
    def __init__(self, content):
        self.data = list(content)
        length = 0
        for texel in content:
            length += len(texel)
        self._length = length
            
    def __len__(self):
        return self._length
        
    def __repr__(self):
        return "G(%s)" % repr(self.data)
        
    def get_style(self, i):
        for texel in self.data:
            n = len(texel)
            if n>i:
                return texel.get_style(i)
            i -= n
        
    def set_properties(self, i1, i2, properties):
        r = []
        i = 0
        for texel in self.data:
            n = len(texel)
            if i1<n and i2>0:
                r.append(texel.set_properties(i1, i2, properties))
            else:
                r.append(texel)
            i1 -= n
            i2 -= n
        return Group(r)
        
    def split(self, i):
        if i<0 or i>len(self):
            raise IndexError(i)
        l = []
        r = []
        for texel in self.data:
            n = len(texel)
            if i<=0:
                r.append(texel)
            elif i>=n:
                l.append(texel)
            elif n>i:
                a, b = texel.split(i)
                l.append(a)
                r.append(b)
            i -= n
        return Group(l), Group(r)
        
    def insert(self, i, texel):
        if i == len(self):
            return Group(self.data+[texel])

        data = []
        for elem in self.data:
            n = len(elem)
            if i<0:
                data.append(elem)
            elif i>=n:
                data.append(elem)
            else:
                data.append(elem.insert(i, texel))
            i -= n
        return Group(data)


C = Characters        
G = Group
