import re

class CEnum:
  """
    Constructs a C style enum from a string argument, automatically
    enumerating the provided labels (defaults to 0). 
    Example:
      States = Enum("Off=-1, On=1, Ready, Busy")
    
    will create the following values:
      States.Off    = -1
      States.On     = 1
      States.Ready  = 2
      States.Busy   = 3
    In addition to tracking the values, the Enum class tracks the
    order in which items where added.
  """
  def __init__(self, value_list, separator=",", increment=True):
    self.__enum_read_only = False
    self.__enum_init_val  = 0
    self.__enum_order     = list()
    values = value_list.split(separator)
    for val in values:
      if re.search("[=:]",val):
        (name,value) = re.split("\s*[=:]\s*",val)
        if value:
          self.__enum_init_val = int(value)
      else:
        name = val
      self.__enum_order.append(name)
      setattr(self,name,self.__enum_init_val)
      if increment:
        self.__enum_init_val += 1
      else:
        self.__enum_init_val -= 1
    self.__enum_read_only = True
      
  def __setattr__(self,name,value):
    if not re.match("_CEnum",name):
      if self.__enum_read_only:
        raise AttributeError("Enum is Read-Only")
    self.__dict__[name] = value
    
  def __getattr__(self,name):
    if name in self.__dict__.keys():
      return name
    raise AttributeError("No such attribute: " + name)
    
  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    my_rep = "("
    for val in self.__enum_order:
      my_rep += val + "=" + str(self.__dict__[val])
      if val != self.__enum_order[-1]:
        my_rep += ","
    my_rep = my_rep.rstrip() + ")"
    return my_rep
    
  def labels(self):
    return list(self.__enum_order)
    
  def count(self):
    return len(self.__enum_order)
    
if __name__ == "__main__":
  DaysOfWeek = CEnum("Sun=1,Mon,Tue,Wed,Thu,Fri,Sat")
  
  print("DaysOfWeek.Sun = " + str(DaysOfWeek.Sun))
  print("DaysOfWeek.Mon = " + str(DaysOfWeek.Mon))
  print("DaysOfWeek.Tue = " + str(DaysOfWeek.Tue))
  print("DaysOfWeek.Wed = " + str(DaysOfWeek.Wed))
  print("DaysOfWeek.Thu = " + str(DaysOfWeek.Thu))
  print("DaysOfWeek.Fri = " + str(DaysOfWeek.Fri))
  print("DaysOfWeek.Sat = " + str(DaysOfWeek.Sat))
  
  print("DaysOfWeek.Sun < DaysOfWeek.Sat ? " + 
    ("True" if DaysOfWeek.Sun < DaysOfWeek.Sat else "False"))
  print("DaysOfWeek.Sat < DaysOfWeek.Sun ? " + 
    ("True" if DaysOfWeek.Sat < DaysOfWeek.Sun else "False"))
    
  try:
    DaysOfWeek.Sun = DaysOfWeek.Sat
    print("DaysOfWeek.Sun = " + str(DaysOfWeek.Sun))
    print("DaysOfWeek.Mon = " + str(DaysOfWeek.Mon))
    print("DaysOfWeek.Tue = " + str(DaysOfWeek.Tue))
    print("DaysOfWeek.Wed = " + str(DaysOfWeek.Wed))
    print("DaysOfWeek.Thu = " + str(DaysOfWeek.Thu))
    print("DaysOfWeek.Fri = " + str(DaysOfWeek.Fri))
    print("DaysOfWeek.Sat = " + str(DaysOfWeek.Sat))
  except AttributeError as ae:
    print("Got exception: " + str(ae))
    
  try:
    DaysOfWeek.Bob = 27
    print("DaysOfWeek.Bob = " + str(DaysOfWeek.Bob))
  except AttributeError as ae:
    print("Got exception: " + str(ae))

  print("DaysOfWeek.count()       = " + str(DaysOfWeek.count()))
  print("DaysOfWeek.labels()      = " + str(DaysOfWeek.labels()))
  
  print(str(DaysOfWeek))
