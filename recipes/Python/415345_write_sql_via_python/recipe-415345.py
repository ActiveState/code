try:
    frozenset
except NameError:
    from sets import ImmutableSet as frozenset

def indent(width, s):
    space = width * ' '
    return '\n'.join([(space + line) for line in s.split('\n')])

def make_indenter(width):
    def indenter(s): return indent(width, s)
    return indenter

class AutoIndent(object):
    r"""AutoIndent

    replace bracketed template '( %s )' with multi-line template that will
    block-indents elements when interpolated with parameter

        >>> s1 = AutoIndent('speak(%s)')
        >>> s2 = AutoIndent('speak( %s )')

        >>> word = 'hello'
        >>> paragraph = '\n'.join(['Hello !', 'How are you ?', 'It\'s nice to see you.'])
    
        >>> print s1 % word
        speak(hello)

        >>> print s2 % paragraph
        speak(
          Hello !
          How are you ?
          It's nice to see you.
        )
    """
    def __init__(self, template):
        super(AutoIndent, self).__init__()
        multiline = template.count('( %s )')
        if multiline and (multiline != template.count('%s')):
            raise ValueError('Template must be homogenious')
        self.template = template.replace('( %s )', '(\n%s\n)')
        if multiline:
            self.indent = make_indenter(2)
        else:
            self.indent = lambda x: x
    def __mod__(self, value):
        if isinstance(value, basestring):
            t = (self.indent(value),)
        else:
            t = tuple([self.indent(v) for v in value])
        return self.template % t

def multiline(s):
    r"""multiline

        >>> multiline('Hello there')
        False

        >>> multiline('\n'.join(['Hello', 'there']))
        True
    """
    return s.find('\n') >= 0

class Source(object):
    """Source

        >>> i = Source('items')
        >>> print i.ITEM_ID
        items.ITEM_ID
    """
    def __init__(self, alias):
        super(Source, self).__init__()
        self.alias = alias
        self.fields = {}
    def __getattr__(self, name):
        if name in self.fields:
            return self.fields[name]
        else:
            f = Field(self, name)
            self.fields[name] = f
            return f
    def __str__(self): return self.alias
    def declaration(self): raise NotImplementedError()

class StatementSource(Source):
    """StatementSource

        >>> s = StatementSource('items', 'select * from IMA')
        >>> print s.declaration()
        (
          select * from IMA
        ) items
    """
    def __init__(self, alias, statement):
        super(StatementSource, self).__init__(alias)
        self.statement = statement
    def declaration(self):
        return AutoIndent('( %s ) ') % str(self.statement) + self.alias

class NamedSource(Source):
    """NamedSource

        >>> i = NamedSource('items', 'i')
        >>> print i
        i
        >>> print i.ITEM_ID
        i.ITEM_ID
    """
    def __init__(self, name, alias=None):
        super(NamedSource, self).__init__(alias)
        self.name = name
    def __str__(self): return self.alias or self.name
    def declaration(self):
        if self.alias:
            return '%s %s' % (self.name, self.alias)
        else:
            return self.name

class Expression(object): pass

class CustomExpression(Expression):
    def __init__(self, text): self.text = text
    def __str__(self): return str(self.text)

custom = CustomExpression

class StringLiteralExpression(Expression):
    """StringLiteralExpression

        >>> s = StringLiteralExpression('Huh?')
        >>> print s
        'Huh?'
    """
    def __init__(self, text): self.text = text
    def __str__(self): return "'%s'" % (self.text.replace("'", "''"))
    def expression(cls, expr):
        if isinstance(expr, Expression) and not isinstance(expr, cls): return expr
        else: return cls(expr)
    expression = classmethod(expression)

strlit = StringLiteralExpression.expression

class BooleanExpression(Expression): pass

class UnaryOperated(object):
    def __init__(self, element):
        super(UnaryOperated, self).__init__()
        self.element = element
    def __nonzero__(self): return bool(self.element)

class BinaryOperated(object):
    def __init__(self, *elements):
        super(BinaryOperated, self).__init__()
        self.elements = elements
    def __len__(self): return len(self.elements)
    def __nonzero__(self):
        for e in self.elements:
            if e: return True
        return False

class IsNull(UnaryOperated, Expression):
    """IsNull

        >>> print IsNull('ITEM_ID')
        ITEM_ID is null
    """
    def __str__(self): return '%s is null' % str(self.element)

class Blanket(UnaryOperated, Expression):
    def __str__(self):
        s = str(self.element)
        if multiline(s): return AutoIndent('( %s )') % s
        else: return '(%s)' % s

def blanket(expression):
    """blanket

        >>> print blanket('Huh?')
        (Huh?)

        >>> print blanket(blanket('Huh?'))
        (Huh?)
    """
    if isinstance(expression, Blanket):
        return expression
    else:
        return Blanket(expression)

def is_composite(expr):
    """is_composite

        >>> is_composite(Not('1=1'))
        False
    
        >>> is_composite(And('1=1'))
        False

        >>> is_composite(And('1=1', '2=2'))
        True
    """
    return isinstance(expr, BinaryOperated) and (len(expr) > 1)

def blanket_as_needed(expression):
    """blanket_as_needed

        >>> print blanket_as_needed('Huh?')
        (Huh?)

        >>> print blanket_as_needed(Not('0=0'))
        not (0=0)

        >>> print blanket_as_needed(And('0=0', '1=1', '2=2'))
        (
          (0=0) and
          (1=1) and
          (2=2)
        )
    """
    if is_composite(expression) or isinstance(expression, basestring): return Blanket(expression)
    else: return expression


class Prefixed(UnaryOperated):
    def __init__(self, prefix, element):
        super(Prefixed, self).__init__(element)
        self.prefix = prefix
    def __str__(self): return '%s %s' % (self.prefix, str(blanket_as_needed(self.element)))

class Infixed(BinaryOperated):
    def __init__(self, infix, *elements):
        super(Infixed, self).__init__(*elements)
        self.infix = infix
    def __str__(self): return (' %s ' % self.infix).join([str(blanket_as_needed(e)) for e in self.elements if e])

class PrefixedExpression(Prefixed, Expression):
    def __init__(self, prefix, expression):
        Prefixed.__init__(self, prefix, expression)
        Expression.__init__(self)

class Plus(PrefixedExpression):
    def __init__(self, expression): super(Plus, self).__init__('+', expression)

class Minus(PrefixedExpression):
    def __init__(self, expression): super(Minus, self).__init__('-', expression)

class PrefixedBooleanExpression(Prefixed, BooleanExpression):
    def __init__(self, prefix, boolexpr):
        Prefixed.__init__(self, prefix, boolexpr)
        Expression.__init__(self)

class Not(Prefixed, BooleanExpression):
    """Not

        >>> print Not('0=0')
        not (0=0)
    """
    def __init__(self, boolexpr): super(Not, self).__init__('not', boolexpr)

def invert(boolexpr):
    """invert

        >>> print invert('0=0')
        not (0=0)
    
        >>> print invert(invert('0=0'))
        0=0
    """
    if isinstance(boolexpr, Not):
        return boolexpr.element
    else:
        return Not(boolexpr)

class Combinative(object):
    
    def combine(cls, *combinatives):
        args = []
        for c in combinatives:
            if type(c) is cls:
                args.extend([e for e in c.elements if e])
            else:
                args.append(c)
        return cls(*args)
    combine = classmethod(combine)

class InfixedExpression(Infixed, Expression):
    def __init__(self, infix, *expressions):
        Infixed.__init__(self, infix, *expressions)
        Expression.__init__(self)

class Add(InfixedExpression, Combinative):
    """Add

        >>> print Add(1,2,3)
        1 + 2 + 3

        >>> print Add.combine(1,2,3)
        1 + 2 + 3

        >>> print Add.combine(1, Add(2,3), 4)
        1 + 2 + 3 + 4
    """
    def __init__(self, *expressions): super(Add, self).__init__('+', *expressions)

class Sub(InfixedExpression):
    def __init__(self, *expressions): super(Sub, self).__init__('-', *expressions)

class Mul(InfixedExpression, Combinative):
    def __init__(self, *expressions): super(Mul, self).__init__('*', *expressions)

class Div(InfixedExpression):
    def __init__(self, *expressions): super(Div, self).__init__('/', *expressions)

class InfixedBooleanExpression(Infixed, BooleanExpression):
    def __init__(self, infix, *boolexprs):
        Infixed.__init__(self, infix, *boolexprs)
        BooleanExpression.__init__(self)
    def __str__(self): return (' %s\n' % self.infix).join([str(blanket(e)) for e in self.elements])

class And(InfixedBooleanExpression, Combinative):
    """And

        >>> print And('0=0', '1=1', '2=2')
        (0=0) and
        (1=1) and
        (2=2)
    """
    def __init__(self, *boolexprs): super(And, self).__init__('and', *boolexprs)

class Or(InfixedBooleanExpression, Combinative):
    def __init__(self, *boolexprs): super(Or, self).__init__('or', *boolexprs)

class InfixedComparisonExpression(Infixed, BooleanExpression):
    def __init__(self, infix, left, right):
        if isinstance(left, basestring): left = strlit(left)
        if isinstance(right, basestring): right = strlit(right)
        Infixed.__init__(self, infix, left, right)
        BooleanExpression.__init__(self)
    left = property(lambda self: self.elements[0])
    right = property(lambda self: self.elements[1])

class Like(InfixedComparisonExpression):
    """Like

        >>> print Like(custom('ITEM_NAME'), 'Staron%')
        ITEM_NAME like 'Staron%'
    """
    def __init__(self, value, pattern):
        super(Like, self).__init__('like', value, pattern)

class LessThan(InfixedComparisonExpression):
    """LessThan
    
        >>> lessthan = LessThan(1, 2)
        >>> print lessthan
        1 < 2
        >>> lessthan.left
        1
        >>> lessthan.right
        2
    """
    def __init__(self, left, right): super(LessThan, self).__init__('<', left, right)

class LessThanOrEqual(InfixedComparisonExpression):
    def __init__(self, left, right): super(LessThanOrEqual, self).__init__('<=', left, right)

class GreaterThan(InfixedComparisonExpression):
    def __init__(self, left, right): super(GreaterThan, self).__init__('>', left, right)

class GreaterThanOrEqual(InfixedComparisonExpression):
    def __init__(self, left, right): super(GreaterThanOrEqual, self).__init__('>=', left, right)

class Equal(InfixedComparisonExpression):
    def __init__(self, left, right): super(Equal, self).__init__('=', left, right)

class OracleOuterDecorator(InfixedComparisonExpression):
    def __init__(self, decorated, left_outer=True):
        super(OracleOuterDecorator, self).__init__(decorated.infix, decorated.left, decorated.right)
        self.decorated = decorated
        self.left_outer = left_outer
    def __str__(self):
        if self.left_outer:
            return '%s %s %s(+)' % (self.left, self.infix, self.right)
        else:
            return '%s(+) %s %s' % (self.left, self.infix, self.right)

class NotEqual(InfixedComparisonExpression):
    def __init__(self, left, right): super(NotEqual, self).__init__('<>', left, right)

class Field(Expression):
    r"""Field

        >>> name = Field('item', 'ITEM_NAME')
        >>> price = Field('item', 'PRICE')
        >>> cost = Field('item', 'COST')
        >>> quantity = Field('invoice', 'QUANTITY')
    
        >>> print '\n'.join([str(x) for x in [name, price, cost, quantity]])
        item.ITEM_NAME
        item.PRICE
        item.COST
        invoice.QUANTITY

        >>> print price > cost
        item.PRICE > item.COST

        >>> print price * quantity
        item.PRICE * invoice.QUANTITY

        >>> print name.like('Staron%')
        item.ITEM_NAME like 'Staron%'

        >>> print name.is_null
        item.ITEM_NAME is null
    """
    
    def __init__(self, source, fieldname):
        super(Field, self).__init__()
        self.source = source
        self.fieldname = fieldname
    def __str__(self): return '%s.%s' % (str(self.source), self.fieldname)
    def __add__(self, other): return Add(self, other)
    def __radd__(self, other): return Add(other, self)
    def __sub__(self, other): return Sub(self, other)
    def __rsub__(self, other): return Sub(other, self)
    def __mul__(self, other): return Mul(self, other)
    def __rmul__(self, other): return Mul(other, self)
    def __div__(self, other): return Div(self, other)
    def __rdiv__(self, other): return Div(other, self)
    def __pos__(self): return Plus(self)
    def __neg__(self): return Minus(self)
    def __pow__(self, other): raise NotImplementedError()
    def __rpow__(self, other): raise NotImplementedError()
    def __abs__(self): raise NotImplementedError()
    def __mod__(self, other): raise NotImplementedError()
    def __rmod__(self, other): raise NotImplementedError()
    def __lt__(self, other): return LessThan(self, other)
    def __le__(self, other): return LessThanOrEqual(self, other)
    def __gt__(self, other): return GreaterThan(self, other)
    def __ge__(self, other): return GreaterThanOrEqual(self, other)
    def __eq__(self, other): return Equal(self, other)
    def __ne__(self, other): return NotEqual(self, other)
    def __and__(self, other): return And(self, other)
    def __rand__(self, other): return And(other, self)
    def __or__(self, other): return Or(self, other)
    def __ror__(self, other): return Or(other, self)
    is_null = property(lambda self: IsNull(self))
    def like(self, other): return Like(self, other)

class SourceList(object):
    """SourceList

        >>> s = SourceList()
        >>> item = s('ITEMS')
        >>> print item
        ITEMS
    
        >>> s('ITEMS')
        Traceback (most recent call last):
          ...
        ValueError: Duplicated key ('ITEMS')
    """
    def __init__(self):
        super(SourceList, self).__init__()
        self.clear()
        
    def clear(self):
        self.keys = []
        self.exprs = []
        self.aliases = []
        
    def clone(self):
        r = SourceList()
        r.assign(self)
        return r
    
    def assign(self, other):
        self.keys = list(other.keys)
        self.exprs = list(other.exprs)
        self.aliases = list(other.aliases)
        
    def __str__(self):
        def line(expr, alias):
            if not alias: return str(expr)
            return '%s %s' % (str(expr), str(alias))
        return ',\n'.join([line(expr, alias) for expr, alias in zip(self.exprs, self.aliases)])

    def __iter__(self): return iter(self.exprs)
        
    def _append(self, expr, alias):
        if isinstance(expr, Source):
            key = str(expr)
        else:
            key = str(alias or expr)
        if key in self.keys: raise ValueError("Duplicated key ('%s')" % key)
        self.keys.append(key)
        self.exprs.append(expr)
        self.aliases.append(alias)
    def __call__(self, name, alias=None):
        result = NamedSource(name, alias)
        self._append(result, alias)
        return result
    def statement(self, alias, statement):
        result = StatementSource(alias, statement)
        self._append(result, alias)
        return result

def iter_fields(expression):
    r"""iter_fields

        >>> ima = NamedSource('ima')
        >>> wko = NamedSource('wko')
        >>> join = And(ima.IMA_ItemID == wko.WKO_ItemID,
        ...            ima.IMA_UnitMeasure == wko.WKO_UnitMeasure,
        ...            Or(ima.IMA_ItemPrice.is_null, wko.WKO_WorkOrderDate == 3))
        ...
        >>> print '\n'.join([str(x) for x in iter_fields(join)])
        ima.IMA_ItemID
        wko.WKO_ItemID
        ima.IMA_UnitMeasure
        wko.WKO_UnitMeasure
        ima.IMA_ItemPrice
        wko.WKO_WorkOrderDate
    """
    if isinstance(expression, Field):
        yield expression
    elif isinstance(expression, UnaryOperated) and isinstance(expression, Expression):
        for x in iter_fields(expression.element):
            yield x
    elif isinstance(expression, BinaryOperated) and isinstance(expression, Expression):
        for expr in expression.elements:
            for x in iter_fields(expr):
                yield x

class FieldList(object):
    """FieldList

        >>> fields = FieldList()

        >>> print fields
        <BLANKLINE>
    
        >>> sources = SourceList()
        >>> ima = sources('IMA')
        >>> wko = sources('WKO')
    
        >>> fields.append(ima.IMA_ItemID)
        >>> len(fields)
        1
        >>> fields.append(wko.IMA_ItemID)
        Traceback (most recent call last):
          ...
        ValueError: Duplicated key ('IMA_ItemID')

        >>> fields.append(wko.IMA_ItemID, 'ITEM_ID')
        >>> len(fields)
        2

        >>> fields.append(ima.WKO_ItemID, 'ITEM_ID')
        Traceback (most recent call last):
          ...
        ValueError: Duplicated key ('ITEM_ID')

        >>> len(fields)
        2

        >>> fields.append('getdate()', 'TODAY')
        >>> len(fields)
        3
        >>> print fields
        IMA.IMA_ItemID                                     IMA_ItemID,
        WKO.IMA_ItemID                                     ITEM_ID,
        getdate()                                          TODAY

        >>> fields = FieldList()
        >>> fields.append(ima.IMA_ItemID)
        >>> fields.append(wko.WKO_ItemID)
        >>> fields.append('DATE')
        >>> print fields
        IMA.IMA_ItemID,
        WKO.WKO_ItemID,
        DATE
    """
    def __init__(self):
        super(FieldList, self).__init__()
        self.clear()
    def clear(self):
        self.keys = []
        self.values = []
        self.aliases = []
    def clone(self):
        r = FieldList()
        r.assign(self)
        return r
    def assign(self, other):
        self.keys = list(other.keys)
        self.values = list(other.values)
        self.aliases = list(other.aliases)
    def __len__(self): return len(self.keys)
    def __str__(self):
        if self.some_was_aliased():
            def line(key, value, alias): return '%-50s %s' % (str(value), str(key or alias or value))
            return ',\n'.join([line(k,v,a) for k,v,a in zip(self.keys, self.values, self.aliases)])
        else:
            return ',\n'.join([str(v) for v in self.values])
    def _check_key(self, key):
        if (key is not None) and (key in self.keys):
            raise ValueError("Duplicated key ('%s')" % key)
    def _do_append(self, key, value, alias):
        self._check_key(key)
        self.keys.append(key)
        self.values.append(value)
        self.aliases.append(alias)
    def _append_value(self, value, alias): self._do_append(alias, value, alias)
    def _append_field(self, field, alias): self._do_append(alias or field.fieldname, field, alias)
    def some_was_aliased(self):
        return [a for a in self.aliases if a is not None]
    def append(self, value, alias=None):
        if isinstance(value, Field):
            self._append_field(value, alias)
        else:
            self._append_value(value, alias)

class BooleanExpressionList(object):
    """BooleanExpressionList

        >>> exprs = BooleanExpressionList()
        >>> print exprs
        <BLANKLINE>

        >>> exprs.And('1=1')
        >>> print exprs
        (1=1)

        >>> exprs.invert()
        >>> print exprs
        not (1=1)

        >>> exprs.invert()
        >>> print exprs
        (1=1)

        >>> exprs.And('2=2')
        >>> print exprs
        (1=1) and
        (2=2)

        >>> exprs.Or('3=3', '4=4', '5=5')
        >>> print exprs
        (
          (1=1) and
          (2=2)
        ) or
        (3=3) or
        (4=4) or
        (5=5)

        >>> exprs.Or('6=6', '7=7')
        >>> print exprs
        (
          (1=1) and
          (2=2)
        ) or
        (3=3) or
        (4=4) or
        (5=5) or
        (6=6) or
        (7=7)
    """
    def __init__(self):
        super(BooleanExpressionList, self).__init__()
        self.clear()
    def clear(self): self.root = None
    def clone(self):
        r = BooleanExpressionList()
        r.assign(self)
        return r
    def assign(self, other):
        import copy
        self.root = copy.deepcopy(other.root)
    def __str__(self): return str(self.root or '')
    def _append(self, booloper, *boolexprs):
        if len(boolexprs) > 0:
            if self.root is None:
                self.root = booloper(*boolexprs)
            else:
                self.root = booloper.combine(self.root, *boolexprs)
    def And(self, *boolexprs): self._append(And, *boolexprs)
    def Or(self, *boolexprs): self._append(Or, *boolexprs)
    def invert(self):
        if self.root is not None: self.root = invert(self.root)

class GroupByList(object):
    """GroupByList

        >>> groupby = GroupByList()
    
        >>> print groupby
        <BLANKLINE>
    
        >>> groupby.append('INVO_DATE')
        >>> groupby.append('ORDER_DATE')
        >>> print groupby
        INVO_DATE,
        ORDER_DATE
    """
    def __init__(self):
        super(GroupByList, self).__init__()
        self.clear()
    def clear(self): self.values = []
    def clone(self):
        r = GroupByList()
        r.assign(self)
        return r
    def assign(self, other): self.values = list(other.values)
    def append(self, value): self.values.append(value)
    def __str__(self):
        return ',\n'.join([str(v) for v in self.values])

class OrderByList(object):
    """OrderByList

        >>> orderby = OrderByList()
    
        >>> print orderby
        <BLANKLINE>
    
        >>> orderby.append('INVO_DATE')
        >>> orderby.append('ORDER_DATE', False)
        >>> orderby.append('LINE_NUMBER', True)
        >>> print orderby
        INVO_DATE,
        ORDER_DATE desc,
        LINE_NUMBER
    """
    def __init__(self):
        super(OrderByList, self).__init__()
        self.clear()
    def clear(self):
        self.values = []
        self.ascendings = []
    def clone(self):
        r = OrderByList()
        r.assign(self)
        return r
    def assign(self, other):
        self.values = list(other.values)
        self.ascendings = list(other.ascendings)
    def append(self, value, ascending=True):
        self.values.append(value)
        self.ascendings.append(ascending)
    def __str__(self):
        def line(value, ascending): return (ascending and str(value)) or (str(value) + ' desc')
        return ',\n'.join([line(v,a) for v,a in zip(self.values, self.ascendings)])

class Function(object):
    def __init__(self, name):
        super(Function, self).__init__()
        self.name = name
    def __call__(self, *args):
        args_text = ', '.join([blanket_as_needed(a) for a in args])
        return '%s(%s)' % (self.name, args_text)

class FunctionFactory(object):
    def __getattr__(self, name): return Function(name)

class Statement(object):
    def __init__(self):
        super(Statement, self).__init__()
        self.func = FunctionFactory()

class BaseJoinList(object):
    def __init__(self):
        super(BaseJoinList, self).__init__()
        self.clear()
    def clear(self):
        self.lefts = []
        self.rights = []
        self.expressions = []
    def clone(self):
        r = type(self)()
        r.assign(self)
        return r
    def assign(self, other):
        self.lefts = list(other.lefts)
        self.rights = list(other.rights)
        self.expressions = list(other.expressions)
    def is_joined(self, left, right): raise NotImplementedError()
    def append(self, left, right, expression):
        if self.is_joined(left, right): raise ValueError('Already joined')
        sources = frozenset([f.source for f in iter_fields(expression)])
        if (len(sources) != 2) or (left not in sources) or (right not in sources):
            raise ValueError('Only expressions of fields of joining sources are allowed')
        self.lefts.append(left)
        self.rights.append(right)
        self.expressions.append(expression)
    def iter_joinings(self, joined): raise NotImplementedError()

class InnerJoinList(BaseJoinList):
    def __init__(self): super(InnerJoinList, self).__init__()
    def is_joined(self, left, right):
        for l,r in zip(self.lefts, self.rights):
            if (l==left) and (r==right): return True
            if (l==right) and (r==left): return True
        return False
    def iter_joinings(self, joined):
        for i in xrange(len(self.lefts)):
            if self.lefts[i]==joined: yield self.rights[i], self.expressions[i]
        for i in xrange(len(self.rights)):
            if self.rights[i]==joined: yield self.lefts[i], self.expressions[i]

class OuterJoinList(BaseJoinList):
    def __init__(self): super(OuterJoinList, self).__init__()
    def is_joined(self, left, right):
        for l,r in zip(self.lefts, self.rights):
            if (l==left) and (r==right): return True
        return False
    def iter_joinings(self, joined):
        for i in xrange(len(self.lefts)):
            if self.lefts[i]==joined: yield self.rights[i], self.expressions[i]

def make_oracle_outer(outer, inner, expression):
    if isinstance(expression, InfixedComparisonExpression) and (not isinstance(expression, OracleOuterDecorator)):
        if (expression.left == outer) and (expression.right == inner): return OracleOuterDecorator(expression, True)
        if (expression.left == inner) and (expression.right == outer): return OracleOuterDecorator(expression, False)
	raise Exception('Not supported expression')
    elif isinstance(expression, InfixedBooleanExpression):
        return type(expression)(*[make_oracle_outer(outer, inner, e) for e in expression.elements])

class BaseSelect(Statement):
    def __init__(self):
        super(BaseSelect, self).__init__()
        self.fields = FieldList()
        self.sources = SourceList()
        self.where = BooleanExpressionList()
        self.groupby = GroupByList()
        self.having = BooleanExpressionList()
        self.orderby = OrderByList()
        self.innerjoins = InnerJoinList()
        self.outerjoins = OuterJoinList()

    def get_from_clause(self): raise NotImplementedError()

    def get_where_clause(self): raise NotImplementedError()

    def __str__(self):
        def section(term, clause):
            if clause:
                return '%s\n%s' % (term, indent(2, clause))
            else:
                return ''
        fields = str(self.fields) or '*'
        froms = section('from', self.get_from_clause())
        where = section('where', self.get_where_clause())
        groupby = section('group by', str(self.groupby))
        having = section('having', str(self.having))
        orderby = section('order by', str(self.orderby))
        return '\n'.join([x for x in ['select', indent(2, fields), froms, where, groupby, having, orderby] if x])

    def join(self, left, right):
        def joiner(*exprs): self.innerjoins.append(left, right, And(*exprs))
        return joiner
    def outer_join(self, left, right):
        def joiner(*exprs): self.outerjoins.append(left, right, And(*exprs))
        return joiner

class StandardSelect(BaseSelect):
    """StandardSelect

        >>> s = StandardSelect()
        >>> ima = s.sources('ima')
        >>> pst = s.sources('pst')
        >>> ima2 = s.sources('ima', 'ima2')
        >>> s.join(ima, pst)(ima.IMA_ItemID == pst.PST_ItemID)
        >>> s.outer_join(ima, ima2)(ima.IMA_ItemID == ima2.IMA_ItemID)
        >>> s.where.And(ima.ItemCost > 100000)
        >>> s.where.And(ima.ItemCost < 200000)
        >>> s.fields.append(ima.IMA_ItemID, 'ID')
        >>> s.fields.append(ima.IMA_ItemCost, 'COST')
        >>> s.fields.append(ima.IMA_ItemName, 'ITEM_NAME')
        >>> s.groupby.append(ima.IMA_ItemID)
        >>> s.groupby.append(ima.IMA_ItemCost)
        >>> s.groupby.append(ima.IMA_ItemName)
        >>> s.having.And(ima.IMA_ItemName.like(strlit('Huh%')))
        >>> s.orderby.append(ima.IMA_ItemName, False)
        >>> s.orderby.append(ima.IMA_ItemCost)
        >>> print s
        select
          ima.IMA_ItemID                                     ID,
          ima.IMA_ItemCost                                   COST,
          ima.IMA_ItemName                                   ITEM_NAME
        from
          ima
            join pst on (ima.IMA_ItemID = pst.PST_ItemID)
            left outer join ima ima2 on (ima.IMA_ItemID = ima2.IMA_ItemID)
        where
          (ima.ItemCost > 100000) and
          (ima.ItemCost < 200000)
        group by
          ima.IMA_ItemID,
          ima.IMA_ItemCost,
          ima.IMA_ItemName
        having
          (ima.IMA_ItemName like 'Huh%')
        order by
          ima.IMA_ItemName desc,
          ima.IMA_ItemCost
    """

    def get_where_clause(self): return str(self.where)
    def get_from_clause(self):
        result = []
        included = []
        for source in self.sources:
            if source not in included:
                queued = [source]
                joinlines = []
                while queued:
                    s = queued.pop(0)
                    if s not in included:
                        included.append(s)
                        for joining, expression in self.innerjoins.iter_joinings(s):
                            if joining not in included:
                                queued.append(joining)
                                joinlines.append('join %s on %s' % (joining.declaration(), str(expression)))
                        for joining, expression in self.outerjoins.iter_joinings(s):
                            if joining not in included:
                                queued.append(joining)
                                joinlines.append('left outer join %s on %s' % (joining.declaration(), str(expression)))
                    included.append(s)
                if result: result[-1] += ','
                result.append(str(source))
                result.extend(['  %s' % x for x in joinlines])
        return '\n'.join(result)

class OracleSelect(BaseSelect):
    """OracleSelect

        >>> s = OracleSelect()
        >>> ima = s.sources('ima')
        >>> pst = s.sources('pst')
        >>> ima2 = s.sources('ima', 'ima2')
        >>> s.join(ima, pst)(ima.IMA_ItemID == pst.PST_ItemID)
        >>> s.outer_join(ima, ima2)(ima.IMA_ItemID == ima2.IMA_ItemID)
        >>> s.where.And(ima.ItemCost > 100000)
        >>> s.where.And(ima.ItemCost < 200000)
        >>> print s
        select
          *
        from
          ima,
          pst,
          ima ima2
        where
          (ima.IMA_ItemID = pst.PST_ItemID) and
          (ima.IMA_ItemID = ima2.IMA_ItemID(+)) and
          (ima.ItemCost > 100000) and
          (ima.ItemCost < 200000)
    """
    def get_where_clause(self):
        inner_exprs = self.innerjoins.expressions
        outer_packs = zip(self.outerjoins.lefts, self.outerjoins.rights, self.outerjoins.expressions)
        outer_exprs = [make_oracle_outer(outer, inner, expr) for outer, inner, expr in outer_packs]
        if self.where.root:
            where_exprs = [self.where.root]
        else:
            where_exprs = []
        return str(And.combine(*(inner_exprs + outer_exprs + where_exprs)))
    
    def get_from_clause(self): return ',\n'.join([source.declaration() for source in self.sources])
    
if __name__ == '__main__':
    try:
        from zope.testing import doctest
    except ImportError:
        import doctest
    doctest.testmod()
