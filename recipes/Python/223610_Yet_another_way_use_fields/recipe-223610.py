import types

class FieldNameError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return `"""Field name '%s' does not exist""" % self.value`


class fRow(tuple):
  # class for each row
  
  def __getattr__(self,i):
    return tuple.__getitem__(self,self.__Field2Index__(i))

  def __call__(self,i):
    return tuple.__getitem__(self,self.__Field2Index__(i))

  def __getitem__(self,i):
    if type(i) != types.SliceType:
      return tuple.__getitem__(self,self.__Field2Index__(i))
    else:
      if i.start is not None and i.stop is not None:
        return self[self.__Field2Index__(i.start):self.__Field2Index__(i.stop)]
      elif i.start is None:
        return self[:self.__Field2Index__(i.stop)]
      elif i.stop is None:
        return self[self.__Field2Index__(i.start):]
      else:
        return self[:]

  def __Field2Index__():
    return None

class fRowset(list):
  # list to hold the rows
  
  def __init__(self,rowset,description):
    # save the description as is
    self.description = fRow(description)
    self.description.__Field2Index__ = self.__fieldToIndex
    
    # Create the list and dict of fields
    self.fields = []
    self.__fieldDict = {}
    for f in range(len(description)):
      if type(description[f]) == types.TupleType or type(description[f]) == types.ListType:
        self.__fieldDict[description[f][0].lower()] = f
        self.fields.append( description[f][0].lower())
      else:
        self.__fieldDict[description[f].lower()] = f
        self.fields.append( description[f].lower())
    # Add all the rows
    for r in rowset:
      self.append(r)  

  def append(self,new):
    # Create a new record
    fR = fRow(new)
    # Pass it the function that looks up the index
    fR.__Field2Index__ = self.__fieldToIndex
    list.append(self,fR)
    return

  # Look up the field and return the index  
  def __fieldToIndex(self,field):
    if type(field) == int:
      return field
    try:
      return self.__fieldDict[field.lower()]
    except:
      raise FieldNameError, field


def ffetchall(cursor):
  # Nice wrapper for fetchall
  return fRowset(cursor.fetchall(),cursor.description)

def ffetchmany(cursor):
  # Nice wrapper for fetchmany
  return fRowset(cursor.fetchmany(),cursor.description)

def fquery(connection,query):
  curs = connection.cursor()
  curs.execute(query)
  rows  = fRowset(curs.fetchall(),curs.description)
  curs.close()
  return rows
