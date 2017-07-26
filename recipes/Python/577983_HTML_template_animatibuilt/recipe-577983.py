from lxml import etree
from pyquery.pyquery import PyQuery

class Animator(PyQuery):
    
    def listfill(self, selector, data):
        """Bind list of items to HTML list. In the event of selector yielding 
        more than prototype item, these are cycled over to be cloned and filled.
        """
        proto = self(selector)
        parent = proto.parent()
        proto.remove()
        N = len(proto)
        for idx, item in enumerate(data):
            parent.append(proto.eq(idx % N).clone().text(item))
        
    def tablefill(self, selector, subselector, data):
        """Bind list of tuples to table. Typically selector='tr' and
        subselector='td'.  In the event of selector yielding more than
        one row, these are cycled over to be cloned and filled."""
        proto = self(selector)
        parent = proto.parent()
        proto.remove()
        N = len(proto)
        for idx, row in enumerate(data):
            parent.append(proto.eq(idx % N).clone().rowfill(subselector, row))
    
    def rowfill(self, selector, values):
        """Bind array to selector's children's text nodes. Length of values
        must be no greater than children available in selector."""
        q = self(selector)
        for idx, value in enumerate(values):
            q.eq(idx).text(value)
        return self
    
    
def test():
    template = '''
    <table id="nametable">
    <tr style="text-color:red"><td>Lorem</td><td>Ipsum</td>
    <tr><td>Lorem</td><td>Ipsum</td>
    </table>
    <p id="error">Error in names</p>
    <p>Your name is <span id="username">Lorem Ipsum</span></p>
    <ul id="namelist">
    <li>Lorem Ipsum</li>
    </ul>
    '''
    data = [('John', 'Smith'), ('Joe', 'Bloggs'), ('Razor', 'Blade')]
    names = ['John Smith', 'Joe Blogs']
    t = Animator(template)
    t('#nametable').tablefill('tr', 'td', data)
    t('#nametable').attr.border = '1'
    t('#namelist').listfill('li', names)
    t('#error').remove()
    t('#username').text('Jimmy Choo')
    print t
    return t

if __name__ == "__main__":
    test()

# Resulting output
"""
<div><table id="nametable" border="1"><tr style="text-color:red"><td>John</td><td>Smith</td>
    </tr><tr><td>Joe</td><td>Bloggs</td>
    </tr><tr style="text-color:red"><td>Razor</td><td>Blade</td>
    </tr></table> 
    <p>Your name is <span id="username">Jimmy Choo</span></p>
    <ul id="namelist"> 
    <li>John Smith</li>
    <li>Joe Blogs</li>
    </ul></div>

"""
