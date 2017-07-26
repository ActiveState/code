import re
_named_to_qmark_re = re.compile('\:([a-zA-Z_][a-zA-Z_0-9]*)')
def named_to_qmark(query, d):
  ''' Converts a query from qmark to named style using dict d '''
  params = []
  def f(mo):
    params.append(d[mo.group(1)])
    return '?'
  query = _named_to_qmark_re.sub(f, query)
  return query, params
