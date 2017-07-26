_html_mapping = (
    ("&", "&amp;"),
    ("  ", "&nbsp;&nbsp;"),
    (">", "&gt;"),
    ("<", "&lt;"),
    ('"', "&quot;"),
)

def encode_html(obj):
    text = str(obj)
    for chr, enc in _html_mapping:
        text = text.replace(chr, enc)
    return text

class AttrDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __iter__ = dict.iteritems

class HElement(object):
    _name = None
    _enclosing = True
    _defaults = {}
    _pretty = True
    
    def __init__(self, *elems, **attrs):
        if self._name is None:
            self.name = self.__class__.__name__.lower()
        else:
            self.name = self._name
        if self._enclosing:
            self.elems = list(elems)
        elif elems:
            raise ElementError("element is not a container")
        self.attrs = AttrDict(self._defaults)
        self.attrs.update(attrs)

    def _render(self, nesting, pretty):
        items = []
        if pretty:
            indent = "    " * nesting
            subindent = "    " * (nesting + 1)
            items.append(indent)
        items.append("<")
        items.append(self.name)
        for k, v in self.attrs:
            if isinstance(v, bool):
                if v:
                    items.append(" ")
                    items.append(k)
            else:
                items.append(" ")
                items.append(k)
                items.append('="')
                items.append(encode_html(v))
                items.append('"')
        items.append(">")
        if pretty: 
            items.append("\n")
        if self._enclosing:
            for elem in self.elems:
                if isinstance(elem, HElement):
                    items.extend(elem._render(nesting + 1, pretty))
                elif pretty:
                    for line in encode_html(elem).splitlines():
                        items.append(subindent)
                        items.append(line)
                        items.append("\n")
                else:
                    items.append(" ".join(encode_html(elem).splitlines()))
            if pretty:
                items.append(indent)
            items.append("</")
            items.append(self.name)
            items.append(">")
            if pretty:
                items.append("\n")
        return items

    def render(self, nesting = 0, pretty = None):
        if pretty is None:
            pretty = self._pretty
        return "".join(self._render(nesting, pretty)).strip()

    __repr__ = render


class SimpleElement(HElement): 
    _enclosing = False

# headers
class Root(HElement): _name = "html"
class Head(HElement): pass
class Title(HElement): pass
class Meta(HElement): pass
class Body(HElement): pass

# formatting
class Break(SimpleElement): _name = "br"
class Para(HElement): _name = "p"
class Bold(HElement): _name = "b"
class Italics(HElement): _name = "i"
class Underline(HElement): _name = "u"
class Font(HElement): pass
class BulletGroup(HElement): _name = "ul"
class Bullet(HElement): _name = "li"
class Quote(HElement): _name = "q"
class Pre(HElement): pass
class Mono(HElement): _name = "tt"

# forms
class Form(HElement): pass
class Field(SimpleElement): _name = "input"
class TextField(Field): _defaults = {"type" : "text"}
class PasswordField(Field): _defaults = {"type" : "password"}
class CheckboxField(Field): _defaults = {"type" : "checkbox"}
class RadioButton(Field): _defaults = {"type" : "radio"}
class SubmitButton(Field): _defaults = {"type" : "submit"}
class ResetButton(Field): _defaults = {"type" : "reset"}
class SelectField(HElement): _name = "select"
class OptionField(HElement): _name = "option"
class TextArea(HElement): pass

# tables
class Table(HElement): pass
class Row(HElement): _name = "tr"
class Col(HElement): _name = "td"


# test
if __name__ == "__main__":
    f = Form(
        "some text",
        Table(
            Row(
                Col(
                    "hello moshe", 
                    Bold("kaki\npipi"), 
                    TextField(name = "moshe"),
                    Break(),
                    "lala", 
                    bgcolor = "white"),
            ),
            Row(
                Col(
                    SubmitButton(value = "send")
                )
            ),
            width = "100%",
        ),
        action = "login", 
        method = "post"
    )
    f.elems[1].elems.append("and some more text")
    f.attrs.method = "get"
    print f
    
        
#    <form action="login" method="get">
#        some text
#        <table width="100%">
#            <tr>
#                <td bgcolor="white">
#                    hello moshe
#                    <b>
#                        kaki
#                        pipi
#                    </b>
#                    <input type="text" name="moshe">
#                    <br>
#                    lala
#                </td>
#            </tr>
#            <tr>
#                <td>
#                    <input type="submit" value="send">
#                </td>
#            </tr>
#            and some more text
#        </table>
#    </form>
