class Param:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'Param(%r)' % (self.value,)

def to_qmark(chunks):
    query_parts = []
    params = []
    for chunk in chunks:
        if isinstance(chunk, Param):
            params.append(chunk.value)
            query_parts.append('?')
        else:
            query_parts.append(chunk)
    return ''.join(query_parts), params

def to_numeric(chunks):
    query_parts = []
    params = []
    for chunk in chunks:
        if isinstance(chunk, Param):
            params.append(chunk.value)
            query_parts.append(':%d' % len(params))
        else:
            query_parts.append(chunk)
    return ''.join(query_parts), tuple(params)  # DCOracle2 has broken support
                                                # for sequences of other types

def to_named(chunks):
    query_parts = []
    params = {}
    for chunk in chunks:
        if isinstance(chunk, Param):
            name = 'p%d' % len(params)  # Are numbers in name allowed?
            params[name] = chunk.value
            query_parts.append(':%s' % name)
        else:
            query_parts.append(chunk)
    return ''.join(query_parts), params

def to_format(chunks):
    query_parts = []
    params = []
    for chunk in chunks:
        if isinstance(chunk, Param):
            params.append(chunk.value)
            query_parts.append('%s')
        else:
            query_parts.append(chunk.replace('%', '%%'))
    return ''.join(query_parts), params

def to_pyformat(chunks):
    query_parts = []
    params = {}
    for chunk in chunks:
        if isinstance(chunk, Param):
            name = '%d' % len(params)
            params[name] = chunk.value
            query_parts.append('%%(%s)s' % name)
        else:
            query_parts.append(chunk.replace('%', '%%'))
    return ''.join(query_parts), params


if __name__=='__main__':
    query = ('SELECT * FROM test WHERE field1>', Param(10),
             ' AND field2 LIKE ', Param('%value%'))
    print 'Query:', query
    for param_style in ('qmark', 'numeric', 'named', 'format', 'pyformat'):
        print '%s: %r' % (param_style, vars()['to_'+param_style](query))
