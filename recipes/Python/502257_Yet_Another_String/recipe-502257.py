import sys, re
def interp(string):
  locals  = sys._getframe(1).f_locals
  globals = sys._getframe(1).f_globals
  for item in re.findall(r'#\{([^}]*)\}', string):
    string = string.replace('#{%s}' % item,
                            str(eval(item, globals, locals)))
  return string

test1 = 'example'
def tryit():
  test2 = 1
  # variable interpolation
  print interp('This is an #{test1} (and another #{test1}) and an int (#{test2})')
  # expression interpolation
  print interp('This is an #{test1 + " (and another " + test1 + ")"} and an int (#{test2})')
tryit()
