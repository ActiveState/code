def transposed(lists):
   if not lists: return []
   return map(lambda *row: list(row), *lists)

def transposed2(lists, defval=0):
   if not lists: return []
   return map(lambda *row: [elem or defval for elem in row], *lists)
